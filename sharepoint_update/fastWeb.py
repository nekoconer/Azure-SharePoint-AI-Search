from fastapi import FastAPI, Request, Response
from pyngrok import ngrok
import uvicorn
import json
import threading
import os
import sys
import requests
from typing import Optional
from test_sp import get_access_token
app = FastAPI()

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import SHAREPOINT_TENANT_ID, SHAREPOINT_APP_ID, SHAREPOINT_CLIENT_SECRET

DELTA_FILE = "delta_links.json"
NOTIFY_QUEUE = []

def get_saved_delta_link(sub_id):
    if not os.path.exists(DELTA_FILE):
        return None
    try:
        with open(DELTA_FILE, 'r') as f:
            content = f.read().strip()
            if not content:  # 文件为空
                return None
            data = json.loads(content)
            return data.get(sub_id)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"读取delta链接文件时出错: {e}")
        return None

def save_delta_link(sub_id, delta_link):
    data = {}
    if os.path.exists(DELTA_FILE):
        try:
            with open(DELTA_FILE, 'r') as f:
                content = f.read().strip()
                if content:  # 文件不为空
                    data = json.loads(content)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"读取现有delta链接文件时出错，将创建新文件: {e}")
            data = {}
    
    data[sub_id] = delta_link
    with open(DELTA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def process_notification(data):
    for n in data.get("value", []):
        print("Received notification:", n)
        sub_id = n.get("subscriptionId")
        changed_id = n.get("resourceData", {}).get("id")
        NOTIFY_QUEUE.append((sub_id, changed_id))
                
    # 启动异步线程处理队列，避免 blocking
    threading.Thread(target=handle_queue).start()

def handle_queue():
    print("开始处理通知队列")
    while NOTIFY_QUEUE:
        sub_id, changed_id = NOTIFY_QUEUE.pop(0)
        print(f"处理订阅 {sub_id} 的变更通知")
        
        delta_link = get_saved_delta_link(sub_id)
        if not delta_link:
            # 如果没有保存的delta链接，创建初始的delta查询
            print("没有找到保存的delta链接，创建初始delta查询")
            drive_id = "b!15loqcZkLUGK6C0oCOL3vvvNNWQegURNvY-5ZGBF091rDBpKdJ6IS6RbBIfXEnsk"
            delta_link = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/root/delta?$select=id,name,content,content.downloadUrl"
        
        try:
            new_delta_link = sync_delta(delta_link)
            if new_delta_link:
                save_delta_link(sub_id, new_delta_link)
                print(f"已保存新的delta链接: {new_delta_link}")
        except Exception as e:
            print(f"处理delta同步时出错: {e}")

def sync_delta(delta_link):
    print(f"同步delta变更，使用链接: {delta_link}")
    token = get_access_token(SHAREPOINT_TENANT_ID, SHAREPOINT_APP_ID, SHAREPOINT_CLIENT_SECRET)
    
    try:
        resp = requests.get(delta_link, headers={"Authorization": f"Bearer {token}"})
        resp.raise_for_status()
        js = resp.json()
        
        print(f"获取到 {len(js.get('value', []))} 个变更项目")
        
        for item in js.get("value", []):
            if "deleted" in item:
                print(f"删除的文件: {item['id']} - {item.get('name', 'Unknown')}")
            else:
                dl = item.get("@microsoft.graph.downloadUrl")
                print(f"更新的文件: {item['id']} - {item.get('name', 'Unknown')}")
                if dl:
                    print(f"  下载链接: {dl}")
                    try:
                        r = requests.get(dl)
                        r.raise_for_status()
                        
                        # 确保downloads目录存在
                        downloads_dir = "downloads"
                        if not os.path.exists(downloads_dir):
                            os.makedirs(downloads_dir)
                        
                        file_path = os.path.join(downloads_dir, item["name"])
                        with open(file_path, "wb") as f:
                            f.write(r.content)
                        print(f"  文件已保存到: {file_path}")
                    except Exception as e:
                        print(f"  下载文件时出错: {e}")
        
        return js.get("@odata.deltaLink")
    
    except Exception as e:
        print(f"同步delta时出错: {e}")
        return None

# Webhook 接收路由 - 分别处理GET和POST
@app.get('/api/notify')
async def notify_get(request: Request, validationToken: Optional[str] = None):
    """处理Microsoft Graph的验证请求"""
    print(f"=== GET Request to /api/notify ===")
    print(f"Headers: {dict(request.headers)}")
    print(f"Query params: {dict(request.query_params)}")
    print(f"URL: {request.url}")
    
    # 从查询参数获取验证token
    if validationToken:
        print(f"Received validation token from parameter: {validationToken}")
        return Response(content=validationToken, media_type="text/plain", status_code=200)
    
    # 如果没有validationToken参数，检查query_params
    validation_token = request.query_params.get('validationToken')
    if validation_token:
        print(f"Received validation token from query_params: {validation_token}")
        return Response(content=validation_token, media_type="text/plain", status_code=200)
    
    print("No validation token found!")
    return Response(content="Missing validationToken", status_code=400)

@app.post('/api/notify')
async def notify_post(request: Request):
    """处理Microsoft Graph的验证和通知请求"""
    print(f"=== POST Request to /api/notify ===")
    print(f"Headers: {dict(request.headers)}")
    print(f"Query params: {dict(request.query_params)}")
    
    # 检查是否是验证请求
    validation_token = request.query_params.get('validationToken')
    if validation_token:
        print(f"Received validation token in POST request: {validation_token}")
        return Response(content=validation_token, media_type="text/plain", status_code=200)
    
    # 处理通知请求
    try:
        data = await request.json()
        print(f"Received notification: {data}")
        # 推送至处理队列
        process_notification(data)
        # Microsoft Graph要求返回200状态码
        return Response(status_code=200)
    except Exception as e:
        print(f"Error processing notification: {e}")
        # 如果JSON解析失败但没有validation token，可能是其他类型的请求
        return Response(status_code=400)

if __name__ == "__main__":
    # 启动 ngrok 隧道
    public_url = ngrok.connect("11451", bind_tls=True).public_url
    print("ngrok public URL:", public_url)

    if public_url is not None:
    # 打印给订阅接口使用
        print("Use this notificationUrl:", public_url + "/api/notify")

    # 启动 FastAPI
    uvicorn.run(app, host="0.0.0.0", port=11451)

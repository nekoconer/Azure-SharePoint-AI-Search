import requests
import sys
import os
import requests
from urllib.parse import urlparse



# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import SHAREPOINT_TENANT_ID, SHAREPOINT_APP_ID, SHAREPOINT_CLIENT_SECRET,SHAREPOINT_SITE_URL

def get_access_token(tenant_id, client_id, client_secret):
    """
    Get access token using client credentials flow
    """
    url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "https://graph.microsoft.com/.default"
    }
    
    try:
        resp = requests.post(url, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
        
        # Print detailed error information
        if resp.status_code != 200:
            print(f"Error Status Code: {resp.status_code}")
            print(f"Error Response: {resp.text}")
            print(f"Request URL: {url}")
            print(f"Request Data: {data}")
        
        resp.raise_for_status()
        return resp.json()["access_token"]
    
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        print(f"Response content: {resp.text}")
        raise
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise

def test_sharepoint_access():
    """
    Test SharePoint access using Microsoft Graph API
    """
    try:
        # Get access token
        print("Getting access token...")
        token = get_access_token(SHAREPOINT_TENANT_ID, SHAREPOINT_APP_ID, SHAREPOINT_CLIENT_SECRET)
        print("✓ Access token obtained successfully")
        
        # Test SharePoint site access
        # hostname = "jppresoft2.sharepoint.com"
        # site_path = "/sites/msteams_2fab82"
        
        parsed = urlparse(SHAREPOINT_SITE_URL)
        # 获取 hostname 和路径
        hostname = parsed.hostname  # 域名部分
        site_path = parsed.path
        
        print(f"Testing access to SharePoint site: {hostname}{site_path}")
        resp = requests.get(
            f"https://graph.microsoft.com/v1.0/sites/{hostname}:{site_path}",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if resp.status_code == 200:
            site_data = resp.json()
            print(f"✓ SharePoint site access successful")
            print(f"Site ID: {site_data.get('id')}")
            print(f"Site Name: {site_data.get('displayName')}")
            print(f"Site URL: {site_data.get('webUrl')}")
            resp1 = requests.get(
                f"https://graph.microsoft.com/v1.0/sites/{site_data.get('id')}/drives",
                headers={"Authorization": f"Bearer {token}"}
                )
            print(resp1)
            for d in resp1.json().get("value", []):
                print(d["id"], d["name"]) #这个id就是drive_id:b!15loqcZkLUGK6C0oCOL3vvvNNWQegURNvY-5ZGBF091rDBpKdJ6IS6RbBIfXEnsk ドキュメント
        else:
            print(f"✗ SharePoint site access failed")
            print(f"Status Code: {resp.status_code}")
            print(f"Response: {resp.text}")
            
    except Exception as e:
        print(f"✗ Test failed: {e}")
        
def test_document_files():
    print("Getting access token...")
    token = get_access_token(SHAREPOINT_TENANT_ID, SHAREPOINT_APP_ID, SHAREPOINT_CLIENT_SECRET)
    print("✓ Access token obtained successfully")
    drive_id = "b!15loqcZkLUGK6C0oCOL3vvvNNWQegURNvY-5ZGBF091rDBpKdJ6IS6RbBIfXEnsk"#替换此处drive_id

    resp = requests.get(
        f"https://graph.microsoft.com/v1.0/drives/{drive_id}/root/children",
        headers={"Authorization": f"Bearer {token}"}
    )
    for item in resp.json().get("value", []):
        print(item["name"], item["webUrl"])

def webhookset():
    print("Getting access token...")
    token = get_access_token(SHAREPOINT_TENANT_ID, SHAREPOINT_APP_ID, SHAREPOINT_CLIENT_SECRET)
    print("✓ Access token obtained successfully")
    drive_id = "b!15loqcZkLUGK6C0oCOL3vvvNNWQegURNvY-5ZGBF091rDBpKdJ6IS6RbBIfXEnsk" #替换此处drive_id
    
    # 首先查询现有订阅
    print("Checking existing subscriptions...")
    resp = requests.get(
        "https://graph.microsoft.com/v1.0/subscriptions",
        headers={"Authorization": f"Bearer {token}"}
    )
    print("Current subscriptions:")
    resp_json = resp.json()
    print(resp_json)
    
    delete_current_link(resp_json["value"],token)
    
    # 创建新的订阅
    print("\nCreating new subscription...")
    payload = {
        "changeType": "updated",
        "notificationUrl": "https://3ca3-122-249-141-175.ngrok-free.app/api/notify",#替换此处订阅网址
        "resource": f"/drives/{drive_id}/root",
        "expirationDateTime": "2025-07-30T23:59:59Z",
        "clientState": "testCondition"
    }
    
    create_resp = requests.post(
        "https://graph.microsoft.com/v1.0/subscriptions",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json=payload
    )
    
    if create_resp.status_code == 201:
        print("✓ Subscription created successfully:")
        print(create_resp.json())
    else:
        print(f"✗ Failed to create subscription. Status: {create_resp.status_code}")
        print(f"Error: {create_resp.text}")

def delete_current_link(value,token):
    subscription_id = [item["id"] for item in value]  # 替换成你要删除的订阅 ID
    for id in subscription_id:
        url = f"https://graph.microsoft.com/v1.0/subscriptions/{id}"

        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = requests.delete(url, headers=headers)

        if response.status_code == 204:
            print("订阅已成功删除。")
        else:
            print(f"删除失败，状态码: {response.status_code}")
            print(response.text)

if __name__ == "__main__":
    print("=== SharePoint Access Test ===")
    print(f"Tenant ID: {SHAREPOINT_TENANT_ID}")
    print(f"Client ID: {SHAREPOINT_APP_ID}")
    print(f"Client Secret: {'*' * len(SHAREPOINT_CLIENT_SECRET)}")
    print()
    
    #test_sharepoint_access()
    #test_document_files()
    webhookset()

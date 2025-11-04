
import os
import base64
from openai import AzureOpenAI
from config import (
  AZURE_OPENAI_API_KEY,AZURE_OPENAI_ENDPOINT,CHAT_DEPLOYMENT_NAME,SEARCH_ENDPOINT,SEARCH_API_KEY,INDEX_NAME
)

# 使用基于密钥的身份验证初始化 Azure OpenAI 客户端
client = AzureOpenAI(
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_API_KEY,
    api_version="2025-01-01-preview",
)

# IMAGE_PATH = "YOUR_IMAGE_PATH"
# encoded_image = base64.b64encode(open(IMAGE_PATH, 'rb').read()).decode('ascii')

#准备聊天提示
chat_prompt =[
        {"role": "system", "content": "You are an AI assistant."},
        {"role": "user", "content": "経費申請"}
    ]

# 如果已启用语音，则包括语音结果
messages = chat_prompt

# 生成完成
completion = client.chat.completions.create(
    model=CHAT_DEPLOYMENT_NAME,
    messages=messages,
    max_tokens=800,
    temperature=1,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    stop=None,
    stream=False,
    extra_body={
      "data_sources": [{
          "type": "azure_search",
          "parameters": {
            "endpoint": f"{SEARCH_ENDPOINT}",
            "index_name": f"{INDEX_NAME}",
            "semantic_configuration": "default",
            "query_type": "simple",
            "fields_mapping": {},
            "in_scope": True,
            "filter": None,
            "strictness": 3,
            "top_n_documents": 5,
            "authentication": {
              "type": "api_key",
              "key": f"{SEARCH_API_KEY}"
            }
          }
        }]
    }
)

print(completion.to_json())
    
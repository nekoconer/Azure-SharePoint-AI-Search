import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# Azure Search 配置
SEARCH_SERVICE_NAME = os.getenv("SEARCH_SERVICE_NAME", "")
SEARCH_API_KEY = os.getenv("SEARCH_API_KEY", "")
SEARCH_ENDPOINT = f"https://{SEARCH_SERVICE_NAME}.search.windows.net"

# SharePoint 配置
SHAREPOINT_SITE_URL = os.getenv("SHAREPOINT_SITE_URL", "")
SHAREPOINT_APP_ID = os.getenv("SHAREPOINT_APP_ID", "")
SHAREPOINT_CLIENT_SECRET = os.getenv("SHAREPOINT_CLIENT_SECRET", "")
SHAREPOINT_TENANT_ID = os.getenv("SHAREPOINT_TENANT_ID", "")

# Azure OpenAI 配置
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "https://xxx.openai.azure.com/")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY", "")
EMBEDDING_DEPLOYMENT_NAME = os.getenv("EMBEDDING_DEPLOYMENT_NAME", "text-embedding-3-large")
CHAT_DEPLOYMENT_NAME = os.getenv("CHAT_DEPLOYMENT_NAME","gpt-4.1-mini")
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "text-embedding-3-large")

# 索引配置
INDEX_NAME = os.getenv("INDEX_NAME", "sharepoint-index")
DATA_SOURCE_NAME = os.getenv("DATA_SOURCE_NAME", "sharepoint-datasource-presentations")
SKILLSET_NAME = os.getenv("SKILLSET_NAME", "sharepoint-skillset")
INDEXER_NAME = os.getenv("INDEXER_NAME", "sharepoint-indexer")

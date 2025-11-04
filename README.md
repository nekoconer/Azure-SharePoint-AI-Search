
[English](#english) | [中文](#中文) | [日本語](#日本語)

---

## English

### 📋 Project Overview

This project provides two main functionalities:

1. **Azure AI Search Integration**: Configure and implement Azure AI Search with SharePoint as a data source, including semantic search, vector search, and hybrid search capabilities.
2. **SharePoint Incremental Updates**: Track and retrieve incremental changes from SharePoint using Microsoft Graph API webhooks and delta queries.

### 🏗️ Project Structure

```
azure_github/
├── Azure_SDK.py              # Azure AI Search implementation
├── chatbot.py                # RAG chatbot using Azure OpenAI
├── config.py                 # Configuration management
├── main.py                   # Main entry point
├── sharepoint_update/        # SharePoint update tracking
│   ├── fastWeb.py           # FastAPI webhook server
│   ├── test_sp.py           # SharePoint access testing
│   └── test_webhook.py      # Webhook testing utilities
├── .env                      # Environment variables (not in repo)
├── pyproject.toml           # Project dependencies
└── README.md                # This file
```

### ✨ Features

#### Azure AI Search
- **Data Source Configuration**: Connect SharePoint Online as a data source
- **Index Management**: Create and manage search indexes with vector fields
- **Skillset Creation**: Implement AI enrichment pipeline with:
  - Entity recognition
  - Language detection
  - Text splitting (chunking)
  - Azure OpenAI embeddings generation
- **Multiple Search Types**:
  - Semantic search with captions and answers
  - Vector search using embeddings
  - Hybrid search (text + vector)
- **RAG Chatbot**: Integrate with Azure OpenAI for question-answering

#### SharePoint Incremental Updates
- **Webhook Subscription**: Subscribe to SharePoint drive changes
- **Delta Query**: Track incremental changes efficiently
- **Automatic Download**: Download modified files automatically
- **Change Tracking**: Persist delta links for continuous synchronization

### 🚀 Getting Started

#### Prerequisites

- Python 3.11+
- Azure subscription with:
  - Azure AI Search service
  - Azure OpenAI service
- Microsoft 365 with SharePoint Online
- Azure AD app registration with appropriate permissions

#### Installation

1. Clone the repository:
```bash
git clone https://github.com/nekoconer/Azure-SharePoint-AI-Search.git
cd Azure-SharePoint-AI-Search
```

2. Install dependencies using uv (recommended) or pip:
```bash
# Using uv
uv sync

# Or using pip
pip install -r requirements.txt
```

3. Configure environment variables:

Create a `.env` file in the project root:

```env
# Azure Search Configuration
SEARCH_SERVICE_NAME=your-search-service
SEARCH_API_KEY=your-search-api-key

# SharePoint Configuration
SHAREPOINT_SITE_URL=https://yourtenant.sharepoint.com/sites/yoursite
SHAREPOINT_APP_ID=your-app-id
SHAREPOINT_CLIENT_SECRET=your-client-secret
SHAREPOINT_TENANT_ID=your-tenant-id

# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT=https://your-openai.openai.azure.com/
AZURE_OPENAI_API_KEY=your-openai-api-key
EMBEDDING_DEPLOYMENT_NAME=text-embedding-3-large
CHAT_DEPLOYMENT_NAME=gpt-4-mini
EMBEDDING_MODEL_NAME=text-embedding-3-large

# Index Configuration
INDEX_NAME=sharepoint-index
DATA_SOURCE_NAME=sharepoint-datasource
SKILLSET_NAME=sharepoint-skillset
INDEXER_NAME=sharepoint-indexer
```

#### Azure AI Search Setup

1. Create the data source, index, skillset, and indexer:

```python
from Azure_SDK import create_datasource, create_indexes, create_skillset, create_indexer

# Run these in order (first time only)
create_datasource()
create_indexes()
create_skillset()
create_indexer()
```

2. Test search functionality:

```python
from Azure_SDK import test_search

test_search()
```

3. Use the RAG chatbot:

```bash
python chatbot.py
```

#### SharePoint Webhook Setup

1. Test SharePoint access:

```bash
cd sharepoint_update
python test_sp.py
```

2. Set up webhook subscription:

Update the `drive_id` and `notificationUrl` in `test_sp.py`, then run:

```python
from test_sp import webhookset
webhookset()
```

3. Start the webhook server:

```bash
python fastWeb.py
```

The server will:
- Start ngrok tunnel for public access
- Listen for SharePoint change notifications
- Process delta queries to get incremental changes
- Download modified files automatically

### 📚 API Reference

#### Azure_SDK.py

- `create_datasource()`: Create SharePoint data source connection
- `create_indexes()`: Create search index with vector fields
- `create_skillset()`: Create AI enrichment skillset
- `create_indexer()`: Create and schedule indexer
- `semantic_search(query, top_k=5)`: Perform semantic search
- `vector_search(query_vector, top_k=5)`: Perform vector search
- `hybrid_search(query, vector=None, top_k=5)`: Perform hybrid search
- `get_embedding(text)`: Generate text embeddings

#### sharepoint_update/test_sp.py

- `get_access_token(tenant_id, client_id, client_secret)`: Get Microsoft Graph access token
- `test_sharepoint_access()`: Test SharePoint site access
- `test_document_files()`: List files in SharePoint drive
- `webhookset()`: Create webhook subscription

#### sharepoint_update/fastWeb.py

- `/api/notify` (GET/POST): Webhook endpoint for Microsoft Graph notifications
- `process_notification(data)`: Process incoming notifications
- `sync_delta(delta_link)`: Sync incremental changes using delta query

### 🔧 Configuration

#### Azure AD App Permissions

Your Azure AD app requires the following Microsoft Graph API permissions:

- `Sites.Read.All` or `Sites.ReadWrite.All`
- `Files.Read.All` or `Files.ReadWrite.All`

#### Supported File Types

The indexer is configured to process:
- PDF files (.pdf)
- Word documents (.docx, .doc)
- Text files (.txt)

Excluded file types:
- Images (.png, .jpg)

### 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### 📄 License

This project is licensed under the MIT License.

---

## 中文

### 📋 项目概述

本项目提供两个主要功能：

1. **Azure AI Search 集成**：配置和实现 Azure AI Search，以 SharePoint 作为数据源，包括语义搜索、向量搜索和混合搜索功能。
2. **SharePoint 增量更新**：使用 Microsoft Graph API webhook 和 delta 查询跟踪和获取 SharePoint 的增量变更。

### 🏗️ 项目结构

```
azure_github/
├── Azure_SDK.py              # Azure AI Search 实现
├── chatbot.py                # 使用 Azure OpenAI 的 RAG 聊天机器人
├── config.py                 # 配置管理
├── main.py                   # 主入口点
├── sharepoint_update/        # SharePoint 更新跟踪
│   ├── fastWeb.py           # FastAPI webhook 服务器
│   ├── test_sp.py           # SharePoint 访问测试
│   └── test_webhook.py      # Webhook 测试工具
├── .env                      # 环境变量（不在仓库中）
├── pyproject.toml           # 项目依赖
└── README.md                # 本文件
```

### ✨ 功能特性

#### Azure AI Search
- **数据源配置**：连接 SharePoint Online 作为数据源
- **索引管理**：创建和管理带有向量字段的搜索索引
- **技能集创建**：实现 AI 增强管道，包括：
  - 实体识别
  - 语言检测
  - 文本分割（分块）
  - Azure OpenAI 嵌入向量生成
- **多种搜索类型**：
  - 带标题和答案的语义搜索
  - 使用嵌入向量的向量搜索
  - 混合搜索（文本 + 向量）
- **RAG 聊天机器人**：与 Azure OpenAI 集成进行问答

#### SharePoint 增量更新
- **Webhook 订阅**：订阅 SharePoint 驱动器变更
- **Delta 查询**：高效跟踪增量变更
- **自动下载**：自动下载修改的文件
- **变更跟踪**：持久化 delta 链接以实现持续同步

### 🚀 快速开始

#### 前置要求

- Python 3.11+
- Azure 订阅，包含：
  - Azure AI Search 服务
  - Azure OpenAI 服务
- Microsoft 365 with SharePoint Online
- 具有适当权限的 Azure AD 应用注册

#### 安装

1. 克隆仓库：
```bash
git clone https://github.com/nekoconer/Azure-SharePoint-AI-Search.git
cd Azure-SharePoint-AI-Search
```

2. 使用 uv（推荐）或 pip 安装依赖：
```bash
# 使用 uv
uv sync

# 或使用 pip
pip install -r requirements.txt
```

3. 配置环境变量：

在项目根目录创建 `.env` 文件：

```env
# Azure Search 配置
SEARCH_SERVICE_NAME=your-search-service
SEARCH_API_KEY=your-search-api-key

# SharePoint 配置
SHAREPOINT_SITE_URL=https://yourtenant.sharepoint.com/sites/yoursite
SHAREPOINT_APP_ID=your-app-id
SHAREPOINT_CLIENT_SECRET=your-client-secret
SHAREPOINT_TENANT_ID=your-tenant-id

# Azure OpenAI 配置
AZURE_OPENAI_ENDPOINT=https://your-openai.openai.azure.com/
AZURE_OPENAI_API_KEY=your-openai-api-key
EMBEDDING_DEPLOYMENT_NAME=text-embedding-3-large
CHAT_DEPLOYMENT_NAME=gpt-4-mini
EMBEDDING_MODEL_NAME=text-embedding-3-large

# 索引配置
INDEX_NAME=sharepoint-index
DATA_SOURCE_NAME=sharepoint-datasource
SKILLSET_NAME=sharepoint-skillset
INDEXER_NAME=sharepoint-indexer
```

#### Azure AI Search 设置

1. 创建数据源、索引、技能集和索引器：

```python
from Azure_SDK import create_datasource, create_indexes, create_skillset, create_indexer

# 按顺序运行（仅首次）
create_datasource()
create_indexes()
create_skillset()
create_indexer()
```

2. 测试搜索功能：

```python
from Azure_SDK import test_search

test_search()
```

3. 使用 RAG 聊天机器人：

```bash
python chatbot.py
```

#### SharePoint Webhook 设置

1. 测试 SharePoint 访问：

```bash
cd sharepoint_update
python test_sp.py
```

2. 设置 webhook 订阅：

在 `test_sp.py` 中更新 `drive_id` 和 `notificationUrl`，然后运行：

```python
from test_sp import webhookset
webhookset()
```

3. 启动 webhook 服务器：

```bash
python fastWeb.py
```

服务器将：
- 启动 ngrok 隧道以供公共访问
- 监听 SharePoint 变更通知
- 处理 delta 查询以获取增量变更
- 自动下载修改的文件

### 📚 API 参考

#### Azure_SDK.py

- `create_datasource()`: 创建 SharePoint 数据源连接
- `create_indexes()`: 创建带有向量字段的搜索索引
- `create_skillset()`: 创建 AI 增强技能集
- `create_indexer()`: 创建和调度索引器
- `semantic_search(query, top_k=5)`: 执行语义搜索
- `vector_search(query_vector, top_k=5)`: 执行向量搜索
- `hybrid_search(query, vector=None, top_k=5)`: 执行混合搜索
- `get_embedding(text)`: 生成文本嵌入向量

#### sharepoint_update/test_sp.py

- `get_access_token(tenant_id, client_id, client_secret)`: 获取 Microsoft Graph 访问令牌
- `test_sharepoint_access()`: 测试 SharePoint 站点访问
- `test_document_files()`: 列出 SharePoint 驱动器中的文件
- `webhookset()`: 创建 webhook 订阅

#### sharepoint_update/fastWeb.py

- `/api/notify` (GET/POST): Microsoft Graph 通知的 webhook 端点
- `process_notification(data)`: 处理传入的通知
- `sync_delta(delta_link)`: 使用 delta 查询同步增量变更

### 🔧 配置

#### Azure AD 应用权限

您的 Azure AD 应用需要以下 Microsoft Graph API 权限：

- `Sites.Read.All` 或 `Sites.ReadWrite.All`
- `Files.Read.All` 或 `Files.ReadWrite.All`

#### 支持的文件类型

索引器配置为处理：
- PDF 文件 (.pdf)
- Word 文档 (.docx, .doc)
- 文本文件 (.txt)

排除的文件类型：
- 图像 (.png, .jpg)

### 🤝 贡献

欢迎贡献！请随时提交 Pull Request。

### 📄 许可证

本项目采用 MIT 许可证。

---

## 日本語

### 📋 プロジェクト概要

このプロジェクトは2つの主要機能を提供します：

1. **Azure AI Search統合**：SharePointをデータソースとしたAzure AI Searchの設定と実装。セマンティック検索、ベクトル検索、ハイブリッド検索機能を含みます。
2. **SharePoint増分更新**：Microsoft Graph API webhookとdeltaクエリを使用してSharePointの増分変更を追跡・取得します。

### 🏗️ プロジェクト構造

```
azure_github/
├── Azure_SDK.py              # Azure AI Search実装
├── chatbot.py                # Azure OpenAIを使用したRAGチャットボット
├── config.py                 # 設定管理
├── main.py                   # メインエントリーポイント
├── sharepoint_update/        # SharePoint更新追跡
│   ├── fastWeb.py           # FastAPI webhookサーバー
│   ├── test_sp.py           # SharePointアクセステスト
│   └── test_webhook.py      # Webhookテストユーティリティ
├── .env                      # 環境変数（リポジトリには含まれません）
├── pyproject.toml           # プロジェクト依存関係
└── README.md                # このファイル
```

### ✨ 機能

#### Azure AI Search
- **データソース設定**：SharePoint Onlineをデータソースとして接続
- **インデックス管理**：ベクトルフィールドを持つ検索インデックスの作成と管理
- **スキルセット作成**：AI強化パイプラインの実装：
  - エンティティ認識
  - 言語検出
  - テキスト分割（チャンキング）
  - Azure OpenAI埋め込みベクトル生成
- **複数の検索タイプ**：
  - キャプションと回答付きのセマンティック検索
  - 埋め込みベクトルを使用したベクトル検索
  - ハイブリッド検索（テキスト + ベクトル）
- **RAGチャットボット**：Azure OpenAIと統合した質問応答

#### SharePoint増分更新
- **Webhook購読**：SharePointドライブの変更を購読
- **Deltaクエリ**：増分変更を効率的に追跡
- **自動ダウンロード**：変更されたファイルを自動的にダウンロード
- **変更追跡**：継続的な同期のためにdeltaリンクを永続化

### 🚀 はじめに

#### 前提条件

- Python 3.11+
- 以下を含むAzureサブスクリプション：
  - Azure AI Searchサービス
  - Azure OpenAIサービス
- SharePoint OnlineのあるMicrosoft 365
- 適切な権限を持つAzure ADアプリ登録

#### インストール

1. リポジトリをクローン：
```bash
git clone https://github.com/nekoconer/Azure-SharePoint-AI-Search.git
cd Azure-SharePoint-AI-Search
```

2. uv（推奨）またはpipを使用して依存関係をインストール：
```bash
# uvを使用
uv sync

# またはpipを使用
pip install -r requirements.txt
```

3. 環境変数を設定：

プロジェクトルートに`.env`ファイルを作成：

```env
# Azure Search設定
SEARCH_SERVICE_NAME=your-search-service
SEARCH_API_KEY=your-search-api-key

# SharePoint設定
SHAREPOINT_SITE_URL=https://yourtenant.sharepoint.com/sites/yoursite
SHAREPOINT_APP_ID=your-app-id
SHAREPOINT_CLIENT_SECRET=your-client-secret
SHAREPOINT_TENANT_ID=your-tenant-id

# Azure OpenAI設定
AZURE_OPENAI_ENDPOINT=https://your-openai.openai.azure.com/
AZURE_OPENAI_API_KEY=your-openai-api-key
EMBEDDING_DEPLOYMENT_NAME=text-embedding-3-large
CHAT_DEPLOYMENT_NAME=gpt-4-mini
EMBEDDING_MODEL_NAME=text-embedding-3-large

# インデックス設定
INDEX_NAME=sharepoint-index
DATA_SOURCE_NAME=sharepoint-datasource
SKILLSET_NAME=sharepoint-skillset
INDEXER_NAME=sharepoint-indexer
```

#### Azure AI Searchセットアップ

1. データソース、インデックス、スキルセット、インデクサーを作成：

```python
from Azure_SDK import create_datasource, create_indexes, create_skillset, create_indexer

# 順番に実行（初回のみ）
create_datasource()
create_indexes()
create_skillset()
create_indexer()
```

2. 検索機能をテスト：

```python
from Azure_SDK import test_search

test_search()
```

3. RAGチャットボットを使用：

```bash
python chatbot.py
```

#### SharePoint Webhookセットアップ

1. SharePointアクセスをテスト：

```bash
cd sharepoint_update
python test_sp.py
```

2. webhook購読を設定：

`test_sp.py`で`drive_id`と`notificationUrl`を更新してから実行：

```python
from test_sp import webhookset
webhookset()
```

3. webhookサーバーを起動：

```bash
python fastWeb.py
```

サーバーは以下を実行します：
- パブリックアクセス用のngrokトンネルを開始
- SharePoint変更通知をリッスン
- deltaクエリを処理して増分変更を取得
- 変更されたファイルを自動的にダウンロード

### 📚 APIリファレンス

#### Azure_SDK.py

- `create_datasource()`: SharePointデータソース接続を作成
- `create_indexes()`: ベクトルフィールドを持つ検索インデックスを作成
- `create_skillset()`: AI強化スキルセットを作成
- `create_indexer()`: インデクサーを作成してスケジュール
- `semantic_search(query, top_k=5)`: セマンティック検索を実行
- `vector_search(query_vector, top_k=5)`: ベクトル検索を実行
- `hybrid_search(query, vector=None, top_k=5)`: ハイブリッド検索を実行
- `get_embedding(text)`: テキスト埋め込みベクトルを生成

#### sharepoint_update/test_sp.py

- `get_access_token(tenant_id, client_id, client_secret)`: Microsoft Graphアクセストークンを取得
- `test_sharepoint_access()`: SharePointサイトアクセスをテスト
- `test_document_files()`: SharePointドライブ内のファイルをリスト
- `webhookset()`: webhook購読を作成

#### sharepoint_update/fastWeb.py

- `/api/notify` (GET/POST): Microsoft Graph通知用のwebhookエンドポイント
- `process_notification(data)`: 受信通知を処理
- `sync_delta(delta_link)`: deltaクエリを使用して増分変更を同期

### 🔧 設定

#### Azure ADアプリの権限

Azure ADアプリには以下のMicrosoft Graph API権限が必要です：

- `Sites.Read.All` または `Sites.ReadWrite.All`
- `Files.Read.All` または `Files.ReadWrite.All`

#### サポートされているファイルタイプ

インデクサーは以下を処理するように設定されています：
- PDFファイル (.pdf)
- Wordドキュメント (.docx, .doc)
- テキストファイル (.txt)

除外されるファイルタイプ：
- 画像 (.png, .jpg)

### 🤝 コントリビューション

コントリビューションを歓迎します！お気軽にPull Requestを提出してください。

### 📄 ライセンス

このプロジェクトはMITライセンスの下でライセンスされています。

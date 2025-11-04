from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexerClient, SearchIndexClient
from azure.search.documents.indexes.models import SearchIndexerDataSourceConnection, SearchIndexerDataContainer
from azure.search.documents import SearchClient

from config import (
    SEARCH_SERVICE_NAME,SEARCH_API_KEY,SEARCH_ENDPOINT,SHAREPOINT_SITE_URL,SHAREPOINT_APP_ID,SHAREPOINT_CLIENT_SECRET,
    SHAREPOINT_TENANT_ID,AZURE_OPENAI_API_KEY,DATA_SOURCE_NAME,INDEX_NAME,SKILLSET_NAME,INDEXER_NAME,AZURE_OPENAI_ENDPOINT
    )

credential = AzureKeyCredential(SEARCH_API_KEY)

client = SearchIndexerClient(endpoint=SEARCH_ENDPOINT, credential=credential)
client_index = SearchIndexClient(endpoint=SEARCH_ENDPOINT, credential=credential)

def create_datasource():
    container = SearchIndexerDataContainer(name="defaultSiteLibrary")
    connection_string = f"SharePointOnlineEndpoint={SHAREPOINT_SITE_URL};ApplicationId={SHAREPOINT_APP_ID};ApplicationSecret={SHAREPOINT_CLIENT_SECRET};TenantId={SHAREPOINT_TENANT_ID}"

    data_source_connection = SearchIndexerDataSourceConnection(
        name=DATA_SOURCE_NAME,
        type="sharepoint",
        connection_string = connection_string,
        container=container
    )

    client.create_data_source_connection(data_source_connection)

def create_indexes():
    from azure.search.documents.indexes.models import (
        SearchIndex,
        SimpleField,
        SearchableField,
        SearchFieldDataType,
        VectorSearch,
        VectorSearchAlgorithmConfiguration,
        HnswAlgorithmConfiguration,
        HnswParameters,
        VectorSearchProfile,
        SearchField,
        SemanticConfiguration,
        SemanticSearch,
        SemanticPrioritizedFields,
        SemanticField,
        AzureOpenAIVectorizer,
        AzureOpenAIVectorizerParameters 
    )
    
    index = SearchIndex(
        name=INDEX_NAME,
        fields=[
            SearchField(name="id", type=SearchFieldDataType.String, key=True, sortable=True, filterable=True, facetable=True, analyzer_name="keyword"),
            SearchField(name="title", type=SearchFieldDataType.String, searchable=True, sortable=False, filterable=True, facetable=False, hidden=False),
            SearchField(name="parent_id", type=SearchFieldDataType.String, filterable=True), 
            SearchField(name="content", type=SearchFieldDataType.String),
            SearchField(name="language", type=SearchFieldDataType.String, searchable=False),
            SearchField(name="chunk_text", type=SearchFieldDataType.String, sortable=False, filterable=False, facetable=False, hidden=False,searchable=True),
            # 修正向量字段类型 - 使用Single类型（Azure AI Search标准）
            SearchField(
                name="chunk_vector", 
                type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
                searchable=True,
                hidden=False,
                vector_search_dimensions=3072,
                vector_search_profile_name="my-vector-profile"
            )
        ],
        vector_search=VectorSearch(
            algorithms=[
                HnswAlgorithmConfiguration(
                    name="my-hnsw-config",
                    kind="hnsw",
                    parameters=HnswParameters(
                        m=4,
                        ef_construction=400,
                        ef_search=500,
                        metric="cosine"
                    )
                )
            ],
            profiles=[
                VectorSearchProfile(
                    name="my-vector-profile",
                    algorithm_configuration_name="my-hnsw-config",
                    vectorizer_name="openai-vectorizer"
                )
            ],
            vectorizers=[
                AzureOpenAIVectorizer(
                    vectorizer_name="openai-vectorizer",
                    kind="azureOpenAI",
                    parameters=AzureOpenAIVectorizerParameters(
                        resource_url=AZURE_OPENAI_ENDPOINT,
                        deployment_name="text-embedding-3-large",
                        api_key=AZURE_OPENAI_API_KEY,
                        model_name="text-embedding-3-large",
                        auth_identity=None
                    )
                    
                )
            ]
        ),
        semantic_search=SemanticSearch(
            configurations=[
                SemanticConfiguration(
                    name="default",
                    prioritized_fields=SemanticPrioritizedFields(
                        title_field=SemanticField(field_name="title"),
                        content_fields=[
                            SemanticField(field_name="chunk_text")
                        ]
                    )
                )
            ]
        ),
        default_semantic_configuration_name="default"
    )
    client_index.create_index(index)
    
def create_skillset():
    from azure.search.documents.indexes.models import (
        SearchIndexerSkillset,
        EntityRecognitionSkill,
        AzureOpenAIEmbeddingSkill,
        SplitSkill,
        OutputFieldMappingEntry,
        InputFieldMappingEntry,
        LanguageDetectionSkill,
        SearchIndexerIndexProjection,
        SearchIndexerIndexProjectionSelector,
        SearchIndexerIndexProjectionsParameters,
        IndexProjectionMode
    )

    skillset = SearchIndexerSkillset(
        name=SKILLSET_NAME,
        skills=[
            EntityRecognitionSkill(
                name="entitySkill",
                inputs=[InputFieldMappingEntry(name="text", source="/document/content")],
                outputs=[OutputFieldMappingEntry(name="namedEntities", target_name="named_entities")]
            ),
            LanguageDetectionSkill(
                name="langDetect",
                inputs=[InputFieldMappingEntry(name="text", source="/document/content")],
                outputs=[OutputFieldMappingEntry(name="languageCode", target_name="languageDetected")]
                ),
            SplitSkill(
                name="textSplit",
                description="Split document into chunks",
                context="/document",
                default_language_code="ja",
                text_split_mode="pages",
                maximum_page_length=1024,
                page_overlap_length=256,
                inputs=[
                    InputFieldMappingEntry(name="text", source="/document/content"), 
                    InputFieldMappingEntry(name="languageCode", source="/document/languageDetected")
                ],
                outputs=[OutputFieldMappingEntry(name="textItems", target_name="chunks")]
            ),
            AzureOpenAIEmbeddingSkill(
                name="embeddingSkill",
                description="Generate embeddings",
                context="/document/chunks/*",
                resource_url=AZURE_OPENAI_ENDPOINT,
                api_key=AZURE_OPENAI_API_KEY,
                deployment_name="text-embedding-3-large",
                model_name="text-embedding-3-large",
                dimensions=3072,
                inputs=[InputFieldMappingEntry(name="text", source="/document/chunks/*")],
                outputs=[OutputFieldMappingEntry(name="embedding", target_name="chunk_vector")]
            )
        ],
        index_projection = SearchIndexerIndexProjection(  
            selectors=[  
                SearchIndexerIndexProjectionSelector(  
                    target_index_name=INDEX_NAME,  
                    parent_key_field_name="parent_id",  
                    source_context="/document/chunks/*",  
                    mappings=[  
                        InputFieldMappingEntry(name="chunk_text", source="/document/chunks"),  
                        InputFieldMappingEntry(name="chunk_vector", source="/document/chunks/*/chunk_vector"),
                        InputFieldMappingEntry(name="title", source="/document/title")
                    ],  
                ),  
            ],  
            parameters=SearchIndexerIndexProjectionsParameters(  
                projection_mode=IndexProjectionMode.SKIP_INDEXING_PARENT_DOCUMENTS  
            ),  
        )
    )
    

    client.create_skillset(skillset)

def create_indexer():
    from azure.search.documents.indexes.models import (
    SearchIndexer,
    IndexingSchedule,
    IndexingParameters,
    FieldMapping,
    OutputFieldMappingEntry,
    FieldMappingFunction,
    )

    indexer = SearchIndexer(
        name=INDEXER_NAME,
        data_source_name=DATA_SOURCE_NAME,
        target_index_name=INDEX_NAME,
        skillset_name=SKILLSET_NAME,
        schedule=IndexingSchedule(interval="PT12H", start_time="2025-06-19T00:00:00Z"),
        parameters=IndexingParameters(
            batch_size=None,
            max_failed_items=None,
            max_failed_items_per_batch=None,
            configuration={
                "indexedFileNameExtensions": ".pdf, .docx, .txt,.doc",
                "excludedFileNameExtensions": ".png, .jpg",
                "dataToExtract": "contentAndMetadata",
                "failOnUnsupportedContentType": False,
                "failOnUnprocessableDocument": False
            }
        ),
        field_mappings=[
            FieldMapping(source_field_name="metadata_spo_site_library_item_id", target_field_name="id", mapping_function=FieldMappingFunction(name="base64Encode")),
            FieldMapping(source_field_name="metadata_spo_item_title", target_field_name="title"),
            FieldMapping(source_field_name="metadata_spo_item_language", target_field_name="language"),
            FieldMapping(source_field_name="content", target_field_name="content")
        ],
        output_field_mappings=[
            FieldMapping(source_field_name="/document/chunks/*/chunk_vector",target_field_name="chunk_vector"),
            FieldMapping(source_field_name="/document/chunks/*",target_field_name="chunk_text")
        ]
    )

    client.create_indexer(indexer)

def semantic_search(query, top_k=5):
    """
    执行语义检索
    """
    search_client = SearchClient(endpoint=SEARCH_ENDPOINT, index_name=INDEX_NAME, credential=credential)
    
    try:
        # 使用语义搜索进行检索
        results = search_client.search(
            search_text=query,
            top=top_k,
            include_total_count=True,
            search_mode="all",
            query_type="semantic",
            semantic_configuration_name="default",
            query_caption="extractive",
            query_answer="extractive"
        )
        
        search_results = []
        for result in results:
            search_results.append({
                "id": result.get("id"),
                "title": result.get("title"),
                "content": result.get("content"),
                "score": result.get("@search.score"),
                "captions": result.get("@search.captions", []),
                "answers": result.get("@search.answers", [])
            })
        
        return search_results
    
    except Exception as e:
        print(f"语义搜索错误: {e}")
        return []

def hybrid_search(query, vector=None, top_k=5):
    """
    执行混合搜索（文本 + 向量）
    """
    search_client = SearchClient(endpoint=SEARCH_ENDPOINT, index_name=INDEX_NAME, credential=credential)
    
    try:
        search_params = {
            "search_text": query,
            "top": top_k,
            "include_total_count": True,
            "search_mode": "all"
        }
        
        # 如果提供了向量，添加向量搜索
        if vector:
            from azure.search.documents.models import VectorizedQuery
            search_params["vector_queries"] = [
                VectorizedQuery(
                    vector=vector,
                    k_nearest_neighbors=top_k,
                    fields="chunk_vector"
                )
            ]
        
        results = search_client.search(**search_params)
        
        search_results = []
        for result in results:
            search_results.append({
                "id": result.get("id"),
                "title": result.get("title"),
                "content": result.get("content"),
                "chunk_text": result.get("chunk_text"),
                "score": result.get("@search.score")
            })
        
        return search_results
    
    except Exception as e:
        print(f"混合搜索错误: {e}")
        return []

def get_embedding(text):
    """
    获取文本的嵌入向量（需要调用Azure OpenAI）
    """
    try:
        from openai import AzureOpenAI
        
        client_openai = AzureOpenAI(
            api_key=AZURE_OPENAI_API_KEY,
            api_version="2024-02-01",
            azure_endpoint=AZURE_OPENAI_ENDPOINT
        )
        
        response = client_openai.embeddings.create(
            input=text,
            model="text-embedding-3-large"
        )
        
        return response.data[0].embedding
    
    except Exception as e:
        print(f"获取嵌入向量错误: {e}")
        return None

def vector_search(query_vector, top_k=5):
    """
    执行纯向量搜索
    """
    search_client = SearchClient(endpoint=SEARCH_ENDPOINT, index_name=INDEX_NAME, credential=credential)
    
    try:
        from azure.search.documents.models import VectorizedQuery
        
        results = search_client.search(
            search_text=None,
            vector_queries=[
                VectorizedQuery(
                    vector=query_vector,
                    k_nearest_neighbors=top_k,
                    fields="chunk_vector"
                )
            ],
            top=top_k
        )
        
        search_results = []
        for result in results:
            search_results.append({
                "id": result.get("id"),
                "title": result.get("title"),
                "content": result.get("content"),
                "chunk_text": result.get("chunk_text"),
                "score": result.get("@search.score")
            })
        
        return search_results
    
    except Exception as e:
        print(f"向量搜索错误: {e}")
        return []

def test_search():
    """
    测试搜索功能
    """
    query = "SharePoint文档管理"
    
    print("=== 语义搜索测试 ===")
    semantic_results = semantic_search(query)
    for i, result in enumerate(semantic_results, 1):
        print(f"{i}. {result['title']} (Score: {result['score']:.4f})")
        print(f"   Content: {result['content'][:100]}...")
        if result['captions']:
            print(f"   Caption: {result['captions'][0].get('text', '')}")
        print()
    
    print("=== 向量搜索测试 ===")
    # 获取查询的嵌入向量
    query_vector = get_embedding(query)
    if query_vector:
        vector_results = vector_search(query_vector)
        for i, result in enumerate(vector_results, 1):
            print(f"{i}. {result['title']} (Score: {result['score']:.4f})")
            print(f"   Content: {result['content'][:100]}...")
            print()
    
    print("=== 混合搜索测试 ===")
    if query_vector:
        hybrid_results = hybrid_search(query, query_vector)
        for i, result in enumerate(hybrid_results, 1):
            print(f"{i}. {result['title']} (Score: {result['score']:.4f})")
            print(f"   Content: {result['content'][:100]}...")
            print()

if __name__ == "__main__":
    # 创建索引、技能集和索引器
    # create_datasource()  # 首次运行时取消注释
    # create_indexes()     # 首次运行时取消注释
    # create_skillset()    # 首次运行时取消注释
    # create_indexer()     # 首次运行时取消注释
    
    # 测试搜索功能
    #test_search()
    pass

import yaml


def load_config():
    with open('configs/config.yml', 'r') as f:
        config  = yaml.safe_load(f)
    return config


class LoadConfig:
    def __init__(self):
        config = load_config()
        # GROQ CONFIG
        self.GROQ_MODEL = config['llm_groq']['model']
        self.GROQ_API = config['llm_groq']['api_key']
        self.GROQ_MAX_TOKENS = config['llm_groq']['max_tokens']
        self.GROQ_TEMPERATURE = config['llm_groq']['temperature']
        self.GROQ_TIMEOUT  = config['llm_groq']['timeout']

        # QDRANT_CONFIG
        self.QDRANT_URL = config['qdrant']['url']
        self.QDRANT_API = config['qdrant']['api_key']
        self.QDRANT_COLLECTION = config['qdrant']['collection_name']
        self.QDRANT_DENSE_EMBEDDING = config['qdrant']['dense_embedding']
        self.QDRANT_SPARSE_EMBEDDING = config['qdrant']['sparse_embedding']
        self.QDRANT_INTERACTION_EMBEDDING = config['qdrant']['late_interaction_embedding']
        self.QDRANT_BATCH_SIZE = config['qdrant']['batch_size']
        self.QDRANT_THRESH_SCORE = config['qdrant']['thresh_score']

        # EMBEDDING CONFIG
        self.HUGGINGFACE_API = config['huggingface']['api_key']
        self.BAAI_EMBEDDING = config['huggingface']['baai_embedding']

        #CHROMA CONFIG
        self.CHROMA_PATH  = config['chroma']['db_path']
        self.CHROMA_COLLECTION = config['chroma']['collection']
        self.CHROMA_TOP_K = config['chroma']['top_k']
        self.CHROMA_SCORE_THRESHOLD = config['chroma']['score_threshold']

        self.ELASTIC_CLOUD_ID = config['elastic_search']['cloud_id']
        self.ELASTIC_API_KEY = config['elastic_search']['api_key']  
        self.ELASTIC_INDEX_NAME = config['elastic_search']['index_name'] 
        self.ELASTIC_TIMEOUT = config['elastic_search']['timeout']   
        # DATA CONFIG
        self.FINAL_DATA_PATH = config['data']['final_data_path']
        # RAG CONFIIG
        self.MEMORY_K = 50

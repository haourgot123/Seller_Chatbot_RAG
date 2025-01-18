from fastembed.embedding import TextEmbedding
from fastembed.sparse.bm25 import Bm25
from fastembed.late_interaction import LateInteractionTextEmbedding
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_groq import ChatGroq
from configs.config import LoadConfig

CONFIG_APP = LoadConfig()


class ModelLoader:
    def load_baai_embedding(self):
        embedding = SentenceTransformerEmbeddings(
            model_name = CONFIG_APP.BAAI_EMBEDDING
        )
        return embedding
    def load_dense_embedding(self):
        dense_embedding = TextEmbedding(CONFIG_APP.QDRANT_DENSE_EMBEDDING)
        return dense_embedding
    def load_sparse_embedding(self):
        sparse_embedding = Bm25(CONFIG_APP.QDRANT_SPARSE_EMBEDDING)
        return sparse_embedding
    def load_lateinteraction_embedding(self):
        lateinteraction_embedding = LateInteractionTextEmbedding(CONFIG_APP.QDRANT_INTERACTION_EMBEDDING)
        return lateinteraction_embedding
    def load_llm_model(self):
        return ChatGroq(
            api_key = CONFIG_APP.GROQ_API,
            model = CONFIG_APP.GROQ_MODEL,
            temperature = CONFIG_APP.GROQ_TEMPERATURE,
            max_tokens = CONFIG_APP.GROQ_MAX_TOKENS,
            timeout = CONFIG_APP.GROQ_TIMEOUT
        )




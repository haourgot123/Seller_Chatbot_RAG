import os
import pandas as pd
import logging
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from models.models import ModelLoader
from configs.config import LoadConfig

logging.basicConfig(
    filename='logs/app.log', 
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

CONFIG_APP  = LoadConfig()
CONFIG_MDOEL = ModelLoader()

class DataPreprocesser:
    def __init__(self):
        pass
    def mergering(self, origin_data, new_data, output_file):
        try:
            origin_data = pd.read_csv(origin_data)
            new_data  = pd.read_csv(new_data)
            output_data = pd.concate([origin_data, new_data], axis = 0)
            output_data.to_csv(output_file, index = False)
        except Exception as e:
            logging.error(f'Error when mergering data : {e}')
    def create_document(self):
        final_df = pd.read_csv(CONFIG_APP.FINAL_DATA_PATH)

        documents = []
        
        for _, row in final_df.iterrows():
            content = (
                """
                Tên sản phẩm: {item_name} - Giá gốc: {origin_price}
                Màu sắc và giá
                """
                f'Tên sản phẩm: {row["item_name"]} - '
                f'Giá gốc: {row["origin_price"]}\n'
                f'Màu sắc và giá tương ứng: {row["color_price"]}\n'
                f'Thông số kĩ thuật: {row["technical_infomation"]}\n\n'
            )
            metadata = {
                'item_link' : row['url'],
                'item_name': row['item_name'],
                'orgin_price': row['origin_price'],
                'color_and_price': row['color_price'],
                'technical_infomation': row['technical_infomation']
            }
            documents.append(Document(content, metadata = metadata))
        return documents

class ChromaDB:
    def __init__(self):
        self.embedding = CONFIG_MDOEL.load_baai_embedding()
    def create_db(self, db_path, documents):
        if not os.path.exists(db_path):
            chroma = Chroma.from_documents(
                collection_name = CONFIG_APP.CHROMA_COLLECTION,
                embedding_function = self.embedding,
                documents = documents,
                persist_directory = db_path
            )
            return chroma
        return Chroma(
            persist_directory = db_path,
            embedding_function = self.embedding
        )
class ChromaRetriever:
    def __init__(self):
        pass

    def ensemble_retriever(self, vector_db, documents):
        '''Create ensemble retriever with mmr, vanilla, bm25'''
        mmr_retriever = self.mmr_retriver(vector_db)
        vanilla_retriever = self.vanilla_retriver(vector_db)
        bm25_retriever = self.bm25_retriever(documents)
        # initialize the ensemble retriever with 3 Retrievers
        ensemble_retriever = EnsembleRetriever(
            retrievers=[mmr_retriever, bm25_retriever, vanilla_retriever], 
            weights=[0.2, 0.4, 0.4]
        )
        return ensemble_retriever
    def mmr_retriver(self, vector_db):
        ''' Create mmr retriever with mmr''' 
        mmr = vector_db.as_retriever(
            search_type = 'mmr',
            search_kwargs = {'k': CONFIG_APP.CHROMA_TOP_K}
        )
        return mmr
    def bm25_retriever(self, documents):
        '''Create bm25 retriever'''
        bm25 = BM25Retriever.from_documents(documents, 
                                            search_kwargs = {'k' : CONFIG_APP.CHROMA_TOP_K}
        )
        return bm25
    def vanilla_retriver(self, vector_db):
        '''Create vanilla retriever with similarity search'''
        vanilla =  vector_db.as_retriever(
            search_type = 'similarity',
            search_kwargs = {'k' : CONFIG_APP.CHROMA_TOP_K}
        )
        return vanilla

class ChromaSearchEngine:
    def __init__(self):
        self.documents= DataPreprocesser()
        self.vector_db = ChromaDB()
        self.retriever = ChromaRetriever()
    def search(self, question):
        documents = self.documents.create_document()
        vector_db = self.vector_db.create_db(db_path = CONFIG_APP.CHROMA_PATH,
                                             documents = documents)
        retriever_engine = self.retriever.ensemble_retriever(vector_db = vector_db,
                                                             documents = documents)
        relevent_docs = retriever_engine.invoke(question)
        relevent_docs = "\n".join(doc.page_content for doc in relevent_docs) if relevent_docs else None
        return relevent_docs


if __name__ == "__main__":
    
    search_engine = ChromaSearchEngine()
    relevent_docs = search_engine.search('Hãy cho tôi thông tin vê Iphone 16 promax')
    print(relevent_docs)

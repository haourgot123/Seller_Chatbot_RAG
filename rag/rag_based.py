import logging
from langchain.schema import SystemMessage
from langchain.schema.output_parser import StrOutputParser
from langchain.memory import ConversationBufferMemory
from langchain_groq import ChatGroq
from langchain.chains import LLMChain
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    AIMessagePromptTemplate
)
from models.models import ModelLoader
from vector_db.chroma import ChromaSearchEngine
from vector_db.elastic_search import ElasticSearch
from rag.prompts import SYSTEM_MESSAGE, HUMAN_MESSAGE, AI_MESSAGE
from configs.config import LoadConfig
from rag.utils import Rewriter, Router
from rag.handle_router import RouteHandler
CONFIG_MODEL = ModelLoader()
CONFIG_APP = LoadConfig()

class RAG:
    def __init__(self, user_info, session_id):
        self.user_info = user_info
        self.session_id = session_id
        self.llm = CONFIG_MODEL.load_llm_model()
        self.rewriter = Rewriter()
        self.router = Router(session_id = self.session_id,
                             user_info = self.user_info)
        self.memory = ConversationBufferMemory(k = CONFIG_APP.MEMORY_K,
                                               memory_key = session_id,
                                               input_key = 'human_input',
                                               return_messages=True)
    def run(self, query):
        query = self.rewriter.reflection_query(query = query,
                                               memory = self.memory)
        prompt = self.router.routing_model(question = query)
        try:
            chain = LLMChain(
                prompt = prompt,
                llm = self.llm,
                verbose = True,
                output_parser = StrOutputParser(),
                memory = self.memory
            )
            response = chain.run(human_input = query)
            return response          
        except Exception as e:
                logging.warning(f'Erorr when using RAG invoke function: {e}')    
if __name__ == "__main__":
    session_id, user_info = '1234', 'PThao'
    rag = RAG(session_id = session_id, user_info = user_info)
    while 1:
        query = input('Nhập câu hỏi: ')
        response = rag.run(query)
        print(response)

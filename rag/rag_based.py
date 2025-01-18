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
from rag.prompts import SYSTEM_MESSAGE, HUMAN_MESSAGE, AI_MESSAGE
from configs.config import LoadConfig
CONFIG_MODEL = ModelLoader()
CONFIG_APP = LoadConfig()

class RAG:
    def __init__(self, session_id):
        self.search_engine  = ChromaSearchEngine()
        self.prompt = ChatPromptTemplate.from_messages([
            SystemMessage (
                SYSTEM_MESSAGE
            ),
            MessagesPlaceholder(
                variable_name = session_id
            ),
            HumanMessagePromptTemplate.from_template(
                HUMAN_MESSAGE
            ),
            AIMessagePromptTemplate.from_template(
                AI_MESSAGE
            )
        ])
        self.llm = CONFIG_MODEL.load_llm_model()
        self.memory = ConversationBufferMemory(k = CONFIG_APP.MEMORY_K,
                                               memory_key = session_id,
                                               return_messages=True)
    def invoke(self, query):
        relevent_docs = self.search_engine.search(query)
        self.prompt.messages[0].content = self.prompt.messages[0].content.format(context = relevent_docs,
                                                                                user_info = 'Hà Vi')
        print(self.prompt) 
        try:
            chain = LLMChain(
                prompt = self.prompt,
                llm = self.llm,
                verbose = True,
                output_parser = StrOutputParser(),
                memory = self.memory
            )
            response = chain.predict(human_input = query)
            return response
        except Exception as e:
            logging.warning(f'Erorr when using RAG invoke function: {e}')
        


if __name__ == "__main__":
    query  = 'Hãy liệt kê một vài điện thoại iphone có màu đen và gía 15 triêu'
    rag = RAG(session_id='A1681')
    response = rag.invoke(query)
    print(response)


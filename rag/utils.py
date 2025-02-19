import ast
from groq import Groq
from langchain.schema import SystemMessage
from langchain.chains import LLMChain
from langchain.schema.output_parser import StrOutputParser
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    AIMessagePromptTemplate
)
from models.models import ModelLoader
from rag.prompts import (
    SYSTEM_MESSAGE,
    HUMAN_MESSAGE,
    AI_MESSAGE,
    REWRITE_PROMPT,
    REWRITE_HUMAN_MESSAGE,
    ROUTING_PROMPT, 
    CHITCHAT_SYSTEM,
    CHITCHAT_HUMAN_MESSAGE,
    INSURANCE_SYSTEM,
    INSURANCE_HUMAN,
    PROMPT_ORDER,
    ORDER_HUMAN
)
from configs.config import LoadConfig
from rag.handle_router import RouteHandler
CONFIG_MODEL = ModelLoader()
CONFIG_APP = LoadConfig()

class Rewriter:
    def reflection_query(self, query,  memory, num_message = 10):
        history = [(msg.type, msg.content) for msg in memory.chat_memory.messages]
        if not history:
            return query
        elif len(history) < num_message:
            recent_history = history
        else:
            recent_history = memory[-num_message : ]
        rewrite_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(REWRITE_PROMPT),
            HumanMessagePromptTemplate.from_template(REWRITE_HUMAN_MESSAGE)
        ])
        rewrite_chain = LLMChain(
            prompt = rewrite_prompt,
            llm = ModelLoader().load_llm_model(),
            output_parser = StrOutputParser()
        )
        rewritten_query = rewrite_chain.predict(history = recent_history, human_input = query)
        return rewritten_query.strip()

class Router:
    def __init__(self, session_id, user_info):
        self.route_handler = RouteHandler()
        self.client = Groq(
            api_key = CONFIG_APP.GROQ_API
        )
        self.session_id = session_id
        self.user_info = user_info
        self.route_handler = RouteHandler()
    def classify_question(self, question):
        messages = [
            {"role": "system", "content": ROUTING_PROMPT},
            {"role": "user", "content": f"Phân loại câu hỏi này vào một trong 5 nhóm: {question}"}
        ]
        response = self.client.chat.completions.create(
                model=CONFIG_APP.GROQ_MODEL,
                messages=messages,
                stream=False,
                tools=CONFIG_APP.ROUTING_TOOLS,
                tool_choice="auto",
                max_completion_tokens=CONFIG_APP.GROQ_MAX_TOKENS
        )
        response  = ast.literal_eval(response.choices[0].message.tool_calls[0].function.arguments)
        return response['category']
    
    def routing_model(self, question):
        category_intent = self.classify_question(question) 
        if category_intent.strip() == 'chitchat':
            prompt = self.create_chitchat_prompt()
        elif category_intent.strip() == 'buy':
            prompt = self.create_buy_prompt()
        elif category_intent.strip() == 'consultation': 
            prompt = self.create_consultation_prompt()
            context = self.route_handler.consultation_query_handler(query = question)
            prompt.messages[0].content = prompt.messages[0].content.format(context = context,
                                                                            user_info = self.user_info)
        elif category_intent.strip() == 'insurance':
            prompt = self.create_insurance_prompt() 
        elif category_intent.strip() == 'compare':
            prompt = self.create_compare_prompt()
            context = self.route_handler.compare_query_handler(query = question)
            prompt.messages[0].content = prompt.messages[0].content.format(context = context,
                                                                            user_info = self.user_info)
        return prompt
    
    def create_chitchat_prompt(self):
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(CHITCHAT_SYSTEM),
            MessagesPlaceholder(variable_name = self.session_id),
            HumanMessagePromptTemplate.from_template(CHITCHAT_HUMAN_MESSAGE)
        ])
        return prompt
    def create_buy_prompt(self):
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(PROMPT_ORDER),
            MessagesPlaceholder(variable_name = self.session_id),
            HumanMessagePromptTemplate.from_template(ORDER_HUMAN)
        ])
        return prompt
    def create_consultation_prompt(self):
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(SYSTEM_MESSAGE),
            MessagesPlaceholder(variable_name = self.session_id),
            HumanMessagePromptTemplate.from_template(HUMAN_MESSAGE),
            AIMessagePromptTemplate.from_template(AI_MESSAGE)
        ])
        
        return prompt
    def create_insurance_prompt(self):
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(INSURANCE_SYSTEM),
            MessagesPlaceholder(variable_name = self.session_id),
            HumanMessagePromptTemplate.from_template(INSURANCE_HUMAN)
        ])
        return prompt
    def create_compare_prompt(self):
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(SYSTEM_MESSAGE),
            MessagesPlaceholder(variable_name = self.session_id),
            HumanMessagePromptTemplate.from_template(HUMAN_MESSAGE)
        ])
        return prompt
#Test
# router = Router(session_id = '123')
# questions = [
#     "Anh cần em tư vấn sản phẩm Iphone 12 pro max",
#     "Anh cần mua một sản phẩm điện thoại SamSung có RAM khoảng 8GB",
#     "Em có thể giảm giá cho anh sản phẩm điện thoại này được không?",
#     "Giảm giá sản phẩm này cho anh nhé!"
#     "Anh thấy điện thoại này bên shoppe bán rẻ hơn em ạ",
#     "Anh cần tìm một sản phẩm điện thoại giá rẻ",
#     "Điện thoại ảnh bị xước màn hình, Anh có thể đổi được không em?",
#     "Cho anh chốt đơn 1 chiếc máy bay"
# ]
# for question in questions:
#     prompt = router.routing_model(question)     
#     print(question, '-', prompt)    

        
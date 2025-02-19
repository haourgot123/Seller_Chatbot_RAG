import yaml
import pandas as pd

def load_config():
    with open('configs/config.yml', 'r') as f:
        config  = yaml.safe_load(f)
    return config
def load_dataset():
    dataset = pd.read_csv('data/final.csv')
    return dataset

class LoadConfig:
    def __init__(self):
        phone_dataset = load_dataset()
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
        self.MEMORY_K = 100
        # KEYWORD
        self.CHEAP_KEYWORD = ['rẻ', 'rẻ nhất', 'thấp', 'thấp nhất', 'nhỏ', 'nhỏ nhất', 'tiết kiệm nhất', 'thấp', 'thấp nhất', 'nhỏ', 'nhỏ nhất', 'yếu', 'yếu nhất']
        self.EXPENSIVE_KEYWORD = ['đắt', 'đắt nhất', 'cao', 'cao nhất', 'lớn', 'lớn nhất', 'cao', 'cao nhất', 'lớn', 'lớn nhất', 'manh', 'mạnh nhất', 'trâu', 'trâu nhất']
        # FUNCTION_CALLING TOOLS
        self.ROUTING_TOOLS = [
            {
                "type": "function",
                "function": {
                    "name": "classify_question",
                    "description": "Phân loại câu hỏi của người dùng vào một trong 5 nhóm: chitchat, buy, consultation, compare, insurance",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "category": {
                                "type": "string",
                                "enum": ["chitchat", "buy", "consultation", "compare", "insurance"],
                                "description": "Nhóm phân loại của câu hỏi"
                            }
                        }
                    },
                    "required": ["category"]
                }
            }
        ]
        self.EXTRACT_TOOLS = [
            {
                "type": "function",
                "function": {
                    "name": "extract_data",
                    "description": "Trích xuất thông tin sản phẩm từ câu hỏi của người dùng. Sử dụng khi trong câu hỏi có các thông số như [tên sản phẩm, giá tiền, màu sắc, RAM, bộ nhớ trong, kích thước màn hình, tần số quét màn hình, công nghệ màn hình, dung lượng pin, hoặc các thông số kĩ thuật khác]",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "item_name": {
                                "type": "string",
                                "description": "Trích xuất ra tên cụ thể của điện thoại trong câu hỏi của người dùng. Ví dụ: Iphone 12 pro max, Samsung Galaxy Z Fold3, ..."
                            },
                            "technical_infomation": {
                                "type": "string",
                                "description": "Trích xuất ra các thông số của sản phẩm trong câu hỏi của người dùng. Ví dụ: 2 sim 2 sóng, chế độ ban đêm, xóa phông, quay video 4K, ..."
                            },
                            "price": {
                                "type": "string",
                                "description": "Trích xuất giá tiền trong câu hỏi của người dùng. Ví dụ: 20 triệu, 30 nghìn, ..."
                            },
                            "renew_value": {
                                "type": "string",
                                "description": "Trích xuất gía tiền lên đời sản phẩm trong câu hỏi của người dùng. Ví dụ: 18 triệu, 18k, 20 nghìn, ..."
                            },
                            "color": {
                                "type": "string",
                                "description": "Trích xuất màu sắc trong câu hỏi của người dùng. Ví dụ: Trắng, Đen, ..."
                            },
                            "ram": {
                                "type": "string",
                                "description": "Trích xuất dung lượng RAM trong câu hỏi của người dùng. Ví dụ: 8GB, 16GB, ..."
                            },
                            "in_memory": {
                                "type": "number",
                                "description": "Trích xuất dung lượng bộ nhớ trong câu hỏi của người dùng. Ví dụ: 128GB, 256GB, ..."
                            },
                            "screen_freq": {
                                "type": "string",
                                "description": "Trích xuất ra tần số quét màn hình trong câu hỏi của nguời dùng. Ví dụ: 120Hz, 100Hz, 60Hz, ..."
                            },
                            "screen_size": {
                                "type": "string",
                                "description": "Trích xuất ra thông tin về kích thước màn hình trong câu hỏi của người dùng. Ví dụ: 7.3', 4.5 inch, ..."
                            },
                            "screen_tech": {
                                "type": "string",
                                "description": "Trích xuất thông tin về công nghệ màn hình trong câu hỏi của người dùng. Ví dụ: Super Retina, OLED, ..."
                            },
                            "battery_capacity": {
                                "type": "string",
                                "description": "Trích xuất thông tin về dung lượng pin của sản phẩm từ câu hỏi của người dùng. Ví dụ: 5000mAh, 4000mAh, ..."
                            }
                        },
                        "required": ["item_name", "price","renew_value", "color", "ram", "in_memory", "screen_freq", "screen_size", "screen_tech"]
                    } 
                }
            }
        ]
        self.ORIGIN_PRICE_MIN = phone_dataset['origin_price'].min() 
        self.ORIGIN_PRICE_MAX = phone_dataset['origin_price'].max()
        self.RENEW_VALUE_MIN = phone_dataset['renew_value'].min()
        self.RENEW_VALUE_MAX = phone_dataset['renew_value'].max()
        self.SCREEN_FREQ_MIN = phone_dataset['screen_freq'].min()
        self.SCREEN_FREQ_MAX = phone_dataset['screen_freq'].max()
        self.SCREEN_SIZE_MIN = phone_dataset['screen_size'].min()
        self.SCREEN_SIZE_MAX = phone_dataset['screen_size'].max()
        self.MEMORY_MIN = phone_dataset['in_memory'].min()
        self.MEMORY_MAX = phone_dataset['in_memory'].max()
        self.RAM_MIN = phone_dataset['RAM'].min()
        self.RAM_MAX = phone_dataset['RAM'].max()
        self.BATTERY_MIN = phone_dataset['battery_capacity'].min()
        self.BATTERY_MAX = phone_dataset['battery_capacity'].max()
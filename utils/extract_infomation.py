from groq import Groq
from configs.config import LoadConfig

CONFIG_APP = LoadConfig()

# define function
tools  = [
    {
      "type": "function",
      "function": {
         "name": "extract_data",
         "description": "Trích xuất thông tin sản phẩm từ câu hỏi của người dùng.",
         "parameters": {
            "type": "object",
            "properties": {
                "item_name": {
                    "type": "string",
                    "description": "Trích xuất ra tên cụ thể của điện thoại trong câu hỏi của người dùng. Ví dụ: Iphone 12 pro max, Samsung Galaxy Z Fold3, ..."
                },
                "techinical_infomation": {
                    "type": "string",
                    "description": "Trích xuất ra các thông số của sản phẩm trong câu hỏi của người dùng. Ví dụ: 2 sim 2 sóng, chế độ ban đêm, xóa phông, quay video 4K, ..."
                },
                "price": {
                    "type": "number",
                    "description": "Trích xuất giá tiền trong câu hỏi của người dùng. Ví dụ: 20 triệu, 30 nghìn, ..."
                },
                "renew_value": {
                    "type": "number",
                    "description": "Trích xuất gía tiền lên đời sản phẩm trong câu hỏi của người dùng. Ví dụ: 18 triệu, 18k, 20 nghìn, ..."
                },
                "color": {
                    "type": "string",
                    "description": "Trích xuất màu sắc trong câu hỏi của người dùng. Ví dụ: Trắng, Đen, ..."
                },
                "ram": {
                    "type": "number",
                    "description": "Trích xuất dung lượng RAM trong câu hỏi của người dùng. Ví dụ: 8GB, 16GB, ..."
                },
                "in_memory": {
                    "type": "number",
                    "description": "Trích xuất dung lượng bộ nhớ trong câu hỏi của người dùng. Ví dụ: 128GB, 256GB, ..."
                },
                "screen_freq": {
                    "type": "number",
                    "description": "Trích xuất ra tần số quét màn hình trong câu hỏi của nguời dùng. Ví dụ: 120Hz, 100Hz, 60Hz, ..."
                },
                "screen_size": {
                    "type": "number",
                    "description": "Trích xuất ra thông tin về kích thước màn hình trong câu hỏi của người dùng. Ví dụ: 7.3', 4.5 inch, ..."
                },
                "screen_tech": {
                    "type": "string",
                    "description": "Trích xuất thông tin về công nghệ màn hình trong câu hỏi của người dùng. Ví dụ: Super Retina, OLED, ..."
                },
                "battery_capacity": {
                    "type": "number",
                    "description": "Trích xuất thông tin về dung lượng pin của sản phẩm từ câu hỏi của người dùng. Ví dụ: 5000mAh, 4000mAh, ..."
                }
            },
            "required": ["item_name", "price","renew_value", "color", "ram", "in_memory", "screen_freq", "screen_size", "screen_tech"]
          } 
      }
      
    }
]

def extract_info(query):
    """
    Hàm trích xuất thông tin về sản phẩm từ câu hỏi của nguời dùng.
    """
    user_prompt = f"Trích xuất thông tin từ câu hỏi sau đây: {query}"
    messages = [
        {"role": "system",
         "content": """ Bạn là một chuyên gia trong việc extract thông tin từ câu hỏi của người dùng.
                        Hãy giúp tôi trích xuất các thông tin về thông số kĩ thuật, tên hoặc loại sản phẩm có trong câu hỏi của người dùng.
                        + Nếu câu hỏi có các thông số  lớn, nhỏ, rẻ, đắt, ... thì trả ra cụm đó.
                        + Nếu không có thông số nào thì trả ra '' cho thông số đó.
                        + Nếu câu hỏi có các thông số trâu, trâu nhất, khỏe nhất liên quan đến dung lượng pin thì trả ra cụm đó.
        """},
        {"role": "user",
        "content": user_prompt}
    ]
    client  = Groq(
        api_key = CONFIG_APP.GROQ_API
    )
    response = client.chat.completions.create(
        model = CONFIG_APP.GROQ_MODEL,
        messages = messages,
        stream = False,
        tools = tools,
        tool_choice = "auto",
        max_completion_tokens = CONFIG_APP.GROQ_MAX_TOKENS
    )
    return response.choices[0].message.tool_calls[0].function.arguments



if __name__ == "__main__":
    queries = ["Tôi cần mua một chiếc điện thoại iphone giá 12 triệu",
               "Tôi cần mua một chiếc điện thoại samsung giá rẻ nhất",
               "Tôi cần mua một chiếc điện thoại iphone pin trâu.",
               "Tôi cần mua một chiếc điện thoại 2 sim 2 sóng.",
               "Tôi cần mua một chiếc điện thoại có camera trước 60 fps.",
               "Tôi cần mua một chiếc điện thoại Iphone màu xanh mòng két.",
               "Tôi cần mua một chiếc điện thoại Samsung có giá khoảng 20 triệu."]
    for query in queries:
        response = extract_info(query)
        print(response)
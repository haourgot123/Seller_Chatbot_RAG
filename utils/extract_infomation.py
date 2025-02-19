import time
from groq import Groq
from configs.config import LoadConfig

CONFIG_APP = LoadConfig()

def process_response(response):
    try:
        result = response.choices[0].message.tool_calls[0].function.arguments
        if not result:
            raise ValueError("Không có kết quả hợp lệ từ function calling")
        return result
    except Exception as e:
        print(f"Lỗi khi xử lý phản hồi: {e}")
        return None

def extract_info(query, max_retries = 3, delay = 2):
    user_prompt = f"Trích xuất thông tin từ câu hỏi sau đây: {query}"
    messages = [
        {"role": "system",
         "content": """ Bạn là một chuyên gia trong việc extract thông tin từ câu hỏi của người dùng.
                        Hãy giúp tôi trích xuất các thông tin về thông số kĩ thuật, tên hoặc loại sản phẩm có trong câu hỏi của người dùng.
                        + Nếu câu hỏi về thông số hoặc giá sản phẩm có các cụm từ {rẻ, rẻ nhất, đắt, đắt nhất, lớn, lớn nhất, nhỏ, nhỏ nhất, yếu, yếu nhất, mạng, mạnh nhất, cao, cao nhất, thấp, thấp nhất} thì chỉ trả về chính xác cụm từ xuất hiện trong danh sách {rẻ, rẻ nhất, đắt, đắt nhất, lớn, lớn nhất, nhỏ, nhỏ nhất, yếu, yếu nhất, mạng, mạnh nhất, cao, cao nhất, thấp, thấp nhất} cho thông số mà khách yêu cầu và không thêm tù nào khác.
                        + Nếu trong câu hỏi về dung lượng pin có các cụm từ: trâu, trâu nhất thì trả về chính xác cụm từ đó.
                        + Nếu không có thông số nào thì trả ra '' cho thông số đó.
                        + Nếu trong câu hỏi có tên của 2 sản phẩm thì trả về tên 2 sản phẩm đó ngăn cách nhau bởi dấu ",".
        """},
        {"role": "user",
        "content": user_prompt}
    ]
    client  = Groq(
        api_key = CONFIG_APP.GROQ_API
    )
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=CONFIG_APP.GROQ_MODEL,
                messages=messages,
                stream=False,
                tools=CONFIG_APP.EXTRACT_TOOLS,
                tool_choice="auto",
                max_completion_tokens=CONFIG_APP.GROQ_MAX_TOKENS
            )
            result = process_response(response)
            if result:
                return result 
            print(f"Lần thử {attempt + 1} thất bại, thử lại")
            time.sleep(delay) 
        except Exception as e:
            print(f"Lỗi trong lần thử {attempt + 1}: {e}")
            time.sleep(delay)
    print("Đã thử lại nhiều lần nhưng không có kết quả.")
    return None 


# if __name__ == "__main__":
#     queries = ["Tôi cần mua một chiếc điện thoại iphone giá 12 triệu",
#                "Tôi cần mua một chiếc điện thoại samsung giá rẻ nhất",
#                "Tôi cần mua một chiếc điện thoại iphone pin trâu.",
#                "Tôi cần mua một chiếc điện thoại 2 sim 2 sóng.",
#                "Tôi cần mua một chiếc điện thoại có camera trước 60 fps.",
#                "Tôi cần mua một chiếc điện thoại Iphone màu xanh mòng két.",
#                "Tôi cần mua một chiếc điện thoại Samsung có giá khoảng 20 triệu.",
#                "So sánh Iphone 16 pro max và SamSung Galaxy S22 Ultra   "]
#     for query in queries:
#         response = extract_info(query)
#         print(response)




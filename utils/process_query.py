import re
import ast
from groq import Groq
from configs.config import LoadConfig
from utils.extract_infomation import extract_info

CONFIG_APP = LoadConfig()


def str2dict_fc(data):
    data_clean = data.replace('""', 'None')
    dictionary_data = ast.literal_eval(data_clean)
    for key, value in dictionary_data.items():
        if value == 'None':
            dictionary_data[key] = ""
    return dictionary_data


def parse_range_value(technical_infomaton):
    pattern = r"(?P<prefix>\b(dưới|trên|từ|đến|khoảng|lớn hơn|bé hơn|nhỏ hơn|hơn|)\s*)?(?P<number>\d+(?:,\d+)*)\s*(?P<unit>triệu|nghìn|tr|k|t|g|gb|tb|hz|'|inch|mah)?\b"
    min_value = 0
    max_value = 100000000
    for match in re.finditer(pattern, technical_infomaton, re.IGNORECASE):
        prefix = match.group('prefix') or ''
        number = float(match.group('number').replace(',', ''))
        unit = match.group('unit') or ''
        if unit.lower() == '':
            return min_value, max_value # nếu không phải giá thì trả về giá trị mặc định

        if unit.lower() in ['triệu','tr','t']:
            number *= 1000000
        elif unit.lower() in ['nghìn','k']:
            number *= 1000
        elif unit.lower() in ['g', 'gb']:
            number *= 1
        elif unit.lower() in ['tb']:
            number *= 100

        if prefix.lower().strip() == 'dưới':
            max_value = min(max_value, number)
        elif prefix.lower().strip() == 'trên':
            min_value = min(max_value, number)
        elif prefix.lower().strip() == 'từ':
            min_value = min(max_value, number)
        elif prefix.lower().strip() == 'đến':
            max_value = max(min_value, number)
        elif prefix.lower().strip() in ['lớn hơn', 'hơn']:
            max_value = max(min_value, number)
        elif prefix.lower().strip() in ['bé hơn', 'nhỏ hơn']:
            min_value = min(max_value, number)
        else:  # Trường hợp không có từ khóa
            min_value = number * 0.8    
            max_value = number * 1.2

    if min_value == float('inf'):
        min_value = 0
    return min_value, max_value


def process_price(price_str):
    CHEAP_KEYWORD = CONFIG_APP.CHEAP_KEYWORD
    EXPENSIVE_KEYWORD = CONFIG_APP.EXPENSIVE_KEYWORD
    if price_str in CHEAP_KEYWORD:
        check = 0
        price = {
             "origin_price": {
                "order": "asc"
             }
        }
    elif price_str in EXPENSIVE_KEYWORD:
        check = 0
        price = {
            "origin_price": {
                "order": "desc"
            }
        }
    else:
        min_value, max_value = parse_range_value(price_str)
        if min_value > CONFIG_APP.ORIGIN_PRICE_MAX:
            min_value = CONFIG_APP.ORIGIN_PRICE_MAX * 0.8
        elif max_value < CONFIG_APP.ORIGIN_PRICE_MIN:
            max_value = CONFIG_APP.ORIGIN_PRICE_MIN * 1.2
        check = 1
        price = {
            "range": {
                "origin_price": {
                    "gte": min_value,
                    "lte": max_value
                }
            }
        }
    return price, check


def process_renew_value(renew_value_str):
    CHEAP_KEYWORD = CONFIG_APP.CHEAP_KEYWORD
    EXPENSIVE_KEYWORD = CONFIG_APP.EXPENSIVE_KEYWORD
    if renew_value_str in CHEAP_KEYWORD:
        check = 0
        price = {
             "renew_value": {
                "order": "asc"
             }
        }
    elif renew_value_str in EXPENSIVE_KEYWORD:
        check = 0
        price = {
            "renew_value": {
                "order": "desc"
            }
        }
    else:
        min_value, max_value = parse_range_value(renew_value_str)
        if min_value > CONFIG_APP.RENEW_VALUE_MAX:
            min_value = CONFIG_APP.RENEW_VALUE_MAX * 0.8
        elif max_value < CONFIG_APP.RENEW_VALUE_MIN:
            max_value = CONFIG_APP.RENEW_VALUE_MIN * 1.2
        check = 1
        price = {
            "range": {
                "renew_value": {
                    "gte": min_value,
                    "lte": max_value
                }
            }
        }
    return price, check

def process_screen_freq(screen_freq_str):
    CHEAP_KEYWORD = CONFIG_APP.CHEAP_KEYWORD
    EXPENSIVE_KEYWORD = CONFIG_APP.EXPENSIVE_KEYWORD
    if screen_freq_str in CHEAP_KEYWORD:
        check = 0
        price = {
             "screen_freq": {
                "order": "asc"
             }
        }
    elif screen_freq_str in EXPENSIVE_KEYWORD:
        check = 0
        price = {
            "screen_freq": {
                "order": "desc"
            }
        }
    else:
        min_value, max_value = parse_range_value(screen_freq_str)
        if min_value > CONFIG_APP.SCREEN_FREQ_MAX:
            min_value = CONFIG_APP.SCREEN_FREQ_MAX * 0.8
        elif max_value < CONFIG_APP.SCREEN_FREQ_MIN:
            max_value = CONFIG_APP.SCREEN_FREQ_MIN * 1.2
        check = 1
        price = {
            "range": {
                "screen_freq": {
                    "gte": min_value,
                    "lte": max_value
                }
            }
        }
    return price, check

def process_screen_size(screen_size_str):
    CHEAP_KEYWORD = CONFIG_APP.CHEAP_KEYWORD
    EXPENSIVE_KEYWORD = CONFIG_APP.EXPENSIVE_KEYWORD
    if screen_size_str in CHEAP_KEYWORD:
        check = 0
        price = {
             "screen_size": {
                "order": "asc"
             }
        }
    elif screen_size_str in EXPENSIVE_KEYWORD:
        check = 0
        price = {
            "screen_size": {
                "order": "desc"
            }
        }
    else:
        min_value, max_value = parse_range_value(screen_size_str)
        if min_value > CONFIG_APP.SCREEN_SIZE_MAX:
            min_value = CONFIG_APP.SCREEN_SIZE_MAX * 0.8
        elif max_value < CONFIG_APP.SCREEN_SIZE_MIN:
            max_value = CONFIG_APP.SCREEN_SIZE_MIN * 1.2
        check = 1
        price = {
            "range": {
                "screen_size": {
                    "gte": min_value,
                    "lte": max_value
                }
            }
        }
    return price, check

def process_memory(in_memory_str):
    CHEAP_KEYWORD = CONFIG_APP.CHEAP_KEYWORD
    EXPENSIVE_KEYWORD = CONFIG_APP.EXPENSIVE_KEYWORD
    if in_memory_str in CHEAP_KEYWORD:
        check = 0
        price = {
             "in_memory": {
                "order": "asc"
             }
        }
    elif in_memory_str in EXPENSIVE_KEYWORD:
        check = 0
        price = {
            "in_memory": {
                "order": "desc"
            }
        }
    else:
        min_value, max_value = parse_range_value(in_memory_str)
        if min_value > CONFIG_APP.MEMORY_MAX:
            min_value = CONFIG_APP.MEMORY_MAX * 0.8
        elif max_value < CONFIG_APP.MEMORY_MIN:
            max_value = CONFIG_APP.MEMORY_MIN * 1.2
        check = 1
        price = {
            "range": {
                "in_memory": {
                    "gte": min_value,
                    "lte": max_value
                }
            }
        }
    return price, check


def process_ram(ram_str):
    CHEAP_KEYWORD = CONFIG_APP.CHEAP_KEYWORD
    EXPENSIVE_KEYWORD = CONFIG_APP.EXPENSIVE_KEYWORD
    if ram_str in CHEAP_KEYWORD:
        check = 0
        price = {
             "RAM": {
                "order": "asc"
             }
        }
    elif ram_str in EXPENSIVE_KEYWORD:
        check = 0
        price = {
            "RAM": {
                "order": "desc"
            }
        }
    else:
        min_value, max_value = parse_range_value(ram_str)
        if min_value > CONFIG_APP.RAM_MAX:
            min_value = CONFIG_APP.RAM_MAX * 0.8
        elif max_value < CONFIG_APP.RAM_MIN:
            max_value = CONFIG_APP.RAM_MIN * 1.2
        check = 1
        price = {
            "range": {
                "RAM": {
                    "gte": min_value,
                    "lte": max_value
                }
            }
        }
    return price, check


def process_battery_capacity(battery_capacity_str):
    CHEAP_KEYWORD = CONFIG_APP.CHEAP_KEYWORD
    EXPENSIVE_KEYWORD = CONFIG_APP.EXPENSIVE_KEYWORD
    if battery_capacity_str in CHEAP_KEYWORD:
        check = 0
        price = {
             "battery_capacity": {
                "order": "asc"
             }
        }
    elif battery_capacity_str in EXPENSIVE_KEYWORD:
        check = 0
        price = {
            "battery_capacity": {
                "order": "desc"
            }
        }
    else:
        min_value, max_value = parse_range_value(battery_capacity_str)
        if min_value > CONFIG_APP.BATTERY_MAX:
            min_value = CONFIG_APP.BATTERY_MAX * 0.8
        elif max_value < CONFIG_APP.BATTERY_MIN:
            max_value = CONFIG_APP.BATTERY_MIN * 1.2
        check = 1
        price = {
            "range": {
                "battery_capacity": {
                    "gte": min_value,
                    "lte": max_value
                }
            }
        }
    return price, check

def process_elastic_query(info, check, elastic_query):
    if check == 1:
        elastic_query['query']['bool']['must'].append(info)
    else:
        elastic_query['sort'].append(info)
    return elastic_query

def create_elastic_query(fc_str, elastic_query):
    fc_dict = str2dict_fc(fc_str)
    for key, value in fc_dict.items():  
        if value is None:
            continue
        if key == 'item_name':
            elastic_query['query']['bool']['must'].append({"match": {"item_name": value}})
        if key == 'technical_infomation':
            elastic_query['query']['bool']['must'].append({"match": {"technical_infomation": value}})
        if key == 'color':
            elastic_query['query']['bool']['must'].append({"match": {"colors": value}})
        if key == "price":
            price, check = process_price(value)
            elastic_query = process_elastic_query(price, check, elastic_query)
        if key == "renew_value":
            renew_value, check = process_renew_value(value)
            elastic_query = process_elastic_query(renew_value, check, elastic_query)
        if key == "screen_freq":
            screen_freq, check = process_screen_freq(value)
            elastic_query = process_elastic_query(screen_freq, check, elastic_query)
        if key == "screen_size":
            screen_size, check = process_screen_size(value)
            elastic_query = process_elastic_query(screen_size, check , elastic_query)
        if key == "in_memory":
            memory, check = process_memory(value)
            elastic_query = process_elastic_query(memory, check, elastic_query)
        if key == "ram":
            ram, check  = process_ram(value)
            elastic_query = process_elastic_query(ram, check, elastic_query)
        if key == "battery_capacity":
            battery_capacity, check = process_battery_capacity(battery_capacity, check, elastic_query)
            elastic_query = process_elastic_query(battery_capacity, check, elastic_query)
    
    return elastic_query

# if __name__ == "__main__":
#     queries = ["Tôi cần mua một chiếc điện thoại iphone giá 12 triệu",
#                "Tôi cần mua một chiếc điện thoại samsung giá rẻ nhất",
#                "Tôi cần mua một chiếc điện thoại iphone pin trâu.",
#                "Tôi cần mua một chiếc điện thoại 2 sim 2 sóng.",
#                "Tôi cần mua một chiếc điện thoại có camera trước 60 fps.",
#                "Tôi cần mua một chiếc điện thoại Iphone màu xanh mòng két.",
#                "Tôi cần mua một chiếc điện thoại Samsung có giá khoảng 20 triệu."]
#     for query in queries:
#         elastic_query = {
#             'query': {
#             "bool": {
#                 "must": [
#                 ]
#             }
#         },
#             'sort': []
#         }
#         response = extract_info(query)
#         print(response)
#         elsastic_query = create_elastic_query(response, elastic_query)
#         print(elastic_query)
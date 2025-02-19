from utils.extract_infomation import extract_info
from utils.process_query import create_elastic_query, str2dict_fc
from vector_db.elastic_search import ElasticSearch
from vector_db.chroma import ChromaSearchEngine

def process_elastic_response(elastic_response):
    response = ""
    for i, item in enumerate(elastic_response):
        response += f"""
        Sản phẩm thứ {i + 1}:
        Tên sản phẩm: {item['_source']['item_name']}
        URL: {item['_source']['url']}
        Màu sắc: {item['_source']['colors']}
        Giá gốc: {item['_source']['origin_price']}
        Giá theo màu sắc: {item['_source']['prices']}
        Giá lên đời: {item['_source']['renew_value']}
        Thông số kĩ thuât: {item['_source']['technical_infomation']}
        ==============================================================================================
        """
    return response
        

class RouteHandler:
    def __init__(self):
        self.chroma_search = ChromaSearchEngine()
        self.elastic_search = ElasticSearch()
    def consultation_query_handler(self, query):
        elastic_query = {
            'query': {
                "bool": {
                    "must": []
                }
            },
            'sort': []
        }
        extracted_query = extract_info(query = query) 
        # print(extracted_query)
        elastic_query = create_elastic_query(fc_str = extracted_query,
                                             elastic_query = elastic_query)
        # print(elastic_query)
        elastic_response = self.elastic_search.search(query = elastic_query['query'],
                                                      sort = elastic_query['sort']) 
        hits = elastic_response['hits']['hits']
        if len(hits) == 0:
            hits = self.chroma_search.search(question = query)
        else:
            hits = process_elastic_response(hits)
        return hits
    def compare_query_handler(self, query):
        extracted_query = extract_info(query)
        extracted_query_dict = str2dict_fc(extracted_query)
        print(extracted_query_dict)
        elastic_responses = []
        for item in extracted_query_dict['item_name'].split(','):
            elastic_query = {
                'query': {
                    'bool': {
                        'must': [{'match': {'item_name': item}}]
                    }
                },
                'sort': []
            }
            elastic_response = self.elastic_search.search(query = elastic_query['query'],
                                                         sort = elastic_query['sort'],
                                                         size = 1)
            elastic_responses.append(elastic_response['hits']['hits'])
        elastic_responses = [item[0] for item in elastic_responses]
        elastic_response = process_elastic_response(elastic_responses)
        return elastic_response
                    
    
# handler = RouteHandler()
# while 1:
#     query = input("Nhập query: ")
#     hits = handler.compare_query_handler(query)
#     print(hits)
        
import logging
import pandas as pd
from elasticsearch import Elasticsearch
from configs.config import LoadConfig


CONFIG_APP = LoadConfig()


class ElasticSearch:
    def __init__(self):
        # Define client ElasticSearch
        self.client = Elasticsearch(
            cloud_id = CONFIG_APP.ELASTIC_CLOUD_ID,
            api_key = CONFIG_APP.ELASTIC_API_KEY,
            request_timeout = CONFIG_APP.ELASTIC_TIMEOUT
        )
    def init_index(self, data_path = CONFIG_APP.FINAL_DATA_PATH,  index_name = CONFIG_APP.ELASTIC_INDEX_NAME):
        # Define mapping
        mapping = {
            "dynamic": False,
            "properties": {
                "url": {"type": "text"},
                "item_name": {"type": "text"},
                "colors" : {"type": "text"},
                "prices": {"type": "text"},
                "origin_price": {"type": "integer"},
                "renew_value": {"type": "integer"},
                "technical_infomation": {"type": "text"},
                "screen_freq": {"type" : "integer"},
                "screen_tech": {"type": "text"},
                "screen_size": {"type": "float"},
                "in_memory": {"type": "integer"},
                "RAM": {"type": "integer"},
                "battery_capacity": {"type": "integer"}
            }
        }
        # Create client mapping and documents
        try:
            if not self.client.indices.exists(index = index_name):
                self.client.indices.create(index = index_name, mappings = mapping)
                df  = pd.read_csv(data_path)
                for i, row in df.iterrows():
                    doc = {
                        "url": row["url"],
                        "item_name": row["item_name"].lower(),
                        "colors": row["colors"].lower(),
                        "prices": row["prices"],
                        "origin_price": row["origin_price"],
                        "renew_value": row["renew_value"],
                        "technical_infomation": row["technical_infomation"].lower(),
                        "screen_freq": row["screen_freq"],
                        "screen_tech": row["screen_tech"].lower(),
                        "screen_size": row["screen_size"],
                        "in_memory": row["in_memory"],
                        "RAM": row["RAM"],
                        "battery_capacity": row["battery_capacity"]
                    }
                    self.client.index(document = doc, id = i, index = index_name)
                print('================== Upload data sucessfully =================')
            else:
                print('================== Index name existed ======================')
        except Exception as e:
            logging.error(f"An eror when indexing documents in elasticsearch: {e}")  
    def search(self, query, sort, size = 3):
        response = self.client.search(
            index = CONFIG_APP.ELASTIC_INDEX_NAME,
            size = size,
            query = query,
            sort = sort
        )
        return response

    def delete_index(self, index_name = CONFIG_APP.ELASTIC_INDEX_NAME):
        try:
            response =  self.client.indices.delete(
                index = index_name
            )
            logging.info('Delete Index Successfully!')
        except Exception as e:
            logging.warning(f'Error when delete index elastic search: {e}')
# if __name__ == "__main__":
#     elasticsearch = ElasticSearch()
#     elasticsearch.init_index()
#     infomation = {
#         "item_name": "iphone 13 pro max",
#         "technical_infomation": "1 sim"
#     }
#     query = elasticsearch.create_query(infomation = infomation)

#     res = elasticsearch.search(
#                                 query = query,
#                                sort = [
#                                 {'origin_price': {"order": "asc"}}
#                                ])
#     # elasticsearch.delete_index()
#     for hit in res['hits']['hits']:
#         print(hit['_source']['item_name'])
#     print(len(res['hits']['hits']))


        
import uuid
import argparse
import logging
import pandas as pd
import tqdm
from qdrant_client import QdrantClient, models
from configs.config import LoadConfig
from models.models import ModelLoader



CONFIG_APP = LoadConfig()
CONFIG_MODEL = ModelLoader()



def load_dataset(data_path):
    dataset = pd.read_csv(data_path)
    return [
        {
            'url': row['url'],
            'item_name' : row['item_name'],
            'origin_price': row['origin_price'],
            'color_price': row['color_price'],
            'technical_infomation': row['technical_infomation']
        }
        for _,row in dataset.iterrows()
    ]

def batch_creater(data, batch_size):
    for i in range(0, len(data), batch_size):
        yield data[i : i + batch_size]


class QdrantVectorDatabase:
    def __init__(self, dataset_path, batch_size):
        self.dataset = load_dataset(dataset_path)
        self.batch_size = batch_size
        self.dense_embedding_model = CONFIG_MODEL.load_dense_embedding()
        self.sparse_embedding_model  = CONFIG_MODEL.load_sparse_embedding()
        self.lateinteraction_embedding_model = CONFIG_MODEL.load_lateinteraction_embedding()
        self.client = QdrantClient(
            url = CONFIG_APP.QDRANT_URL,
            api_key = CONFIG_APP.QDRANT_API
        )
    def create_collection(self):
        vectors_config, sparse_config = self.vetor_config()
        return self.client.create_collection(
            collection_name = CONFIG_APP.QDRANT_COLLECTION,
            vectors_config = vectors_config,
            sparse_vectors_config = sparse_config
        )   
    def vetor_config(self):
        dense_embeddings = list(self.dense_embedding_model.passage_embed(self.dataset[0]['item_name']))
        lateinteraction_embeddings = list(self.lateinteraction_embedding_model.passage_embed(self.dataset[0]['item_name']))

        vectors_config = {
            'bge-small-en-v1.5': models.VectorParams(
                size = len(dense_embeddings[0]),
                distance=models.Distance.COSINE
            ),
            'colbertv2.0' : models.VectorParams(
                size= len(lateinteraction_embeddings[0][0]),
                distance= models.Distance.COSINE,
                multivector_config= models.MultiVectorConfig(
                    comparator=models.MultiVectorComparator.MAX_SIM
                )
            )
        }

        sparse_config = {
            'bm25': models.SparseVectorParams(
                modifier=models.Modifier.IDF
            )
        }

        return vectors_config, sparse_config
    def upload_data(self):
        self.client = self.create_collection()
        for batch in tqdm.tqdm(batch_creater(self.dataset, self.batch_size), total= len(self.dataset) // self.batch_size):
            urls = [item['url'] for item in batch]
            item_names = [item['items_name'] for item in batch]
            origin_prices = [item['origin_price'] for item in batch]
            color_prices = [item['color_price'] for item in batch]
            technical_infomations = [item['technical_infomation'] for item in batch]

            dense_embeddings = list(self.dense_embedding_model.passage_embed(item_names))
            sparse_embeddings = list(self.sparse_embedding_model.passage_embed(item_names))
            lateinteraction_embeddings = list(self.lateinteraction_embedding_model.passage_embed(item_names))

            self.client.upload_points(
                collection_name = CONFIG_APP.QDRANT_COLLECTION,
                points = [
                    models.PointStruct(
                        id = uuid.uuid4().hex,
                        vector = {
                            'bge-small-en-v1.5': dense_embeddings[i].to_list(),
                            'bm25': sparse_embeddings[i].as_object(),
                            'colbertv2.0': lateinteraction_embeddings[i].to_list()
                        },
                        payload = {
                            'url': urls[i],
                            'item_name': item_names[i],
                            'origin_price': origin_prices[i],
                            'color_price': color_prices[i],
                            'technical_infomation': technical_infomations[i]
                        }
                    )
                    for i in range(len(item_names))
                ],
                batch_size = self.batch_size
            )
            logging.info('Upload data to Qdrant Successfully')


class HybridSearch:
    def __init__(self):
        self.client = QdrantClient(
            url = CONFIG_APP.QDRANT_URL,
            api_key = CONFIG_APP.QDRANT_API
        )
        self.dense_embedding_model = CONFIG_MODEL.load_dense_embedding()
        self.sparse_embeddiing_model = CONFIG_MODEL.load_sparse_embedding()
        self.lateinteraction_embedding_model = CONFIG_MODEL.load_lateinteraction_embedding()
    def query_docs(self, query_text):
        dense_embedding_query = next(self.dense_embedding_model.query_embed(query_text))
        sparse_embedding_query = next(self.sparse_embeddiing_model.query_embed(query_text))
        lateinteraction_embedding_query = next(self.lateinteraction_embedding_model.query_embed(query_text))

        prerefetch = [
            models.Prefetch(
                query = dense_embedding_query,
                using = 'bge-small-en-v1.5',
                limit = 10,
            ),
            models.Prefetch(
                query = sparse_embedding_query,
                using = 'bm25',
                limit = 10
            ),
            models.Prefetch(
                query = lateinteraction_embedding_query,
                using = 'colbertv2.0',
                limit = 10
            )
        ]

        responses = self.client.query_points(
            collection_name = CONFIG_APP.QDRANT_COLLECTION,
            prefetch = prerefetch,
            query  = models.FusionQuery(
                fusion = models.Fusion.RRF
            ),
            with_payload = True,
            limit = 10
        )

        score_threshold = CONFIG_APP.CHROMA_SCORE_THRESHOLD
        docs = ''
        for i, response in enumerate(responses.points):
            if response.score >= score_threshold:
                docs += f'Example{i + 1}:\n {self.format_output(response)}'
        return docs
    def format_output(self, response):
        url = response.payload['url']
        item_name = response.payload['item_name']
        origin_price = response.payload['origin_price']
        color_price = response.payload['color_price']
        technical_infomation = response.payload['technical_infomation']

        doc = doc = f'''Đường dẫn sản phẩm: {url},\nTên sản phẩm: {item_name},\nGiá gốc: {origin_price},\nMàu sắc và giá: {color_price},\nThông số kĩ thuât: {technical_infomation}\n'''
        return doc


if __name__ == "__main__":
    qdrant = QdrantVectorDatabase(dataset_path = 'data/final.csv',
                                  batch_size = CONFIG_APP.QDRANT_BATCH_SIZE)
    qdrant.upload_data()

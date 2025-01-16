import pandas as pd
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
        for row in dataset.iterrows()
    ]

def batch_creater(data, batch_size):
    for i in range(0, len(data), batch_size):
        yield data[i : i + batch_size]









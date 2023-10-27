import yaml
import argparse
from pprint import pprint

from langchain.chat_models import ChatOpenAI
from applibot.utils.lancedb_store import LanceDBStore
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.embeddings import CacheBackedEmbeddings
from langchain.globals import set_llm_cache
from langchain.cache import SQLiteCache
from langchain.storage import LocalFileStore

class AttributeDict(dict):
    """ Dictionary subclass whose entries can be accessed by attributes
        (as well as normally).
    """
    def __getattr__(self, attr):
        return self[attr]

    def __setattr__(self, attr, value):
        self[attr] = value

    def dict(self):
        return dict(self)

def load_config(yaml_path):
    with open(yaml_path, 'r') as f:
        raw_config = yaml.safe_load(f)

    config_objects = AttributeDict()

    # Derive paths from service.data_path
    data_path = raw_config['service']['data_path']
    lancedb_path = f"{data_path}/lancedb"
    llm_cache_path = f"{data_path}/sqlite"
    embeddings_cache_path = f"{data_path}/ecache"

    # Load vector-store
    config_objects.resume_store = LanceDBStore(
        f"{lancedb_path}",
        raw_config['vector-store']['lancedb']['resume-store']['table-name'],
        raw_config['vector-store']['lancedb']['resume-store']['schema']
    )
    config_objects.info_store = LanceDBStore(
        f"{lancedb_path}",
        raw_config['vector-store']['lancedb']['info-store']['table-name'],
        raw_config['vector-store']['lancedb']['info-store']['schema']
    )

    # Load chat-model
    set_llm_cache(SQLiteCache(database_path=llm_cache_path))
    config_objects.llm = ChatOpenAI(
        openai_api_key=raw_config['chat-model']['key'],
        model=raw_config['chat-model']['model-name'],
        temperature=raw_config['chat-model']['temperature'],
        cache=bool(raw_config['chat-model']['cache']),
    )

    # Load embeddings-model (assuming OpenAIEmbeddings is the only option for now)
    cache_embeddings=bool(raw_config['embeddings-model']['cache'])
    underlying_embeddings = OpenAIEmbeddings(openai_api_key=raw_config['embeddings-model']['key'])
    fs = LocalFileStore(embeddings_cache_path)
    cached_embedder = CacheBackedEmbeddings.from_bytes_store(
        underlying_embeddings, fs, namespace=underlying_embeddings.model
    )
    if cache_embeddings:
            config_objects.embedding = underlying_embeddings
    else:
         config_objects.embedding = cached_embedder

    # Load service details
    config_objects.service = AttributeDict()
    config_objects.service.host = raw_config['service']['host']
    config_objects.service.port = raw_config['service']['port']
    config_objects.service.workers = raw_config['service']['workers']

    config = AttributeDict()
    config.raw = raw_config
    config.objects = config_objects

    return config

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Load configuration from a YAML file.')
    parser.add_argument('--config-yaml', required=True, type=str, help='Path to the configuration YAML file.')
    args = parser.parse_args()

    config_objects = load_config(args.config_yaml)
    pprint(config_objects.dict())

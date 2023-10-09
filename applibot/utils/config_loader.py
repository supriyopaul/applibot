import yaml
import argparse
from pprint import pprint

from langchain.chat_models import ChatOpenAI
from applibot.utils.lancedb_store import LanceDBStore
from langchain.embeddings.openai import OpenAIEmbeddings


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

    # Load vector-store
    config_objects.resume_store = LanceDBStore(
        raw_config['vector-store']['lancedb']['resume-store']['path'],
        raw_config['vector-store']['lancedb']['resume-store']['table-name'],
        raw_config['vector-store']['lancedb']['resume-store']['schema']
    )
    config_objects.info_store = LanceDBStore(
        raw_config['vector-store']['lancedb']['info-store']['path'],
        raw_config['vector-store']['lancedb']['info-store']['table-name'],
        raw_config['vector-store']['lancedb']['info-store']['schema']
    )

    # Load chat-model
    config_objects.llm = ChatOpenAI(
        model=raw_config['chat-model']['model-name'],
        temperature=raw_config['chat-model']['temperature']
    )

    # Load embeddings-model (assuming OpenAIEmbeddings is the only option for now)
    config_objects.embedding = OpenAIEmbeddings()

    # Load service details
    config_objects.service = AttributeDict()
    config_objects.service.host = raw_config['service']['host']
    config_objects.service.port = raw_config['service']['port']

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

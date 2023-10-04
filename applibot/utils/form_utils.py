import argparse
import urllib3
import hashlib

import lancedb
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

embedding = OpenAIEmbeddings()
DB_PATH = "data/lancedb"
INFO_TABLE = "info" 

def compute_sha256(text):
    """Compute the SHA-256 hash of a given text."""
    return hashlib.sha256(text.encode()).hexdigest()

def save_information(text_file):
    loader = TextLoader(text_file)
    documents = loader.load()
    documents = CharacterTextSplitter().split_documents(documents)
    db = lancedb.connect(DB_PATH)
    data = [
        {
            "vector": embedding.embed_query(doc.page_content),
            "text": doc.page_content,
            "id": compute_sha256(doc.page_content),
        }
        for doc in documents
    ]
    if INFO_TABLE not in db.table_names():
        table = db.create_table(
            INFO_TABLE,
            data=data,
            mode="overwrite",
        )
    else:
        table = db.open_table(INFO_TABLE)
        table.add(data)

def retrieve_information_by_similarity(query):
    db = lancedb.connect(DB_PATH)
    table = db.open_table(INFO_TABLE)
    query_vector = embedding.embed_query(query)
    results = table.search(query_vector).limit(5).to_df()
    return results

def main():
    parser = argparse.ArgumentParser(description='Script to save and retrieve information.')
    subparsers = parser.add_subparsers()
    
    parser_save = subparsers.add_parser('save', help='Save information to LanceDB.')
    parser_save.add_argument('--text-file', required=True, type=str, help='Path to the text file to be saved.')
    parser_save.set_defaults(func=save_information)
    
    parser_retrieve = subparsers.add_parser('retrieve', help='Retrieve saved information using similarity from LanceDB.')
    parser_retrieve.add_argument('--query', required=True, type=str, help='Query to search for in the saved documents.')
    parser_retrieve.set_defaults(func=retrieve_information_by_similarity)
    
    args = parser.parse_args()
    
    if 'func' in args:
        args.func(args.text_file if 'text_file' in args else args.query)
    else:
        print("Please specify a sub-command (save or retrieve).")

if __name__ == "__main__":
    main()

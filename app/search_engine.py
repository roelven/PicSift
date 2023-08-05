from elasticsearch import Elasticsearch
import os

class SearchEngine:
    def __init__(self):
        self.es = Elasticsearch([os.getenv('ELASTICSEARCH_URI')])

    def index_document(self, index_name: str, doc_type: str, doc: dict):
        return self.es.index(index=index_name, doc_type=doc_type, body=doc)

    def search(self, index_name: str, query: str):
        return self.es.search(index=index_name, body=query)

    def delete(self, index_name: str, doc_type: str, id: str):
        self.es.delete(index=index_name, doc_type=doc_type, id=id)

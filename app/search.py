import os
import time
from elasticsearch import Elasticsearch, NotFoundError, RequestError, ConnectionError


class SearchError(Exception):
    pass

class ElasticsearchClient:
    def __init__(self, timeout=10, max_retries=5):
        host = os.getenv('ES_HOST', 'localhost')
        port = os.getenv('ES_PORT', 9200)
        self.es = Elasticsearch([{'host': host, 'port': port}], 
                                timeout=timeout, 
                                max_retries=max_retries, 
                                retry_on_timeout=True)
        self._ensure_connected()

    def _ensure_connected(self):
        """Ensure that we can connect to the Elasticsearch instance."""
        for _ in range(self.es.transport.max_retries + 1):
            try:
                if self.es.ping():
                    print("Connected to Elasticsearch")
                    return
            except ConnectionError:
                print("Cannot connect to Elasticsearch, retrying...")
                time.sleep(self.es.transport.timeout)
        raise SearchError("Unable to connect to Elasticsearch")

    def create_index(self, index_name):
        try:
            if not self.es.indices.exists(index=index_name):
                self.es.indices.create(index=index_name)
        except RequestError as e:
            raise SearchError(f"Unable to create index: {str(e)}")

    def index_screenshot(self, index_name, doc_id, document):
        try:
            response = self.es.index(index=index_name, id=doc_id, body=document)
            return response
        except RequestError as e:
            raise SearchError(f"Unable to index document: {str(e)}")

    def search_document(self, index_name, query):
        body = {
            "query": {
                "match": {
                    "text": query
                }
            }
        }
        try:
            res = self.es.search(index=index_name, body=body)
            return res['hits']['hits']
        except RequestError as e:
            raise SearchError(f"Search error: {str(e)}")

    def delete_screenshot(self, index_name, doc_id):
        try:
            self.es.delete(index=index_name, id=doc_id)
        except NotFoundError:
            pass  # It's okay if the document is not found in the index
        except RequestError as e:
            raise SearchError(f"Error deleting document: {str(e)}")

from elasticsearch import Elasticsearch
import os

class SearchEngine:
    def __init__(self):
        host = os.getenv('ES_URI')
        port = os.getenv('ES_PORT')
        self.es = Elasticsearch([f'http://{host}:{port}'])

    def index_image(self, image_data):
        try:
            res = self.es.index(index="screenshots", body=image_data)
            return res['result']
        except Exception as e:
            print('Error while indexing:', e)
            return None

    def search_images(self, query_text):
        try:
            result = self.es.search(index="screenshots", body={
                "query": {
                    "match": {
                        "text": query_text
                    }
                }
            })
            return result
        except Exception as e:
            print('Error while searching for images:', e)
            return None

    def delete_image(self, image_id):
        try:
            self.es.delete(index="screenshots", id=image_id)
        except NotFoundError:
            print(f'Image with id {image_id} not found in index')
        except Exception as e:
            print('Error while deleting image from index:', e)

from elasticsearch import Elasticsearch, NotFoundError

class SearchEngine:
    def __init__(self):
        self.es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

    def index_image(self, image_id, image_data):
        try:
            self.es.index(index="screenshots", id=image_id, body=image_data)
        except Exception as e:
            print('Error while indexing image:', e)

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

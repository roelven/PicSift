from elasticsearch import Elasticsearch, ConnectionError, NotFoundError, TransportError, exceptions
import os
import logging

#
## SET NUMBER OF REPLICAS AND ASSIGN SHARD:
# 
# curl -X PUT "localhost:9200/screenshots" -H 'Content-Type: application/json' -d'
# {
#   "settings" : {
#       "number_of_replicas" : 0,
#       "number_of_shards" : 1
#   }
# }'

# 
## VERIFY IF INDICES HAVE BEEN CREATED:
#
# curl -X GET "localhost:9200/_cat/indices?v"
#

logging.basicConfig(level=logging.INFO)

class SearchEngine:
    def __init__(self):
        self.es = None
        host = os.getenv('ES_URI')
        port = os.getenv('ES_PORT')
        
        try:
            temp_es = Elasticsearch([f'http://{host}:{port}'])
            # A simple ping to see if it's available
            if temp_es.info():
                self.es = temp_es
            else:
                print(f"   ⚠️ Elasticsearch at {host}:{port} did not respond to ping. ")
        except exceptions.ConnectionError:
            print(f"   ⚠️ Failed to connect to Elasticsearch at {host}:{port}.")
        except Exception as e:
            print(f"   ⚠️ An error occurred while trying to connect to Elasticsearch: {e}")

        # Check Elasticsearch health, if we have a valid connection
        if self.es:
            try:
                health = self.es.cluster.health()
                if health['status'] in ['yellow', 'green']:
                    print("   ⏳ Connected to Elasticsearch successfully!")
                else:
                    print("   ⏳ Elasticsearch is running but cluster health is not optimal.")
            except Exception as e:
                print(f"   ⚠️ An error occurred while checking Elasticsearch health: {e}")

    def index_image(self, image_data):
        try:
            res = self.es.index(index="screenshots", body=image_data)
            return res['result']
        except (ConnectionError, TransportError) as e:
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
        except (ConnectionError, TransportError) as e:
            print('Error while searching for images:', e)
            return None

    def delete_image(self, image_id):
        try:
            self.es.delete(index="screenshots", id=image_id)
        except NotFoundError:
            print(f'Image with id {image_id} not found in index')
        except (ConnectionError, TransportError) as e:
            print('Error while deleting image from index:', e)

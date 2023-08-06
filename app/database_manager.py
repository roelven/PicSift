from pymongo import MongoClient, errors
from datetime import datetime
import os

class DatabaseManager:
    def __init__(self):
        self.client = MongoClient(os.getenv('MONGO_CONNECTION'))
        self.db = self.client['screenshot_app']

    def insert_image_data(self, filename, image_url, text):
        # Error handling for database operations
        try:
            collection = self.db['screenshots']
            document = {
                'filename': filename,
                'image_url': image_url,
                'text': text,
                'upload_date': datetime.utcnow()
            }
            result = collection.insert_one(document)
            return {**document, '_id': result.inserted_id}
        except errors.PyMongoError as e:
            print('An error occurred:', e)
            return None

    def get_image_data(self, image_id):
        try:
            collection = self.db['screenshots']
            document = collection.find_one({'_id': image_id})
            return document
        except errors.PyMongoError as e:
            print('An error occurred:', e)
            return None

    def delete_image_data(self, image_id):
        try:
            collection = self.db['screenshots']
            collection.delete_one({'_id': image_id})
        except errors.PyMongoError as e:
            print('An error occurred:', e)

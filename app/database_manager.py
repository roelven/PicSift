from pymongo import MongoClient, errors
from datetime import datetime
import os

class DatabaseManager:
    def __init__(self):
        self.client = MongoClient(os.getenv('MONGO_CONNECTION'))
        self.db = self.client['picsift_db']
        self.collection = self.db['screenshots']

    def store_image_metadata(self, image_data):
        try:
            self.collection.insert_one(image_data)
            print('Image metadata successfully stored in MongoDB as ')
            return {**document, '_id': result.inserted_id}
        except Exception as e:
            print('Error while storing image metadata in MongoDB:', e)

    def get_image_data(self, image_id):
        try:
            document = collection.find_one({'_id': image_id})
            return document
        except errors.PyMongoError as e:
            print('An error occurred:', e)
            return None

    def delete_image_data(self, image_id):
        try:
            collection.delete_one({'_id': image_id})
        except errors.PyMongoError as e:
            print('An error occurred:', e)

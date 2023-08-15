from pymongo import MongoClient, errors
from datetime import datetime
import os
import time

class DatabaseManager:
    def __init__(self):
        mongo_host = os.getenv('MONGODB_URI')
        print(f'   ⏳ Initializing MongoDB client to connect to {mongo_host}... ')
        self.client = MongoClient({mongo_host}, serverSelectionTimeoutMS = 5000)
        self.db = self.client['picsift_db']
        self.collection = self.db['screenshots']

        # Verify MongoDB connection
        try:
            # The ismaster command is cheap and does not require auth.
            self.client.admin.command('ismaster')
            print("   👍 Connected to MongoDB successfully!")
        except Exception as e:
            raise ValueError("   ⚠️ Failed to connect to MongoDB:", e)        

    def store_image_metadata(self, image_data):
        try:
            result = self.collection.insert_one(image_data)
            print('Image metadata successfully stored in MongoDB')
            return {**image_data, '_id': str(result.inserted_id)}
        except Exception as e:
            print('Error while storing image metadata in MongoDB:', e)
            return None

    def get_image_data(self, image_id):
        try:
            document = self.collection.find_one({'_id': image_id})
            return document
        except errors.PyMongoError as e:
            print('An error occurred:', e)
            return None

    def delete_image_data(self, image_id):
        try:
            self.collection.delete_one({'_id': image_id})
        except errors.PyMongoError as e:
            print('An error occurred:', e)
            return None

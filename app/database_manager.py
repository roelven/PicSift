from pymongo import MongoClient
import os

class DatabaseManager:
    def __init__(self):
        self.client = MongoClient(os.getenv('MONGODB_URI'))
        self.db = self.client[os.getenv('MONGODB_DB')]
        self.collection = self.db['screenshots']

    def insert(self, data: dict) -> str:
        result = self.collection.insert_one(data)
        return str(result.inserted_id)

    def find(self, query: dict):
        return self.collection.find(query)

    def delete(self, id: str):
        self.collection.delete_one({'_id': id})

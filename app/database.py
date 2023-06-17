from pymongo import MongoClient, errors

class DatabaseError(Exception):
    pass


class DatabaseClient:
    def __init__(self):
        self.host = os.getenv('MONGO_HOST', 'localhost')
        self.port = int(os.getenv('MONGO_PORT', 27017))
        self.db_name = os.getenv('MONGO_DB', 'screenshotDB')
        self.collection_name = os.getenv('MONGO_COLLECTION', 'screenshots')

        self.client = MongoClient(self.host, self.port)
        self.db = self.client[self.db_name]
        self.collection = self.db[self.collection_name]

    def create_screenshot(self, screenshot_data):
        try:
            result = self.collection.insert_one(screenshot_data)
            return result.inserted_id
        except errors.PyMongoError as e:
            raise DatabaseError(str(e))

    def get_screenshots(self, page, size):
        try:
            screenshots = list(self.collection.find().skip((page - 1) * size).limit(size))
            return screenshots
        except errors.PyMongoError as e:
            raise DatabaseError(str(e))

    def get_screenshot(self, screenshot_id):
        try:
            screenshot = self.collection.find_one({"_id": screenshot_id})
            return screenshot
        except errors.PyMongoError as e:
            raise DatabaseError(str(e))

    def update_screenshot(self, screenshot_id, metadata):
        try:
            result = self.collection.update_one({"_id": screenshot_id}, {"$set": metadata})
            if result.modified_count == 0:
                return None
            return self.get_screenshot(screenshot_id)
        except errors.PyMongoError as e:
            raise DatabaseError(str(e))

    def delete_screenshot(self, screenshot_id):
        try:
            result = self.collection.delete_one({"_id": screenshot_id})
            if result.deleted_count == 0:
                return False
            return True
        except errors.PyMongoError as e:
            raise DatabaseError(str(e))

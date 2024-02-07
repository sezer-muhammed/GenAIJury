from genaijury.database.base import DatabaseInterface
from pymongo import MongoClient
from pymongo.collection import Collection

class MongoDBInterface(DatabaseInterface):
    def __init__(self, uri, database_name, collection_name):
        self.client = MongoClient(uri)
        self.database = self.client[database_name]
        self.collection: Collection = self.database[collection_name]
        self.connect()

    def connect(self):
        # Connection is established in the constructor.
        pass

    def create(self, data):
        result = self.collection.insert_one(data)
        return result.inserted_id

    def read(self, query):
        documents = self.collection.find(query)
        return list(documents)

    def update(self, query, data):
        updated = self.collection.update_many(query, {'$set': data})
        return updated.modified_count

    def delete(self, query):
        deleted = self.collection.delete_many(query)
        return deleted.deleted_count

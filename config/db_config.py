from config.env import Env
from pymongo import MongoClient

class DBClient:
    def __init__(self):
        self.client = MongoClient(Env.MONGO_URI())
        self.db = self.client[Env.DB_NAME()]

    def get_collection(self, collection_name):
        return self.db[collection_name]

    def find_one(self, collection_name, query):
        return self.get_collection(collection_name).find_one({})
    
    def find(self, collection_name, query):
        return self.get_collection(collection_name).find({}).to_list()
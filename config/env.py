
import os
import json

class Env:
    ENV = os.getenv("ENV", "qa")   # default = qa

    @staticmethod
    def _load_config():
        path = os.path.join(os.path.dirname(__file__), "env.json")
        with open(path, "r") as f:
            return json.load(f)[Env.ENV]

    @staticmethod
    def BASE_URL():
        return Env._load_config()["environment"]["API_BASE_URL"]

    @staticmethod
    def USERNAME():
        return Env._load_config()["environment"]["username"]

    @staticmethod
    def PASSWORD():
        return Env._load_config()["environment"]["password"]

    @staticmethod
    def TOKEN():
        return Env._load_config()["environment"]["token"]

    @staticmethod
    def MONGO_URI():
        return Env._load_config()["mongodb"]["uri"]

    @staticmethod
    def DB_NAME():
        return Env._load_config()["mongodb"]["db_name"]


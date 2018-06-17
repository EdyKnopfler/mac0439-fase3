from eadopt.settings import MONGO_HOST, MONGO_PORT
from pymongo import MongoClient

def conectar_mongo():
    client = MongoClient(MONGO_HOST, MONGO_PORT) 
    db = client[MONGO_DATABASE]
    return db

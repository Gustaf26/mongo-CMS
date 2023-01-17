from pymongo import MongoClient
import os
from dotenv import load_dotenv, dotenv_values
config = dotenv_values(".env")
load_dotenv()

def getDB():
    client = MongoClient(os.getenv('Mongo_URI'))
    db = client['butik-vt-23']
    return db

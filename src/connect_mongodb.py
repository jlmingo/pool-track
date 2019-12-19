from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import pymongo
from dotenv import load_dotenv
import os

load_dotenv()

mongodbUrl = os.getenv("CLIENT")
client = MongoClient(mongodbUrl)
try:
    print(f"connecting to {mongodbUrl[0:12]}")
    # The ismaster command is cheap and does not require auth.
    client.admin.command('ismaster')
    print("Connected")
except ConnectionFailure:
    raise Exception("Server not available")


def connect(database, collection):
    db = client[database]
    coll = db[collection]
    return db, coll
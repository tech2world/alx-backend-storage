import pymongo
from pymongo import MongoClient


def connect_to_mongodb():
    """
    Connects to the MongoDB database and returns the collection.
    """
    try:
        client = MongoClient('mongodb://127.0.0.1:27017')
        db = client.logs
        collection = db.nginx
        return collection
    except Exception as e:
        print(f"An error occurred while connecting to MongoDB: {e}")
        return None

def nginx_log_stats(mongo_collection):
    """
    Provides some stats about nginx logs.
    """
    if not mongo_collection:
        return

    print(f'{mongo_collection.count_documents({})} logs')

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print('Methods:')
    for method in methods:
        count = mongo_collection.count_documents({"method": method})
        print(f'\tmethod {method}: {count}')

    num_of_gets = mongo_collection.count_documents({"method": "GET",
                                                     "path": "/status"})
    print(f'{num_of_gets} status check')

if __name__ == "__main__":
    mongo_collection = connect_to_mongodb()
    if mongo_collection:
        nginx_log_stats(mongo_collection)

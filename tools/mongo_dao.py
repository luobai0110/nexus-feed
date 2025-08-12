import os

from dotenv import load_dotenv
from pymongo import MongoClient, UpdateOne

load_dotenv()
mongo_url = os.getenv("MONGO_URL")
client = MongoClient(mongo_url)
db = client['data_collectors']


def save_weather_single_day_data(data):
    collection = db['single_day_weather']
    result = collection.update_one(
        {'_id': data['_id']},
        {'$set': data},
        upsert=True
    )
    return result.upserted_id


def save_weather_multiple_day_data(data):
    collection = db['multiple_day_weather']
    result = collection.update_one(
        {'_id': data['_id']},
        {'$set': data},
        upsert=True
    )
    return result.upserted_id


def save_github_trending_data(data):
    collection = db['github_trending']
    result = collection.update_one(
        {'_id': data['_id']},
        {'$set': data},
        upsert=True
    )
    return result.upserted_id


def save_github_trending_data_all(data):
    collection = db['github_trending']
    requests = []
    for one_data in data:
        requests.append(
            UpdateOne(
                {'_id': one_data['_id']},
                {'$set': one_data},
                upsert=True
            )
        )
    if requests:
        result = collection.bulk_write(requests)
        return result.bulk_api_result
    return None

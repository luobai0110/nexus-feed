import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
mongo_url = os.getenv("MONGO_URL")
client = MongoClient(mongo_url)
db = client['data_collectors']


def save_weather_single_day_data(data):
    collection = db['single_day_weather']
    result = collection.insert_one(data)
    return result.inserted_id

def save_weather_multiple_day_data(data):
    collection = db['multiple_day_weather']
    result = collection.insert_one(data)
    return result.inserted_id
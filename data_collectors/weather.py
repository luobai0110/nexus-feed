# 在 data-collectors/weather.py 文件中修改函数
import os
import json
from bson import ObjectId
import requests
from dotenv import load_dotenv

from tools import mongo_dao

load_dotenv("../.env")
amap_key = os.getenv("AMAP_KEY")

amap_url = "https://restapi.amap.com/v3/weather/weatherInfo?key=" + amap_key
open_weather_url = ""

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

def get_weather_data(city="330108"):
    url = amap_url + "&city=" + city
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        mongo_dao.save_weather_single_day_data(data)
        # 返回JSON格式数据而不是包含ObjectId的对象
        return json.dumps(data, cls=JSONEncoder)
    return json.dumps({"error": "Failed to fetch weather data"})

def get_weather_multiple_day_data(city="330108"):
    url = amap_url + "&city=" + city + "&extensions=all"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        mongo_dao.save_weather_multiple_day_data(data)
        # 返回JSON格式数据而不是包含ObjectId的对象
        return json.dumps(data, cls=JSONEncoder)
    return json.dumps({"error": "Failed to fetch weather data"})

import os

import requests
from dotenv import load_dotenv

from tools import mongo_dao

load_dotenv("../.env")
amap_key=os.getenv("AMAP_KEY")

amap_url = "https://restapi.amap.com/v3/weather/weatherInfo?key=" + amap_key
open_weather_url = ""

def get_weather_data(city="330108"):
    url = amap_url + "&city=" + city
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        mongo_dao.save_weather_single_day_data(data)


def get_weather_multiple_day_data(city="330108"):
    url = amap_url + "&city=" + city + "&extensions=all"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        mongo_dao.save_weather_multiple_day_data(data)
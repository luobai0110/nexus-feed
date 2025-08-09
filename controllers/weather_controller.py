from flask import Blueprint


from tools.city_dao import CityDao
from tools.database_pg import get_db_session
from data_collectors.weather import get_weather_data, get_weather_multiple_day_data

weather_bp = Blueprint('weather', __name__, url_prefix="/api/nexus-feed/weather")
db_session = get_db_session()
city_dao = CityDao(db_session)

@weather_bp.route('/single/<city_name>')
def get_weather_single(city_name):
    city_code = city_dao.get_city(city_name).ad_code
    return get_weather_data(city_code)

@weather_bp.route('/multiple/<city_name>')
def get_weather_multiple(city_name):
    city_code = city_dao.get_city(city_name).ad_code
    return get_weather_multiple_day_data(city_code)

@weather_bp.route('/')
def get_weather():
    return get_weather_data()

# 通过adcode获取
@weather_bp.route('/<city_code>')
def get_weather_by_code(city_code):
    return get_weather_data(city_code)


@weather_bp.route('/<uuid>')
def get_weather_by_id(uuid):
    city_code = city_dao.get_city_by_uuid(uuid).ad_code
    return get_weather_data(uuid)

@weather_bp.route('/update')
def update_weather():
    return 'Update weather successfully.'

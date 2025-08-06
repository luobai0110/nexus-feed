from flask import Blueprint

weather_bp = Blueprint('weather', __name__, url_prefix="/weather")


@weather_bp.route('/single/<city_name>')
def get_weather_single(city_name):
    return f'The weather in {city_name} is sunny.'

@weather_bp.route('/multiple/<city_name>')
def get_weather_multiple(city_name):
    return f'The weather in {city_name} is sunny.'

@weather_bp.route('/update')
def update_weather():
    return 'Update weather successfully.'

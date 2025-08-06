from flask import Flask

from controllers.weather_controller import weather_bp

app = Flask(__name__)


app.register_blueprint(weather_bp)
@app.route('/')
def hello_world():
    return '<h1>nexus-feed</h1>'
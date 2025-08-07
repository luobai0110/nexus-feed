import atexit
import os
import socket
import time
import uuid

import consul
from dotenv import load_dotenv
from flask import Flask, jsonify

from controllers.weather_controller import weather_bp
load_dotenv()
host = os.getenv("SERVER_HOST")
app = Flask(__name__)


app.register_blueprint(weather_bp)
@app.route('/')
def hello_world():
    return '<h1>nexus-feed</h1>'

def get_host_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

SERVICE_NAME = "nexus-feed"
SERVICE_ID = f"{SERVICE_NAME}-{uuid.uuid4()}"
SERVICE_PORT = 8000
SERVICE_IP = get_host_ip()

consul_client = consul.Consul(host=host, port=os.getenv("CONSUL_PORT"))
START_TIME = time.time()
register_success = False
def register_service():
    global register_success
    consul_client.agent.service.register(
        name=SERVICE_NAME,
        service_id=SERVICE_ID,
        address=SERVICE_IP,
        port=SERVICE_PORT,
        tags=["nexus-feed"],
        check=consul.Check.tcp(SERVICE_IP, SERVICE_PORT, "10s")
    )
    register_success = True
    print(f"Registered service {SERVICE_ID} to Consul")


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "registered_in_consul": register_success,
        "service_name": SERVICE_NAME,
        "service_id": SERVICE_ID,
        "ip": SERVICE_IP,
        "port": SERVICE_PORT,
        "uptime_seconds": round(time.time() - START_TIME, 2)
    }), 200


def deregister_from_consul():
    consul_client.agent.service.deregister(SERVICE_ID)
    print(f"Deregistered service {SERVICE_ID} from Consul")

atexit.register(deregister_from_consul)

if __name__ == '__main__':
    register_service()
    app.run(host="0.0.0.0", port=SERVICE_PORT)
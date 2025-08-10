import atexit
import os
import socket
import time
import uuid

import consul
from dotenv import load_dotenv
from flask import Flask, jsonify

from controllers.github_controllers import github_bp
from controllers.weather_controller import weather_bp
load_dotenv()

host = os.getenv("SERVER_HOST", "192.168.78.3")
app = Flask(__name__)

app.register_blueprint(weather_bp)
app.register_blueprint(github_bp)
@app.route('/')
def hello_world():
    return '<h1>nexus-feed</h1>'


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


def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception as e:
        print(f"Error getting host IP: {e}")
        return "192.168.78.3"


# 常量定义应该在使用之前
SERVICE_NAME = "nexus-feed"
SERVICE_ID = f"{SERVICE_NAME}-{uuid.uuid4()}"
SERVICE_PORT = int(os.getenv("SERVICE_PORT", 8000))  # 确保端口是整数
SERVICE_IP = get_host_ip()

# Consul客户端初始化
consul_host = os.getenv("CONSUL_HOST", "localhost")
consul_port = int(os.getenv("CONSUL_PORT", 8500))  # 提供默认端口
consul_client = consul.Consul(host=consul_host, port=consul_port)

START_TIME = time.time()
register_success = False


def register_service():
    global register_success
    try:
        # 检查Consul是否可达
        consul_client.agent.self()  # 测试连接

        # 注册服务
        check = consul.Check.http(
            f"http://{SERVICE_IP}:{SERVICE_PORT}/health",
            interval="10s",
            timeout="5s"
        )

        consul_client.agent.service.register(
            name=SERVICE_NAME,
            service_id=SERVICE_ID,
            address=SERVICE_IP,
            port=SERVICE_PORT,
            tags=["nexus-feed"],
            check=check
        )

        register_success = True
        print(f"Successfully registered service {SERVICE_ID} to Consul")
        print(f"Service details: {SERVICE_NAME} at {SERVICE_IP}:{SERVICE_PORT}")

    except Exception as e:
        print(f"Failed to register service to Consul: {e}")
        register_success = False


def deregister_from_consul():
    try:
        consul_client.agent.service.deregister(SERVICE_ID)
        print(f"Deregistered service {SERVICE_ID} from Consul")
    except Exception as e:
        print(f"Error deregistering from Consul: {e}")


# 注册退出处理函数
atexit.register(deregister_from_consul)

if __name__ == '__main__':
    register_service()
    if register_success:
        print(f"Starting Flask app on {SERVICE_IP}:{SERVICE_PORT}")
        app.run(host="0.0.0.0", port=SERVICE_PORT, debug=False)
    else:
        print("Failed to start service due to Consul registration failure")
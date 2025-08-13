import atexit
import os
import signal
import socket
import sys
import time

import nacos
from dotenv import load_dotenv
from flask import Flask

from controllers.github_controllers import github_bp
from controllers.weather_controller import weather_bp
from tools.nacos import NacosServiceRegistry

load_dotenv()

app = Flask(__name__)
app.register_blueprint(weather_bp)
app.register_blueprint(github_bp)

SERVICE_PORT = os.getenv("SERVICE_PORT", 8000)
SERVER_HOST = os.getenv('SERVER_HOST', '192.168.78.3')
SERVICE_NAME = os.getenv("SERVICE_NAME", "nexus-feed")
NACOS_PORT = os.getenv("NACOS_PORT", 8848)
NACOS_GROUP = os.getenv("NACOS_GROUP", "DEFAULT_GROUP")
NACOS_NAMESPACE = os.getenv("NACOS_NAMESPACE", "public")

client = nacos.NacosClient(f"{SERVER_HOST}:{NACOS_PORT}", namespace="public")
SERVICE_IP = socket.gethostbyname(socket.gethostname())

nacos_registry = NacosServiceRegistry(
    server_addresses=f"{SERVER_HOST}:{NACOS_PORT}",
    namespace=NACOS_NAMESPACE,
    group=NACOS_GROUP
)


def deregister_from_nacos(signum, frame):
    """优雅关闭处理"""
    print("\n🔄 正在关闭服务...")
    nacos_registry.deregister_service()
    sys.exit(0)


signal.signal(signal.SIGINT, deregister_from_nacos)
signal.signal(signal.SIGTERM, deregister_from_nacos)

atexit.register(deregister_from_nacos)


@app.route('/')
def hello_world():
    return {
        'message': 'Hello from Flask with Nacos!',
        'service': SERVICE_NAME,
        'ip': SERVICE_IP,
        'port': SERVICE_PORT
    }


def register_service():
    """在第一次请求前注册服务"""
    success = nacos_registry.register_service(
        service_name=SERVICE_NAME,
        ip=SERVICE_IP,
        port=SERVICE_PORT,
        weight=1.0,
        metadata={
            "preserved.register.source": "PYTHON",
            "version": "1.0.0",
            "timestamp": str(int(time.time()))
        }
    )
    if success:
        print("🚀 服务启动完成")
    else:
        print("⚠️  服务注册失败，但应用将继续运行")


with app.app_context():
    register_service()


@app.route('/health')
def health_check():
    """健康检查接口"""
    return {
        'status': 'UP',
        'service': SERVICE_NAME,
        'timestamp': int(time.time())
    }


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=SERVICE_PORT, debug=False)

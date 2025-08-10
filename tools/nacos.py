import threading
import time

import nacos


class NacosServiceRegistry:
    def __init__(self, server_addresses, namespace="public", group="DEFAULT_GROUP"):
        self.client = nacos.NacosClient(server_addresses, namespace=namespace)
        self.namespace = namespace
        self.group = group
        self.heartbeat_thread = None
        self.running = False
        self.service_info = {}

    def register_service(self, service_name, ip, port, weight=1.0, metadata=None):
        """注册服务到 Nacos"""
        try:
            # 注册服务实例
            self.client.add_naming_instance(
                service_name=service_name,
                ip=ip,
                port=port,
                group_name=self.group,
                weight=weight,
                metadata=metadata or {},
                ephemeral=True  # 临时实例，需要心跳维持
            )

            # 保存服务信息用于心跳
            self.service_info = {
                'service_name': service_name,
                'ip': ip,
                'port': port,
                'weight': weight,
                'metadata': metadata
            }

            print(f"✅ 服务注册成功: {service_name} -> {ip}:{port}")

            # 启动心跳线程
            self.start_heartbeat()

            return True
        except Exception as e:
            print(f"❌ 服务注册失败: {e}")
            return False

    def start_heartbeat(self):
        """启动心跳线程"""
        if self.running:
            return

        self.running = True
        self.heartbeat_thread = threading.Thread(target=self._heartbeat_worker, daemon=True)
        self.heartbeat_thread.start()
        print("💓 心跳线程已启动")

    def _heartbeat_worker(self):
        """心跳工作线程"""
        while self.running:
            try:
                if self.service_info:
                    # 发送心跳
                    self.client.send_heartbeat(
                        service_name=self.service_info['service_name'],
                        ip=self.service_info['ip'],
                        port=self.service_info['port'],
                        group_name=self.group,
                        weight=self.service_info['weight']
                    )
                # 等待指定时间
                time.sleep(5)  # 每5秒发送一次心跳

            except Exception as e:
                print(f"❌ 心跳发送失败: {e}")
                time.sleep(5)  # 出错后继续尝试

    def deregister_service(self):
        """注销服务"""
        if not self.service_info:
            return

        try:
            self.running = False  # 停止心跳

            self.client.remove_naming_instance(
                service_name=self.service_info['service_name'],
                ip=self.service_info['ip'],
                port=self.service_info['port'],
                group_name=self.group
            )

            print(f"✅ 服务注销成功: {self.service_info['service_name']}")
        except Exception as e:
            print(f"❌ 服务注销失败: {e}")
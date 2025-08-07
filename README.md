# Nexus Feed

一个基于Flask的天气数据收集和API服务项目。

## 项目说明

Nexus Feed是一个用于收集、存储和提供天气数据的服务。它使用高德地图API获取天气数据，并将数据存储在MongoDB中。

### 主要功能

- 获取单日天气数据
- 获取多日天气预报数据
- 通过城市名称或城市代码查询天气
- 数据自动存储到MongoDB

## 技术栈

- Python 3.9
- Flask
- PostgreSQL (城市数据)
- MongoDB (天气数据)
- Docker

## 环境要求

- Python 3.9+
- PostgreSQL
- MongoDB
- Docker (可选)

## 安装与运行

### 本地运行

1. 克隆项目

```bash
git clone <repository-url>
cd nexus-feed
```

2. 创建并激活虚拟环境

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. 安装依赖

```bash
pip install -r requirements.txt
```

4. 配置环境变量

```bash
cp .env.example .env
# 编辑.env文件，填入实际的配置值
```

5. 运行应用

```bash
flask run --host=0.0.0.0 --port=8000
```

### 使用Docker运行

1. 构建Docker镜像

```bash
docker build -t nexus-feed .
```

2. 运行Docker容器

```bash
docker run -p 8000:8000 --env-file .env nexus-feed
```

## API接口

### 获取单日天气

```
GET /weather/single/<city_name>
```

### 获取多日天气预报

```
GET /weather/multiple/<city_name>
```

### 通过城市代码获取天气

```
GET /weather/<city_code>
```

## 开发指南

### 项目结构

```
├── controllers/         # 控制器
├── data_collectors/     # 数据收集器
├── data_read/           # 数据读取
├── tools/               # 工具类
├── main.py              # 应用入口
├── Dockerfile           # Docker配置
├── requirements.txt     # 项目依赖
└── .env.example         # 环境变量示例
```

### 添加新的数据源

1. 在`data_collectors`目录下创建新的数据收集模块
2. 在`controllers`目录下创建对应的控制器
3. 在`main.py`中注册新的蓝图

## 许可证

[MIT](LICENSE)
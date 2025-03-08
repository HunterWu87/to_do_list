from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import json

# 如果不存在，创建数据目录
os.makedirs('data', exist_ok=True)

# 创建数据库引擎
DATABASE_URL = "sqlite:///data/todo.db"
engine = create_engine(DATABASE_URL)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 为我们的模型创建基类
Base = declarative_base()

# 配置文件路径
CONFIG_FILE = "data/config.json"

def get_db():
    """
    获取数据库会话
    """
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()

def init_db():
    """
    初始化数据库
    """
    Base.metadata.create_all(bind=engine)

def save_config(config_data):
    """
    保存配置到文件
    """
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config_data, f)

def load_config():
    """
    从文件加载配置
    """
    if not os.path.exists(CONFIG_FILE):
        return {}
    
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {} 
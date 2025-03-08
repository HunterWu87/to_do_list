from sqlalchemy import create_engine  # 导入SQLAlchemy的create_engine函数，用于创建数据库引擎
from sqlalchemy.ext.declarative import declarative_base  # 导入declarative_base，用于创建ORM模型的基类
from sqlalchemy.orm import sessionmaker  # 导入sessionmaker，用于创建数据库会话
import os  # 导入os模块，用于文件和目录操作
import json  # 导入json模块，用于处理JSON格式的数据

# 如果不存在，创建数据目录
# exist_ok=True 参数表示如果目录已存在，不会引发错误
os.makedirs('data', exist_ok=True)

# 创建数据库引擎
# 这里使用SQLite数据库，数据库文件保存在data/todo.db
DATABASE_URL = "sqlite:///data/todo.db"
# create_engine创建了一个数据库引擎，它是SQLAlchemy与数据库交互的入口点
engine = create_engine(DATABASE_URL)

# 创建会话工厂
# sessionmaker创建一个工厂，用于生成与数据库交互的会话对象
# autocommit=False：默认不自动提交事务
# autoflush=False：默认不自动刷新更改到数据库
# bind=engine：将会话绑定到我们创建的引擎
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 为我们的模型创建基类
# declarative_base()返回一个类，所有ORM模型类都将继承这个基类
Base = declarative_base()

# 配置文件路径
# 用于存储用户配置，如上次选择的分类等
CONFIG_FILE = "data/config.json"

def get_db():
    """
    获取数据库会话
    
    返回:
        一个数据库会话对象，用于与数据库交互
        
    注意:
        使用try-finally确保会话在使用后被关闭，防止资源泄漏
    """
    # 创建一个新的数据库会话
    db = SessionLocal()
    try:
        # 返回会话供调用者使用
        return db
    finally:
        # 确保会话在使用后被关闭
        # 这部分代码会在函数返回后执行
        db.close()

def init_db():
    """
    初始化数据库
    
    作用:
        根据模型定义创建数据库表结构
        如果表已存在，则不会重新创建
    """
    # create_all方法会根据Base的子类(即我们的模型类)创建所有表
    Base.metadata.create_all(bind=engine)

def save_config(config_data):
    """
    保存配置到文件
    
    参数:
        config_data: 要保存的配置数据，通常是一个字典
        
    作用:
        将配置数据序列化为JSON并保存到配置文件
    """
    # 以写模式打开配置文件，如果文件不存在则创建
    # encoding='utf-8'确保正确处理中文等Unicode字符
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        # 将配置数据转换为JSON格式并写入文件
        json.dump(config_data, f)

def load_config():
    """
    从文件加载配置
    
    返回:
        配置数据字典，如果文件不存在或格式错误则返回空字典
        
    作用:
        读取配置文件并将JSON数据反序列化为Python对象
    """
    # 检查配置文件是否存在
    if not os.path.exists(CONFIG_FILE):
        # 如果不存在，返回空字典
        return {}
    
    try:
        # 尝试打开并读取配置文件
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            # 将JSON数据转换为Python对象并返回
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        # 如果文件格式错误或找不到文件，返回空字典
        return {} 
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, Text, Enum  # 导入SQLAlchemy的列类型和工具
from sqlalchemy.orm import relationship  # 导入relationship，用于定义模型之间的关系
import enum  # 导入enum模块，用于创建枚举类型
from datetime import datetime  # 导入datetime，用于处理日期和时间

from models.database import Base  # 从database模块导入Base类，所有模型都将继承这个类

class PriorityEnum(enum.Enum):
    """
    任务优先级的枚举类
    
    定义了三个优先级级别：低、中、高
    每个级别对应一个字符串值，用于存储在数据库中
    """
    LOW = "low"      # 低优先级
    MEDIUM = "medium"  # 中优先级
    HIGH = "high"    # 高优先级

class Category(Base):
    """
    分类模型
    
    用于对任务进行分组，如工作、个人、学习等
    """
    __tablename__ = "categories"  # 数据库表名

    # 主键，自动递增的整数ID
    id = Column(Integer, primary_key=True, index=True)
    # 分类名称，必须唯一，并创建索引以加快查询
    name = Column(String, unique=True, index=True)
    # 图标，可以为空
    icon = Column(String, nullable=True)
    # 颜色，默认为蓝色
    color = Column(String, default="#3498db")
    
    # 与任务的关系
    # relationship定义了与Task模型的一对多关系
    # back_populates指定了Task模型中的对应属性名
    # cascade="all, delete-orphan"表示删除分类时，也会删除属于该分类的所有任务
    tasks = relationship("Task", back_populates="category", cascade="all, delete-orphan")

    def __repr__(self):
        """
        返回分类的字符串表示
        
        用于调试和日志记录
        """
        return f"<Category {self.name}>"

class Task(Base):
    """
    任务模型
    
    表示用户的待办事项任务
    """
    __tablename__ = "tasks"  # 数据库表名

    # 主键，自动递增的整数ID
    id = Column(Integer, primary_key=True, index=True)
    # 任务标题，创建索引以加快查询
    title = Column(String, index=True)
    # 任务描述，可以为空
    description = Column(Text, nullable=True)
    # 完成状态，默认为未完成
    completed = Column(Boolean, default=False)
    # 优先级，默认为中等优先级
    priority = Column(String, default=PriorityEnum.MEDIUM.value)
    # 截止日期，可以为空
    due_date = Column(Date, nullable=True)
    # 创建日期，默认为当前日期
    created_at = Column(Date, default=datetime.now().date)
    
    # 分类的外键
    # ForeignKey指定了外键关联的表和列
    category_id = Column(Integer, ForeignKey("categories.id"))
    # relationship定义了与Category模型的多对一关系
    # back_populates指定了Category模型中的对应属性名
    category = relationship("Category", back_populates="tasks")

    def __repr__(self):
        """
        返回任务的字符串表示
        
        用于调试和日志记录
        """
        return f"<Task {self.title}>" 
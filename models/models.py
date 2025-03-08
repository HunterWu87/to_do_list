from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, Text, Enum
from sqlalchemy.orm import relationship
import enum
from datetime import datetime

from models.database import Base

class PriorityEnum(enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    icon = Column(String, nullable=True)
    color = Column(String, default="#3498db")
    
    # 与任务的关系
    tasks = relationship("Task", back_populates="category", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Category {self.name}>"

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text, nullable=True)
    completed = Column(Boolean, default=False)
    priority = Column(String, default=PriorityEnum.MEDIUM.value)
    due_date = Column(Date, nullable=True)
    created_at = Column(Date, default=datetime.now().date)
    
    # 分类的外键
    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", back_populates="tasks")

    def __repr__(self):
        return f"<Task {self.title}>" 
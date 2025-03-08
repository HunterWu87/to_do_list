import sys
import os
import tkinter as tk
from tkinter import ttk

from views import MainWindow
from models import init_db

# 待办事项应用 v0.1
# 一个简洁的个人任务管理桌面应用程序
# 作者：hunter
# 许可证：MIT

def main():
    """应用程序的主入口点"""
    # 如果不存在，创建数据目录
    os.makedirs('data', exist_ok=True)
    
    # 初始化数据库
    init_db()
    
    # 创建应用程序
    root = tk.Tk()
    root.title("待办事项 v0.1")
    
    # 设置主题
    style = ttk.Style()
    style.theme_use("clam")  # 使用现代主题
    
    # 创建并显示主窗口
    app = MainWindow(root)
    
    # 运行应用程序
    root.mainloop()

if __name__ == "__main__":
    main() 
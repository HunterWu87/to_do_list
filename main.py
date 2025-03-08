import sys  # 导入系统模块，用于访问与Python解释器和环境相关的变量和函数
import os   # 导入操作系统模块，用于文件和目录操作
import tkinter as tk  # 导入tkinter库，Python的标准GUI库，用于创建图形用户界面
from tkinter import ttk  # 导入ttk模块，提供了themed Tk小部件，外观更现代

# 从views包导入MainWindow类，这是应用程序的主窗口
from views import MainWindow
# 从models包导入init_db函数，用于初始化数据库
from models import init_db

# 待办事项应用 v0.1
# 一个简洁的个人任务管理桌面应用程序
# 作者：hunter
# 许可证：MIT

def main():
    """应用程序的主入口点"""
    # 如果不存在，创建数据目录
    # exist_ok=True 参数表示如果目录已存在，不会引发错误
    os.makedirs('data', exist_ok=True)
    
    # 初始化数据库
    # 这个函数在models包中定义，用于创建数据库表结构
    init_db()
    
    # 创建应用程序
    # Tk()是tkinter的主窗口类，所有GUI元素都将放在这个窗口中
    root = tk.Tk()
    # 设置窗口标题
    root.title("待办事项 v0.1")
    
    # 设置主题
    # ttk.Style()用于自定义ttk小部件的外观
    style = ttk.Style()
    # 使用"clam"主题，这是一个现代外观的主题
    style.theme_use("clam")  # 使用现代主题
    
    # 创建并显示主窗口
    # 实例化MainWindow类，传入root作为父窗口
    app = MainWindow(root)
    
    # 运行应用程序
    # mainloop()是tkinter的主事件循环，它等待用户操作并处理事件
    root.mainloop()

# 这是Python的标准惯例，确保只有在直接运行此脚本时才执行main()函数
# 如果此文件被导入为模块，则不会执行main()
if __name__ == "__main__":
    main() 
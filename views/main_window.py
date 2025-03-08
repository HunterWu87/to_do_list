import tkinter as tk
from tkinter import ttk, messagebox
import datetime

from views.task_dialog import TaskDialog
from views.category_dialog import CategoryDialog
from models import Category, Task, get_db
from models.database import save_config, load_config

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("待办事项")
        self.root.geometry("900x600")
        self.root.minsize(800, 600)
        
        # 设置全局样式
        style = ttk.Style()
        style.configure("Treeview", font=("TkDefaultFont", 9, "bold"))
        style.configure("Treeview.Heading", font=("TkDefaultFont", 9, "bold"))
        
        # 设置主框架
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建可调整大小的面板窗口
        self.paned_window = ttk.PanedWindow(self.main_frame, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)
        
        # 创建左侧面板（分类）
        self.left_panel = ttk.Frame(self.paned_window, width=200)
        self.paned_window.add(self.left_panel, weight=1)
        
        # 分类标题
        self.category_header = ttk.Label(self.left_panel, text="分类", font=("TkDefaultFont", 12, "bold"))
        self.category_header.pack(pady=(0, 10), anchor=tk.W)
        
        # 分类列表
        self.category_frame = ttk.Frame(self.left_panel)
        self.category_frame.pack(fill=tk.BOTH, expand=True)
        
        self.category_list = ttk.Treeview(self.category_frame, columns=("id",), show="tree")
        self.category_list.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        # 为分类列表添加滚动条
        self.category_scrollbar = ttk.Scrollbar(self.category_frame, orient=tk.VERTICAL, command=self.category_list.yview)
        self.category_scrollbar.pack(fill=tk.Y, side=tk.RIGHT)
        self.category_list.configure(yscrollcommand=self.category_scrollbar.set)
        
        # 分类按钮
        self.category_buttons_frame = ttk.Frame(self.left_panel)
        self.category_buttons_frame.pack(fill=tk.X, pady=5)
        
        self.add_category_button = ttk.Button(self.category_buttons_frame, text="添加", command=self.add_category)
        self.add_category_button.pack(side=tk.LEFT, padx=2)
        
        self.edit_category_button = ttk.Button(self.category_buttons_frame, text="编辑", command=self.edit_category)
        self.edit_category_button.pack(side=tk.LEFT, padx=2)
        
        self.delete_category_button = ttk.Button(self.category_buttons_frame, text="删除", command=self.delete_category)
        self.delete_category_button.pack(side=tk.LEFT, padx=2)
        
        # 创建右侧面板（任务）
        self.right_panel = ttk.Frame(self.paned_window, width=600)
        self.paned_window.add(self.right_panel, weight=3)
        
        # 任务标题
        self.task_header = ttk.Label(self.right_panel, text="任务", font=("TkDefaultFont", 12, "bold"))
        self.task_header.pack(pady=(0, 10), anchor=tk.W)
        
        # 任务列表
        self.task_frame = ttk.Frame(self.right_panel)
        self.task_frame.pack(fill=tk.BOTH, expand=True)
        
        self.task_list = ttk.Treeview(
            self.task_frame, 
            columns=("id", "title", "priority", "completed"),
            show="headings"
        )
        self.task_list.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        # 配置列
        self.task_list.heading("id", text="ID")
        self.task_list.heading("title", text="任务名称")
        self.task_list.heading("priority", text="优先级")
        self.task_list.heading("completed", text="状态")
        
        # 隐藏ID列并调整其他列宽度
        self.task_list.column("id", width=0, stretch=tk.NO)
        self.task_list.column("title", width=250, stretch=tk.YES)
        self.task_list.column("priority", width=60, stretch=tk.NO)
        self.task_list.column("completed", width=60, stretch=tk.NO)
        
        # 为任务列表添加滚动条
        self.task_scrollbar = ttk.Scrollbar(self.task_frame, orient=tk.VERTICAL, command=self.task_list.yview)
        self.task_scrollbar.pack(fill=tk.Y, side=tk.RIGHT)
        self.task_list.configure(yscrollcommand=self.task_scrollbar.set)
        
        # 任务按钮
        self.task_buttons_frame = ttk.Frame(self.right_panel)
        self.task_buttons_frame.pack(fill=tk.X, pady=5)
        
        self.add_task_button = ttk.Button(self.task_buttons_frame, text="添加任务", command=self.add_task)
        self.add_task_button.pack(side=tk.LEFT, padx=2)
        
        self.edit_task_button = ttk.Button(self.task_buttons_frame, text="编辑", command=self.edit_task)
        self.edit_task_button.pack(side=tk.LEFT, padx=2)
        
        self.complete_task_button = ttk.Button(self.task_buttons_frame, text="切换完成状态", command=self.toggle_task_completion)
        self.complete_task_button.pack(side=tk.LEFT, padx=2)
        
        self.delete_task_button = ttk.Button(self.task_buttons_frame, text="删除", command=self.delete_task)
        self.delete_task_button.pack(side=tk.LEFT, padx=2)
        
        # 状态栏
        self.status_bar = ttk.Label(self.root, text="就绪", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # 设置键盘快捷键
        self.root.bind("<Control-n>", lambda event: self.add_task())
        self.root.bind("<Control-e>", lambda event: self.edit_task())
        self.root.bind("<Control-d>", lambda event: self.delete_task())
        self.root.bind("<Control-space>", lambda event: self.toggle_task_completion())
        self.root.bind("<Control-q>", lambda event: self.root.destroy())
        
        # 设置分类选择事件
        self.category_list.bind("<<TreeviewSelect>>", self.category_selected)
        
        # 设置窗口关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # 初始化数据
        self.current_category = None
        self.load_categories()
        
        # 加载上次选择的分类
        self.restore_last_category()
    
    def show_status(self, message, timeout=3000):
        """在状态栏显示消息并在超时后清除"""
        self.status_bar.config(text=message)
        self.root.after(timeout, lambda: self.status_bar.config(text="就绪"))
    
    def load_categories(self):
        """从数据库加载分类"""
        # 清除现有项目
        for item in self.category_list.get_children():
            self.category_list.delete(item)
        
        # 从数据库获取分类
        db = get_db()
        categories = db.query(Category).all()
        
        # 将分类添加到列表
        for category in categories:
            self.category_list.insert("", tk.END, text=category.name, values=(category.id,))
    
    def load_tasks(self):
        """加载选定分类的任务"""
        if not self.current_category:
            return
            
        # 清除现有项目
        for item in self.task_list.get_children():
            self.task_list.delete(item)
        
        # 从数据库获取任务
        db = get_db()
        tasks = db.query(Task).filter(Task.category_id == self.current_category).all()
        
        # 将任务添加到列表
        for task in tasks:
            # 格式化状态
            status = "已完成" if task.completed else "进行中"
            
            # 格式化优先级
            priority_text = "低" if task.priority == "low" else "中" if task.priority == "medium" else "高"
            
            # 添加到列表
            item_id = self.task_list.insert(
                "", 
                tk.END, 
                values=(task.id, task.title, priority_text, status)
            )
            
            # 为所有任务设置相同的黑色字体样式
            self.task_list.item(item_id, tags=("task_item",))
        
        # 配置样式标签 - 所有文字都设置为黑色黑体字
        self.task_list.tag_configure("task_item", font=("TkDefaultFont", 9, "bold"), foreground="black")
    
    def category_selected(self, event):
        """处理分类选择"""
        selected_items = self.category_list.selection()
        if not selected_items:
            return
            
        item = selected_items[0]
        category_id = self.category_list.item(item, "values")[0]
        category_name = self.category_list.item(item, "text")
        
        self.current_category = category_id
        self.task_header.config(text=f"任务 - {category_name}")
        self.load_tasks()
        
        # 保存当前选择的分类ID
        self.save_last_category()
    
    def save_last_category(self):
        """保存最后选择的分类ID"""
        if self.current_category:
            config = load_config()
            config['last_category_id'] = self.current_category
            save_config(config)
    
    def restore_last_category(self):
        """恢复上次选择的分类"""
        config = load_config()
        last_category_id = config.get('last_category_id')
        
        if last_category_id:
            # 查找对应的分类项
            for item in self.category_list.get_children():
                category_id = self.category_list.item(item, "values")[0]
                if str(category_id) == str(last_category_id):
                    # 选择该项
                    self.category_list.selection_set(item)
                    self.category_list.focus(item)
                    self.category_list.see(item)
                    
                    # 手动触发选择事件
                    self.current_category = last_category_id
                    category_name = self.category_list.item(item, "text")
                    self.task_header.config(text=f"任务 - {category_name}")
                    self.load_tasks()
                    break
    
    def on_closing(self):
        """窗口关闭时的处理"""
        # 保存当前选择的分类
        self.save_last_category()
        # 关闭窗口
        self.root.destroy()
    
    def add_category(self):
        """添加新分类"""
        dialog = CategoryDialog(self.root)
        if dialog.result:
            name, icon, color = dialog.result
            
            db = get_db()
            new_category = Category(name=name, icon=icon, color=color)
            db.add(new_category)
            db.commit()
            
            self.load_categories()
            self.show_status(f"分类 '{name}' 已添加")
    
    def edit_category(self):
        """编辑选定的分类"""
        selected_items = self.category_list.selection()
        if not selected_items:
            self.show_status("未选择分类")
            return
            
        item = selected_items[0]
        category_id = self.category_list.item(item, "values")[0]
        
        db = get_db()
        category = db.query(Category).filter(Category.id == category_id).first()
        
        dialog = CategoryDialog(self.root, category)
        if dialog.result:
            name, icon, color = dialog.result
            
            category.name = name
            category.icon = icon
            category.color = color
            db.commit()
            
            self.load_categories()
            self.show_status(f"分类 '{name}' 已更新")
    
    def delete_category(self):
        """删除选定的分类"""
        selected_items = self.category_list.selection()
        if not selected_items:
            self.show_status("未选择分类")
            return
            
        item = selected_items[0]
        category_id = self.category_list.item(item, "values")[0]
        category_name = self.category_list.item(item, "text")
        
        # 确认删除
        if not messagebox.askyesno("确认删除", f"删除分类 '{category_name}' 及其所有任务?"):
            return
        
        db = get_db()
        db.query(Category).filter(Category.id == category_id).delete()
        db.commit()
        
        self.load_categories()
        self.current_category = None
        
        # 清除任务列表
        for item in self.task_list.get_children():
            self.task_list.delete(item)
            
        self.task_header.config(text="任务")
        self.show_status(f"分类 '{category_name}' 已删除")
    
    def add_task(self):
        """添加新任务"""
        if not self.current_category:
            self.show_status("请先选择一个分类")
            return
            
        dialog = TaskDialog(self.root)
        if dialog.result:
            title, description, priority, _ = dialog.result  # 忽略截止日期
            
            db = get_db()
            new_task = Task(
                title=title,
                description=description,
                priority=priority,
                category_id=self.current_category
            )
            db.add(new_task)
            db.commit()
            
            self.load_tasks()
            self.show_status(f"任务 '{title}' 已添加")
    
    def edit_task(self):
        """编辑选定的任务"""
        selected_items = self.task_list.selection()
        if not selected_items:
            self.show_status("未选择任务")
            return
            
        item = selected_items[0]
        task_id = self.task_list.item(item, "values")[0]
        
        db = get_db()
        task = db.query(Task).filter(Task.id == task_id).first()
        
        dialog = TaskDialog(self.root, task)
        if dialog.result:
            title, description, priority, _ = dialog.result  # 忽略截止日期
            
            task.title = title
            task.description = description
            task.priority = priority
            db.commit()
            
            self.load_tasks()
            self.show_status(f"任务 '{title}' 已更新")
    
    def toggle_task_completion(self):
        """切换选定任务的完成状态"""
        selected_items = self.task_list.selection()
        if not selected_items:
            self.show_status("未选择任务")
            return
            
        item = selected_items[0]
        task_id = self.task_list.item(item, "values")[0]
        
        db = get_db()
        task = db.query(Task).filter(Task.id == task_id).first()
        task.completed = not task.completed
        db.commit()
        
        self.load_tasks()
        status = "已完成" if task.completed else "标记为未完成"
        self.show_status(f"任务 '{task.title}' {status}")
    
    def delete_task(self):
        """删除选定的任务"""
        selected_items = self.task_list.selection()
        if not selected_items:
            self.show_status("未选择任务")
            return
            
        item = selected_items[0]
        task_id = self.task_list.item(item, "values")[0]
        
        db = get_db()
        task = db.query(Task).filter(Task.id == task_id).first()
        task_title = task.title
        
        # 确认删除
        if not messagebox.askyesno("确认删除", f"删除任务 '{task_title}'?"):
            return
        
        db.delete(task)
        db.commit()
        
        self.load_tasks()
        self.show_status(f"任务 '{task_title}' 已删除") 
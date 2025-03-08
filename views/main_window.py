import tkinter as tk  # 导入tkinter库，Python的标准GUI库
from tkinter import ttk, messagebox  # 导入ttk模块(提供主题化的小部件)和messagebox模块(用于显示消息对话框)
import datetime  # 导入datetime模块，用于处理日期和时间

from views.task_dialog import TaskDialog  # 导入任务对话框类，用于添加和编辑任务
from views.category_dialog import CategoryDialog  # 导入分类对话框类，用于添加和编辑分类
from models import Category, Task, get_db  # 导入数据模型和获取数据库会话的函数
from models.database import save_config, load_config  # 导入保存和加载配置的函数

class MainWindow:
    """
    应用程序的主窗口类
    
    负责创建和管理用户界面，处理用户交互，并与数据库交互
    """
    def __init__(self, root):
        """
        初始化主窗口
        
        参数:
            root: tkinter的根窗口对象
        """
        self.root = root  # 保存根窗口引用
        self.root.title("待办事项")  # 设置窗口标题
        self.root.geometry("900x600")  # 设置窗口初始大小
        self.root.minsize(800, 600)  # 设置窗口最小大小
        
        # 设置全局样式
        # 创建Style对象，用于自定义ttk小部件的外观
        style = ttk.Style()
        # 配置Treeview(树状视图)的字体为粗体
        style.configure("Treeview", font=("TkDefaultFont", 9, "bold"))
        # 配置Treeview标题的字体为粗体
        style.configure("Treeview.Heading", font=("TkDefaultFont", 9, "bold"))
        
        # 设置主框架
        # 创建一个Frame作为主容器
        self.main_frame = ttk.Frame(self.root)
        # 将主框架放置在窗口中，填充整个窗口并留出边距
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建可调整大小的面板窗口
        # PanedWindow允许用户通过拖动分隔线来调整子窗口的大小
        self.paned_window = ttk.PanedWindow(self.main_frame, orient=tk.HORIZONTAL)
        # 将PanedWindow放置在主框架中，填充整个空间
        self.paned_window.pack(fill=tk.BOTH, expand=True)
        
        # 创建左侧面板（分类）
        # 创建一个Frame作为左侧面板，设置初始宽度
        self.left_panel = ttk.Frame(self.paned_window, width=200)
        # 将左侧面板添加到PanedWindow，权重为1
        self.paned_window.add(self.left_panel, weight=1)
        
        # 分类标题
        # 创建一个Label作为分类列表的标题
        self.category_header = ttk.Label(self.left_panel, text="分类", font=("TkDefaultFont", 12, "bold"))
        # 将标题放置在左侧面板顶部，左对齐
        self.category_header.pack(pady=(0, 10), anchor=tk.W)
        
        # 分类列表
        # 创建一个Frame作为分类列表的容器
        self.category_frame = ttk.Frame(self.left_panel)
        # 将分类列表容器放置在左侧面板中，填充剩余空间
        self.category_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建一个Treeview作为分类列表
        # columns=("id",)定义了一个隐藏的ID列
        # show="tree"表示只显示树状结构，不显示列标题
        self.category_list = ttk.Treeview(self.category_frame, columns=("id",), show="tree")
        # 将分类列表放置在容器中，填充剩余空间，靠左对齐
        self.category_list.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        # 为分类列表添加滚动条
        # 创建一个垂直滚动条，绑定到分类列表的yview方法
        self.category_scrollbar = ttk.Scrollbar(self.category_frame, orient=tk.VERTICAL, command=self.category_list.yview)
        # 将滚动条放置在容器右侧，填充垂直方向
        self.category_scrollbar.pack(fill=tk.Y, side=tk.RIGHT)
        # 配置分类列表，使其与滚动条同步
        self.category_list.configure(yscrollcommand=self.category_scrollbar.set)
        
        # 分类按钮
        # 创建一个Frame作为分类按钮的容器
        self.category_buttons_frame = ttk.Frame(self.left_panel)
        # 将按钮容器放置在左侧面板底部，填充水平方向
        self.category_buttons_frame.pack(fill=tk.X, pady=5)
        
        # 创建添加分类按钮，点击时调用add_category方法
        self.add_category_button = ttk.Button(self.category_buttons_frame, text="添加", command=self.add_category)
        # 将按钮放置在容器左侧
        self.add_category_button.pack(side=tk.LEFT, padx=2)
        
        # 创建编辑分类按钮，点击时调用edit_category方法
        self.edit_category_button = ttk.Button(self.category_buttons_frame, text="编辑", command=self.edit_category)
        # 将按钮放置在容器左侧
        self.edit_category_button.pack(side=tk.LEFT, padx=2)
        
        # 创建删除分类按钮，点击时调用delete_category方法
        self.delete_category_button = ttk.Button(self.category_buttons_frame, text="删除", command=self.delete_category)
        # 将按钮放置在容器左侧
        self.delete_category_button.pack(side=tk.LEFT, padx=2)
        
        # 创建右侧面板（任务）
        # 创建一个Frame作为右侧面板，设置初始宽度
        self.right_panel = ttk.Frame(self.paned_window, width=600)
        # 将右侧面板添加到PanedWindow，权重为3(比左侧面板大)
        self.paned_window.add(self.right_panel, weight=3)
        
        # 任务标题
        # 创建一个Label作为任务列表的标题
        self.task_header = ttk.Label(self.right_panel, text="任务", font=("TkDefaultFont", 12, "bold"))
        # 将标题放置在右侧面板顶部，左对齐
        self.task_header.pack(pady=(0, 10), anchor=tk.W)
        
        # 任务列表
        # 创建一个Frame作为任务列表的容器
        self.task_frame = ttk.Frame(self.right_panel)
        # 将任务列表容器放置在右侧面板中，填充剩余空间
        self.task_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建一个Treeview作为任务列表
        # columns定义了列名
        # show="headings"表示只显示列标题和数据，不显示树状结构
        self.task_list = ttk.Treeview(
            self.task_frame, 
            columns=("id", "title", "priority", "completed"),
            show="headings"
        )
        # 将任务列表放置在容器中，填充剩余空间，靠左对齐
        self.task_list.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        # 配置列
        # 设置各列的标题文本
        self.task_list.heading("id", text="ID")
        self.task_list.heading("title", text="任务名称")
        self.task_list.heading("priority", text="优先级")
        self.task_list.heading("completed", text="状态")
        
        # 隐藏ID列并调整其他列宽度
        # width=0使ID列不可见
        # stretch=tk.NO表示列宽不会随窗口大小变化
        self.task_list.column("id", width=0, stretch=tk.NO)
        # 设置任务名称列宽度为250像素，并允许拉伸
        self.task_list.column("title", width=250, stretch=tk.YES)
        # 设置优先级列宽度为60像素，不允许拉伸
        self.task_list.column("priority", width=60, stretch=tk.NO)
        # 设置状态列宽度为60像素，不允许拉伸
        self.task_list.column("completed", width=60, stretch=tk.NO)
        
        # 为任务列表添加滚动条
        # 创建一个垂直滚动条，绑定到任务列表的yview方法
        self.task_scrollbar = ttk.Scrollbar(self.task_frame, orient=tk.VERTICAL, command=self.task_list.yview)
        # 将滚动条放置在容器右侧，填充垂直方向
        self.task_scrollbar.pack(fill=tk.Y, side=tk.RIGHT)
        # 配置任务列表，使其与滚动条同步
        self.task_list.configure(yscrollcommand=self.task_scrollbar.set)
        
        # 任务按钮
        # 创建一个Frame作为任务按钮的容器
        self.task_buttons_frame = ttk.Frame(self.right_panel)
        # 将任务按钮容器放置在右侧面板底部，填充水平方向
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
        # 创建一个Label作为状态栏，显示应用程序状态信息
        # relief=tk.SUNKEN使其看起来像是嵌入窗口
        # anchor=tk.W使文本左对齐
        self.status_bar = ttk.Label(self.root, text="就绪", relief=tk.SUNKEN, anchor=tk.W)
        # 将状态栏放置在窗口底部，填充水平方向
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # 设置键盘快捷键
        # 绑定Ctrl+N快捷键到添加任务功能
        self.root.bind("<Control-n>", lambda event: self.add_task())
        # 绑定Ctrl+E快捷键到编辑任务功能
        self.root.bind("<Control-e>", lambda event: self.edit_task())
        # 绑定Ctrl+D快捷键到删除任务功能
        self.root.bind("<Control-d>", lambda event: self.delete_task())
        # 绑定Ctrl+Space快捷键到切换任务完成状态功能
        self.root.bind("<Control-space>", lambda event: self.toggle_task_completion())
        # 绑定Ctrl+Q快捷键到退出应用程序功能
        self.root.bind("<Control-q>", lambda event: self.root.destroy())
        
        # 设置分类选择事件
        # 当用户在分类列表中选择一项时，调用category_selected方法
        self.category_list.bind("<<TreeviewSelect>>", self.category_selected)
        
        # 设置窗口关闭事件
        # 当用户关闭窗口时，调用on_closing方法
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # 初始化数据
        # 当前选中的分类ID，初始为None
        self.current_category = None
        # 加载分类列表
        self.load_categories()
        
        # 加载上次选择的分类
        # 从配置文件中恢复上次选择的分类
        self.restore_last_category()
    
    def show_status(self, message, timeout=3000):
        """
        在状态栏显示消息并在超时后清除
        
        参数:
            message: 要显示的消息文本
            timeout: 消息显示的时间(毫秒)，默认为3000毫秒
        
        作用:
            在状态栏显示指定的消息，然后在指定的时间后恢复为"就绪"状态
        """
        # 更新状态栏文本
        self.status_bar.config(text=message)
        # 设置定时器，在timeout毫秒后将状态栏文本恢复为"就绪"
        self.root.after(timeout, lambda: self.status_bar.config(text="就绪"))
    
    def load_categories(self):
        """
        从数据库加载分类
        
        作用:
            清空当前分类列表，然后从数据库加载所有分类并显示在界面上
        """
        # 清除现有项目
        # 获取所有分类项的ID
        for item in self.category_list.get_children():
            # 删除每一项
            self.category_list.delete(item)
        
        # 从数据库获取分类
        # 获取数据库会话
        db = get_db()
        # 查询所有分类
        categories = db.query(Category).all()
        
        # 将分类添加到列表
        for category in categories:
            # 插入一个新项，text显示分类名称，values存储分类ID
            self.category_list.insert("", tk.END, text=category.name, values=(category.id,))
    
    def load_tasks(self):
        """
        加载选定分类的任务
        
        作用:
            清空当前任务列表，然后从数据库加载选定分类的所有任务并显示在界面上
        """
        # 如果没有选择分类，则不加载任务
        if not self.current_category:
            return
            
        # 清除现有项目
        # 获取所有任务项的ID
        for item in self.task_list.get_children():
            # 删除每一项
            self.task_list.delete(item)
        
        # 从数据库获取任务
        # 获取数据库会话
        db = get_db()
        # 查询属于当前选定分类的所有任务
        tasks = db.query(Task).filter(Task.category_id == self.current_category).all()
        
        # 将任务添加到列表
        for task in tasks:
            # 格式化状态
            # 如果任务已完成，显示"已完成"，否则显示"进行中"
            status = "已完成" if task.completed else "进行中"
            
            # 格式化优先级
            # 将英文优先级转换为中文显示
            priority_text = "低" if task.priority == "low" else "中" if task.priority == "medium" else "高"
            
            # 添加到列表
            # 插入一个新项，values包含任务ID、标题、优先级和状态
            item_id = self.task_list.insert(
                "", 
                tk.END, 
                values=(task.id, task.title, priority_text, status)
            )
            
            # 为所有任务设置相同的黑色字体样式
            # 使用"task_item"标签来应用样式
            self.task_list.item(item_id, tags=("task_item",))
        
        # 配置样式标签 - 所有文字都设置为黑色黑体字
        # 定义"task_item"标签的样式：黑色粗体字
        self.task_list.tag_configure("task_item", font=("TkDefaultFont", 9, "bold"), foreground="black")
    
    def category_selected(self, event):
        """
        处理分类选择
        
        参数:
            event: Tkinter事件对象，包含有关选择事件的信息
            
        作用:
            当用户选择一个分类时，更新当前选择的分类ID，
            更新任务列表标题，并加载该分类下的所有任务
        """
        # 获取当前选中的项
        selected_items = self.category_list.selection()
        # 如果没有选中项，则直接返回
        if not selected_items:
            return
            
        # 获取选中项的第一个（通常只有一个）
        item = selected_items[0]
        # 从选中项的values中获取分类ID
        category_id = self.category_list.item(item, "values")[0]
        # 从选中项的text中获取分类名称
        category_name = self.category_list.item(item, "text")
        
        # 更新当前选中的分类ID
        self.current_category = category_id
        # 更新任务列表标题，显示当前分类名称
        self.task_header.config(text=f"任务 - {category_name}")
        # 加载该分类下的所有任务
        self.load_tasks()
        
        # 保存当前选择的分类ID
        self.save_last_category()
    
    def save_last_category(self):
        """
        保存最后选择的分类ID
        
        作用:
            将当前选中的分类ID保存到配置文件中，
            以便下次启动应用程序时可以恢复选择
        """
        # 如果有选中的分类
        if self.current_category:
            # 加载当前配置
            config = load_config()
            # 更新配置中的last_category_id
            config['last_category_id'] = self.current_category
            # 保存配置到文件
            save_config(config)
    
    def restore_last_category(self):
        """
        恢复上次选择的分类
        
        作用:
            从配置文件中读取上次选择的分类ID，
            如果存在，则自动选择该分类
        """
        # 加载配置
        config = load_config()
        # 获取上次选择的分类ID
        last_category_id = config.get('last_category_id')
        
        # 如果存在上次选择的分类ID
        if last_category_id:
            # 查找对应的分类项
            for item in self.category_list.get_children():
                # 获取当前项的分类ID
                category_id = self.category_list.item(item, "values")[0]
                # 比较ID（转换为字符串以确保类型一致）
                if str(category_id) == str(last_category_id):
                    # 选择该项
                    self.category_list.selection_set(item)
                    # 设置焦点到该项
                    self.category_list.focus(item)
                    # 确保该项可见
                    self.category_list.see(item)
                    
                    # 手动触发选择事件
                    # 更新当前选中的分类ID
                    self.current_category = last_category_id
                    # 获取分类名称
                    category_name = self.category_list.item(item, "text")
                    # 更新任务列表标题
                    self.task_header.config(text=f"任务 - {category_name}")
                    # 加载该分类下的所有任务
                    self.load_tasks()
                    break
    
    def on_closing(self):
        """
        窗口关闭时的处理
        
        作用:
            当用户关闭应用程序窗口时，保存当前选择的分类，
            然后销毁窗口
        """
        # 保存当前选择的分类
        self.save_last_category()
        # 关闭窗口
        self.root.destroy()
    
    def add_category(self):
        """
        添加新分类
        
        作用:
            打开分类对话框，让用户输入新分类的信息，
            然后将新分类添加到数据库并更新界面
        """
        # 创建分类对话框
        dialog = CategoryDialog(self.root)
        # 如果用户点击了保存按钮（对话框返回结果）
        if dialog.result:
            # 解包对话框返回的结果
            name, icon, color = dialog.result
            
            # 获取数据库会话
            db = get_db()
            # 创建新的分类对象
            new_category = Category(name=name, icon=icon, color=color)
            # 将新分类添加到数据库
            db.add(new_category)
            # 提交事务
            db.commit()
            
            # 重新加载分类列表
            self.load_categories()
            # 在状态栏显示成功消息
            self.show_status(f"分类 '{name}' 已添加")
    
    def edit_category(self):
        """
        编辑选定的分类
        
        作用:
            获取当前选中的分类，打开分类对话框让用户编辑信息，
            然后更新数据库中的分类并刷新界面
        """
        # 获取当前选中的项
        selected_items = self.category_list.selection()
        # 如果没有选中项，显示错误消息并返回
        if not selected_items:
            self.show_status("未选择分类")
            return
            
        # 获取选中项的第一个
        item = selected_items[0]
        # 从选中项的values中获取分类ID
        category_id = self.category_list.item(item, "values")[0]
        
        # 获取数据库会话
        db = get_db()
        # 查询选中的分类
        category = db.query(Category).filter(Category.id == category_id).first()
        
        # 创建分类对话框，传入当前分类对象
        dialog = CategoryDialog(self.root, category)
        # 如果用户点击了保存按钮
        if dialog.result:
            # 解包对话框返回的结果
            name, icon, color = dialog.result
            
            # 更新分类信息
            category.name = name
            category.icon = icon
            category.color = color
            # 提交事务
            db.commit()
            
            # 重新加载分类列表
            self.load_categories()
            # 在状态栏显示成功消息
            self.show_status(f"分类 '{name}' 已更新")
    
    def delete_category(self):
        """
        删除选定的分类
        
        作用:
            获取当前选中的分类，询问用户是否确认删除，
            如果确认，则从数据库中删除该分类及其所有任务，并更新界面
        """
        # 获取当前选中的项
        selected_items = self.category_list.selection()
        # 如果没有选中项，显示错误消息并返回
        if not selected_items:
            self.show_status("未选择分类")
            return
            
        # 获取选中项的第一个
        item = selected_items[0]
        # 从选中项的values中获取分类ID
        category_id = self.category_list.item(item, "values")[0]
        # 从选中项的text中获取分类名称
        category_name = self.category_list.item(item, "text")
        
        # 确认删除
        # 显示确认对话框，询问用户是否确认删除
        if not messagebox.askyesno("确认删除", f"删除分类 '{category_name}' 及其所有任务?"):
            return
        
        # 获取数据库会话
        db = get_db()
        # 删除选中的分类（级联删除会自动删除属于该分类的所有任务）
        db.query(Category).filter(Category.id == category_id).delete()
        # 提交事务
        db.commit()
        
        # 重新加载分类列表
        self.load_categories()
        # 清除当前选中的分类
        self.current_category = None
        
        # 清除任务列表
        for item in self.task_list.get_children():
            self.task_list.delete(item)
            
        # 重置任务列表标题
        self.task_header.config(text="任务")
        # 在状态栏显示成功消息
        self.show_status(f"分类 '{category_name}' 已删除")
    
    def add_task(self):
        """
        添加新任务
        
        作用:
            检查是否选择了分类，然后打开任务对话框让用户输入新任务的信息，
            将新任务添加到数据库并更新界面
        """
        # 如果没有选择分类，显示错误消息并返回
        if not self.current_category:
            self.show_status("请先选择一个分类")
            return
            
        # 创建任务对话框
        dialog = TaskDialog(self.root)
        # 如果用户点击了保存按钮
        if dialog.result:
            # 解包对话框返回的结果，忽略截止日期（使用None）
            title, description, priority, _ = dialog.result  # 忽略截止日期
            
            # 获取数据库会话
            db = get_db()
            # 创建新的任务对象
            new_task = Task(
                title=title,
                description=description,
                priority=priority,
                category_id=self.current_category
            )
            # 将新任务添加到数据库
            db.add(new_task)
            # 提交事务
            db.commit()
            
            # 重新加载任务列表
            self.load_tasks()
            # 在状态栏显示成功消息
            self.show_status(f"任务 '{title}' 已添加")
    
    def edit_task(self):
        """
        编辑选定的任务
        
        作用:
            获取当前选中的任务，打开任务对话框让用户编辑信息，
            然后更新数据库中的任务并刷新界面
        """
        # 获取当前选中的项
        selected_items = self.task_list.selection()
        # 如果没有选中项，显示错误消息并返回
        if not selected_items:
            self.show_status("未选择任务")
            return
            
        # 获取选中项的第一个
        item = selected_items[0]
        # 从选中项的values中获取任务ID
        task_id = self.task_list.item(item, "values")[0]
        
        # 获取数据库会话
        db = get_db()
        # 查询选中的任务
        task = db.query(Task).filter(Task.id == task_id).first()
        
        # 创建任务对话框，传入当前任务对象
        dialog = TaskDialog(self.root, task)
        # 如果用户点击了保存按钮
        if dialog.result:
            # 解包对话框返回的结果，忽略截止日期
            title, description, priority, _ = dialog.result  # 忽略截止日期
            
            # 更新任务信息
            task.title = title
            task.description = description
            task.priority = priority
            # 提交事务
            db.commit()
            
            # 重新加载任务列表
            self.load_tasks()
            # 在状态栏显示成功消息
            self.show_status(f"任务 '{title}' 已更新")
    
    def toggle_task_completion(self):
        """
        切换选定任务的完成状态
        
        作用:
            获取当前选中的任务，切换其完成状态（完成/未完成），
            然后更新数据库并刷新界面
        """
        # 获取当前选中的项
        selected_items = self.task_list.selection()
        # 如果没有选中项，显示错误消息并返回
        if not selected_items:
            self.show_status("未选择任务")
            return
            
        # 获取选中项的第一个
        item = selected_items[0]
        # 从选中项的values中获取任务ID
        task_id = self.task_list.item(item, "values")[0]
        
        # 获取数据库会话
        db = get_db()
        # 查询选中的任务
        task = db.query(Task).filter(Task.id == task_id).first()
        # 切换完成状态
        task.completed = not task.completed
        # 提交事务
        db.commit()
        
        # 重新加载任务列表
        self.load_tasks()
        # 根据新的完成状态设置状态消息
        status = "已完成" if task.completed else "标记为未完成"
        # 在状态栏显示成功消息
        self.show_status(f"任务 '{task.title}' {status}")
    
    def delete_task(self):
        """
        删除选定的任务
        
        作用:
            获取当前选中的任务，询问用户是否确认删除，
            如果确认，则从数据库中删除该任务并更新界面
        """
        # 获取当前选中的项
        selected_items = self.task_list.selection()
        # 如果没有选中项，显示错误消息并返回
        if not selected_items:
            self.show_status("未选择任务")
            return
            
        # 获取选中项的第一个
        item = selected_items[0]
        # 从选中项的values中获取任务ID
        task_id = self.task_list.item(item, "values")[0]
        
        # 获取数据库会话
        db = get_db()
        # 查询选中的任务
        task = db.query(Task).filter(Task.id == task_id).first()
        # 保存任务标题，用于显示消息
        task_title = task.title
        
        # 确认删除
        # 显示确认对话框，询问用户是否确认删除
        if not messagebox.askyesno("确认删除", f"删除任务 '{task_title}'?"):
            return
        
        # 删除任务
        db.delete(task)
        # 提交事务
        db.commit()
        
        # 重新加载任务列表
        self.load_tasks()
        # 在状态栏显示成功消息
        self.show_status(f"任务 '{task_title}' 已删除") 
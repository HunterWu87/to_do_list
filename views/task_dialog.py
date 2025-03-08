import tkinter as tk  # 导入tkinter库，Python的标准GUI库
from tkinter import ttk, messagebox  # 导入ttk模块(提供主题化的小部件)和messagebox模块(用于显示消息对话框)
import datetime  # 导入datetime模块，用于处理日期和时间

from models import PriorityEnum  # 从models模块导入优先级枚举类

class TaskDialog:
    """
    任务对话框类
    
    用于添加新任务或编辑现有任务的对话框
    """
    def __init__(self, parent, task=None):
        """
        初始化任务对话框
        
        参数:
            parent: 父窗口
            task: 要编辑的任务对象，如果为None则表示添加新任务
        """
        self.parent = parent  # 保存父窗口引用
        self.task = task  # 保存任务对象引用
        self.result = None  # 初始化结果为None
        
        # 创建对话框窗口
        # Toplevel创建一个顶层窗口，作为对话框
        self.dialog = tk.Toplevel(parent)
        # 设置窗口标题，根据是编辑还是添加任务
        self.dialog.title("编辑任务" if task else "添加任务")
        # 设置窗口大小
        self.dialog.geometry("400x400")
        # 禁止调整窗口大小
        self.dialog.resizable(False, False)
        # 设置对话框为父窗口的子窗口
        self.dialog.transient(parent)
        # 设置对话框为模态，阻止用户与其他窗口交互
        self.dialog.grab_set()
        
        # 使对话框成为模态
        # 设置焦点到对话框
        self.dialog.focus_set()
        
        # 创建表单框架
        # 创建一个Frame作为表单容器，设置内边距为20像素
        self.form_frame = ttk.Frame(self.dialog, padding=20)
        # 将表单框架放置在对话框中，填充整个空间
        self.form_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题字段
        # 创建标题标签
        ttk.Label(self.form_frame, text="标题:").grid(row=0, column=0, sticky=tk.W, pady=5)
        # 创建标题变量，用于存储标题文本
        self.title_var = tk.StringVar()
        # 创建标题输入框，绑定到标题变量
        self.title_entry = ttk.Entry(self.form_frame, textvariable=self.title_var, width=30)
        # 将标题输入框放置在网格的第0行第1列
        self.title_entry.grid(row=0, column=1, sticky=tk.W+tk.E, pady=5)
        
        # 描述字段
        # 创建描述标签
        ttk.Label(self.form_frame, text="描述:").grid(row=1, column=0, sticky=tk.W, pady=5)
        # 创建描述文本框
        self.description_text = tk.Text(self.form_frame, width=30, height=5)
        # 将描述文本框放置在网格的第1行第1列
        self.description_text.grid(row=1, column=1, sticky=tk.W+tk.E, pady=5)
        
        # 优先级字段
        # 创建优先级标签
        ttk.Label(self.form_frame, text="优先级:").grid(row=2, column=0, sticky=tk.W, pady=5)
        # 创建优先级变量，用于存储选择的优先级
        self.priority_var = tk.StringVar()
        # 创建优先级下拉框，绑定到优先级变量
        self.priority_combo = ttk.Combobox(self.form_frame, textvariable=self.priority_var, width=15)
        # 设置下拉框的选项为低、中、高
        self.priority_combo['values'] = ["低", "中", "高"]
        # 默认选择中等优先级
        self.priority_combo.current(1)  # 默认为中等
        # 将优先级下拉框放置在网格的第2行第1列
        self.priority_combo.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # 按钮
        # 创建一个Frame作为按钮容器
        self.button_frame = ttk.Frame(self.dialog)
        # 将按钮框架放置在对话框底部，填充水平方向
        self.button_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # 创建保存按钮，点击时调用save方法
        self.save_button = ttk.Button(self.button_frame, text="保存", command=self.save)
        # 将保存按钮放置在按钮框架右侧
        self.save_button.pack(side=tk.RIGHT, padx=5)
        
        # 创建取消按钮，点击时调用cancel方法
        self.cancel_button = ttk.Button(self.button_frame, text="取消", command=self.cancel)
        # 将取消按钮放置在保存按钮左侧
        self.cancel_button.pack(side=tk.RIGHT, padx=5)
        
        # 如果是编辑模式，填充字段
        if task:
            self.populate_fields()
        
        # 等待对话框关闭
        # wait_window会阻塞直到对话框被销毁
        self.dialog.wait_window()
    
    def populate_fields(self):
        """
        用任务数据填充字段
        
        作用:
            如果是编辑现有任务，将任务的数据填充到表单字段中
        """
        # 如果没有任务对象，直接返回
        if not self.task:
            return
            
        # 设置标题字段
        self.title_var.set(self.task.title)
        
        # 如果有描述，设置描述字段
        if self.task.description:
            self.description_text.insert("1.0", self.task.description)
        
        # 设置优先级
        if self.task.priority:
            # 将英文优先级转换为中文显示
            priority_index = 0  # 默认为低
            if self.task.priority == "medium":
                priority_index = 1
            elif self.task.priority == "high":
                priority_index = 2
            self.priority_combo.current(priority_index)
    
    def save(self):
        """
        保存任务数据并关闭对话框
        
        作用:
            验证输入数据，如果有效则保存并关闭对话框
        """
        # 获取标题
        title = self.title_var.get()
        
        # 验证标题不能为空
        if not title:
            messagebox.showerror("错误", "标题是必填项")
            return
            
        # 获取描述
        description = self.description_text.get("1.0", tk.END).strip()
        
        # 将中文优先级转换为英文存储
        priority_text = self.priority_combo.get()
        if priority_text == "低":
            priority = "low"
        elif priority_text == "高":
            priority = "high"
        else:
            priority = "medium"
        
        # 设置结果元组，包含标题、描述、优先级和None(截止日期)
        self.result = (title, description, priority, None)
        # 销毁对话框
        self.dialog.destroy()
    
    def cancel(self):
        """
        取消并关闭对话框
        
        作用:
            不保存任何数据，直接关闭对话框
        """
        # 销毁对话框
        self.dialog.destroy() 
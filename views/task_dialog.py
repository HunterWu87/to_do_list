import tkinter as tk
from tkinter import ttk, messagebox
import datetime

from models import PriorityEnum

class TaskDialog:
    def __init__(self, parent, task=None):
        self.parent = parent
        self.task = task
        self.result = None
        
        # 创建对话框窗口
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("编辑任务" if task else "添加任务")
        self.dialog.geometry("400x350")  # 减小高度
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # 使对话框成为模态
        self.dialog.focus_set()
        
        # 创建表单框架
        self.form_frame = ttk.Frame(self.dialog, padding=20)
        self.form_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题字段
        ttk.Label(self.form_frame, text="标题:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.title_var = tk.StringVar()
        self.title_entry = ttk.Entry(self.form_frame, textvariable=self.title_var, width=30)
        self.title_entry.grid(row=0, column=1, sticky=tk.W+tk.E, pady=5)
        
        # 描述字段
        ttk.Label(self.form_frame, text="描述:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.description_text = tk.Text(self.form_frame, width=30, height=5)
        self.description_text.grid(row=1, column=1, sticky=tk.W+tk.E, pady=5)
        
        # 优先级字段
        ttk.Label(self.form_frame, text="优先级:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.priority_var = tk.StringVar()
        self.priority_combo = ttk.Combobox(self.form_frame, textvariable=self.priority_var, width=15)
        self.priority_combo['values'] = ["低", "中", "高"]
        self.priority_combo.current(1)  # 默认为中等
        self.priority_combo.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # 按钮
        self.button_frame = ttk.Frame(self.dialog)
        self.button_frame.pack(fill=tk.X, padx=20, pady=20)
        
        self.save_button = ttk.Button(self.button_frame, text="保存", command=self.save)
        self.save_button.pack(side=tk.RIGHT, padx=5)
        
        self.cancel_button = ttk.Button(self.button_frame, text="取消", command=self.cancel)
        self.cancel_button.pack(side=tk.RIGHT, padx=5)
        
        # 如果是编辑模式，填充字段
        if task:
            self.populate_fields()
        
        # 等待对话框关闭
        self.dialog.wait_window()
    
    def populate_fields(self):
        """用任务数据填充字段"""
        if not self.task:
            return
            
        self.title_var.set(self.task.title)
        
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
        """保存任务数据并关闭对话框"""
        title = self.title_var.get()
        
        if not title:
            messagebox.showerror("错误", "标题是必填项")
            return
            
        description = self.description_text.get("1.0", tk.END).strip()
        
        # 将中文优先级转换为英文存储
        priority_text = self.priority_combo.get()
        if priority_text == "低":
            priority = "low"
        elif priority_text == "高":
            priority = "high"
        else:
            priority = "medium"
        
        # 不再需要截止日期
        self.result = (title, description, priority, None)
        self.dialog.destroy()
    
    def cancel(self):
        """取消并关闭对话框"""
        self.dialog.destroy() 
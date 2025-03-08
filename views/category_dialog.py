import tkinter as tk
from tkinter import ttk, colorchooser, messagebox

class CategoryDialog:
    def __init__(self, parent, category=None):
        self.parent = parent
        self.category = category
        self.result = None
        self.color = "#3498db"  # 默认颜色
        
        # 创建对话框窗口
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("编辑分类" if category else "添加分类")
        self.dialog.geometry("400x250")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # 使对话框成为模态
        self.dialog.focus_set()
        
        # 创建表单框架
        self.form_frame = ttk.Frame(self.dialog, padding=20)
        self.form_frame.pack(fill=tk.BOTH, expand=True)
        
        # 名称字段
        ttk.Label(self.form_frame, text="名称:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.name_var = tk.StringVar()
        self.name_entry = ttk.Entry(self.form_frame, textvariable=self.name_var, width=30)
        self.name_entry.grid(row=0, column=1, sticky=tk.W+tk.E, pady=5)
        
        # 图标字段
        ttk.Label(self.form_frame, text="图标:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.icon_var = tk.StringVar()
        self.icon_entry = ttk.Entry(self.form_frame, textvariable=self.icon_var, width=30)
        self.icon_entry.grid(row=1, column=1, sticky=tk.W+tk.E, pady=5)
        
        # 颜色字段
        ttk.Label(self.form_frame, text="颜色:").grid(row=2, column=0, sticky=tk.W, pady=5)
        
        self.color_frame = ttk.Frame(self.form_frame)
        self.color_frame.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        self.color_preview = tk.Canvas(self.color_frame, width=24, height=24, bg=self.color, highlightthickness=1, highlightbackground="#cccccc")
        self.color_preview.pack(side=tk.LEFT, padx=(0, 10))
        
        self.color_button = ttk.Button(self.color_frame, text="选择颜色", command=self.choose_color)
        self.color_button.pack(side=tk.LEFT)
        
        # 按钮
        self.button_frame = ttk.Frame(self.dialog)
        self.button_frame.pack(fill=tk.X, padx=20, pady=20)
        
        self.save_button = ttk.Button(self.button_frame, text="保存", command=self.save)
        self.save_button.pack(side=tk.RIGHT, padx=5)
        
        self.cancel_button = ttk.Button(self.button_frame, text="取消", command=self.cancel)
        self.cancel_button.pack(side=tk.RIGHT, padx=5)
        
        # 如果是编辑模式，填充字段
        if category:
            self.populate_fields()
        
        # 等待对话框关闭
        self.dialog.wait_window()
    
    def choose_color(self):
        """打开颜色选择对话框"""
        color = colorchooser.askcolor(initialcolor=self.color, title="选择分类颜色")
        if color[1]:  # color是一个元组(RGB, hex)
            self.color = color[1]
            self.color_preview.config(bg=self.color)
    
    def populate_fields(self):
        """用分类数据填充字段"""
        if not self.category:
            return
            
        self.name_var.set(self.category.name)
        
        if self.category.icon:
            self.icon_var.set(self.category.icon)
        
        if self.category.color:
            self.color = self.category.color
            self.color_preview.config(bg=self.color)
    
    def save(self):
        """保存分类数据并关闭对话框"""
        name = self.name_var.get()
        
        if not name:
            messagebox.showerror("错误", "名称是必填项")
            return
            
        icon = self.icon_var.get()
        
        self.result = (name, icon, self.color)
        self.dialog.destroy()
    
    def cancel(self):
        """取消并关闭对话框"""
        self.dialog.destroy() 
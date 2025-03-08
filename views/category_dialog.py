import tkinter as tk  # 导入tkinter库，Python的标准GUI库
from tkinter import ttk, colorchooser, messagebox  # 导入ttk模块、颜色选择器和消息对话框

class CategoryDialog:
    """
    分类对话框类
    
    用于添加新分类或编辑现有分类的对话框
    """
    def __init__(self, parent, category=None):
        """
        初始化分类对话框
        
        参数:
            parent: 父窗口
            category: 要编辑的分类对象，如果为None则表示添加新分类
        """
        self.parent = parent  # 保存父窗口引用
        self.category = category  # 保存分类对象引用
        self.result = None  # 初始化结果为None
        self.color = "#3498db"  # 默认颜色（蓝色）
        
        # 创建对话框窗口
        # Toplevel创建一个顶层窗口，作为对话框
        self.dialog = tk.Toplevel(parent)
        # 设置窗口标题，根据是编辑还是添加分类
        self.dialog.title("编辑分类" if category else "添加分类")
        # 设置窗口大小
        self.dialog.geometry("400x250")
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
        
        # 名称字段
        # 创建名称标签
        ttk.Label(self.form_frame, text="名称:").grid(row=0, column=0, sticky=tk.W, pady=5)
        # 创建名称变量，用于存储名称文本
        self.name_var = tk.StringVar()
        # 创建名称输入框，绑定到名称变量
        self.name_entry = ttk.Entry(self.form_frame, textvariable=self.name_var, width=30)
        # 将名称输入框放置在网格的第0行第1列
        self.name_entry.grid(row=0, column=1, sticky=tk.W+tk.E, pady=5)
        
        # 图标字段
        # 创建图标标签
        ttk.Label(self.form_frame, text="图标:").grid(row=1, column=0, sticky=tk.W, pady=5)
        # 创建图标变量，用于存储图标文本
        self.icon_var = tk.StringVar()
        # 创建图标输入框，绑定到图标变量
        self.icon_entry = ttk.Entry(self.form_frame, textvariable=self.icon_var, width=30)
        # 将图标输入框放置在网格的第1行第1列
        self.icon_entry.grid(row=1, column=1, sticky=tk.W+tk.E, pady=5)
        
        # 颜色字段
        # 创建颜色标签
        ttk.Label(self.form_frame, text="颜色:").grid(row=2, column=0, sticky=tk.W, pady=5)
        
        # 创建一个Frame作为颜色选择器的容器
        self.color_frame = ttk.Frame(self.form_frame)
        # 将颜色框架放置在网格的第2行第1列
        self.color_frame.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # 创建一个Canvas作为颜色预览
        self.color_preview = tk.Canvas(self.color_frame, width=24, height=24, bg=self.color, highlightthickness=1, highlightbackground="#cccccc")
        # 将颜色预览放置在颜色框架左侧
        self.color_preview.pack(side=tk.LEFT, padx=(0, 10))
        
        # 创建选择颜色按钮，点击时调用choose_color方法
        self.color_button = ttk.Button(self.color_frame, text="选择颜色", command=self.choose_color)
        # 将选择颜色按钮放置在颜色预览右侧
        self.color_button.pack(side=tk.LEFT)
        
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
        if category:
            self.populate_fields()
        
        # 等待对话框关闭
        # wait_window会阻塞直到对话框被销毁
        self.dialog.wait_window()
    
    def choose_color(self):
        """
        打开颜色选择对话框
        
        作用:
            打开系统颜色选择器，让用户选择一个颜色，
            然后更新颜色预览
        """
        # 打开颜色选择对话框，传入当前颜色作为初始值
        color = colorchooser.askcolor(initialcolor=self.color, title="选择分类颜色")
        # 如果用户选择了颜色（没有点击取消）
        if color[1]:  # color是一个元组(RGB, hex)
            # 更新当前颜色为用户选择的颜色
            self.color = color[1]
            # 更新颜色预览的背景色
            self.color_preview.config(bg=self.color)
    
    def populate_fields(self):
        """
        用分类数据填充字段
        
        作用:
            如果是编辑现有分类，将分类的数据填充到表单字段中
        """
        # 如果没有分类对象，直接返回
        if not self.category:
            return
            
        # 设置名称字段
        self.name_var.set(self.category.name)
        
        # 如果有图标，设置图标字段
        if self.category.icon:
            self.icon_var.set(self.category.icon)
        
        # 如果有颜色，更新颜色预览
        if self.category.color:
            self.color = self.category.color
            self.color_preview.config(bg=self.color)
    
    def save(self):
        """
        保存分类数据并关闭对话框
        
        作用:
            验证输入数据，如果有效则保存并关闭对话框
        """
        # 获取名称
        name = self.name_var.get()
        
        # 验证名称不能为空
        if not name:
            messagebox.showerror("错误", "名称是必填项")
            return
            
        # 获取图标
        icon = self.icon_var.get()
        
        # 设置结果元组，包含名称、图标和颜色
        self.result = (name, icon, self.color)
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
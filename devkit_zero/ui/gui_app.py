"""
GUI 应用程序 (使用 tkinter)
DevKit-Zero 的图形界面
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import sys
import os

# 处理相对导入和直接运行的兼容性
try:
    # 尝试相对导入(作为模块运行时)
    from ..tools import formatter, random_gen, diff_tool, converter, linter, unused_func_detector
except ImportError:
    # 如果相对导入失败,添加父目录到路径(直接运行时)
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
    from devkit_zero.tools import formatter, random_gen, diff_tool, converter, linter, unused_func_detector


class DevKitZeroGUI:
    """DevKit-Zero GUI 主类"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("DevKit-Zero - 零依赖开发者工具箱")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # 设置图标 (如果存在)
        try:
            icon_path = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'app.ico')
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except:
            pass
        
        self.setup_ui()
    
    def setup_ui(self):
        """设置用户界面"""
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # 工具选择区域
        tool_frame = ttk.LabelFrame(main_frame, text="工具选择", padding="10")
        tool_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.tool_var = tk.StringVar(value="formatter")
        tools = [
            ("代码格式化", "formatter"),
            ("随机数据生成", "random_gen"),
            ("文本差异对比", "diff_tool"),
            ("数据格式转换", "converter"),
            ("代码静态检查", "linter"),
            ("未使用函数检测", "unused_func")
        ]
        
        for i, (name, value) in enumerate(tools):
            ttk.Radiobutton(tool_frame, text=name, variable=self.tool_var, 
                           value=value, command=self.on_tool_change).grid(row=0, column=i, padx=5)
        
        # 左侧控制面板
        control_frame = ttk.LabelFrame(main_frame, text="控制面板", padding="10")
        control_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        control_frame.columnconfigure(0, weight=1)
        
        # 右侧结果面板
        result_frame = ttk.LabelFrame(main_frame, text="结果输出", padding="10")
        result_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)
        
        # 结果文本框
        self.result_text = scrolledtext.ScrolledText(result_frame, wrap=tk.WORD, height=20)
        self.result_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 控制面板容器
        self.control_container = control_frame
        
        # 初始化工具面板
        self.on_tool_change()
    
    def on_tool_change(self):
        """工具选择改变时的处理"""
        # 清除现有控件
        for widget in self.control_container.winfo_children():
            widget.destroy()
        
        tool = self.tool_var.get()
        
        if tool == "formatter":
            self.setup_formatter_ui()
        elif tool == "random_gen":
            self.setup_random_gen_ui()
        elif tool == "diff_tool":
            self.setup_diff_tool_ui()
        elif tool == "converter":
            self.setup_converter_ui()
        elif tool == "linter":
            self.setup_linter_ui()
        elif tool == "unused_func":
            self.setup_unused_func_ui()
    
    def setup_formatter_ui(self):
        """设置代码格式化工具界面"""
        # 语言选择
        ttk.Label(self.control_container, text="编程语言:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.format_lang_var = tk.StringVar(value="python")
        lang_combo = ttk.Combobox(self.control_container, textvariable=self.format_lang_var,
                                 values=["python", "javascript"], state="readonly")
        lang_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2)
        
        # 输入方式选择
        ttk.Label(self.control_container, text="输入方式:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.format_input_type = tk.StringVar(value="text")
        ttk.Radiobutton(self.control_container, text="直接输入", variable=self.format_input_type,
                       value="text").grid(row=1, column=1, sticky=tk.W, pady=2)
        ttk.Radiobutton(self.control_container, text="选择文件", variable=self.format_input_type,
                       value="file").grid(row=2, column=1, sticky=tk.W, pady=2)
        
        # 文件选择
        file_frame = ttk.Frame(self.control_container)
        file_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=2)
        file_frame.columnconfigure(0, weight=1)
        
        self.format_file_var = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.format_file_var).grid(row=0, column=0, sticky=(tk.W, tk.E))
        ttk.Button(file_frame, text="选择", command=self.select_format_file).grid(row=0, column=1, padx=(5, 0))
        
        # 代码输入框
        ttk.Label(self.control_container, text="代码输入:").grid(row=4, column=0, sticky=tk.W, pady=(10, 2))
        self.format_code_text = tk.Text(self.control_container, height=10, wrap=tk.WORD)
        self.format_code_text.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=2)
        
        # 执行按钮
        ttk.Button(self.control_container, text="格式化代码", 
                  command=self.run_formatter).grid(row=6, column=0, columnspan=2, pady=(10, 0))
        
        self.control_container.columnconfigure(1, weight=1)
    
    def setup_random_gen_ui(self):
        """设置随机数据生成工具界面"""
        # 生成类型
        ttk.Label(self.control_container, text="生成类型:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.random_type_var = tk.StringVar(value="uuid")
        type_combo = ttk.Combobox(self.control_container, textvariable=self.random_type_var,
                                 values=["uuid", "string", "password", "number", "color"], state="readonly")
        type_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2)
        type_combo.bind('<<ComboboxSelected>>', self.on_random_type_change)
        
        # 动态参数框架
        self.random_params_frame = ttk.Frame(self.control_container)
        self.random_params_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        self.random_params_frame.columnconfigure(1, weight=1)
        
        # 执行按钮
        ttk.Button(self.control_container, text="生成", 
                  command=self.run_random_gen).grid(row=2, column=0, columnspan=2, pady=(10, 0))
        
        self.control_container.columnconfigure(1, weight=1)
        
        # 初始化参数界面
        self.on_random_type_change()
    
    def setup_diff_tool_ui(self):
        """设置文本差异对比工具界面"""
        # 文本1
        ttk.Label(self.control_container, text="文本1:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.diff_text1 = tk.Text(self.control_container, height=8, wrap=tk.WORD)
        self.diff_text1.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=2)
        
        # 文本2
        ttk.Label(self.control_container, text="文本2:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.diff_text2 = tk.Text(self.control_container, height=8, wrap=tk.WORD)
        self.diff_text2.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=2)
        
        # 对比格式
        ttk.Label(self.control_container, text="输出格式:").grid(row=4, column=0, sticky=tk.W, pady=2)
        self.diff_format_var = tk.StringVar(value="unified")
        format_combo = ttk.Combobox(self.control_container, textvariable=self.diff_format_var,
                                   values=["unified", "side-by-side", "stats"], state="readonly")
        format_combo.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=2)
        
        # 执行按钮
        ttk.Button(self.control_container, text="对比差异", 
                  command=self.run_diff_tool).grid(row=5, column=0, columnspan=2, pady=(10, 0))
        
        self.control_container.columnconfigure(1, weight=1)
    
    def setup_converter_ui(self):
        """设置数据格式转换工具界面"""
        # 转换格式选择
        ttk.Label(self.control_container, text="从格式:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.convert_from_var = tk.StringVar(value="json")
        from_combo = ttk.Combobox(self.control_container, textvariable=self.convert_from_var,
                                 values=["json", "csv"], state="readonly")
        from_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2)
        
        ttk.Label(self.control_container, text="到格式:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.convert_to_var = tk.StringVar(value="csv")
        to_combo = ttk.Combobox(self.control_container, textvariable=self.convert_to_var,
                               values=["json", "csv"], state="readonly")
        to_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=2)
        
        # 输入数据
        ttk.Label(self.control_container, text="输入数据:").grid(row=2, column=0, sticky=tk.W, pady=(10, 2))
        self.convert_input_text = tk.Text(self.control_container, height=12, wrap=tk.WORD)
        self.convert_input_text.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=2)
        
        # 执行按钮
        ttk.Button(self.control_container, text="转换格式", 
                  command=self.run_converter).grid(row=4, column=0, columnspan=2, pady=(10, 0))
        
        self.control_container.columnconfigure(1, weight=1)
    
    def setup_linter_ui(self):
        """设置代码静态检查工具界面"""
        # 输入方式选择
        ttk.Label(self.control_container, text="输入方式:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.lint_input_type = tk.StringVar(value="text")
        ttk.Radiobutton(self.control_container, text="直接输入", variable=self.lint_input_type,
                       value="text").grid(row=0, column=1, sticky=tk.W, pady=2)
        ttk.Radiobutton(self.control_container, text="选择文件", variable=self.lint_input_type,
                       value="file").grid(row=1, column=1, sticky=tk.W, pady=2)
        
        # 文件选择
        file_frame = ttk.Frame(self.control_container)
        file_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=2)
        file_frame.columnconfigure(0, weight=1)
        
        self.lint_file_var = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.lint_file_var).grid(row=0, column=0, sticky=(tk.W, tk.E))
        ttk.Button(file_frame, text="选择", command=self.select_lint_file).grid(row=0, column=1, padx=(5, 0))
        
        # 代码输入框
        ttk.Label(self.control_container, text="代码输入:").grid(row=3, column=0, sticky=tk.W, pady=(10, 2))
        self.lint_code_text = tk.Text(self.control_container, height=12, wrap=tk.WORD)
        self.lint_code_text.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=2)
        
        # 执行按钮
        ttk.Button(self.control_container, text="检查代码", 
                  command=self.run_linter).grid(row=5, column=0, columnspan=2, pady=(10, 0))
        
        self.control_container.columnconfigure(1, weight=1)
    
    def setup_unused_func_ui(self):
        """设置未使用函数检测工具界面"""
        # 项目路径选择
        ttk.Label(self.control_container, text="项目路径:").grid(row=0, column=0, sticky=tk.W, pady=2)
        
        path_frame = ttk.Frame(self.control_container)
        path_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=2)
        path_frame.columnconfigure(0, weight=1)
        
        self.unused_func_path_var = tk.StringVar(value=".")
        ttk.Entry(path_frame, textvariable=self.unused_func_path_var).grid(row=0, column=0, sticky=(tk.W, tk.E))
        ttk.Button(path_frame, text="选择目录", command=self.select_project_dir).grid(row=0, column=1, padx=(5, 0))
        
        # 排除目录
        ttk.Label(self.control_container, text="排除目录:").grid(row=2, column=0, sticky=tk.W, pady=(10, 2))
        ttk.Label(self.control_container, text="(逗号分隔)", font=("", 8)).grid(row=2, column=1, sticky=tk.W, pady=(10, 2))
        
        self.unused_func_exclude_var = tk.StringVar(value="venv,__pycache__,.git,build,dist")
        ttk.Entry(self.control_container, textvariable=self.unused_func_exclude_var).grid(
            row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=2)
        
        # 输出格式
        ttk.Label(self.control_container, text="输出格式:").grid(row=4, column=0, sticky=tk.W, pady=(10, 2))
        self.unused_func_format_var = tk.StringVar(value="text")
        format_frame = ttk.Frame(self.control_container)
        format_frame.grid(row=5, column=0, columnspan=2, sticky=tk.W, pady=2)
        
        ttk.Radiobutton(format_frame, text="文本", variable=self.unused_func_format_var,
                       value="text").grid(row=0, column=0, padx=(0, 10))
        ttk.Radiobutton(format_frame, text="JSON", variable=self.unused_func_format_var,
                       value="json").grid(row=0, column=1, padx=(0, 10))
        ttk.Radiobutton(format_frame, text="HTML", variable=self.unused_func_format_var,
                       value="html").grid(row=0, column=2)
        
        # 详细输出选项
        self.unused_func_verbose_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(self.control_container, text="显示详细信息", 
                       variable=self.unused_func_verbose_var).grid(row=6, column=0, columnspan=2, sticky=tk.W, pady=(10, 2))
        
        # 执行按钮
        ttk.Button(self.control_container, text="检测未使用函数", 
                  command=self.run_unused_func_detector).grid(row=7, column=0, columnspan=2, pady=(10, 0))
        
        self.control_container.columnconfigure(1, weight=1)
    
    def select_project_dir(self):
        """选择项目目录"""
        directory = filedialog.askdirectory(
            title="选择要分析的项目目录",
            initialdir="."
        )
        if directory:
            self.unused_func_path_var.set(directory)
    
    def on_random_type_change(self, event=None):
        """随机数据类型改变时更新参数界面"""
        # 清除现有参数控件
        for widget in self.random_params_frame.winfo_children():
            widget.destroy()
        
        gen_type = self.random_type_var.get()
        
        if gen_type == "string":
            ttk.Label(self.random_params_frame, text="长度:").grid(row=0, column=0, sticky=tk.W, pady=2)
            self.string_length_var = tk.StringVar(value="8")
            ttk.Entry(self.random_params_frame, textvariable=self.string_length_var, width=10).grid(row=0, column=1, sticky=tk.W, pady=2)
            
            self.string_numbers_var = tk.BooleanVar(value=True)
            self.string_uppercase_var = tk.BooleanVar(value=True)
            self.string_lowercase_var = tk.BooleanVar(value=True)
            self.string_symbols_var = tk.BooleanVar(value=False)
            
            ttk.Checkbutton(self.random_params_frame, text="包含数字", variable=self.string_numbers_var).grid(row=1, column=0, sticky=tk.W, pady=1)
            ttk.Checkbutton(self.random_params_frame, text="包含大写字母", variable=self.string_uppercase_var).grid(row=2, column=0, sticky=tk.W, pady=1)
            ttk.Checkbutton(self.random_params_frame, text="包含小写字母", variable=self.string_lowercase_var).grid(row=3, column=0, sticky=tk.W, pady=1)
            ttk.Checkbutton(self.random_params_frame, text="包含特殊符号", variable=self.string_symbols_var).grid(row=4, column=0, sticky=tk.W, pady=1)
            
        elif gen_type == "password":
            ttk.Label(self.random_params_frame, text="长度:").grid(row=0, column=0, sticky=tk.W, pady=2)
            self.password_length_var = tk.StringVar(value="16")
            ttk.Entry(self.random_params_frame, textvariable=self.password_length_var, width=10).grid(row=0, column=1, sticky=tk.W, pady=2)
            
        elif gen_type == "number":
            ttk.Label(self.random_params_frame, text="最小值:").grid(row=0, column=0, sticky=tk.W, pady=2)
            self.number_min_var = tk.StringVar(value="0")
            ttk.Entry(self.random_params_frame, textvariable=self.number_min_var, width=10).grid(row=0, column=1, sticky=tk.W, pady=2)
            
            ttk.Label(self.random_params_frame, text="最大值:").grid(row=1, column=0, sticky=tk.W, pady=2)
            self.number_max_var = tk.StringVar(value="100")
            ttk.Entry(self.random_params_frame, textvariable=self.number_max_var, width=10).grid(row=1, column=1, sticky=tk.W, pady=2)
            
            self.number_float_var = tk.BooleanVar(value=False)
            ttk.Checkbutton(self.random_params_frame, text="浮点数", variable=self.number_float_var).grid(row=2, column=0, sticky=tk.W, pady=1)
    
    def select_format_file(self):
        """选择格式化文件"""
        filename = filedialog.askopenfilename(
            title="选择要格式化的文件",
            filetypes=[("Python files", "*.py"), ("JavaScript files", "*.js"), ("All files", "*.*")]
        )
        if filename:
            self.format_file_var.set(filename)
    
    def select_lint_file(self):
        """选择检查文件"""
        filename = filedialog.askopenfilename(
            title="选择要检查的文件",
            filetypes=[("Python files", "*.py"), ("All files", "*.*")]
        )
        if filename:
            self.lint_file_var.set(filename)
    
    def display_result(self, result: str):
        """显示结果"""
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(1.0, result)
    
    def display_error(self, error: str):
        """显示错误"""
        messagebox.showerror("错误", error)
    
    def run_formatter(self):
        """运行代码格式化"""
        try:
            language = self.format_lang_var.get()
            input_type = self.format_input_type.get()
            
            if input_type == "file":
                file_path = self.format_file_var.get().strip()
                if not file_path:
                    raise ValueError("请选择要格式化的文件")
                result = formatter.format_file(file_path, language)
            else:
                code = self.format_code_text.get(1.0, tk.END).strip()
                if not code:
                    raise ValueError("请输入要格式化的代码")
                result = formatter.format_code(code, language)
            
            self.display_result(result)
            
        except Exception as e:
            self.display_error(str(e))
    
    def run_random_gen(self):
        """运行随机数据生成"""
        try:
            gen_type = self.random_type_var.get()
            
            if gen_type == "uuid":
                result = random_gen.generate_uuid()
            elif gen_type == "string":
                length = int(self.string_length_var.get())
                result = random_gen.generate_random_string(
                    length=length,
                    include_numbers=self.string_numbers_var.get(),
                    include_uppercase=self.string_uppercase_var.get(),
                    include_lowercase=self.string_lowercase_var.get(),
                    include_symbols=self.string_symbols_var.get()
                )
            elif gen_type == "password":
                length = int(self.password_length_var.get())
                result = random_gen.generate_secure_password(length)
            elif gen_type == "number":
                min_val = int(self.number_min_var.get())
                max_val = int(self.number_max_var.get())
                if self.number_float_var.get():
                    result = str(random_gen.generate_random_float(float(min_val), float(max_val)))
                else:
                    result = str(random_gen.generate_random_number(min_val, max_val))
            elif gen_type == "color":
                result = random_gen.generate_random_hex_color()
            else:
                raise ValueError(f"不支持的生成类型: {gen_type}")
            
            self.display_result(result)
            
        except Exception as e:
            self.display_error(str(e))
    
    def run_diff_tool(self):
        """运行文本差异对比"""
        try:
            text1 = self.diff_text1.get(1.0, tk.END).strip()
            text2 = self.diff_text2.get(1.0, tk.END).strip()
            
            if not text1 or not text2:
                raise ValueError("请输入两段要对比的文本")
            
            format_type = self.diff_format_var.get()
            
            if format_type == "unified":
                result = diff_tool.compare_texts(text1, text2)
                result_text = ''.join(result)
            elif format_type == "side-by-side":
                result = diff_tool.get_side_by_side_diff(text1, text2)
                result_text = '\n'.join(result)
            elif format_type == "stats":
                stats = diff_tool.analyze_changes(text1, text2)
                result_text = f"""变化统计:
文本1行数: {stats['total_lines_1']}
文本2行数: {stats['total_lines_2']}
新增行数: {stats['additions']}
删除行数: {stats['deletions']}
修改行数: {stats['modifications']}
相似度: {stats['similarity']:.2%}
总变更数: {stats['total_changes']}"""
            
            self.display_result(result_text)
            
        except Exception as e:
            self.display_error(str(e))
    
    def run_converter(self):
        """运行数据格式转换"""
        try:
            from_format = self.convert_from_var.get()
            to_format = self.convert_to_var.get()
            input_data = self.convert_input_text.get(1.0, tk.END).strip()
            
            if not input_data:
                raise ValueError("请输入要转换的数据")
            
            if from_format == "json" and to_format == "csv":
                result = converter.json_to_csv(input_data)
            elif from_format == "csv" and to_format == "json":
                result = converter.csv_to_json(input_data)
            else:
                raise ValueError(f"不支持从 {from_format} 转换到 {to_format}")
            
            self.display_result(result)
            
        except Exception as e:
            self.display_error(str(e))
    
    def run_linter(self):
        """运行代码静态检查"""
        try:
            input_type = self.lint_input_type.get()
            
            if input_type == "file":
                file_path = self.lint_file_var.get().strip()
                if not file_path:
                    raise ValueError("请选择要检查的文件")
                issues = linter.lint_file(file_path)
            else:
                code = self.lint_code_text.get(1.0, tk.END).strip()
                if not code:
                    raise ValueError("请输入要检查的代码")
                issues = linter.lint_code(code)
            
            result = linter.format_issues(issues)
            self.display_result(result)
            
        except Exception as e:
            self.display_error(str(e))
    
    def run_unused_func_detector(self):
        """运行未使用函数检测"""
        try:
            from pathlib import Path
            
            # 获取参数
            project_path = self.unused_func_path_var.get().strip()
            if not project_path:
                raise ValueError("请选择要分析的项目目录")
            
            project_path = Path(project_path).resolve()
            if not project_path.exists():
                raise ValueError(f"项目路径不存在: {project_path}")
            
            if not project_path.is_dir():
                raise ValueError(f"路径不是目录: {project_path}")
            
            # 解析排除目录
            exclude_text = self.unused_func_exclude_var.get().strip()
            exclude_dirs = [d.strip() for d in exclude_text.split(',') if d.strip()] if exclude_text else None
            
            # 显示进度信息
            self.display_result("正在分析项目，请稍候...\n")
            self.root.update()
            
            # 检测未使用的函数
            if self.unused_func_verbose_var.get():
                progress_msg = f"扫描项目: {project_path}\n"
                if exclude_dirs:
                    progress_msg += f"排除目录: {', '.join(exclude_dirs)}\n"
                progress_msg += "\n分析中...\n"
                self.display_result(progress_msg)
                self.root.update()
            
            unused_functions = unused_func_detector.detect_unused_functions(project_path, exclude_dirs)
            
            # 生成报告
            output_format = self.unused_func_format_var.get()
            if output_format == 'json':
                result = unused_func_detector.format_json_report(unused_functions)
            elif output_format == 'html':
                result = unused_func_detector.format_html_report(unused_functions)
            else:
                result = unused_func_detector.format_text_report(unused_functions)
            
            self.display_result(result)
            
        except Exception as e:
            self.display_error(str(e))
    
    def run(self):
        """运行 GUI 应用程序"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    app = DevKitZeroGUI()
    app.run()

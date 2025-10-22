"""
GUI 应用程序 (使用 tkinter)
DevKit-Zero 的图形界面
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import sys
import os

# 使用相对导入
# from ..tools import formatter, random_gen, diff_tool, converter, linter
from ..tools import formatter, random_gen, diff_tool, converter, linter, port_checker


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
            ("端口检查", "port_checker")
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
        elif tool == "port_checker":
            self.setup_port_checker_ui()
    
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
    
    def run(self):
        """运行 GUI 应用程序"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            pass
    


    def setup_port_checker_ui(self):
        """设置端口检查工具界面"""
        import tkinter as tk
        from tkinter import ttk

        # 操作类型
        ttk.Label(self.control_container, text="操作类型:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.port_action_var = tk.StringVar(value="check")
        action_combo = ttk.Combobox(
            self.control_container,
            textvariable=self.port_action_var,
            values=["check", "scan", "list"],
            state="readonly"
        )
        action_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2)
        action_combo.bind("<<ComboboxSelected>>", lambda e: self.update_port_params_ui())

        # 参数区容器
        self.port_params_frame = ttk.Frame(self.control_container)
        self.port_params_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(6, 6))
        self.port_params_frame.columnconfigure(1, weight=1)

        # 执行按钮
        self.port_run_btn = ttk.Button(self.control_container, text="执行", command=self.run_port_checker)
        self.port_run_btn.grid(row=2, column=0, columnspan=2, pady=(10, 0))

        # 初始参数区
        self.update_port_params_ui()
        self.control_container.columnconfigure(1, weight=1)

    def update_port_params_ui(self):
        """根据操作类型刷新参数表单"""
        import tkinter as tk
        from tkinter import ttk
        for w in self.port_params_frame.winfo_children():
            w.destroy()

        action = self.port_action_var.get()
        if action == "check":
            # host
            ttk.Label(self.port_params_frame, text="主机:").grid(row=0, column=0, sticky=tk.W, pady=2)
            self.port_host_var = tk.StringVar(value="localhost")
            ttk.Entry(self.port_params_frame, textvariable=self.port_host_var).grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2)

            # port
            ttk.Label(self.port_params_frame, text="端口:").grid(row=1, column=0, sticky=tk.W, pady=2)
            self.port_port_var = tk.StringVar(value="8080")
            ttk.Entry(self.port_params_frame, textvariable=self.port_port_var).grid(row=1, column=1, sticky=(tk.W, tk.E), pady=2)

            # timeout
            ttk.Label(self.port_params_frame, text="超时(秒):").grid(row=2, column=0, sticky=tk.W, pady=2)
            self.port_timeout_var = tk.StringVar(value="3")
            ttk.Entry(self.port_params_frame, textvariable=self.port_timeout_var).grid(row=2, column=1, sticky=(tk.W, tk.E), pady=2)

        elif action == "scan":
            # host
            ttk.Label(self.port_params_frame, text="主机:").grid(row=0, column=0, sticky=tk.W, pady=2)
            self.scan_host_var = tk.StringVar(value="localhost")
            ttk.Entry(self.port_params_frame, textvariable=self.scan_host_var).grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2)

            # start
            ttk.Label(self.port_params_frame, text="起始端口:").grid(row=1, column=0, sticky=tk.W, pady=2)
            self.scan_start_var = tk.StringVar(value="1")
            ttk.Entry(self.port_params_frame, textvariable=self.scan_start_var).grid(row=1, column=1, sticky=(tk.W, tk.E), pady=2)

            # end
            ttk.Label(self.port_params_frame, text="结束端口:").grid(row=2, column=0, sticky=tk.W, pady=2)
            self.scan_end_var = tk.StringVar(value="1000")
            ttk.Entry(self.port_params_frame, textvariable=self.scan_end_var).grid(row=2, column=1, sticky=(tk.W, tk.E), pady=2)

        else:  # list
            ttk.Label(self.port_params_frame, text="操作说明：显示常见端口及服务名，无需参数").grid(
                row=0, column=0, columnspan=2, sticky=tk.W, pady=2
            )

    def run_port_checker(self):
        """运行端口检查"""
        try:
            action = self.port_action_var.get()
            if action == "check":
                host = self.port_host_var.get().strip()
                port = int(self.port_port_var.get())
                timeout = int(self.port_timeout_var.get())
                result = port_checker.check_port(host, port, timeout)
                text = port_checker.format_port_result(result)

            elif action == "scan":
                host = self.scan_host_var.get().strip()
                start = int(self.scan_start_var.get())
                end = int(self.scan_end_var.get())
                if end <= start:
                    raise ValueError("结束端口必须大于起始端口")
                results = port_checker.scan_ports(host, start, end)
                text = port_checker.format_scan_results(results)

            else:  # list
                common = port_checker.get_common_ports()
                lines = ["常见端口列表:\n"]
                for p in sorted(common):
                    lines.append(f"  {p:>5}  - {common[p]}")
                text = "\n".join(lines)

            self.display_result(text)

        except Exception as e:
            self.display_error(str(e))


if __name__ == "__main__":
    app = DevKitZeroGUI()
    app.run()
"""
GUI 应用程序 (使用 tkinter)
DevKit-Zero 的图形界面
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import sys
import os
import re
from pathlib import Path

# 处理相对导入和直接运行的兼容性
try:
    # 尝试相对导入(作为模块运行时)
    from ..tools import formatter, random_gen, diff_tool, converter, linter, unused_func_detector, api_contract_diff, \
        port_checker, regex_tester
    from ..tools.Robot_checker import core_logic as robots_core_logic
except ImportError:
    # 如果相对导入失败,添加父目录到路径(直接运行时)
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
    from devkit_zero.tools import formatter, random_gen, diff_tool, converter, linter, unused_func_detector, \
        api_contract_diff, port_checker, regex_tester
    from devkit_zero.tools.Robot_checker import core_logic as robots_core_logic


# 动态导入文件工具类，处理不同的目录结构
def import_file_tools():
    """动态导入文件工具模块"""
    # 可能的模块路径
    possible_paths = [
        # 从父目录的tools文件夹导入
        os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'tools')),
        # 从当前目录的父目录导入
        os.path.abspath(os.path.join(os.path.dirname(__file__), '..')),
        # 从当前目录导入
        os.path.dirname(__file__),
    ]

    for path in possible_paths:
        if path not in sys.path:
            sys.path.insert(0, path)

    # 尝试不同的导入方式
    
        # 方式1: 直接从tools模块导入
    from tools.batch_process import BatchFileProcessor
    from tools.FormatDetector import FormatDetector
    return BatchFileProcessor, FormatDetector
    # except ImportError:
    #     try:
    #         # 方式2: 从当前目录的tools子文件夹导入
    #         sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tools'))
    #         from batch_process import BatchFileProcessor
    #         from FormatDetector import FormatDetector
    #         return BatchFileProcessor, FormatDetector
    #     except ImportError:
    #         try:
    #             # 方式3: 直接导入
    #             from batch_process import BatchFileProcessor
    #             from FormatDetector import FormatDetector
    #             return BatchFileProcessor, FormatDetector
    #         except ImportError as e:
    #             print(f"文件工具导入失败: {e}")
    #             return None, None


class PlaceholderEntry(ttk.Entry):
    """支持占位符文本的Entry控件"""

    def __init__(self, parent, placeholder="", *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.placeholder = placeholder
        self.placeholder_color = 'grey'
        self.default_color = self.cget('foreground')

        self.bind("<FocusIn>", self._on_focus_in)
        self.bind("<FocusOut>", self._on_focus_out)

        self._show_placeholder()

    def _on_focus_in(self, event):
        if self.get() == self.placeholder:
            self.delete(0, tk.END)
            self.config(foreground=self.default_color)

    def _on_focus_out(self, event):
        if not self.get():
            self._show_placeholder()

    def _show_placeholder(self):
        self.delete(0, tk.END)
        self.insert(0, self.placeholder)
        self.config(foreground=self.placeholder_color)

    def get_value(self):
        """获取实际值（如果不是占位符）"""
        value = self.get()
        if value == self.placeholder:
            return ""
        return value


class DevKitZeroGUI:
    """DevKit-Zero GUI 主类"""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("DevKit-Zero - 零依赖开发者工具箱")
        self.root.geometry("1100x650")
        self.root.resizable(True, True)

        # 创建工具实例
        self.regex_tester = regex_tester.RegexTester()

        # 导入文件工具
        self.BatchFileProcessor, self.FormatDetector = import_file_tools()

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
            ("未使用函数检测", "unused_func"),
            ("端口检查", "port_checker"),
            ("接口契约对比器", "api_diff"),
            ("正则表达式测试", "regex_tester"),
            ("Robots检查器", "robots_checker"),
            ("批量文件处理器", "batch_processor"),  # 新增
            ("格式检测器", "format_detector")  # 新增
        ]

        # 创建两行工具选择按钮
        for i, (name, value) in enumerate(tools):
            row = 0 if i < 8 else 1  # 前8个在第一行，其余在第二行
            col = i if i < 8 else i - 8
            ttk.Radiobutton(tool_frame, text=name, variable=self.tool_var,
                            value=value, command=self.on_tool_change).grid(row=row, column=col, padx=5, pady=2)

        # 左侧控制面板
        control_frame = ttk.LabelFrame(main_frame, text="控制面板", padding="10")
        control_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        control_frame.columnconfigure(0, weight=1)
        control_frame.rowconfigure(0, weight=1)
        # 右侧结果面板
        result_frame = ttk.LabelFrame(main_frame, text="结果输出", padding="10")
        result_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)

        # 结果文本框（用于大部分工具）
        self.result_text = scrolledtext.ScrolledText(result_frame, wrap=tk.WORD, height=20)
        self.result_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 控制面板和结果面板容器
        self.control_container = control_frame
        self.result_container = result_frame

        # 初始化工具面板
        self.on_tool_change()

    def on_tool_change(self):
        """工具选择改变时的处理"""
        # 清除控制面板现有控件
        for widget in self.control_container.winfo_children():
            widget.destroy()

        tool = self.tool_var.get()

        # 清除结果容器并根据工具类型设置结果面板
        for widget in self.result_container.winfo_children():
            widget.destroy()

        # 为使用默认结果文本框的工具重新创建结果文本框
        if tool not in ["regex_tester", "robots_checker"]:
            self.result_text = scrolledtext.ScrolledText(self.result_container, wrap=tk.WORD, height=20)
            self.result_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
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
        elif tool == "port_checker":
            self.setup_port_checker_ui()
        elif tool == "api_diff":
            self.setup_api_diff_ui()
        elif tool == "regex_tester":
            self.setup_regex_tester_ui()
        elif tool == "robots_checker":
            self.setup_robots_checker_ui()
        elif tool == "batch_processor":  # 新增
            self.setup_batch_processor_ui()
        elif tool == "format_detector":  # 新增
            self.setup_format_detector_ui()

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
        ttk.Label(self.control_container, text="(逗号分隔)", font=("", 8)).grid(row=2, column=1, sticky=tk.W,
                                                                                pady=(10, 2))

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
                        variable=self.unused_func_verbose_var).grid(row=6, column=0, columnspan=2, sticky=tk.W,
                                                                    pady=(10, 2))

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
            ttk.Entry(self.random_params_frame, textvariable=self.string_length_var, width=10).grid(row=0, column=1,
                                                                                                    sticky=tk.W, pady=2)

            self.string_numbers_var = tk.BooleanVar(value=True)
            self.string_uppercase_var = tk.BooleanVar(value=True)
            self.string_lowercase_var = tk.BooleanVar(value=True)
            self.string_symbols_var = tk.BooleanVar(value=False)
            
            
            ttk.Checkbutton(self.random_params_frame, text="包含数字", variable=self.string_numbers_var).grid(row=1,
                                                                                                          column=0,
                                                                                                          sticky=tk.W,
                                                                                                          pady=1)
            ttk.Checkbutton(self.random_params_frame, text="包含大写字母", variable=self.string_uppercase_var).grid(row=2,
                                                                                                              column=0,
                                                                                                              sticky=tk.W,
                                                                                                              pady=1)
            ttk.Checkbutton(self.random_params_frame, text="包含小写字母", variable=self.string_lowercase_var).grid(row=3,
                                                                                                              column=0,
                                                                                                              sticky=tk.W,
                                                                                                              pady=1)
            ttk.Checkbutton(self.random_params_frame, text="包含特殊符号", variable=self.string_symbols_var).grid(row=4,
                                                                                                            column=0,
                                                                                                            sticky=tk.W,
                                                                                                            pady=1)

        elif gen_type == "password":
            ttk.Label(self.random_params_frame, text="长度:").grid(row=0, column=0, sticky=tk.W, pady=2)
            self.password_length_var = tk.StringVar(value="16")
            ttk.Entry(self.random_params_frame, textvariable=self.password_length_var, width=10).grid(row=0, column=1,
                                                                                                      sticky=tk.W,
                                                                                                      pady=2)

        elif gen_type == "number":
            ttk.Label(self.random_params_frame, text="最小值:").grid(row=0, column=0, sticky=tk.W, pady=2)
            self.number_min_var = tk.StringVar(value="0")
            ttk.Entry(self.random_params_frame, textvariable=self.number_min_var, width=10).grid(row=0, column=1,
                                                                                                 sticky=tk.W, pady=2)

            ttk.Label(self.random_params_frame, text="最大值:").grid(row=1, column=0, sticky=tk.W, pady=2)
            self.number_max_var = tk.StringVar(value="100")
            ttk.Entry(self.random_params_frame, textvariable=self.number_max_var, width=10).grid(row=1, column=1,
                                                                                                 sticky=tk.W, pady=2)

            self.number_float_var = tk.BooleanVar(value=False)
            ttk.Checkbutton(self.random_params_frame, text="浮点数", variable=self.number_float_var).grid(row=2, column=0,
                                                                                                       sticky=tk.W,
                                                                                                       pady=1)
    
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
            ttk.Entry(self.port_params_frame, textvariable=self.port_host_var).grid(row=0, column=1,
                                                                                    sticky=(tk.W, tk.E), pady=2)

            # port
            ttk.Label(self.port_params_frame, text="端口:").grid(row=1, column=0, sticky=tk.W, pady=2)
            self.port_port_var = tk.StringVar(value="8080")
            ttk.Entry(self.port_params_frame, textvariable=self.port_port_var).grid(row=1, column=1,
                                                                                    sticky=(tk.W, tk.E), pady=2)

            # timeout
            ttk.Label(self.port_params_frame, text="超时(秒):").grid(row=2, column=0, sticky=tk.W, pady=2)
            self.port_timeout_var = tk.StringVar(value="3")
            ttk.Entry(self.port_params_frame, textvariable=self.port_timeout_var).grid(row=2, column=1,
                                                                                       sticky=(tk.W, tk.E), pady=2)

        elif action == "scan":
            # host
            ttk.Label(self.port_params_frame, text="主机:").grid(row=0, column=0, sticky=tk.W, pady=2)
            self.scan_host_var = tk.StringVar(value="localhost")
            ttk.Entry(self.port_params_frame, textvariable=self.scan_host_var).grid(row=0, column=1,
                                                                                    sticky=(tk.W, tk.E), pady=2)

            # start
            ttk.Label(self.port_params_frame, text="起始端口:").grid(row=1, column=0, sticky=tk.W, pady=2)
            self.scan_start_var = tk.StringVar(value="1")
            ttk.Entry(self.port_params_frame, textvariable=self.scan_start_var).grid(row=1, column=1,
                                                                                     sticky=(tk.W, tk.E), pady=2)

            # end
            ttk.Label(self.port_params_frame, text="结束端口:").grid(row=2, column=0, sticky=tk.W, pady=2)
            self.scan_end_var = tk.StringVar(value="1000")
            ttk.Entry(self.port_params_frame, textvariable=self.scan_end_var).grid(row=2, column=1, sticky=(tk.W, tk.E),
                                                                                   pady=2)

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

    def setup_api_diff_ui(self):
        import tkinter as tk
        from tkinter import ttk

        # ===== 顶部：输出格式 =====
        ttk.Label(self.control_container, text="输出格式:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.api_fmt_var = tk.StringVar(value="text")
        ttk.Combobox(self.control_container, textvariable=self.api_fmt_var,
                     values=["text", "json", "md"], state="readonly") \
            .grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2)

        # ===== 契约 v1 =====
        ttk.Label(self.control_container, text="契约 v1:").grid(row=1, column=0, sticky=tk.W, pady=(8, 2))
        ttk.Button(self.control_container, text="从文件加载",
                   command=lambda: self.load_contract_from_file("v1")) \
            .grid(row=1, column=1, sticky=tk.E, pady=(8, 2))

        # 说明小字（灰色）
        tk.Label(self.control_container,
                 text="支持：简化契约 JSON 或 OpenAPI JSON",
                 fg="#666").grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=(0, 6))

        # v1 文本框（行号顺延）
        self.api_old_text = tk.Text(self.control_container, height=12)
        self.api_old_text.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E))

        # ===== 契约 v2 =====
        ttk.Label(self.control_container, text="契约 v2:").grid(row=4, column=0, sticky=tk.W, pady=(8, 2))
        ttk.Button(self.control_container, text="从文件加载",
                   command=lambda: self.load_contract_from_file("v2")) \
            .grid(row=4, column=1, sticky=tk.E, pady=(8, 2))

        # 说明小字（灰色）
        tk.Label(self.control_container,
                 text="支持：简化契约 JSON 或 OpenAPI JSON",
                 fg="#666").grid(row=5, column=0, columnspan=2, sticky=tk.W, pady=(0, 6))

        # v2 文本框（行号顺延）
        self.api_new_text = tk.Text(self.control_container, height=12)
        self.api_new_text.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E))

        # ===== 操作区 =====
        ttk.Button(self.control_container, text="对比契约", command=self.run_api_diff) \
            .grid(row=7, column=0, columnspan=2, pady=(10, 0))
        ttk.Button(self.control_container, text="填充示例", command=self.fill_demo_api_diff) \
            .grid(row=8, column=0, columnspan=2, pady=(6, 0))

        # 右侧列可伸缩
        self.control_container.columnconfigure(1, weight=1)

    '''
    def setup_api_diff_ui(self):
        import tkinter as tk
        from tkinter import ttk

        # 输出格式
        ttk.Label(self.control_container, text="输出格式:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.api_fmt_var = tk.StringVar(value="text")
        ttk.Combobox(self.control_container, textvariable=self.api_fmt_var,
                    values=["text", "json", "md"], state="readonly")\
            .grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2)

        # 契约 v1
        ttk.Label(self.control_container, text="契约 v1:").grid(row=1, column=0, sticky=tk.W, pady=(8, 2))
        ttk.Button(self.control_container, text="从文件加载",
                command=lambda: self.load_contract_from_file("v1"))\
            .grid(row=1, column=1, sticky=tk.E, pady=(8, 2))
        self.api_old_text = tk.Text(self.control_container, height=12)
        self.api_old_text.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E))

        # 契约 v2
        ttk.Label(self.control_container, text="契约 v2:").grid(row=3, column=0, sticky=tk.W, pady=(8, 2))
        ttk.Button(self.control_container, text="从文件加载",
                command=lambda: self.load_contract_from_file("v2"))\
            .grid(row=3, column=1, sticky=tk.E, pady=(8, 2))
        self.api_new_text = tk.Text(self.control_container, height=12)
        self.api_new_text.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E))

        # 操作区
        ttk.Button(self.control_container, text="对比契约", command=self.run_api_diff)\
            .grid(row=5, column=0, columnspan=2, pady=(10, 0))
        ttk.Button(self.control_container, text="填充示例", command=self.fill_demo_api_diff)\
            .grid(row=6, column=0, columnspan=2, pady=(6, 0))

        self.control_container.columnconfigure(1, weight=1)
    '''

    def load_contract_from_file(self, target="v1"):
        import json
        from tkinter import filedialog
        path = filedialog.askopenfilename(
            title="选择契约 JSON 文件",
            filetypes=[("JSON 文件", "*.json"), ("所有文件", "*.*")]
        )
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                raw = f.read()
            # 提前校验 JSON，便于在 GUI 里给出明确信息
            json.loads(raw)
        except Exception as e:
            self.display_error(f"读取/解析失败：{e}")
            return

        widget = self.api_old_text if target == "v1" else self.api_new_text
        widget.delete("1.0", "end")
        widget.insert("1.0", raw)
        self.display_result(f"已加载：{path}")

    def run_api_diff(self):
        try:
            old_text = self.api_old_text.get("1.0", "end").strip()
            new_text = self.api_new_text.get("1.0", "end").strip()
            if not old_text or not new_text:
                raise ValueError("请分别在“契约 v1 / 契约 v2”填入 JSON 文本或点击“从文件加载”")
            old = api_contract_diff.parse_contract(text=old_text)
            new = api_contract_diff.parse_contract(text=new_text)
            report = api_contract_diff.compare_contracts(old, new)

            fmt = self.api_fmt_var.get()
            if fmt == "json":
                out = api_contract_diff.format_report_json(report)
            elif fmt == "md":
                out = api_contract_diff.format_report_md(report)
            else:
                out = api_contract_diff.format_report_text(report)

            self.display_result(out)
        except Exception as e:
            self.display_error(str(e))

    def fill_demo_api_diff(self):
        demo_v1 = '''{
      "apis": [
        {
        "name": "GetUser",
        "method": "GET",
        "path": "/users/{id}",
        "params": [{"in":"path","name":"id","type":"string","required":true}],
        "responses": {"200":{"type":"object","required":["id"],
            "properties":{"id":{"type":"string"}, "name":{"type":"string"}}}}
        },
        {
        "name": "ListUsers",
        "method": "GET",
        "path": "/users",
        "query": [{"name":"active","type":"boolean","required":false}],
        "responses": {"200":{"type":"object","properties":{"items":{"type":"array",
            "items":{"type":"object","properties":{"id":{"type":"string"}}}}}}}
        }
    ]
    }'''
        demo_v2 = '''{
      "apis": [
        {
        "name": "GetUser",
        "method": "GET",
        "path": "/users/{id}",
        "params": [{"in":"path","name":"id","type":"string","required":true}],
        "responses": {"200":{"type":"object","required":["id"],
            "properties":{"id":{"type":"string"}, "email":{"type":"string"}}}}
        },
        {
        "name": "ListUsers",
        "method": "GET",
        "path": "/users",
        "query": [
            {"name":"active","type":"boolean","required":false},
            {"name":"page","type":"integer","required":true}
        ],
        "responses": {"200":{"type":"object","properties":{"items":{"type":"array",
            "items":{"type":"object","properties":{"id":{"type":"string"}}}}}}}
        },
        {"name":"CreateUser","method":"POST","path":"/users",
        "request":{"type":"object","required":["name"],
        "properties":{"name":{"type":"string"},"age":{"type":"integer"}}},
        "responses":{"201":{"type":"object","properties":{"id":{"type":"string"}}}}}
    ]
    }'''
        self.api_old_text.delete("1.0", "end");
        self.api_old_text.insert("1.0", demo_v1)
        self.api_new_text.delete("1.0", "end");
        self.api_new_text.insert("1.0", demo_v2)

    # ========== 正则表达式测试工具 ==========
    def setup_regex_tester_ui(self):
        """设置正则表达式测试工具界面"""
        # 控制面板 - 正则相关控件
        control_frame = ttk.Frame(self.control_container)
        control_frame.pack(fill=tk.BOTH, expand=True)

        # 常用模式选择
        ttk.Label(control_frame, text="常用模式:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.pattern_var = tk.StringVar()
        self.common_patterns_combo = ttk.Combobox(
            control_frame,
            textvariable=self.pattern_var,
            values=list(self.regex_tester.get_common_patterns().keys()),
            state="readonly",
            width=30
        )
        self.common_patterns_combo.set("选择常用模式...")
        self.common_patterns_combo.grid(row=0, column=1, sticky=tk.EW, pady=5, padx=(5, 0))
        self.common_patterns_combo.bind('<<ComboboxSelected>>', self.on_pattern_selected)

        # 自定义模式输入
        ttk.Label(control_frame, text="自定义模式:").grid(row=1, column=0, sticky=tk.NW, pady=5)
        self.pattern_entry = scrolledtext.ScrolledText(control_frame, width=40, height=3)
        self.pattern_entry.grid(row=1, column=1, sticky=tk.EW, pady=5, padx=(5, 0))

        # 选项框架
        options_frame = ttk.LabelFrame(control_frame, text="选项", padding=5)
        options_frame.grid(row=2, column=1, sticky=tk.EW, pady=5, padx=(5, 0))

        # 正则标志
        self.ignore_case_var = tk.BooleanVar()
        ttk.Checkbutton(
            options_frame,
            text="忽略大小写 (re.IGNORECASE)",
            variable=self.ignore_case_var
        ).pack(anchor=tk.W)

        self.multiline_var = tk.BooleanVar()
        ttk.Checkbutton(
            options_frame,
            text="多行模式 (re.MULTILINE)",
            variable=self.multiline_var
        ).pack(anchor=tk.W)

        self.dotall_var = tk.BooleanVar()
        ttk.Checkbutton(
            options_frame,
            text="点匹配换行 (re.DOTALL)",
            variable=self.dotall_var
        ).pack(anchor=tk.W)

        # 测试文本区域
        ttk.Label(control_frame, text="测试文本:").grid(row=3, column=0, sticky=tk.NW, pady=5)
        self.text_area = scrolledtext.ScrolledText(control_frame, width=40, height=10)
        self.text_area.grid(row=3, column=1, sticky=tk.NSEW, pady=5, padx=(5, 0))

        # 按钮区域
        button_frame = ttk.Frame(control_frame)
        button_frame.grid(row=4, column=0, columnspan=2, sticky=tk.EW, pady=10)

        self.test_button = ttk.Button(
            button_frame,
            text="测试正则",
            command=self.test_regex
        )
        self.test_button.pack(side=tk.LEFT, padx=(0, 10))

        self.clear_button = ttk.Button(
            button_frame,
            text="清空所有",
            command=self.clear_all_regex
        )
        self.clear_button.pack(side=tk.LEFT, padx=(0, 10))

        self.copy_result_button = ttk.Button(
            button_frame,
            text="复制结果",
            command=self.copy_regex_results
        )
        self.copy_result_button.pack(side=tk.LEFT)

        # 配置权重
        control_frame.columnconfigure(1, weight=1)
        control_frame.rowconfigure(3, weight=1)

        # 设置快捷键
        self.text_area.bind('<Control-Return>', lambda e: self.test_regex())
        self.pattern_entry.bind('<Control-Return>', lambda e: self.test_regex())

        # 结果面板 - 正则测试结果
        result_frame = ttk.Frame(self.result_container)
        result_frame.pack(fill=tk.BOTH, expand=True)

        # 匹配统计
        stats_frame = ttk.Frame(result_frame)
        stats_frame.pack(fill=tk.X, pady=(0, 10))
        self.stats_label = ttk.Label(stats_frame, text="匹配结果: 0 个匹配", font=('Arial', 10, 'bold'))
        self.stats_label.pack(side=tk.LEFT)
        self.pattern_status_label = ttk.Label(stats_frame, text="模式状态: 未测试", foreground="gray")
        self.pattern_status_label.pack(side=tk.RIGHT)

        # 匹配详情
        ttk.Label(result_frame, text="匹配详情:").pack(anchor=tk.W, pady=(0, 5))
        self.matches_text = scrolledtext.ScrolledText(
            result_frame,
            width=60,
            height=8,
            state=tk.DISABLED
        )
        self.matches_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # 替换结果显示
        replace_frame = ttk.LabelFrame(result_frame, text="替换结果", padding=5)
        replace_frame.pack(fill=tk.X)
        self.replace_text = scrolledtext.ScrolledText(
            replace_frame,
            width=60,
            height=4,
            state=tk.DISABLED
        )
        self.replace_text.pack(fill=tk.BOTH, expand=True)

    def on_pattern_selected(self, event):
        """选择常用模式时的回调"""
        pattern_name = self.pattern_var.get()
        common_patterns = self.regex_tester.get_common_patterns()

        if pattern_name in common_patterns:
            self.pattern_entry.delete(1.0, tk.END)
            self.pattern_entry.insert(1.0, common_patterns[pattern_name])

    def test_regex(self):
        """测试正则表达式"""
        pattern = self.pattern_entry.get(1.0, tk.END).strip()
        text = self.text_area.get(1.0, tk.END)

        if not pattern:
            messagebox.showerror("错误", "请输入正则表达式模式")
            return

        if not text.strip():
            messagebox.showwarning("警告", "请输入测试文本")
            return

        # 计算标志
        flags = 0
        if self.ignore_case_var.get():
            flags |= re.IGNORECASE
        if self.multiline_var.get():
            flags |= re.MULTILINE
        if self.dotall_var.get():
            flags |= re.DOTALL

        # 测试正则
        result = self.regex_tester.test_pattern(pattern, text, flags)

        # 显示结果
        self.display_regex_results(result)

    def display_regex_results(self, result):
        """显示匹配结果"""
        # 更新统计
        if result['success']:
            self.stats_label.config(
                text=f"匹配结果: {result['match_count']} 个匹配",
                foreground="green"
            )
            self.pattern_status_label.config(
                text="模式状态: 有效",
                foreground="green"
            )
        else:
            self.stats_label.config(
                text=f"错误: {result['error']}",
                foreground="red"
            )
            self.pattern_status_label.config(
                text="模式状态: 无效",
                foreground="red"
            )

        # 更新匹配详情
        self.matches_text.config(state=tk.NORMAL)
        self.matches_text.delete(1.0, tk.END)

        if result['success'] and result['match_count'] > 0:
            for i, match in enumerate(result['matches'], 1):
                self.matches_text.insert(tk.END, f"匹配 {i}:\n")
                self.matches_text.insert(tk.END, f"  位置: {match['start']}-{match['end']}\n")
                self.matches_text.insert(tk.END, f"  值: {match['group']}\n")

                if match['groups']:
                    self.matches_text.insert(tk.END, "  分组:\n")
                    for j, group in enumerate(match['groups'], 1):
                        self.matches_text.insert(tk.END, f"    分组 {j}: {group}\n")
                self.matches_text.insert(tk.END, "\n")
        elif result['success']:
            self.matches_text.insert(tk.END, "未找到匹配。")
        else:
            self.matches_text.insert(tk.END, f"模式错误: {result['error']}")

        self.matches_text.config(state=tk.DISABLED)

        # 更新替换文本
        self.replace_text.config(state=tk.NORMAL)
        self.replace_text.delete(1.0, tk.END)
        self.replace_text.insert(tk.END, result['replaced_text'])
        self.replace_text.config(state=tk.DISABLED)

    def clear_all_regex(self):
        """清空所有输入和结果"""
        self.pattern_entry.delete(1.0, tk.END)
        self.text_area.delete(1.0, tk.END)
        self.matches_text.config(state=tk.NORMAL)
        self.matches_text.delete(1.0, tk.END)
        self.matches_text.config(state=tk.DISABLED)
        self.replace_text.config(state=tk.NORMAL)
        self.replace_text.delete(1.0, tk.END)
        self.replace_text.config(state=tk.DISABLED)
        self.stats_label.config(text="匹配结果: 0 个匹配", foreground="black")
        self.pattern_status_label.config(text="模式状态: 未测试", foreground="gray")
        self.common_patterns_combo.set("选择常用模式...")
        self.ignore_case_var.set(False)
        self.multiline_var.set(False)
        self.dotall_var.set(False)

    def copy_regex_results(self):
        """复制正则测试结果到剪贴板"""
        self.root.clipboard_clear()
        results = self.matches_text.get(1.0, tk.END).strip()
        self.root.clipboard_append(results)
        messagebox.showinfo("已复制", "结果已复制到剪贴板")

    # ========== Robots检查器 ==========
    def setup_robots_checker_ui(self):
        """设置Robots检查器界面"""
        # 控制面板 - robots检查器相关控件
        control_frame = ttk.Frame(self.control_container)
        control_frame.pack(fill=tk.BOTH, expand=True)

        # URL输入
        ttk.Label(control_frame, text="网站URL:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.robots_url_entry = ttk.Entry(control_frame, width=40)
        self.robots_url_entry.grid(row=0, column=1, sticky=tk.EW, pady=5, padx=(5, 0))
        self.robots_url_entry.insert(0, "https://")  # 默认前缀

        # 选项框架
        options_frame = ttk.LabelFrame(control_frame, text="选项", padding=5)
        options_frame.grid(row=1, column=0, columnspan=2, sticky=tk.EW, pady=5)

        # 超时设置
        ttk.Label(options_frame, text="超时(秒):").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.robots_timeout_var = tk.StringVar(value="10")
        ttk.Entry(options_frame, textvariable=self.robots_timeout_var, width=10).grid(row=0, column=1, sticky=tk.W, padx=5)

        # 原始输出选项
        self.robots_raw_var = tk.BooleanVar()
        ttk.Checkbutton(
            options_frame,
            text="显示原始robots.txt内容",
            variable=self.robots_raw_var
        ).grid(row=0, column=2, sticky=tk.W, padx=10)

        # 按钮区域
        button_frame = ttk.Frame(control_frame)
        button_frame.grid(row=2, column=0, columnspan=2, sticky=tk.EW, pady=10)

        self.check_robots_button = ttk.Button(
            button_frame,
            text="检查Robots规则",
            command=self.check_robots
        )
        self.check_robots_button.pack(side=tk.LEFT, padx=(0, 10))

        self.copy_robots_button = ttk.Button(
            button_frame,
            text="复制结果",
            command=self.copy_robots_results
        )
        self.copy_robots_button.pack(side=tk.LEFT)

        # 配置权重
        control_frame.columnconfigure(1, weight=1)
        options_frame.columnconfigure(2, weight=1)

        # 设置快捷键: Ctrl+Enter检查
        self.robots_url_entry.bind('<Control-Return>', lambda e: self.check_robots())

        # 结果面板 - robots检查器结果
        result_frame = ttk.Frame(self.result_container)
        result_frame.pack(fill=tk.BOTH, expand=True)

        # 状态栏
        self.robots_status_label = ttk.Label(result_frame, text="状态: 就绪", font=('Arial', 10, 'bold'))
        self.robots_status_label.pack(anchor=tk.W, pady=(0, 5))

        # Robots URL显示
        self.robots_url_label = ttk.Label(result_frame, text="", foreground="blue")
        self.robots_url_label.pack(anchor=tk.W, pady=(0, 10))

        # 结果笔记本(标签页)
        notebook = ttk.Notebook(result_frame)
        notebook.pack(fill=tk.BOTH, expand=True)

        # 解析规则标签页
        self.robots_parsed_text = scrolledtext.ScrolledText(
            notebook,
            width=60,
            height=15,
            state=tk.DISABLED
        )
        notebook.add(self.robots_parsed_text, text="解析规则")

        # 原始内容标签页
        self.robots_raw_text = scrolledtext.ScrolledText(
            notebook,
            width=60,
            height=15,
            state=tk.DISABLED
        )
        notebook.add(self.robots_raw_text, text="原始内容")

    def check_robots(self):
        """检查给定URL的robots.txt"""
        url = self.robots_url_entry.get().strip()

        if not url:
            messagebox.showerror("错误", "请输入网站URL")
            return

        try:
            # 获取超时值
            timeout = int(self.robots_timeout_var.get())

            # 更新状态
            self.robots_status_label.config(text="状态: 检查中...", foreground="orange")
            self.root.update()  # 强制UI更新

            # 调用核心逻辑
            result = robots_core_logic(url, timeout=timeout)

            # 更新状态
            self.robots_status_label.config(
                text=f"状态: {result['message']}",
                foreground="green" if result['success'] else "red"
            )
            self.robots_url_label.config(text=result['url'])

            # 显示原始内容
            self.robots_raw_text.config(state=tk.NORMAL)
            self.robots_raw_text.delete(1.0, tk.END)
            self.robots_raw_text.insert(1.0, result['content'] or "无可用内容")
            self.robots_raw_text.config(state=tk.DISABLED)

            # 显示解析规则(如果成功)
            self.robots_parsed_text.config(state=tk.NORMAL)
            self.robots_parsed_text.delete(1.0, tk.END)

            if result['success'] and result['rules']:
                rules = result['rules']

                if rules['host']:
                    self.robots_parsed_text.insert(tk.END, f"主机: {rules['host']}\n\n")

                if rules['crawl_delay']:
                    self.robots_parsed_text.insert(tk.END, f"抓取延迟: {rules['crawl_delay']} 秒\n\n")

                if rules['sitemaps']:
                    self.robots_parsed_text.insert(tk.END, "站点地图:\n")
                    for sitemap in rules['sitemaps']:
                        self.robots_parsed_text.insert(tk.END, f"- {sitemap}\n")
                    self.robots_parsed_text.insert(tk.END, "\n")

                self.robots_parsed_text.insert(tk.END, "用户代理规则:\n")
                for agent, agent_rules in rules['user_agents'].items():
                    self.robots_parsed_text.insert(tk.END, f"\n用户代理: {agent}\n")

                    if agent_rules['allow']:
                        self.robots_parsed_text.insert(tk.END, "  允许:\n")
                        for path in agent_rules['allow']:
                            self.robots_parsed_text.insert(tk.END, f"    - {path}\n")

                    if agent_rules['disallow']:
                        self.robots_parsed_text.insert(tk.END, "  禁止:\n")
                        for path in agent_rules['disallow']:
                            self.robots_parsed_text.insert(tk.END, f"    - {path}\n")
            else:
                self.robots_parsed_text.insert(tk.END, "未找到有效的robots规则或无法解析内容。")

            self.robots_parsed_text.config(state=tk.DISABLED)

        except ValueError as e:
            self.robots_status_label.config(text=f"状态: 错误 - {str(e)}", foreground="red")
            messagebox.showerror("错误", str(e))
        except Exception as e:
            self.robots_status_label.config(text=f"状态: 错误 - {str(e)}", foreground="red")
            messagebox.showerror("错误", f"检查robots规则失败: {str(e)}")

    def copy_robots_results(self):
        """复制robots检查结果到剪贴板"""
        self.root.clipboard_clear()
        parsed_content = self.robots_parsed_text.get(1.0, tk.END).strip()
        self.root.clipboard_append(parsed_content)
        messagebox.showinfo("已复制", "结果已复制到剪贴板")

    # ========== 文件处理工具 ==========

    def setup_batch_processor_ui(self):
        """设置批量文件处理器界面"""
        # 操作类型选择
        ttk.Label(self.control_container, text="操作类型:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.batch_operation_var = tk.StringVar(value="rename")
        op_combo = ttk.Combobox(self.control_container, textvariable=self.batch_operation_var,
                                values=["rename", "copy", "move"], state="readonly")
        op_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)
        op_combo.bind('<<ComboboxSelected>>', self.on_batch_operation_change)

        # 目录选择
        ttk.Label(self.control_container, text="目录路径:").grid(row=1, column=0, sticky=tk.W, pady=5)
        dir_frame = ttk.Frame(self.control_container)
        dir_frame.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
        dir_frame.columnconfigure(0, weight=1)

        self.batch_dir_var = tk.StringVar(value=".")
        ttk.Entry(dir_frame, textvariable=self.batch_dir_var).grid(row=0, column=0, sticky=(tk.W, tk.E))
        ttk.Button(dir_frame, text="选择目录", command=self.select_batch_dir).grid(row=0, column=1, padx=(5, 0))

        # 目标目录（用于复制和移动）
        self.target_dir_frame = ttk.Frame(self.control_container)
        self.target_dir_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        self.target_dir_frame.columnconfigure(1, weight=1)

        # 参数框架
        self.params_frame = ttk.Frame(self.control_container)
        self.params_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        self.params_frame.columnconfigure(1, weight=1)

        # 选项框架
        options_frame = ttk.LabelFrame(self.control_container, text="选项", padding="5")
        options_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        # 预览模式
        self.preview_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="预览模式", variable=self.preview_var).grid(row=0, column=0, sticky=tk.W)

        # 递归搜索
        self.recursive_var = tk.BooleanVar(value=False)
        self.recursive_check = ttk.Checkbutton(options_frame, text="递归搜索", variable=self.recursive_var)

        # 覆盖文件
        self.overwrite_var = tk.BooleanVar(value=False)
        self.overwrite_check = ttk.Checkbutton(options_frame, text="覆盖已存在文件", variable=self.overwrite_var)

        # 按钮框架
        button_frame = ttk.Frame(self.control_container)
        button_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

        ttk.Button(button_frame, text="执行操作", command=self.run_batch_operation).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(button_frame, text="执行预览的操作", command=self.execute_batch_operations).grid(row=0, column=1)

        self.control_container.columnconfigure(1, weight=1)

        # 初始化操作界面
        self.on_batch_operation_change()

    def on_batch_operation_change(self, event=None):
        """批量操作类型改变时的处理"""
        # 清除参数框架
        for widget in self.params_frame.winfo_children():
            widget.destroy()

        # 清除目标目录框架
        for widget in self.target_dir_frame.winfo_children():
            widget.destroy()

        operation = self.batch_operation_var.get()

        if operation == "rename":
            self.setup_rename_params()
        elif operation == "copy":
            self.setup_copy_params()
            self.setup_target_dir()
        elif operation == "move":
            self.setup_move_params()
            self.setup_target_dir()

    def setup_rename_params(self):
        """设置重命名参数"""
        row = 0

        # 查找模式
        ttk.Label(self.params_frame, text="查找模式:").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.pattern_var = tk.StringVar()
        ttk.Entry(self.params_frame, textvariable=self.pattern_var).grid(row=row, column=1, sticky=(tk.W, tk.E), pady=2)
        row += 1

        # 替换为
        ttk.Label(self.params_frame, text="替换为:").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.replacement_var = tk.StringVar()
        ttk.Entry(self.params_frame, textvariable=self.replacement_var).grid(row=row, column=1, sticky=(tk.W, tk.E),
                                                                             pady=2)
        row += 1

        # 选项
        self.regex_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(self.params_frame, text="使用正则表达式", variable=self.regex_var).grid(
            row=row, column=0, columnspan=2, sticky=tk.W, pady=2)
        row += 1

        self.case_sensitive_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(self.params_frame, text="大小写敏感", variable=self.case_sensitive_var).grid(
            row=row, column=0, columnspan=2, sticky=tk.W, pady=2)
        row += 1

        # 扩展名过滤 - 使用自定义的占位符Entry
        ttk.Label(self.params_frame, text="扩展名过滤:").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.extension_entry = PlaceholderEntry(self.params_frame, placeholder="例如: .txt, .jpg")
        self.extension_entry.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=2)

        self.params_frame.columnconfigure(1, weight=1)

    def setup_copy_params(self):
        """设置复制参数"""
        row = 0

        # 文件模式
        ttk.Label(self.params_frame, text="文件模式:").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.copy_pattern_var = tk.StringVar(value="*")
        ttk.Entry(self.params_frame, textvariable=self.copy_pattern_var).grid(row=row, column=1, sticky=(tk.W, tk.E),
                                                                              pady=2)
        row += 1

        # 显示选项
        self.recursive_check.grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=2)
        row += 1
        self.overwrite_check.grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=2)

        self.params_frame.columnconfigure(1, weight=1)

    def setup_move_params(self):
        """设置移动参数"""
        row = 0

        # 文件模式
        ttk.Label(self.params_frame, text="文件模式:").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.move_pattern_var = tk.StringVar(value="*")
        ttk.Entry(self.params_frame, textvariable=self.move_pattern_var).grid(row=row, column=1, sticky=(tk.W, tk.E),
                                                                              pady=2)
        row += 1

        # 显示选项
        self.recursive_check.grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=2)
        row += 1
        self.overwrite_check.grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=2)

        self.params_frame.columnconfigure(1, weight=1)

    def setup_target_dir(self):
        """设置目标目录"""
        ttk.Label(self.target_dir_frame, text="目标目录:").grid(row=0, column=0, sticky=tk.W, pady=2)
        dir_frame = ttk.Frame(self.target_dir_frame)
        dir_frame.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2)
        dir_frame.columnconfigure(0, weight=1)

        self.target_dir_var = tk.StringVar()
        ttk.Entry(dir_frame, textvariable=self.target_dir_var).grid(row=0, column=0, sticky=(tk.W, tk.E))
        ttk.Button(dir_frame, text="选择目录", command=self.select_target_dir).grid(row=0, column=1, padx=(5, 0))

        self.target_dir_frame.columnconfigure(1, weight=1)

    def setup_format_detector_ui(self):
        """设置格式检测器界面"""
        # 检测模式选择
        ttk.Label(self.control_container, text="检测模式:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.detect_mode_var = tk.StringVar(value="file")
        mode_combo = ttk.Combobox(self.control_container, textvariable=self.detect_mode_var,
                                  values=["file", "directory", "content"], state="readonly")
        mode_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)
        mode_combo.bind('<<ComboboxSelected>>', self.on_detect_mode_change)

        # 文件/目录选择框架
        self.path_frame = ttk.Frame(self.control_container)
        self.path_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        self.path_frame.columnconfigure(1, weight=1)

        # 内容输入框架
        self.content_frame = ttk.Frame(self.control_container)

        # 详细输出选项
        ttk.Label(self.control_container, text="输出选项:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.verbose_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(self.control_container, text="详细输出", variable=self.verbose_var).grid(
            row=3, column=1, sticky=tk.W, pady=5)

        # 按钮
        ttk.Button(self.control_container, text="开始检测", command=self.run_format_detection).grid(
            row=4, column=0, columnspan=2, pady=10)

        self.control_container.columnconfigure(1, weight=1)

        # 初始化检测模式界面
        self.on_detect_mode_change()

    def on_detect_mode_change(self, event=None):
        """检测模式改变时的处理"""
        # 清除路径框架
        for widget in self.path_frame.winfo_children():
            widget.destroy()

        # 隐藏内容框架
        self.content_frame.grid_forget()

        mode = self.detect_mode_var.get()

        if mode == "file":
            self.setup_file_detection_ui()
        elif mode == "directory":
            self.setup_directory_detection_ui()
        elif mode == "content":
            self.setup_content_detection_ui()

    def setup_file_detection_ui(self):
        """设置文件检测界面"""
        ttk.Label(self.path_frame, text="文件路径:").grid(row=0, column=0, sticky=tk.W, pady=2)
        file_frame = ttk.Frame(self.path_frame)
        file_frame.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2)
        file_frame.columnconfigure(0, weight=1)

        self.file_path_var = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.file_path_var).grid(row=0, column=0, sticky=(tk.W, tk.E))
        ttk.Button(file_frame, text="选择文件", command=self.select_detect_file).grid(row=0, column=1, padx=(5, 0))

        self.path_frame.columnconfigure(1, weight=1)

    def setup_directory_detection_ui(self):
        """设置目录检测界面"""
        ttk.Label(self.path_frame, text="目录路径:").grid(row=0, column=0, sticky=tk.W, pady=2)
        dir_frame = ttk.Frame(self.path_frame)
        dir_frame.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2)
        dir_frame.columnconfigure(0, weight=1)

        self.dir_path_var = tk.StringVar(value=".")
        ttk.Entry(dir_frame, textvariable=self.dir_path_var).grid(row=0, column=0, sticky=(tk.W, tk.E))
        ttk.Button(dir_frame, text="选择目录", command=self.select_detect_dir).grid(row=0, column=1, padx=(5, 0))

        self.path_frame.columnconfigure(1, weight=1)

    def setup_content_detection_ui(self):
        """设置内容检测界面"""
        # 隐藏路径框架，显示内容框架
        self.path_frame.grid_forget()
        self.content_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        self.content_frame.columnconfigure(0, weight=1)

        ttk.Label(self.content_frame, text="输入内容:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.content_text = scrolledtext.ScrolledText(self.content_frame, height=10, wrap=tk.WORD)
        self.content_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=2)

        ttk.Label(self.content_frame, text="文件名(可选):").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.content_filename_var = tk.StringVar()
        ttk.Entry(self.content_frame, textvariable=self.content_filename_var).grid(
            row=3, column=0, sticky=(tk.W, tk.E), pady=2)

        self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.rowconfigure(1, weight=1)

    def select_batch_dir(self):
        """选择批量处理目录"""
        directory = filedialog.askdirectory(initialdir=".")
        if directory:
            self.batch_dir_var.set(directory)

    def select_target_dir(self):
        """选择目标目录"""
        directory = filedialog.askdirectory(initialdir=".")
        if directory:
            self.target_dir_var.set(directory)

    def select_detect_file(self):
        """选择检测文件"""
        filename = filedialog.askopenfilename(
            title="选择要检测的文件",
            filetypes=[("所有文件", "*.*"), ("文本文件", "*.txt"), ("JSON文件", "*.json"),
                       ("XML文件", "*.xml"), ("CSV文件", "*.csv")]
        )
        if filename:
            self.file_path_var.set(filename)

    def select_detect_dir(self):
        """选择检测目录"""
        directory = filedialog.askdirectory(initialdir=".")
        if directory:
            self.dir_path_var.set(directory)

    def run_batch_operation(self):
        """运行批量操作"""
        try:
            if self.BatchFileProcessor is None:
                raise ImportError("无法导入 BatchFileProcessor，请检查文件位置")

            operation = self.batch_operation_var.get()
            directory = self.batch_dir_var.get().strip()

            if not directory:
                raise ValueError("请选择目录")

            # 创建处理器实例
            batch_processor = self.BatchFileProcessor(preview=self.preview_var.get())
            batch_processor.operations = []  # 清空之前的操作

            if operation == "rename":
                self.run_rename_operation(directory, batch_processor)
            elif operation == "copy":
                self.run_copy_operation(directory, batch_processor)
            elif operation == "move":
                self.run_move_operation(directory, batch_processor)

            # 显示结果
            if batch_processor.preview:
                result = "预览模式 - 以下操作将被执行:\n\n"
                for i, (op_type, src, dst) in enumerate(batch_processor.operations, 1):
                    result += f"{i}. {op_type}: '{os.path.basename(src)}' -> '{os.path.basename(dst)}'\n"
                result += f"\n共 {len(batch_processor.operations)} 个操作"
                # 保存处理器实例供后续使用
                self.current_batch_processor = batch_processor
            else:
                result = "操作已完成！"

            self.display_result(result)

        except Exception as e:
            self.display_error(str(e))

    def run_rename_operation(self, directory, batch_processor):
        """运行重命名操作"""
        pattern = self.pattern_var.get().strip()
        replacement = self.replacement_var.get().strip()

        if not pattern:
            raise ValueError("请输入查找模式")

        # 使用自定义Entry的get_value方法获取扩展名
        extension = self.extension_entry.get_value().strip()
        extension = extension if extension else None

        batch_processor.rename_files(
            directory=directory,
            pattern=pattern,
            replacement=replacement,
            regex=self.regex_var.get(),
            case_sensitive=self.case_sensitive_var.get(),
            extension_filter=extension
        )

    def run_copy_operation(self, directory, batch_processor):
        """运行复制操作"""
        target_dir = self.target_dir_var.get().strip()
        if not target_dir:
            raise ValueError("请选择目标目录")

        pattern = self.copy_pattern_var.get().strip()

        batch_processor.copy_files(
            source_dir=directory,
            target_dir=target_dir,
            pattern=pattern,
            recursive=self.recursive_var.get(),
            overwrite=self.overwrite_var.get()
        )

    def run_move_operation(self, directory, batch_processor):
        """运行移动操作"""
        target_dir = self.target_dir_var.get().strip()
        if not target_dir:
            raise ValueError("请选择目标目录")

        pattern = self.move_pattern_var.get().strip()

        batch_processor.move_files(
            source_dir=directory,
            target_dir=target_dir,
            pattern=pattern,
            recursive=self.recursive_var.get(),
            overwrite=self.overwrite_var.get()
        )

    def execute_batch_operations(self):
        """执行预览的操作"""
        if not hasattr(self, 'current_batch_processor') or not self.current_batch_processor.operations:
            messagebox.showinfo("提示", "没有操作需要执行")
            return

        try:
            self.current_batch_processor.execute_operations()
            self.display_result("所有操作已完成！")
        except Exception as e:
            self.display_error(str(e))

    def run_format_detection(self):
        """运行格式检测"""
        try:
            if self.FormatDetector is None:
                raise ImportError("无法导入 FormatDetector，请检查文件位置")

            mode = self.detect_mode_var.get()
            verbose = self.verbose_var.get()

            # 创建检测器实例
            format_detector = self.FormatDetector()

            if mode == "file":
                file_path = self.file_path_var.get().strip()
                if not file_path:
                    raise ValueError("请选择要检测的文件")

                result = format_detector.detect_file(file_path)
                output = self.format_detection_result(result, verbose)

            elif mode == "directory":
                dir_path = self.dir_path_var.get().strip()
                if not dir_path:
                    raise ValueError("请选择要检测的目录")

                results = format_detector.batch_detect(dir_path)
                output = "批量格式检测结果:\n\n"
                for filename, result in results.items():
                    output += f"文件: {filename}\n"
                    if 'error' in result:
                        output += f"  错误: {result['error']}\n"
                    else:
                        output += f"  最可能格式: {result.get('most_likely_format', 'unknown').upper()}\n"
                        for fmt, detection in result['detections'].items():
                            status = "✓ 有效" if detection.get('is_valid', False) else "✗ 无效"
                            confidence = detection.get('confidence', 0)
                            output += f"  {fmt.upper():6} : {status} (置信度: {confidence:.2f})\n"
                    output += "\n"

            elif mode == "content":
                content = self.content_text.get(1.0, tk.END).strip()
                if not content:
                    raise ValueError("请输入要检测的内容")

                filename = self.content_filename_var.get().strip()
                filename = filename if filename else None

                result = format_detector.detect_content(content, filename)
                output = self.format_detection_result(result, verbose)

            self.display_result(output)

        except Exception as e:
            self.display_error(str(e))

    def format_detection_result(self, result, verbose=False):
        """自定义格式化检测结果函数"""
        if 'error' in result:
            return f"错误: {result['error']}"

        output = f"文件: {result.get('filename', 'N/A')}\n"
        output += f"内容预览: {result.get('content_preview', 'N/A')}\n\n"
        output += "检测结果:\n"

        for format_name, detection in result['detections'].items():
            status = "✓ 有效" if detection.get('is_valid', False) else "✗ 无效"
            confidence = detection.get('confidence', 0)
            output += f"  {format_name.upper():6} : {status} (置信度: {confidence:.2f})\n"

            if verbose and detection.get('is_valid', False):
                details = detection.get('details', '')
                if details:
                    output += f"          详情: {details}\n"

            if verbose and detection.get('error'):
                output += f"          错误: {detection['error']}\n"

        output += f"\n最可能格式: {result.get('most_likely_format', 'unknown').upper()}\n"

        return output


if __name__ == "__main__":
    app = DevKitZeroGUI()
    app.run()

"""
GUI主应用程序

这个模块实现Tkinter图形界面。
"""

# TODO: 实现GUI界面

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import os

# 使用相对导入
from ..tools import random_gen


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
            # ("代码格式化", "formatter"),
            ("随机数据生成", "random_gen"),
            # ("文本差异对比", "diff_tool"),
            # ("数据格式转换", "converter"),
            # ("代码静态检查", "linter")
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

        # if tool == "formatter":
        #     self.setup_formatter_ui()
        # elif tool == "random_gen":
        #     self.setup_random_gen_ui()
        # elif tool == "diff_tool":
        #     self.setup_diff_tool_ui()
        # elif tool == "converter":
        #     self.setup_converter_ui()
        # elif tool == "linter":
        #     self.setup_linter_ui()

        if tool == "random_gen":
            self.setup_random_gen_ui()

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

    def display_result(self, result: str):
        """显示结果"""
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(1.0, result)

    def display_error(self, error: str):
        """显示错误"""
        messagebox.showerror("错误", error)

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

    def run(self):
        """运行 GUI 应用程序"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    app = DevKitZeroGUI()
    app.run()
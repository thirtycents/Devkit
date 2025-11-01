import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import sys
from pathlib import Path

# 处理导入：支持相对导入和独立运行
try:
    from ..tools import formatter
except ImportError:
    # 如果相对导入失败,尝试绝对导入
    from devkit_zero.tools import formatter


class DevKitZeroGUI:
    """DevKit-Zero GUI 主类（仅保留主框架）"""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("DevKit-Zero - 零依赖开发者工具箱")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        self.setup_ui()

    def setup_ui(self):
        """设置用户界面主框架"""
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 配置权重以支持缩放
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
            ("工具 2", "tool2"),
            ("工具 3", "tool3"),
            ("工具 4", "tool4"),
            ("工具 5", "tool5")
        ]

        for i, (name, value) in enumerate(tools):
            ttk.Radiobutton(
                tool_frame, text=name, variable=self.tool_var,
                value=value, command=self.on_tool_change
            ).grid(row=0, column=i, padx=5)

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

        # 保存控制面板容器引用
        self.control_container = control_frame

        # 初始化（清空）
        self.on_tool_change()

    def on_tool_change(self):
        """工具切换时清空控制面板"""
        for widget in self.control_container.winfo_children():
            widget.destroy()
        
        tool = self.tool_var.get()
        if tool == "formatter":
            self.setup_formatter_ui()
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
    
    def select_format_file(self):
        """选择要格式化的文件"""
        filename = filedialog.askopenfilename(
            title="选择代码文件",
            filetypes=[("Python files", "*.py"), ("JavaScript files", "*.js"), ("All files", "*.*")]
        )
        if filename:
            self.format_file_var.set(filename)
    
    def run_formatter(self):
        """执行格式化"""
        try:
            input_type = self.format_input_type.get()
            language = self.format_lang_var.get()
            
            if input_type == "text":
                # 格式化直接输入的代码
                code = self.format_code_text.get("1.0", tk.END)
                if not code.strip():
                    messagebox.showwarning("提示", "请输入要格式化的代码")
                    return
                
                formatted_code = formatter.format_code(code, language)
                self.result_text.delete("1.0", tk.END)
                self.result_text.insert(tk.END, formatted_code)
                
            else:
                # 格式化文件
                file_path = self.format_file_var.get()
                if not file_path:
                    messagebox.showwarning("提示", "请选择要格式化的文件")
                    return
                
                formatted_code = formatter.format_file(file_path, language)
                self.result_text.delete("1.0", tk.END)
                self.result_text.insert(tk.END, formatted_code)
                
        except Exception as e:
            messagebox.showerror("错误", f"格式化失败：{str(e)}")
    def run(self):
        """启动 GUI"""
        self.root.mainloop()


if __name__ == "__main__":
    app = DevKitZeroGUI()
    app.run()
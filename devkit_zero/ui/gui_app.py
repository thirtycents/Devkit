import tkinter as tk
from tkinter import ttk, scrolledtext


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

        self.tool_var = tk.StringVar(value="tool1")
        tools = [
            ("工具 1", "tool1"),
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
        # 此处不再加载具体工具 UI，仅保留占位提示（可选）
        ttk.Label(self.control_container, text="请选择工具以显示选项").grid(padx=10, pady=20)
        """
        if tool == "formatter":-> 自己的 UI 组件    
            self.setup_formatter_ui()
        elif tool == "random_gen":
            self.setup_random_gen_ui()
        elif tool == "diff_tool":
            self.setup_diff_tool_ui()
        elif tool == "converter":
            self.setup_converter_ui()
        elif tool == "linter":
            self.setup_linter_ui()
        def setup_formatter_ui(self):  -> 自己的 UI 组件
        ..... 
        """

    def run(self):
        """启动 GUI"""
        self.root.mainloop()


if __name__ == "__main__":
    app = DevKitZeroGUI()
    app.run()
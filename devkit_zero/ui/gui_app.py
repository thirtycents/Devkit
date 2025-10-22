import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import re
from typing import Dict, Any


class RegexTester:
    """Regular expression testing tool"""

    def __init__(self):
        self.match_history = []

    def test_pattern(self, pattern: str, text: str, flags: int = 0) -> Dict[str, Any]:
        """
        Test regular expression pattern
        Args:
            pattern: Regular expression pattern
            text: Text to match against
            flags: Regular expression flags
        Returns:
            Dictionary containing match results
        """
        try:
            # Compile regular expression
            regex = re.compile(pattern, flags)

            # Find all matches
            matches = list(regex.finditer(text))

            # Extract match information
            match_info = []
            for match in matches:
                match_info.append({
                    'start': match.start(),
                    'end': match.end(),
                    'group': match.group(),
                    'groups': match.groups()
                })

            # Test replacement functionality
            replaced_text = regex.sub(r'[MATCH]', text)

            result = {
                'success': True,
                'matches': match_info,
                'match_count': len(matches),
                'replaced_text': replaced_text,
                'pattern_valid': True
            }

        except re.error as e:
            result = {
                'success': False,
                'error': str(e),
                'matches': [],
                'match_count': 0,
                'replaced_text': text,
                'pattern_valid': False
            }

        # Save to history
        self.match_history.append({
            'pattern': pattern,
            'text': text,
            'result': result
        })

        return result

    def get_common_patterns(self) -> Dict[str, str]:
        """Get common regular expression patterns"""
        return {
            # Email and Contact
            'Email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'Email (Simple)': r'\S+@\S+\.\S+',
            # URLs and Web
            'URL': r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+',
            'URL with Path': r'https?://[^\s/$.?#].[^\s]*',
            'Domain Name': r'\b([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}\b',
            # Phone Numbers
            'Phone (US)': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            'Phone (International)': r'\+\d{1,3}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}',
            'Phone (with Extension)': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\s*(?:ext\.?|x)\s*\d{1,5}',
            # Network
            'IP Address': r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b',
            'IP Address (with Port)': r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}:\d{1,5}\b',
            'MAC Address': r'([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})',
            'IPv6 Address': r'(?:[A-F0-9]{1,4}:){7}[A-F0-9]{1,4}',
            # Dates and Times
            'Date (YYYY-MM-DD)': r'\b\d{4}-\d{2}-\d{2}\b',
            'Date (MM/DD/YYYY)': r'\b(0[1-9]|1[0-2])/(0[1-9]|[12][0-9]|3[01])/\d{4}\b',
            'Date (DD/MM/YYYY)': r'\b(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}\b',
            'Time (24-hour)': r'\b(?:[01]?[0-9]|2[0-3]):[0-5][0-9](?::[0-5][0-9])?\b',
            'Time (12-hour)': r'\b(1[0-2]|0?[1-9]):[0-5][0-9]\s?(?:AM|PM)\b',
            'Timestamp': r'\d{4}-\d{2}-\d{2}[T\s]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})?',
            # Chinese Specific (if needed)
            'Chinese Characters': r'[\u4e00-\u9fff]+',
            'Chinese Mobile': r'\b1[3-9]\d{9}\b',
            'Chinese ID Card': r'\b[1-9]\d{5}(18|19|20)\d{2}((0[1-9])|(1[0-2]))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]\b',
        }

    def clear_history(self):
        """Clear match history"""
        self.match_history.clear()


class DevKitZeroGUI:
    """DevKit-Zero GUI 主类"""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("DevKit-Zero - 零依赖开发者工具箱")
        self.root.geometry("900x700")
        self.root.resizable(True, True)

        # 创建正则表达式测试器实例
        self.regex_tester = RegexTester()

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

        self.tool_var = tk.StringVar(value="regex_tester")
        tools = [
            ("正则表达式测试器", "regex_tester"),
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
        control_frame.rowconfigure(0, weight=1)

        # 右侧结果面板
        result_frame = ttk.LabelFrame(main_frame, text="结果输出", padding="10")
        result_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)

        # 保存面板引用
        self.control_container = control_frame
        self.result_container = result_frame

        # 初始化显示正则表达式测试器
        self.on_tool_change()

    def on_tool_change(self):
        """工具切换时更新控制面板和结果面板"""
        # 清空控制面板
        for widget in self.control_container.winfo_children():
            widget.destroy()

        # 清空结果面板
        for widget in self.result_container.winfo_children():
            widget.destroy()

        # 根据选择的工具加载对应的UI
        tool = self.tool_var.get()
        if tool == "regex_tester":
            self.setup_regex_tester_ui()
        else:
            # 其他工具的占位提示
            ttk.Label(self.control_container, text=f"工具 {tool} 的选项将在这里显示").grid(padx=10, pady=20)
            ttk.Label(self.result_container, text=f"工具 {tool} 的结果将在这里显示").grid(padx=10, pady=20)

    def setup_regex_tester_ui(self):
        """设置正则表达式测试器的UI组件"""
        # 控制面板 - 正则表达式相关控件
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

        # 正则表达式标志
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
            text="测试正则表达式",
            command=self.test_regex
        )
        self.test_button.pack(side=tk.LEFT, padx=(0, 10))

        self.clear_button = ttk.Button(
            button_frame,
            text="清空所有",
            command=self.clear_all
        )
        self.clear_button.pack(side=tk.LEFT, padx=(0, 10))

        self.copy_result_button = ttk.Button(
            button_frame,
            text="复制结果",
            command=self.copy_results
        )
        self.copy_result_button.pack(side=tk.LEFT)

        # 配置权重，使控件可以随窗口缩放
        control_frame.columnconfigure(1, weight=1)
        control_frame.rowconfigure(3, weight=1)

        # 设置快捷键
        self.text_area.bind('<Control-Return>', lambda e: self.test_regex())
        self.pattern_entry.bind('<Control-Return>', lambda e: self.test_regex())

        # 结果面板 - 正则表达式测试结果
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
        """当选择常用模式时的回调"""
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

        # 测试正则表达式
        result = self.regex_tester.test_pattern(pattern, text, flags)

        # 显示结果
        self.display_results(result)

    def display_results(self, result):
        """显示匹配结果"""
        # 更新统计信息
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

        # 显示匹配详情
        self.matches_text.config(state=tk.NORMAL)
        self.matches_text.delete(1.0, tk.END)

        if result['success']:
            if result['matches']:
                for i, match in enumerate(result['matches']):
                    self.matches_text.insert(tk.END,
                        f"匹配 {i+1}:\n"
                        f"  位置: {match['start']}-{match['end']}\n"
                        f"  内容: '{match['group']}'\n"
                    )
                    if match['groups']:
                        groups_str = ', '.join(f"'{g}'" if g else 'None' for g in match['groups'])
                        self.matches_text.insert(tk.END, f"  分组: [{groups_str}]\n")
                    self.matches_text.insert(tk.END, "-" * 50 + "\n")
            else:
                self.matches_text.insert(tk.END, "没有找到匹配项\n")
        else:
            self.matches_text.insert(tk.END, f"正则表达式错误: {result['error']}\n")

        self.matches_text.config(state=tk.DISABLED)

        # 显示替换结果
        self.replace_text.config(state=tk.NORMAL)
        self.replace_text.delete(1.0, tk.END)
        self.replace_text.insert(tk.END, result['replaced_text'])
        self.replace_text.config(state=tk.DISABLED)

    def clear_all(self):
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

        self.regex_tester.clear_history()

    def copy_results(self):
        """复制结果到剪贴板"""
        try:
            results = self.matches_text.get(1.0, tk.END)
            if results.strip():
                self.root.clipboard_clear()
                self.root.clipboard_append(results)
                messagebox.showinfo("成功", "结果已复制到剪贴板")
            else:
                messagebox.showwarning("警告", "没有可复制的内容")
        except Exception as e:
            messagebox.showerror("错误", f"复制失败: {e}")

    def run(self):
        """启动 GUI"""
        self.root.mainloop()


if __name__ == "__main__":
    app = DevKitZeroGUI()
    app.run()
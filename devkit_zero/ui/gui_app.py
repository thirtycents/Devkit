"""DevKit-Zero GUI Main Class"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import re
from devkit_zero.tools.regex_tester import RegexTester
from devkit_zero.tools.Robot_checker import core_logic as robots_core_logic  # 新增


class DevKitZeroGUI:
    """DevKit-Zero GUI Main Class"""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("DevKit-Zero - Zero-dependency Developer Toolkit")
        self.root.geometry("900x700")
        self.root.resizable(True, True)

        # Create tool instances
        self.regex_tester = RegexTester()

        self.setup_ui()

    def setup_ui(self):
        """Set up main UI framework"""
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure weights for scaling
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # Tool selection area
        tool_frame = ttk.LabelFrame(main_frame, text="Tool Selection", padding="10")
        tool_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        self.tool_var = tk.StringVar(value="regex_tester")
        # 更新工具列表，包含Regex Tester和Robots Checker
        tools = [
            ("Regex Tester", "regex_tester"),
            ("Robots Checker", "robots_checker")  # 新增工具
        ]

        for i, (name, value) in enumerate(tools):
            ttk.Radiobutton(
                tool_frame, text=name, variable=self.tool_var,
                value=value, command=self.on_tool_change
            ).grid(row=0, column=i, padx=5)

        # Left control panel
        control_frame = ttk.LabelFrame(main_frame, text="Control Panel", padding="10")
        control_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        control_frame.columnconfigure(0, weight=1)
        control_frame.rowconfigure(0, weight=1)

        # Right result panel
        result_frame = ttk.LabelFrame(main_frame, text="Result Output", padding="10")
        result_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)

        # Save panel references
        self.control_container = control_frame
        self.result_container = result_frame

        # Initialize with regex tester
        self.on_tool_change()

    def on_tool_change(self):
        """Update control panel and result panel when tool changes"""
        # Clear control panel
        for widget in self.control_container.winfo_children():
            widget.destroy()

        # Clear result panel
        for widget in self.result_container.winfo_children():
            widget.destroy()

        # Load corresponding UI based on selected tool
        tool = self.tool_var.get()
        if tool == "regex_tester":
            self.setup_regex_tester_ui()
        elif tool == "robots_checker":  # 新增工具UI设置
            self.setup_robots_checker_ui()
        else:
            # Placeholder for other tools
            ttk.Label(self.control_container, text=f"Options for {tool} will be displayed here").grid(padx=10, pady=20)
            ttk.Label(self.result_container, text=f"Results for {tool} will be displayed here").grid(padx=10, pady=20)

    def setup_regex_tester_ui(self):
        """Set up UI components for regex tester"""
        # Control panel - regex related widgets
        control_frame = ttk.Frame(self.control_container)
        control_frame.pack(fill=tk.BOTH, expand=True)

        # Common patterns selection
        ttk.Label(control_frame, text="Common Patterns:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.pattern_var = tk.StringVar()
        self.common_patterns_combo = ttk.Combobox(
            control_frame,
            textvariable=self.pattern_var,
            values=list(self.regex_tester.get_common_patterns().keys()),
            state="readonly",
            width=30
        )
        self.common_patterns_combo.set("Select common pattern...")
        self.common_patterns_combo.grid(row=0, column=1, sticky=tk.EW, pady=5, padx=(5, 0))
        self.common_patterns_combo.bind('<<ComboboxSelected>>', self.on_pattern_selected)

        # Custom pattern input
        ttk.Label(control_frame, text="Custom Pattern:").grid(row=1, column=0, sticky=tk.NW, pady=5)
        self.pattern_entry = scrolledtext.ScrolledText(control_frame, width=40, height=3)
        self.pattern_entry.grid(row=1, column=1, sticky=tk.EW, pady=5, padx=(5, 0))

        # Options frame
        options_frame = ttk.LabelFrame(control_frame, text="Options", padding=5)
        options_frame.grid(row=2, column=1, sticky=tk.EW, pady=5, padx=(5, 0))

        # Regex flags
        self.ignore_case_var = tk.BooleanVar()
        ttk.Checkbutton(
            options_frame,
            text="Ignore case (re.IGNORECASE)",
            variable=self.ignore_case_var
        ).pack(anchor=tk.W)

        self.multiline_var = tk.BooleanVar()
        ttk.Checkbutton(
            options_frame,
            text="Multiline mode (re.MULTILINE)",
            variable=self.multiline_var
        ).pack(anchor=tk.W)

        self.dotall_var = tk.BooleanVar()
        ttk.Checkbutton(
            options_frame,
            text="Dot matches newlines (re.DOTALL)",
            variable=self.dotall_var
        ).pack(anchor=tk.W)

        # Test text area
        ttk.Label(control_frame, text="Test Text:").grid(row=3, column=0, sticky=tk.NW, pady=5)
        self.text_area = scrolledtext.ScrolledText(control_frame, width=40, height=10)
        self.text_area.grid(row=3, column=1, sticky=tk.NSEW, pady=5, padx=(5, 0))

        # Buttons area
        button_frame = ttk.Frame(control_frame)
        button_frame.grid(row=4, column=0, columnspan=2, sticky=tk.EW, pady=10)

        self.test_button = ttk.Button(
            button_frame,
            text="Test Regex",
            command=self.test_regex
        )
        self.test_button.pack(side=tk.LEFT, padx=(0, 10))

        self.clear_button = ttk.Button(
            button_frame,
            text="Clear All",
            command=self.clear_all
        )
        self.clear_button.pack(side=tk.LEFT, padx=(0, 10))

        self.copy_result_button = ttk.Button(
            button_frame,
            text="Copy Results",
            command=self.copy_results
        )
        self.copy_result_button.pack(side=tk.LEFT)

        # Configure weights for scaling
        control_frame.columnconfigure(1, weight=1)
        control_frame.rowconfigure(3, weight=1)

        # Set up shortcuts
        self.text_area.bind('<Control-Return>', lambda e: self.test_regex())
        self.pattern_entry.bind('<Control-Return>', lambda e: self.test_regex())

        # Result panel - regex test results
        result_frame = ttk.Frame(self.result_container)
        result_frame.pack(fill=tk.BOTH, expand=True)

        # Match statistics
        stats_frame = ttk.Frame(result_frame)
        stats_frame.pack(fill=tk.X, pady=(0, 10))
        self.stats_label = ttk.Label(stats_frame, text="Match Results: 0 matches", font=('Arial', 10, 'bold'))
        self.stats_label.pack(side=tk.LEFT)
        self.pattern_status_label = ttk.Label(stats_frame, text="Pattern Status: Not tested", foreground="gray")
        self.pattern_status_label.pack(side=tk.RIGHT)

        # Match details
        ttk.Label(result_frame, text="Match Details:").pack(anchor=tk.W, pady=(0, 5))
        self.matches_text = scrolledtext.ScrolledText(
            result_frame,
            width=60,
            height=8,
            state=tk.DISABLED
        )
        self.matches_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Replacement result display
        replace_frame = ttk.LabelFrame(result_frame, text="Replacement Result", padding=5)
        replace_frame.pack(fill=tk.X)
        self.replace_text = scrolledtext.ScrolledText(
            replace_frame,
            width=60,
            height=4,
            state=tk.DISABLED
        )
        self.replace_text.pack(fill=tk.BOTH, expand=True)

    def on_pattern_selected(self, event):
        """Callback when a common pattern is selected"""
        pattern_name = self.pattern_var.get()
        common_patterns = self.regex_tester.get_common_patterns()

        if pattern_name in common_patterns:
            self.pattern_entry.delete(1.0, tk.END)
            self.pattern_entry.insert(1.0, common_patterns[pattern_name])

    def test_regex(self):
        """Test regular expression"""
        pattern = self.pattern_entry.get(1.0, tk.END).strip()
        text = self.text_area.get(1.0, tk.END)

        if not pattern:
            messagebox.showerror("Error", "Please enter a regex pattern")
            return

        if not text.strip():
            messagebox.showwarning("Warning", "Please enter test text")
            return

        # Calculate flags
        flags = 0
        if self.ignore_case_var.get():
            flags |= re.IGNORECASE
        if self.multiline_var.get():
            flags |= re.MULTILINE
        if self.dotall_var.get():
            flags |= re.DOTALL

        # Test regex
        result = self.regex_tester.test_pattern(pattern, text, flags)

        # Display results
        self.display_results(result)

    def display_results(self, result):
        """Display match results"""
        # Update statistics
        if result['success']:
            self.stats_label.config(
                text=f"Match Results: {result['match_count']} matches",
                foreground="green"
            )
            self.pattern_status_label.config(
                text="Pattern Status: Valid",
                foreground="green"
            )
        else:
            self.stats_label.config(
                text=f"Error: {result['error']}",
                foreground="red"
            )
            self.pattern_status_label.config(
                text="Pattern Status: Invalid",
                foreground="red"
            )

        # Update match details
        self.matches_text.config(state=tk.NORMAL)
        self.matches_text.delete(1.0, tk.END)

        if result['success'] and result['match_count'] > 0:
            for i, match in enumerate(result['matches'], 1):
                self.matches_text.insert(tk.END, f"Match {i}:\n")
                self.matches_text.insert(tk.END, f"  Position: {match['start']}-{match['end']}\n")
                self.matches_text.insert(tk.END, f"  Value: {match['group']}\n")

                if match['groups']:
                    self.matches_text.insert(tk.END, "  Groups:\n")
                    for j, group in enumerate(match['groups'], 1):
                        self.matches_text.insert(tk.END, f"    Group {j}: {group}\n")
                self.matches_text.insert(tk.END, "\n")
        elif result['success']:
            self.matches_text.insert(tk.END, "No matches found.")
        else:
            self.matches_text.insert(tk.END, f"Pattern error: {result['error']}")

        self.matches_text.config(state=tk.DISABLED)

        # Update replacement text
        self.replace_text.config(state=tk.NORMAL)
        self.replace_text.delete(1.0, tk.END)
        self.replace_text.insert(tk.END, result['replaced_text'])
        self.replace_text.config(state=tk.DISABLED)

    def clear_all(self):
        """Clear all input fields and results"""
        self.pattern_entry.delete(1.0, tk.END)
        self.text_area.delete(1.0, tk.END)
        self.matches_text.config(state=tk.NORMAL)
        self.matches_text.delete(1.0, tk.END)
        self.matches_text.config(state=tk.DISABLED)
        self.replace_text.config(state=tk.NORMAL)
        self.replace_text.delete(1.0, tk.END)
        self.replace_text.config(state=tk.DISABLED)
        self.stats_label.config(text="Match Results: 0 matches", foreground="black")
        self.pattern_status_label.config(text="Pattern Status: Not tested", foreground="gray")
        self.common_patterns_combo.set("Select common pattern...")
        self.ignore_case_var.set(False)
        self.multiline_var.set(False)
        self.dotall_var.set(False)

    def copy_results(self):
        """Copy regex test results to clipboard"""
        self.root.clipboard_clear()
        results = self.matches_text.get(1.0, tk.END).strip()
        self.root.clipboard_append(results)
        messagebox.showinfo("Copied", "Results copied to clipboard")

    def setup_robots_checker_ui(self):
        """Set up UI components for robots checker"""
        # Control panel - robots checker related widgets
        control_frame = ttk.Frame(self.control_container)
        control_frame.pack(fill=tk.BOTH, expand=True)

        # URL input
        ttk.Label(control_frame, text="Website URL:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.robots_url_entry = ttk.Entry(control_frame, width=40)
        self.robots_url_entry.grid(row=0, column=1, sticky=tk.EW, pady=5, padx=(5, 0))
        self.robots_url_entry.insert(0, "https://")  # 默认前缀

        # Options frame
        options_frame = ttk.LabelFrame(control_frame, text="Options", padding=5)
        options_frame.grid(row=1, column=0, columnspan=2, sticky=tk.EW, pady=5)

        # Timeout setting
        ttk.Label(options_frame, text="Timeout (seconds):").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.robots_timeout_var = tk.StringVar(value="10")
        ttk.Entry(options_frame, textvariable=self.robots_timeout_var, width=10).grid(row=0, column=1, sticky=tk.W,
                                                                                      padx=5)

        # Raw output option
        self.robots_raw_var = tk.BooleanVar()
        ttk.Checkbutton(
            options_frame,
            text="Show raw robots.txt content",
            variable=self.robots_raw_var
        ).grid(row=0, column=2, sticky=tk.W, padx=10)

        # Buttons area
        button_frame = ttk.Frame(control_frame)
        button_frame.grid(row=2, column=0, columnspan=2, sticky=tk.EW, pady=10)

        self.check_robots_button = ttk.Button(
            button_frame,
            text="Check Robots Rules",
            command=self.check_robots
        )
        self.check_robots_button.pack(side=tk.LEFT, padx=(0, 10))

        self.copy_robots_button = ttk.Button(
            button_frame,
            text="Copy Results",
            command=self.copy_robots_results
        )
        self.copy_robots_button.pack(side=tk.LEFT)

        # Configure weights for scaling
        control_frame.columnconfigure(1, weight=1)
        options_frame.columnconfigure(2, weight=1)

        # Set up shortcut: Ctrl+Enter to check
        self.robots_url_entry.bind('<Control-Return>', lambda e: self.check_robots())

        # Result panel - robots checker results
        result_frame = ttk.Frame(self.result_container)
        result_frame.pack(fill=tk.BOTH, expand=True)

        # Status bar
        self.robots_status_label = ttk.Label(result_frame, text="Status: Ready", font=('Arial', 10, 'bold'))
        self.robots_status_label.pack(anchor=tk.W, pady=(0, 5))

        # Robots URL display
        self.robots_url_label = ttk.Label(result_frame, text="", foreground="blue")
        self.robots_url_label.pack(anchor=tk.W, pady=(0, 10))

        # Result notebook (tabs)
        notebook = ttk.Notebook(result_frame)
        notebook.pack(fill=tk.BOTH, expand=True)

        # Parsed rules tab
        self.robots_parsed_text = scrolledtext.ScrolledText(
            notebook,
            width=60,
            height=15,
            state=tk.DISABLED
        )
        notebook.add(self.robots_parsed_text, text="Parsed Rules")

        # Raw content tab
        self.robots_raw_text = scrolledtext.ScrolledText(
            notebook,
            width=60,
            height=15,
            state=tk.DISABLED
        )
        notebook.add(self.robots_raw_text, text="Raw Content")

    def check_robots(self):
        """Check robots.txt for the given URL"""
        url = self.robots_url_entry.get().strip()

        if not url:
            messagebox.showerror("Error", "Please enter a website URL")
            return

        try:
            # Get timeout value
            timeout = int(self.robots_timeout_var.get())

            # Update status
            self.robots_status_label.config(text="Status: Checking...", foreground="orange")
            self.root.update()  # Force UI update

            # Call core logic
            result = robots_core_logic(url, timeout=timeout)

            # Update status
            self.robots_status_label.config(
                text=f"Status: {result['message']}",
                foreground="green" if result['success'] else "red"
            )
            self.robots_url_label.config(text=result['url'])

            # Display raw content
            self.robots_raw_text.config(state=tk.NORMAL)
            self.robots_raw_text.delete(1.0, tk.END)
            self.robots_raw_text.insert(1.0, result['content'] or "No content available")
            self.robots_raw_text.config(state=tk.DISABLED)

            # Display parsed rules if successful
            self.robots_parsed_text.config(state=tk.NORMAL)
            self.robots_parsed_text.delete(1.0, tk.END)

            if result['success'] and result['rules']:
                rules = result['rules']

                if rules['host']:
                    self.robots_parsed_text.insert(tk.END, f"Host: {rules['host']}\n\n")

                if rules['crawl_delay']:
                    self.robots_parsed_text.insert(tk.END, f"Crawl Delay: {rules['crawl_delay']} seconds\n\n")

                if rules['sitemaps']:
                    self.robots_parsed_text.insert(tk.END, "Sitemaps:\n")
                    for sitemap in rules['sitemaps']:
                        self.robots_parsed_text.insert(tk.END, f"- {sitemap}\n")
                    self.robots_parsed_text.insert(tk.END, "\n")

                self.robots_parsed_text.insert(tk.END, "User Agent Rules:\n")
                for agent, agent_rules in rules['user_agents'].items():
                    self.robots_parsed_text.insert(tk.END, f"\nUser-agent: {agent}\n")

                    if agent_rules['allow']:
                        self.robots_parsed_text.insert(tk.END, "  Allow:\n")
                        for path in agent_rules['allow']:
                            self.robots_parsed_text.insert(tk.END, f"    - {path}\n")

                    if agent_rules['disallow']:
                        self.robots_parsed_text.insert(tk.END, "  Disallow:\n")
                        for path in agent_rules['disallow']:
                            self.robots_parsed_text.insert(tk.END, f"    - {path}\n")
            else:
                self.robots_parsed_text.insert(tk.END, "No valid robots rules found or unable to parse content.")

            self.robots_parsed_text.config(state=tk.DISABLED)

        except ValueError as e:
            self.robots_status_label.config(text=f"Status: Error - {str(e)}", foreground="red")
            messagebox.showerror("Error", str(e))
        except Exception as e:
            self.robots_status_label.config(text=f"Status: Error - {str(e)}", foreground="red")
            messagebox.showerror("Error", f"Failed to check robots rules: {str(e)}")

    def copy_robots_results(self):
        """Copy robots check results to clipboard"""
        self.root.clipboard_clear()
        parsed_content = self.robots_parsed_text.get(1.0, tk.END).strip()
        self.root.clipboard_append(parsed_content)
        messagebox.showinfo("Copied", "Results copied to clipboard")

    def run(self):
        """Run the GUI application"""
        self.root.mainloop()


if __name__ == "__main__":
    app = DevKitZeroGUI()
    app.run()
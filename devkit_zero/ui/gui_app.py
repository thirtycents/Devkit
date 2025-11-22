"""
GUI Application (using tkinter)
DevKit-Zero Graphical Interface
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import sys
import os
import re
from pathlib import Path

# Handle relative import and direct execution compatibility
try:
    # Try relative import (when running as a module)
    from ..tools import formatter, random_gen, diff_tool, converter, linter, unused_func_detector, api_contract_diff, \
        port_checker, regex_tester
    from ..tools.Robot_checker import core_logic as robots_core_logic
except ImportError:
    # If relative import fails, add parent directory to path (when running directly)
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
    from devkit_zero.tools import formatter, random_gen, diff_tool, converter, linter, unused_func_detector, \
        api_contract_diff, port_checker, regex_tester
    from devkit_zero.tools.Robot_checker import core_logic as robots_core_logic


# Dynamically import file tool classes, handling different directory structures
def import_file_tools():
    """Dynamically import file tool modules"""
    # Possible module paths
    possible_paths = [
        # Import from parent directory's tools folder
        os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'tools')),
        # Import from parent directory of current directory
        os.path.abspath(os.path.join(os.path.dirname(__file__), '..')),
        # Import from current directory
        os.path.dirname(__file__),
    ]

    for path in possible_paths:
        if path not in sys.path:
            sys.path.insert(0, path)

    # Try different import methods
    
        # Method 1: Import directly from tools module
    from tools.batch_process import BatchFileProcessor
    from tools.FormatDetector import FormatDetector
    return BatchFileProcessor, FormatDetector
    # except ImportError:
    #     try:
    #         # Method 2: Import from tools subfolder in current directory
    #         sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tools'))
    #         from batch_process import BatchFileProcessor
    #         from FormatDetector import FormatDetector
    #         return BatchFileProcessor, FormatDetector
    #     except ImportError:
    #         try:
    #             # Method 3: Import directly
    #             from batch_process import BatchFileProcessor
    #             from FormatDetector import FormatDetector
    #             return BatchFileProcessor, FormatDetector
    #         except ImportError as e:
    #             print(f"File tools import failed: {e}")
    #             return None, None


class PlaceholderEntry(ttk.Entry):
    """Entry widget with placeholder text support"""

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
        """Get actual value (if not placeholder)"""
        value = self.get()
        if value == self.placeholder:
            return ""
        return value


class DevKitZeroGUI:
    """DevKit-Zero GUI Main Class"""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("DevKit-Zero - Zero Dependency Developer Toolkit")
        self.root.geometry("1100x650")
        self.root.resizable(True, True)

        # Create tool instances
        self.regex_tester = regex_tester.RegexTester()

        # Import file tools
        self.BatchFileProcessor, self.FormatDetector = import_file_tools()

        # Set icon (if exists)
        try:
            icon_path = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'app.ico')
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except:
            pass

        self.setup_ui()

    def setup_ui(self):
        """Setup user interface"""
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        # Configure weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # Tool selection area
        tool_frame = ttk.LabelFrame(main_frame, text="Tool Selection", padding="10")
        tool_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        self.tool_var = tk.StringVar(value="formatter")
        tools = [
            ("Code Formatter", "formatter"),
            ("Random Generator", "random_gen"),
            ("Text Diff", "diff_tool"),
            ("Format Converter", "converter"),
            ("Code Linter", "linter"),
            ("Unused Function", "unused_func"),
            ("Port Checker", "port_checker"),
            ("API Contract Diff", "api_diff"),
            ("Regex Tester", "regex_tester"),
            ("Robots Checker", "robots_checker"),
            ("Batch Processor", "batch_processor"),
            ("Format Detector", "format_detector")
        ]

        # Create two rows of tool selection buttons
        for i, (name, value) in enumerate(tools):
            row = 0 if i < 8 else 1  # First 8 in the first row, others in the second row
            col = i if i < 8 else i - 8
            ttk.Radiobutton(tool_frame, text=name, variable=self.tool_var,
                            value=value, command=self.on_tool_change).grid(row=row, column=col, padx=5, pady=2)

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

        # Result text box (for most tools)
        self.result_text = scrolledtext.ScrolledText(result_frame, wrap=tk.WORD, height=20)
        self.result_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Control panel and result panel container
        self.control_container = control_frame
        self.result_container = result_frame

        # Initialize tool panel
        self.on_tool_change()

    def on_tool_change(self):
        """Handle tool selection change"""
        # Clear existing widgets in control panel
        for widget in self.control_container.winfo_children():
            widget.destroy()

        tool = self.tool_var.get()

        # Clear result container and setup result panel based on tool type
        for widget in self.result_container.winfo_children():
            widget.destroy()

        # Recreate result text box for tools using default result text box
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
        elif tool == "batch_processor":  # New
            self.setup_batch_processor_ui()
        elif tool == "format_detector":  # New
            self.setup_format_detector_ui()

    def setup_formatter_ui(self):
        """Setup code formatter tool UI"""
        # Language selection
        ttk.Label(self.control_container, text="Language:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.format_lang_var = tk.StringVar(value="python")
        lang_combo = ttk.Combobox(self.control_container, textvariable=self.format_lang_var,
                                  values=["python", "javascript"], state="readonly")
        lang_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2)

        # Input method selection
        ttk.Label(self.control_container, text="Input Type:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.format_input_type = tk.StringVar(value="text")
        ttk.Radiobutton(self.control_container, text="Direct Input", variable=self.format_input_type,
                        value="text").grid(row=1, column=1, sticky=tk.W, pady=2)
        ttk.Radiobutton(self.control_container, text="Select File", variable=self.format_input_type,
                        value="file").grid(row=2, column=1, sticky=tk.W, pady=2)

        # File selection
        file_frame = ttk.Frame(self.control_container)
        file_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=2)
        file_frame.columnconfigure(0, weight=1)

        self.format_file_var = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.format_file_var).grid(row=0, column=0, sticky=(tk.W, tk.E))
        ttk.Button(file_frame, text="Select", command=self.select_format_file).grid(row=0, column=1, padx=(5, 0))

        # Code input box
        ttk.Label(self.control_container, text="Code Input:").grid(row=4, column=0, sticky=tk.W, pady=(10, 2))
        self.format_code_text = tk.Text(self.control_container, height=10, wrap=tk.WORD)
        self.format_code_text.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=2)

        # Execute button
        ttk.Button(self.control_container, text="Format Code",
                   command=self.run_formatter).grid(row=6, column=0, columnspan=2, pady=(10, 0))

        self.control_container.columnconfigure(1, weight=1)

    def setup_random_gen_ui(self):
        """Setup random data generator tool UI"""
        # Generation type
        ttk.Label(self.control_container, text="Type:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.random_type_var = tk.StringVar(value="uuid")
        type_combo = ttk.Combobox(self.control_container, textvariable=self.random_type_var,
                                  values=["uuid", "string", "password", "number", "color"], state="readonly")
        type_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2)
        type_combo.bind('<<ComboboxSelected>>', self.on_random_type_change)

        # Dynamic parameters frame
        self.random_params_frame = ttk.Frame(self.control_container)
        self.random_params_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        self.random_params_frame.columnconfigure(1, weight=1)

        # Execute button
        ttk.Button(self.control_container, text="Generate",
                   command=self.run_random_gen).grid(row=2, column=0, columnspan=2, pady=(10, 0))

        self.control_container.columnconfigure(1, weight=1)

        # Initialize parameters UI
        self.on_random_type_change()

    def setup_diff_tool_ui(self):
        """Setup text diff tool UI"""
        # Text 1
        ttk.Label(self.control_container, text="Text 1:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.diff_text1 = tk.Text(self.control_container, height=8, wrap=tk.WORD)
        self.diff_text1.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=2)
        # Text 2
        ttk.Label(self.control_container, text="Text 2:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.diff_text2 = tk.Text(self.control_container, height=8, wrap=tk.WORD)
        self.diff_text2.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=2)
        # Comparison format
        ttk.Label(self.control_container, text="Output Format:").grid(row=4, column=0, sticky=tk.W, pady=2)
        self.diff_format_var = tk.StringVar(value="unified")
        format_combo = ttk.Combobox(self.control_container, textvariable=self.diff_format_var,
                                    values=["unified", "side-by-side", "stats"], state="readonly")
        format_combo.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=2)

        # Execute button
        ttk.Button(self.control_container, text="Compare Diff",
                   command=self.run_diff_tool).grid(row=5, column=0, columnspan=2, pady=(10, 0))

        self.control_container.columnconfigure(1, weight=1)

    def setup_converter_ui(self):
        """Setup data format converter tool UI"""
        # Conversion format selection
        ttk.Label(self.control_container, text="From Format:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.convert_from_var = tk.StringVar(value="json")
        from_combo = ttk.Combobox(self.control_container, textvariable=self.convert_from_var,
                                  values=["json", "csv"], state="readonly")
        from_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2)

        ttk.Label(self.control_container, text="To Format:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.convert_to_var = tk.StringVar(value="csv")
        to_combo = ttk.Combobox(self.control_container, textvariable=self.convert_to_var,
                                values=["json", "csv"], state="readonly")
        to_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=2)

        # Input data
        ttk.Label(self.control_container, text="Input Data:").grid(row=2, column=0, sticky=tk.W, pady=(10, 2))
        self.convert_input_text = tk.Text(self.control_container, height=12, wrap=tk.WORD)
        self.convert_input_text.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=2)

        # Execute button
        ttk.Button(self.control_container, text="Convert Format",
                   command=self.run_converter).grid(row=4, column=0, columnspan=2, pady=(10, 0))

        self.control_container.columnconfigure(1, weight=1)

    def setup_linter_ui(self):
        """Setup code linter tool UI"""
        # Input method selection
        ttk.Label(self.control_container, text="Input Type:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.lint_input_type = tk.StringVar(value="text")
        ttk.Radiobutton(self.control_container, text="Direct Input", variable=self.lint_input_type,
                        value="text").grid(row=0, column=1, sticky=tk.W, pady=2)
        ttk.Radiobutton(self.control_container, text="Select File", variable=self.lint_input_type,
                        value="file").grid(row=1, column=1, sticky=tk.W, pady=2)

        # File selection
        file_frame = ttk.Frame(self.control_container)
        file_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=2)
        file_frame.columnconfigure(0, weight=1)

        self.lint_file_var = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.lint_file_var).grid(row=0, column=0, sticky=(tk.W, tk.E))
        ttk.Button(file_frame, text="Select", command=self.select_lint_file).grid(row=0, column=1, padx=(5, 0))

        # Code input box
        ttk.Label(self.control_container, text="Code Input:").grid(row=3, column=0, sticky=tk.W, pady=(10, 2))
        self.lint_code_text = tk.Text(self.control_container, height=12, wrap=tk.WORD)
        self.lint_code_text.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=2)

        # Execute button
        ttk.Button(self.control_container, text="Lint Code",
                   command=self.run_linter).grid(row=5, column=0, columnspan=2, pady=(10, 0))

        self.control_container.columnconfigure(1, weight=1)

    def setup_unused_func_ui(self):
        """Setup unused function detector tool UI"""
        # Project path selection
        ttk.Label(self.control_container, text="Project Path:").grid(row=0, column=0, sticky=tk.W, pady=2)

        path_frame = ttk.Frame(self.control_container)
        path_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=2)
        path_frame.columnconfigure(0, weight=1)

        self.unused_func_path_var = tk.StringVar(value=".")
        ttk.Entry(path_frame, textvariable=self.unused_func_path_var).grid(row=0, column=0, sticky=(tk.W, tk.E))
        ttk.Button(path_frame, text="Select Dir", command=self.select_project_dir).grid(row=0, column=1, padx=(5, 0))

        # Exclude directories
        ttk.Label(self.control_container, text="Exclude Dirs:").grid(row=2, column=0, sticky=tk.W, pady=(10, 2))
        ttk.Label(self.control_container, text="(comma separated)", font=("", 8)).grid(row=2, column=1, sticky=tk.W,
                                                                                pady=(10, 2))

        self.unused_func_exclude_var = tk.StringVar(value="venv,__pycache__,.git,build,dist")
        ttk.Entry(self.control_container, textvariable=self.unused_func_exclude_var).grid(
            row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=2)

        # Output format
        ttk.Label(self.control_container, text="Output Format:").grid(row=4, column=0, sticky=tk.W, pady=(10, 2))
        self.unused_func_format_var = tk.StringVar(value="text")
        format_frame = ttk.Frame(self.control_container)
        format_frame.grid(row=5, column=0, columnspan=2, sticky=tk.W, pady=2)

        ttk.Radiobutton(format_frame, text="Text", variable=self.unused_func_format_var,
                        value="text").grid(row=0, column=0, padx=(0, 10))
        ttk.Radiobutton(format_frame, text="JSON", variable=self.unused_func_format_var,
                        value="json").grid(row=0, column=1, padx=(0, 10))
        ttk.Radiobutton(format_frame, text="HTML", variable=self.unused_func_format_var,
                        value="html").grid(row=0, column=2)

        # Verbose output option
        self.unused_func_verbose_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(self.control_container, text="Show Verbose Info",
                        variable=self.unused_func_verbose_var).grid(row=6, column=0, columnspan=2, sticky=tk.W,
                                                                    pady=(10, 2))

        # Execute button
        ttk.Button(self.control_container, text="Detect Unused Functions",
                   command=self.run_unused_func_detector).grid(row=7, column=0, columnspan=2, pady=(10, 0))

        self.control_container.columnconfigure(1, weight=1)

    def select_project_dir(self):
        """Select project directory"""
        directory = filedialog.askdirectory(
            title="Select Project Directory to Analyze",
            initialdir="."
        )
        if directory:
            self.unused_func_path_var.set(directory)
    def on_random_type_change(self, event=None):
        """Update parameter UI when random data type changes"""
        # Clear existing parameter widgets
        for widget in self.random_params_frame.winfo_children():
            widget.destroy()

        gen_type = self.random_type_var.get()

        if gen_type == "string":
            ttk.Label(self.random_params_frame, text="Length:").grid(row=0, column=0, sticky=tk.W, pady=2)
            self.string_length_var = tk.StringVar(value="8")
            ttk.Entry(self.random_params_frame, textvariable=self.string_length_var, width=10).grid(row=0, column=1,
                                                                                                    sticky=tk.W, pady=2)

            self.string_numbers_var = tk.BooleanVar(value=True)
            self.string_uppercase_var = tk.BooleanVar(value=True)
            self.string_lowercase_var = tk.BooleanVar(value=True)
            self.string_symbols_var = tk.BooleanVar(value=False)
            
            
            ttk.Checkbutton(self.random_params_frame, text="Include Numbers", variable=self.string_numbers_var).grid(row=1,
                                                                                                          column=0,
                                                                                                          sticky=tk.W,
                                                                                                          pady=1)
            ttk.Checkbutton(self.random_params_frame, text="Include Uppercase", variable=self.string_uppercase_var).grid(row=2,
                                                                                                              column=0,
                                                                                                              sticky=tk.W,
                                                                                                              pady=1)
            ttk.Checkbutton(self.random_params_frame, text="Include Lowercase", variable=self.string_lowercase_var).grid(row=3,
                                                                                                              column=0,
                                                                                                              sticky=tk.W,
                                                                                                              pady=1)
            ttk.Checkbutton(self.random_params_frame, text="Include Symbols", variable=self.string_symbols_var).grid(row=4,
                                                                                                            column=0,
                                                                                                            sticky=tk.W,
                                                                                                            pady=1)

        elif gen_type == "password":
            ttk.Label(self.random_params_frame, text="Length:").grid(row=0, column=0, sticky=tk.W, pady=2)
            self.password_length_var = tk.StringVar(value="16")
            ttk.Entry(self.random_params_frame, textvariable=self.password_length_var, width=10).grid(row=0, column=1,
                                                                                                      sticky=tk.W,
                                                                                                      pady=2)

        elif gen_type == "number":
            ttk.Label(self.random_params_frame, text="Min Value:").grid(row=0, column=0, sticky=tk.W, pady=2)
            self.number_min_var = tk.StringVar(value="0")
            ttk.Entry(self.random_params_frame, textvariable=self.number_min_var, width=10).grid(row=0, column=1,
                                                                                                 sticky=tk.W, pady=2)

            ttk.Label(self.random_params_frame, text="Max Value:").grid(row=1, column=0, sticky=tk.W, pady=2)
            self.number_max_var = tk.StringVar(value="100")
            ttk.Entry(self.random_params_frame, textvariable=self.number_max_var, width=10).grid(row=1, column=1,
                                                                                                 sticky=tk.W, pady=2)

            self.number_float_var = tk.BooleanVar(value=False)
            ttk.Checkbutton(self.random_params_frame, text="Float", variable=self.number_float_var).grid(row=2, column=0,
                                                                                                       sticky=tk.W,
                                                                                                       pady=1)
    
    def select_format_file(self):
        """Select file to format"""
        filename = filedialog.askopenfilename(
            title="Select File to Format",
            filetypes=[("Python files", "*.py"), ("JavaScript files", "*.js"), ("All files", "*.*")]
        )
        if filename:
            self.format_file_var.set(filename)
    
    def select_lint_file(self):
        """Select file to check"""
        filename = filedialog.askopenfilename(
            title="Select File to Check",
            filetypes=[("Python files", "*.py"), ("All files", "*.*")]
        )
        if filename:
            self.lint_file_var.set(filename)
    


    def display_result(self, result: str):
        """Show result"""
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(1.0, result)
    
    def display_error(self, error: str):
        """Show error"""
        messagebox.showerror("Error", error)
    
    def run_formatter(self):
        """Run code formatter"""
        try:
            language = self.format_lang_var.get()
            input_type = self.format_input_type.get()
            
            if input_type == "file":
                file_path = self.format_file_var.get().strip()
                if not file_path:
                    raise ValueError("Please select a file to format")
                result = formatter.format_file(file_path, language)
            else:
                code = self.format_code_text.get(1.0, tk.END).strip()
                if not code:
                    raise ValueError("Please enter code to format")
                result = formatter.format_code(code, language)
            
            self.display_result(result)
            
        except Exception as e:
            self.display_error(str(e))
    
    def run_random_gen(self):
        """Run random data generation"""
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
                raise ValueError(f"Unsupported generation type: {gen_type}")
            
            self.display_result(result)
            
        except Exception as e:
            self.display_error(str(e))
    
    def run_diff_tool(self):
        """Run text diff comparison"""
        try:
            text1 = self.diff_text1.get(1.0, tk.END).strip()
            text2 = self.diff_text2.get(1.0, tk.END).strip()
            
            if not text1 or not text2:
                raise ValueError("Please enter two texts to compare")
            
            format_type = self.diff_format_var.get()
            
            if format_type == "unified":
                result = diff_tool.compare_text(text1, text2)
                result_text = result
            elif format_type == "side-by-side":
                result = diff_tool.get_side_by_side_diff(text1, text2)
                result_text = '\n'.join(result)
            elif format_type == "stats":
                stats = diff_tool.analyze_changes(text1, text2)
                result_text = f"""Change Statistics:
Text 1 Lines: {stats['total_lines_1']}
Text 2 Lines: {stats['total_lines_2']}
Added Lines: {stats['additions']}
Deleted Lines: {stats['deletions']}
Modified Lines: {stats['modifications']}
Similarity: {stats['similarity']:.2%}
Total Changes: {stats['total_changes']}"""
            
            self.display_result(result_text)
            
        except Exception as e:
            self.display_error(str(e))
    
    def run_converter(self):
        """Run data format conversion"""
        try:
            from_format = self.convert_from_var.get()
            to_format = self.convert_to_var.get()
            input_data = self.convert_input_text.get(1.0, tk.END).strip()
            
            if not input_data:
                raise ValueError("Please enter data to convert")
            
            if from_format == "json" and to_format == "csv":
                result = converter.json_to_csv(input_data)
            elif from_format == "csv" and to_format == "json":
                result = converter.csv_to_json(input_data)
            else:
                raise ValueError(f"Conversion from {from_format} to {to_format} is not supported")
            
            self.display_result(result)
            
        except Exception as e:
            self.display_error(str(e))
    
    def run_linter(self):
        """Run static code analysis"""
        try:
            input_type = self.lint_input_type.get()
            
            if input_type == "file":
                file_path = self.lint_file_var.get().strip()
                if not file_path:
                    raise ValueError("Please select a file to check")
                issues = linter.lint_file(file_path)
            else:
                code = self.lint_code_text.get(1.0, tk.END).strip()
                if not code:
                    raise ValueError("Please enter code to check")
                issues = linter.lint_code(code)
            
            result = linter.format_issues(issues)
            self.display_result(result)
            
        except Exception as e:
            self.display_error(str(e))
    
    def run_unused_func_detector(self):
        """Run unused function detection"""
        try:
            from pathlib import Path
            
            # Get parameters
            project_path = self.unused_func_path_var.get().strip()
            if not project_path:
                raise ValueError("Please select a project directory to analyze")
            
            project_path = Path(project_path).resolve()
            if not project_path.exists():
                raise ValueError(f"Project path does not exist: {project_path}")
            
            if not project_path.is_dir():
                raise ValueError(f"Path is not a directory: {project_path}")
            
            # Parse exclude directories
            exclude_text = self.unused_func_exclude_var.get().strip()
            exclude_dirs = [d.strip() for d in exclude_text.split(',') if d.strip()] if exclude_text else None
            
            # Show progress info
            self.display_result("Analyzing project, please wait...\n")
            self.root.update()
            
            # Detect unused functions
            if self.unused_func_verbose_var.get():
                progress_msg = f"Scanning project: {project_path}\n"
                if exclude_dirs:
                    progress_msg += f"Exclude dirs: {', '.join(exclude_dirs)}\n"
                progress_msg += "\nAnalyzing...\n"
                self.display_result(progress_msg)
                self.root.update()
            
            unused_functions = unused_func_detector.detect_unused_functions(project_path, exclude_dirs)
            
            # Generate report
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
        """Run GUI Application"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            pass
    

    def setup_port_checker_ui(self):
        """Setup Port Checker UI"""
        import tkinter as tk
        from tkinter import ttk

        # Action Type
        ttk.Label(self.control_container, text="Action Type:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.port_action_var = tk.StringVar(value="check")
        action_combo = ttk.Combobox(
            self.control_container,
            textvariable=self.port_action_var,
            values=["check", "scan", "list"],
            state="readonly"
        )
        action_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2)
        action_combo.bind("<<ComboboxSelected>>", lambda e: self.update_port_params_ui())

        # Parameter Area Container
        self.port_params_frame = ttk.Frame(self.control_container)
        self.port_params_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(6, 6))
        self.port_params_frame.columnconfigure(1, weight=1)

        # Execute Button
        self.port_run_btn = ttk.Button(self.control_container, text="Execute", command=self.run_port_checker)
        self.port_run_btn.grid(row=2, column=0, columnspan=2, pady=(10, 0))

        # Initial Parameter Area
        self.update_port_params_ui()
        self.control_container.columnconfigure(1, weight=1)

    def update_port_params_ui(self):
        """Refresh parameter form based on action type"""
        import tkinter as tk
        from tkinter import ttk
        for w in self.port_params_frame.winfo_children():
            w.destroy()

        action = self.port_action_var.get()
        if action == "check":
            # host
            ttk.Label(self.port_params_frame, text="Host:").grid(row=0, column=0, sticky=tk.W, pady=2)
            self.port_host_var = tk.StringVar(value="localhost")
            ttk.Entry(self.port_params_frame, textvariable=self.port_host_var).grid(row=0, column=1,
                                                                                    sticky=(tk.W, tk.E), pady=2)

            # port
            ttk.Label(self.port_params_frame, text="Port:").grid(row=1, column=0, sticky=tk.W, pady=2)
            self.port_port_var = tk.StringVar(value="8080")
            ttk.Entry(self.port_params_frame, textvariable=self.port_port_var).grid(row=1, column=1,
                                                                                    sticky=(tk.W, tk.E), pady=2)

            # timeout
            ttk.Label(self.port_params_frame, text="Timeout (s):").grid(row=2, column=0, sticky=tk.W, pady=2)
            self.port_timeout_var = tk.StringVar(value="3")
            ttk.Entry(self.port_params_frame, textvariable=self.port_timeout_var).grid(row=2, column=1,
                                                                                       sticky=(tk.W, tk.E), pady=2)

        elif action == "scan":
            # host
            ttk.Label(self.port_params_frame, text="Host:").grid(row=0, column=0, sticky=tk.W, pady=2)
            self.scan_host_var = tk.StringVar(value="localhost")
            ttk.Entry(self.port_params_frame, textvariable=self.scan_host_var).grid(row=0, column=1,
                                                                                    sticky=(tk.W, tk.E), pady=2)

            # start
            ttk.Label(self.port_params_frame, text="Start Port:").grid(row=1, column=0, sticky=tk.W, pady=2)
            self.scan_start_var = tk.StringVar(value="1")
            ttk.Entry(self.port_params_frame, textvariable=self.scan_start_var).grid(row=1, column=1,
                                                                                     sticky=(tk.W, tk.E), pady=2)

            # end
            ttk.Label(self.port_params_frame, text="End Port:").grid(row=2, column=0, sticky=tk.W, pady=2)
            self.scan_end_var = tk.StringVar(value="1000")
            ttk.Entry(self.port_params_frame, textvariable=self.scan_end_var).grid(row=2, column=1, sticky=(tk.W, tk.E),
                                                                                   pady=2)

        else:  # list
            ttk.Label(self.port_params_frame, text="Note: Shows common ports and services, no params needed.").grid(
                row=0, column=0, columnspan=2, sticky=tk.W, pady=2
            )

    def run_port_checker(self):
        """Run Port Checker"""
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
                    raise ValueError("End port must be greater than start port")
                results = port_checker.scan_ports(host, start, end)
                text = port_checker.format_scan_results(results)

            else:  # list
                common = port_checker.get_common_ports()
                lines = ["Common Ports List:\n"]
                for p in sorted(common):
                    lines.append(f"  {p:>5}  - {common[p]}")
                text = "\n".join(lines)

            self.display_result(text)

        except Exception as e:
            self.display_error(str(e))

    def setup_api_diff_ui(self):
        import tkinter as tk
        from tkinter import ttk

        # ===== Top: Output Format =====
        ttk.Label(self.control_container, text="Output Format:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.api_fmt_var = tk.StringVar(value="text")
        ttk.Combobox(self.control_container, textvariable=self.api_fmt_var,
                     values=["text", "json", "md"], state="readonly") \
            .grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2)

        # ===== Contract v1 =====
        ttk.Label(self.control_container, text="Contract v1:").grid(row=1, column=0, sticky=tk.W, pady=(8, 2))
        ttk.Button(self.control_container, text="Load from File",
                   command=lambda: self.load_contract_from_file("v1")) \
            .grid(row=1, column=1, sticky=tk.E, pady=(8, 2))

        # Small description text (gray)
        tk.Label(self.control_container,
                 text="Supports: Simplified Contract JSON or OpenAPI JSON",
                 fg="#666").grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=(0, 6))

        # v1 text box (line number continues)
        self.api_old_text = tk.Text(self.control_container, height=12)
        self.api_old_text.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E))

        # ===== Contract v2 =====
        ttk.Label(self.control_container, text="Contract v2:").grid(row=4, column=0, sticky=tk.W, pady=(8, 2))
        ttk.Button(self.control_container, text="Load from File",
                   command=lambda: self.load_contract_from_file("v2")) \
            .grid(row=4, column=1, sticky=tk.E, pady=(8, 2))

        # Small description text (gray)
        tk.Label(self.control_container,
                 text="Supports: Simplified Contract JSON or OpenAPI JSON",
                 fg="#666").grid(row=5, column=0, columnspan=2, sticky=tk.W, pady=(0, 6))

        # v2 text box (line number continues)
        self.api_new_text = tk.Text(self.control_container, height=12)
        self.api_new_text.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E))

        # ===== Operation Area =====
        ttk.Button(self.control_container, text="Compare Contracts", command=self.run_api_diff) \
            .grid(row=7, column=0, columnspan=2, pady=(10, 0))
        ttk.Button(self.control_container, text="Fill Example", command=self.fill_demo_api_diff) \
            .grid(row=8, column=0, columnspan=2, pady=(6, 0))

        # Right column expandable
        self.control_container.columnconfigure(1, weight=1)

    '''
    def setup_api_diff_ui(self):
        import tkinter as tk
        from tkinter import ttk

        # Output Format
        ttk.Label(self.control_container, text="Output Format:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.api_fmt_var = tk.StringVar(value="text")
        ttk.Combobox(self.control_container, textvariable=self.api_fmt_var,
                    values=["text", "json", "md"], state="readonly")\
            .grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2)

        # Contract v1
        ttk.Label(self.control_container, text="Contract v1:").grid(row=1, column=0, sticky=tk.W, pady=(8, 2))
        ttk.Button(self.control_container, text="Load from File",
                command=lambda: self.load_contract_from_file("v1"))\
            .grid(row=1, column=1, sticky=tk.E, pady=(8, 2))
        self.api_old_text = tk.Text(self.control_container, height=12)
        self.api_old_text.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E))

        # Contract v2
        ttk.Label(self.control_container, text="Contract v2:").grid(row=3, column=0, sticky=tk.W, pady=(8, 2))
        ttk.Button(self.control_container, text="Load from File",
                command=lambda: self.load_contract_from_file("v2"))\
            .grid(row=3, column=1, sticky=tk.E, pady=(8, 2))
        self.api_new_text = tk.Text(self.control_container, height=12)
        self.api_new_text.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E))

        # Operation Area
        ttk.Button(self.control_container, text="Compare Contracts", command=self.run_api_diff)\
            .grid(row=5, column=0, columnspan=2, pady=(10, 0))
        ttk.Button(self.control_container, text="Fill Example", command=self.fill_demo_api_diff)\
            .grid(row=6, column=0, columnspan=2, pady=(6, 0))

        self.control_container.columnconfigure(1, weight=1)
    '''

    def load_contract_from_file(self, target="v1"):
        import json
        from tkinter import filedialog
        path = filedialog.askopenfilename(
            title="Select Contract JSON File",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
        )
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                raw = f.read()
            # Pre-validate JSON to give clear info in GUI
            json.loads(raw)
        except Exception as e:
            self.display_error(f"Read/Parse failed: {e}")
            return

        widget = self.api_old_text if target == "v1" else self.api_new_text
        widget.delete("1.0", "end")
        widget.insert("1.0", raw)
        self.display_result(f"Loaded: {path}")

    def run_api_diff(self):
        try:
            old_text = self.api_old_text.get("1.0", "end").strip()
            new_text = self.api_new_text.get("1.0", "end").strip()
            if not old_text or not new_text:
                raise ValueError("Please fill in JSON text in 'Contract v1 / Contract v2' or click 'Load from File'")
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

    # ========== Regex Tester Tool ==========
    def setup_regex_tester_ui(self):
        """Setup Regex Tester UI"""
        # Control Panel - Regex related controls
        control_frame = ttk.Frame(self.control_container)
        control_frame.pack(fill=tk.BOTH, expand=True)

        # Common Pattern Selection
        ttk.Label(control_frame, text="Common Patterns:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.pattern_var = tk.StringVar()
        self.common_patterns_combo = ttk.Combobox(
            control_frame,
            textvariable=self.pattern_var,
            values=list(self.regex_tester.get_common_patterns().keys()),
            state="readonly",
            width=30
        )
        self.common_patterns_combo.set("Select Common Pattern...")
        self.common_patterns_combo.grid(row=0, column=1, sticky=tk.EW, pady=5, padx=(5, 0))
        self.common_patterns_combo.bind('<<ComboboxSelected>>', self.on_pattern_selected)

        # Custom Pattern Input
        ttk.Label(control_frame, text="Custom Pattern:").grid(row=1, column=0, sticky=tk.NW, pady=5)
        self.pattern_entry = scrolledtext.ScrolledText(control_frame, width=40, height=3)
        self.pattern_entry.grid(row=1, column=1, sticky=tk.EW, pady=5, padx=(5, 0))

        # Options Frame
        options_frame = ttk.LabelFrame(control_frame, text="Options", padding=5)
        options_frame.grid(row=2, column=1, sticky=tk.EW, pady=5, padx=(5, 0))

        # Regex Flags
        self.ignore_case_var = tk.BooleanVar()
        ttk.Checkbutton(
            options_frame,
            text="Ignore Case (re.IGNORECASE)",
            variable=self.ignore_case_var
        ).pack(anchor=tk.W)

        self.multiline_var = tk.BooleanVar()
        ttk.Checkbutton(
            options_frame,
            text="Multiline (re.MULTILINE)",
            variable=self.multiline_var
        ).pack(anchor=tk.W)

        self.dotall_var = tk.BooleanVar()
        ttk.Checkbutton(
            options_frame,
            text="Dot Matches All (re.DOTALL)",
            variable=self.dotall_var
        ).pack(anchor=tk.W)

        # Test Text Area
        ttk.Label(control_frame, text="Test Text:").grid(row=3, column=0, sticky=tk.NW, pady=5)
        self.text_area = scrolledtext.ScrolledText(control_frame, width=40, height=10)
        self.text_area.grid(row=3, column=1, sticky=tk.NSEW, pady=5, padx=(5, 0))

        # Button Area
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
            command=self.clear_all_regex
        )
        self.clear_button.pack(side=tk.LEFT, padx=(0, 10))

        self.copy_result_button = ttk.Button(
            button_frame,
            text="Copy Result",
            command=self.copy_regex_results
        )
        self.copy_result_button.pack(side=tk.LEFT)

        # Configure Weights
        control_frame.columnconfigure(1, weight=1)
        control_frame.rowconfigure(3, weight=1)

        # Setup Shortcuts
        self.text_area.bind('<Control-Return>', lambda e: self.test_regex())
        self.pattern_entry.bind('<Control-Return>', lambda e: self.test_regex())

        # Result Panel - Regex Test Results
        result_frame = ttk.Frame(self.result_container)
        result_frame.pack(fill=tk.BOTH, expand=True)

        # Match Statistics
        stats_frame = ttk.Frame(result_frame)
        stats_frame.pack(fill=tk.X, pady=(0, 10))
        self.stats_label = ttk.Label(stats_frame, text="Match Result: 0 matches", font=('Arial', 10, 'bold'))
        self.stats_label.pack(side=tk.LEFT)
        self.pattern_status_label = ttk.Label(stats_frame, text="Pattern Status: Untested", foreground="gray")
        self.pattern_status_label.pack(side=tk.RIGHT)

        # Match Details
        ttk.Label(result_frame, text="Match Details:").pack(anchor=tk.W, pady=(0, 5))
        self.matches_text = scrolledtext.ScrolledText(
            result_frame,
            width=60,
            height=8,
            state=tk.DISABLED
        )
        self.matches_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Replacement Result Display
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
        """Callback when common pattern is selected"""
        pattern_name = self.pattern_var.get()
        common_patterns = self.regex_tester.get_common_patterns()

        if pattern_name in common_patterns:
            self.pattern_entry.delete(1.0, tk.END)
            self.pattern_entry.insert(1.0, common_patterns[pattern_name])

    def test_regex(self):
        """Test Regex"""
        pattern = self.pattern_entry.get(1.0, tk.END).strip()
        text = self.text_area.get(1.0, tk.END)

        if not pattern:
            messagebox.showerror("Error", "Please enter regex pattern")
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
        self.display_regex_results(result)

    def display_regex_results(self, result):
        """Display match results"""
        # Update statistics
        if result['success']:
            self.stats_label.config(
                text=f"Match Result: {result['match_count']} matches",
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

        # Update Match Details
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
            self.matches_text.insert(tk.END, f"Pattern Error: {result['error']}")

        self.matches_text.config(state=tk.DISABLED)

        # Update Replacement Text
        self.replace_text.config(state=tk.NORMAL)
        self.replace_text.delete(1.0, tk.END)
        self.replace_text.insert(tk.END, result['replaced_text'])
        self.replace_text.config(state=tk.DISABLED)

    def clear_all_regex(self):
        """Clear all inputs and results"""
        self.pattern_entry.delete(1.0, tk.END)
        self.text_area.delete(1.0, tk.END)
        self.matches_text.config(state=tk.NORMAL)
        self.matches_text.delete(1.0, tk.END)
        self.matches_text.config(state=tk.DISABLED)
        self.replace_text.config(state=tk.NORMAL)
        self.replace_text.delete(1.0, tk.END)
        self.replace_text.config(state=tk.DISABLED)
        self.stats_label.config(text="Match Result: 0 matches", foreground="black")
        self.pattern_status_label.config(text="Pattern Status: Untested", foreground="gray")
        self.common_patterns_combo.set("Select Common Pattern...")
        self.ignore_case_var.set(False)
        self.multiline_var.set(False)
        self.dotall_var.set(False)

    def copy_regex_results(self):
        """Copy regex results to clipboard"""
        self.root.clipboard_clear()
        results = self.matches_text.get(1.0, tk.END).strip()
        self.root.clipboard_append(results)
        messagebox.showinfo("Copied", "Results copied to clipboard")

    # ========== Robots Checker ==========
    def setup_robots_checker_ui(self):
        """Setup Robots Checker UI"""
        # Control Panel - Robots Checker related controls
        control_frame = ttk.Frame(self.control_container)
        control_frame.pack(fill=tk.BOTH, expand=True)

        # URL Input
        ttk.Label(control_frame, text="Website URL:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.robots_url_entry = ttk.Entry(control_frame, width=40)
        self.robots_url_entry.grid(row=0, column=1, sticky=tk.EW, pady=5, padx=(5, 0))
        self.robots_url_entry.insert(0, "https://")  # Default Prefix

        # Options Frame
        options_frame = ttk.LabelFrame(control_frame, text="Options", padding=5)
        options_frame.grid(row=1, column=0, columnspan=2, sticky=tk.EW, pady=5)

        # Timeout Settings
        ttk.Label(options_frame, text="Timeout (s):").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.robots_timeout_var = tk.StringVar(value="10")
        ttk.Entry(options_frame, textvariable=self.robots_timeout_var, width=10).grid(row=0, column=1, sticky=tk.W, padx=5)

        # Raw Output Options
        self.robots_raw_var = tk.BooleanVar()
        ttk.Checkbutton(
            options_frame,
            text="Show raw robots.txt content",
            variable=self.robots_raw_var
        ).grid(row=0, column=2, sticky=tk.W, padx=10)

        # Button Area
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
            text="Copy Result",
            command=self.copy_robots_results
        )
        self.copy_robots_button.pack(side=tk.LEFT)

        # Configure Weights
        control_frame.columnconfigure(1, weight=1)
        options_frame.columnconfigure(2, weight=1)

        # Setup Shortcut: Ctrl+Enter to check
        self.robots_url_entry.bind('<Control-Return>', lambda e: self.check_robots())

        # Result Panel - Robots Checker Results
        result_frame = ttk.Frame(self.result_container)
        result_frame.pack(fill=tk.BOTH, expand=True)

        # Status Bar
        self.robots_status_label = ttk.Label(result_frame, text="Status: Ready", font=('Arial', 10, 'bold'))
        self.robots_status_label.pack(anchor=tk.W, pady=(0, 5))

        # Robots URL Display
        self.robots_url_label = ttk.Label(result_frame, text="", foreground="blue")
        self.robots_url_label.pack(anchor=tk.W, pady=(0, 10))

        # Result Notebook (Tabs)
        notebook = ttk.Notebook(result_frame)
        notebook.pack(fill=tk.BOTH, expand=True)

        # Parsed Rules Tab
        self.robots_parsed_text = scrolledtext.ScrolledText(
            notebook,
            width=60,
            height=15,
            state=tk.DISABLED
        )
        notebook.add(self.robots_parsed_text, text="Parsed Rules")

        # Raw Content Tab
        self.robots_raw_text = scrolledtext.ScrolledText(
            notebook,
            width=60,
            height=15,
            state=tk.DISABLED
        )
        notebook.add(self.robots_raw_text, text="Raw Content")

    def check_robots(self):
        """Check robots.txt for given URL"""
        url = self.robots_url_entry.get().strip()

        if not url:
            messagebox.showerror("Error", "Please enter website URL")
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

            # Show raw content
            self.robots_raw_text.config(state=tk.NORMAL)
            self.robots_raw_text.delete(1.0, tk.END)
            self.robots_raw_text.insert(1.0, result['content'] or "No content available")
            self.robots_raw_text.config(state=tk.DISABLED)

            # Show parsed rules (if successful)
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
                    self.robots_parsed_text.insert(tk.END, f"\nUser Agent: {agent}\n")

                    if agent_rules['allow']:
                        self.robots_parsed_text.insert(tk.END, "  Allow:\n")
                        for path in agent_rules['allow']:
                            self.robots_parsed_text.insert(tk.END, f"    - {path}\n")

                    if agent_rules['disallow']:
                        self.robots_parsed_text.insert(tk.END, "  Disallow:\n")
                        for path in agent_rules['disallow']:
                            self.robots_parsed_text.insert(tk.END, f"    - {path}\n")
            else:
                self.robots_parsed_text.insert(tk.END, "No valid robots rules found or content could not be parsed.")

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

    # ========== File Processing Tool ==========

    def setup_batch_processor_ui(self):
        """Setup Batch File Processor UI"""
        # Operation Type Selection
        ttk.Label(self.control_container, text="Operation Type:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.batch_operation_var = tk.StringVar(value="rename")
        op_combo = ttk.Combobox(self.control_container, textvariable=self.batch_operation_var,
                                values=["rename", "copy", "move"], state="readonly")
        op_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)
        op_combo.bind('<<ComboboxSelected>>', self.on_batch_operation_change)

        # Directory Selection
        ttk.Label(self.control_container, text="Directory Path:").grid(row=1, column=0, sticky=tk.W, pady=5)
        dir_frame = ttk.Frame(self.control_container)
        dir_frame.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
        dir_frame.columnconfigure(0, weight=1)

        self.batch_dir_var = tk.StringVar(value=".")
        ttk.Entry(dir_frame, textvariable=self.batch_dir_var).grid(row=0, column=0, sticky=(tk.W, tk.E))
        ttk.Button(dir_frame, text="Select Dir", command=self.select_batch_dir).grid(row=0, column=1, padx=(5, 0))

        # Target Directory (for copy and move)
        self.target_dir_frame = ttk.Frame(self.control_container)
        self.target_dir_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        self.target_dir_frame.columnconfigure(1, weight=1)

        # Parameters Frame
        self.params_frame = ttk.Frame(self.control_container)
        self.params_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        self.params_frame.columnconfigure(1, weight=1)

        # Options Frame
        options_frame = ttk.LabelFrame(self.control_container, text="Options", padding="5")
        options_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        # Preview Mode
        self.preview_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Preview Mode", variable=self.preview_var).grid(row=0, column=0, sticky=tk.W)

        # Recursive Search
        self.recursive_var = tk.BooleanVar(value=False)
        self.recursive_check = ttk.Checkbutton(options_frame, text="Recursive Search", variable=self.recursive_var)

        # Overwrite Files
        self.overwrite_var = tk.BooleanVar(value=False)
        self.overwrite_check = ttk.Checkbutton(options_frame, text="Overwrite Existing Files", variable=self.overwrite_var)

        # Button Frame
        button_frame = ttk.Frame(self.control_container)
        button_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

        ttk.Button(button_frame, text="Execute Operation", command=self.run_batch_operation).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(button_frame, text="Execute Previewed Ops", command=self.execute_batch_operations).grid(row=0, column=1)

        self.control_container.columnconfigure(1, weight=1)

        # Initialize operation UI
        self.on_batch_operation_change()

    def on_batch_operation_change(self, event=None):
        """Handle batch operation type change"""
        # Clear parameters frame
        for widget in self.params_frame.winfo_children():
            widget.destroy()

        # Clear target directory frame
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
        """Setup rename parameters"""
        row = 0

        # Find Pattern
        ttk.Label(self.params_frame, text="Find Pattern:").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.pattern_var = tk.StringVar()
        ttk.Entry(self.params_frame, textvariable=self.pattern_var).grid(row=row, column=1, sticky=(tk.W, tk.E), pady=2)
        row += 1

        # Replace With
        ttk.Label(self.params_frame, text="Replace With:").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.replacement_var = tk.StringVar()
        ttk.Entry(self.params_frame, textvariable=self.replacement_var).grid(row=row, column=1, sticky=(tk.W, tk.E),
                                                                             pady=2)
        row += 1

        # Options
        self.regex_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(self.params_frame, text="Use Regex", variable=self.regex_var).grid(
            row=row, column=0, columnspan=2, sticky=tk.W, pady=2)
        row += 1

        self.case_sensitive_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(self.params_frame, text="Case Sensitive", variable=self.case_sensitive_var).grid(
            row=row, column=0, columnspan=2, sticky=tk.W, pady=2)
        row += 1

        # Extension Filter - Use custom placeholder Entry
        ttk.Label(self.params_frame, text="Extension Filter:").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.extension_entry = PlaceholderEntry(self.params_frame, placeholder="e.g.: .txt, .jpg")
        self.extension_entry.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=2)

        self.params_frame.columnconfigure(1, weight=1)

    def setup_copy_params(self):
        """Setup copy parameters"""
        row = 0

        # File Pattern
        ttk.Label(self.params_frame, text="File Pattern:").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.copy_pattern_var = tk.StringVar(value="*")
        ttk.Entry(self.params_frame, textvariable=self.copy_pattern_var).grid(row=row, column=1, sticky=(tk.W, tk.E),
                                                                              pady=2)
        row += 1

        # Display Options
        self.recursive_check.grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=2)
        row += 1
        self.overwrite_check.grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=2)

        self.params_frame.columnconfigure(1, weight=1)

    def setup_move_params(self):
        """Setup move parameters"""
        row = 0

        # File Pattern
        ttk.Label(self.params_frame, text="File Pattern:").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.move_pattern_var = tk.StringVar(value="*")
        ttk.Entry(self.params_frame, textvariable=self.move_pattern_var).grid(row=row, column=1, sticky=(tk.W, tk.E),
                                                                              pady=2)
        row += 1

        # Display Options
        self.recursive_check.grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=2)
        row += 1
        self.overwrite_check.grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=2)

        self.params_frame.columnconfigure(1, weight=1)

    def setup_target_dir(self):
        """Setup target directory"""
        ttk.Label(self.target_dir_frame, text="Target Dir:").grid(row=0, column=0, sticky=tk.W, pady=2)
        dir_frame = ttk.Frame(self.target_dir_frame)
        dir_frame.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2)
        dir_frame.columnconfigure(0, weight=1)

        self.target_dir_var = tk.StringVar()
        ttk.Entry(dir_frame, textvariable=self.target_dir_var).grid(row=0, column=0, sticky=(tk.W, tk.E))
        ttk.Button(dir_frame, text="Select Dir", command=self.select_target_dir).grid(row=0, column=1, padx=(5, 0))

        self.target_dir_frame.columnconfigure(1, weight=1)

    def setup_format_detector_ui(self):
        """Setup Format Detector UI"""
        # Detection Mode Selection
        ttk.Label(self.control_container, text="Detection Mode:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.detect_mode_var = tk.StringVar(value="file")
        mode_combo = ttk.Combobox(self.control_container, textvariable=self.detect_mode_var,
                                  values=["file", "directory", "content"], state="readonly")
        mode_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)
        mode_combo.bind('<<ComboboxSelected>>', self.on_detect_mode_change)

        # File/Directory Selection Frame
        self.path_frame = ttk.Frame(self.control_container)
        self.path_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        self.path_frame.columnconfigure(1, weight=1)

        # Content Input Frame
        self.content_frame = ttk.Frame(self.control_container)

        # Detailed Output Options
        ttk.Label(self.control_container, text="Output Options:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.verbose_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(self.control_container, text="Verbose Output", variable=self.verbose_var).grid(
            row=3, column=1, sticky=tk.W, pady=5)

        # Buttons
        ttk.Button(self.control_container, text="Start Detection", command=self.run_format_detection).grid(
            row=4, column=0, columnspan=2, pady=10)

        self.control_container.columnconfigure(1, weight=1)

        # Initialize detection mode UI
        self.on_detect_mode_change()

    def on_detect_mode_change(self, event=None):
        """Handle detection mode change"""
        # Clear path frame
        for widget in self.path_frame.winfo_children():
            widget.destroy()

        # Hide content frame
        self.content_frame.grid_forget()

        mode = self.detect_mode_var.get()

        if mode == "file":
            self.setup_file_detection_ui()
        elif mode == "directory":
            self.setup_directory_detection_ui()
        elif mode == "content":
            self.setup_content_detection_ui()

    def setup_file_detection_ui(self):
        """Setup file detection UI"""
        ttk.Label(self.path_frame, text="File Path:").grid(row=0, column=0, sticky=tk.W, pady=2)
        file_frame = ttk.Frame(self.path_frame)
        file_frame.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2)
        file_frame.columnconfigure(0, weight=1)

        self.file_path_var = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.file_path_var).grid(row=0, column=0, sticky=(tk.W, tk.E))
        ttk.Button(file_frame, text="Select File", command=self.select_detect_file).grid(row=0, column=1, padx=(5, 0))

        self.path_frame.columnconfigure(1, weight=1)

    def setup_directory_detection_ui(self):
        """Setup directory detection UI"""
        ttk.Label(self.path_frame, text="Directory Path:").grid(row=0, column=0, sticky=tk.W, pady=2)
        dir_frame = ttk.Frame(self.path_frame)
        dir_frame.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2)
        dir_frame.columnconfigure(0, weight=1)

        self.dir_path_var = tk.StringVar(value=".")
        ttk.Entry(dir_frame, textvariable=self.dir_path_var).grid(row=0, column=0, sticky=(tk.W, tk.E))
        ttk.Button(dir_frame, text="Select Dir", command=self.select_detect_dir).grid(row=0, column=1, padx=(5, 0))

        self.path_frame.columnconfigure(1, weight=1)

    def setup_content_detection_ui(self):
        """Setup content detection UI"""
        # Hide path frame, show content frame
        self.path_frame.grid_forget()
        self.content_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        self.content_frame.columnconfigure(0, weight=1)

        ttk.Label(self.content_frame, text="Input Content:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.content_text = scrolledtext.ScrolledText(self.content_frame, height=10, wrap=tk.WORD)
        self.content_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=2)

        ttk.Label(self.content_frame, text="Filename (Optional):").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.content_filename_var = tk.StringVar()
        ttk.Entry(self.content_frame, textvariable=self.content_filename_var).grid(
            row=3, column=0, sticky=(tk.W, tk.E), pady=2)

        self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.rowconfigure(1, weight=1)

    def select_batch_dir(self):
        """Select batch processing directory"""
        directory = filedialog.askdirectory(initialdir=".")
        if directory:
            self.batch_dir_var.set(directory)

    def select_target_dir(self):
        """Select target directory"""
        directory = filedialog.askdirectory(initialdir=".")
        if directory:
            self.target_dir_var.set(directory)

    def select_detect_file(self):
        """Select file to detect"""
        filename = filedialog.askopenfilename(
            title="Select File to Detect",
            filetypes=[("All Files", "*.*"), ("Text Files", "*.txt"), ("JSON Files", "*.json"),
                       ("XML Files", "*.xml"), ("CSV Files", "*.csv")]
        )
        if filename:
            self.file_path_var.set(filename)

    def select_detect_dir(self):
        """Select directory to detect"""
        directory = filedialog.askdirectory(initialdir=".")
        if directory:
            self.dir_path_var.set(directory)

    def run_batch_operation(self):
        """Run batch operation"""
        try:
            if self.BatchFileProcessor is None:
                raise ImportError("Cannot import BatchFileProcessor, please check file location")

            operation = self.batch_operation_var.get()
            directory = self.batch_dir_var.get().strip()

            if not directory:
                raise ValueError("Please select a directory")

            # Create processor instance
            batch_processor = self.BatchFileProcessor(preview=self.preview_var.get())
            batch_processor.operations = []  # Clear previous operations

            if operation == "rename":
                self.run_rename_operation(directory, batch_processor)
            elif operation == "copy":
                self.run_copy_operation(directory, batch_processor)
            elif operation == "move":
                self.run_move_operation(directory, batch_processor)

            # Show results
            if batch_processor.preview:
                result = "Preview Mode - The following operations will be performed:\n\n"
                for i, (op_type, src, dst) in enumerate(batch_processor.operations, 1):
                    result += f"{i}. {op_type}: '{os.path.basename(src)}' -> '{os.path.basename(dst)}'\n"
                result += f"\nTotal {len(batch_processor.operations)} operations"
                # Save processor instance for later use
                self.current_batch_processor = batch_processor
            else:
                result = "Operation completed!"

            self.display_result(result)

        except Exception as e:
            self.display_error(str(e))

    def run_rename_operation(self, directory, batch_processor):
        """Run rename operation"""
        pattern = self.pattern_var.get().strip()
        replacement = self.replacement_var.get().strip()

        if not pattern:
            raise ValueError("Please enter search pattern")

        # Get extension using custom Entry method
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
        """Run copy operation"""
        target_dir = self.target_dir_var.get().strip()
        if not target_dir:
            raise ValueError("Please select target directory")

        pattern = self.copy_pattern_var.get().strip()

        batch_processor.copy_files(
            source_dir=directory,
            target_dir=target_dir,
            pattern=pattern,
            recursive=self.recursive_var.get(),
            overwrite=self.overwrite_var.get()
        )

    def run_move_operation(self, directory, batch_processor):
        """Run move operation"""
        target_dir = self.target_dir_var.get().strip()
        if not target_dir:
            raise ValueError("Please select target directory")

        pattern = self.move_pattern_var.get().strip()

        batch_processor.move_files(
            source_dir=directory,
            target_dir=target_dir,
            pattern=pattern,
            recursive=self.recursive_var.get(),
            overwrite=self.overwrite_var.get()
        )

    def execute_batch_operations(self):
        """Execute previewed operations"""
        if not hasattr(self, 'current_batch_processor') or not self.current_batch_processor.operations:
            messagebox.showinfo("Info", "No operations to execute")
            return

        try:
            self.current_batch_processor.execute_operations()
            self.display_result("All operations completed!")
        except Exception as e:
            self.display_error(str(e))

    def run_format_detection(self):
        """Run format detection"""
        try:
            if self.FormatDetector is None:
                raise ImportError("Cannot import FormatDetector, please check file location")

            mode = self.detect_mode_var.get()
            verbose = self.verbose_var.get()

            # Create detector instance
            format_detector = self.FormatDetector()

            if mode == "file":
                file_path = self.file_path_var.get().strip()
                if not file_path:
                    raise ValueError("Please select a file to detect")

                result = format_detector.detect_file(file_path)
                output = self.format_detection_result(result, verbose)

            elif mode == "directory":
                dir_path = self.dir_path_var.get().strip()
                if not dir_path:
                    raise ValueError("Please select a directory to detect")

                results = format_detector.batch_detect(dir_path)
                output = "Batch Format Detection Results:\n\n"
                for filename, result in results.items():
                    output += f"File: {filename}\n"
                    if 'error' in result:
                        output += f"  Error: {result['error']}\n"
                    else:
                        output += f"  Most likely format: {result.get('most_likely_format', 'unknown').upper()}\n"
                        for fmt, detection in result['detections'].items():
                            status = "✓ Valid" if detection.get('is_valid', False) else "✗ Invalid"
                            confidence = detection.get('confidence', 0)
                            output += f"  {fmt.upper():6} : {status} (Confidence: {confidence:.2f})\n"
                    output += "\n"

            elif mode == "content":
                content = self.content_text.get(1.0, tk.END).strip()
                if not content:
                    raise ValueError("Please enter content to detect")

                filename = self.content_filename_var.get().strip()
                filename = filename if filename else None

                result = format_detector.detect_content(content, filename)
                output = self.format_detection_result(result, verbose)

            self.display_result(output)

        except Exception as e:
            self.display_error(str(e))

    def format_detection_result(self, result, verbose=False):
        """Format detection result"""
        if 'error' in result:
            return f"Error: {result['error']}"

        output = f"File: {result.get('filename', 'N/A')}\n"
        output += f"Content Preview: {result.get('content_preview', 'N/A')}\n\n"
        output += "Detection Results:\n"

        for format_name, detection in result['detections'].items():
            status = "✓ Valid" if detection.get('is_valid', False) else "✗ Invalid"
            confidence = detection.get('confidence', 0)
            output += f"  {format_name.upper():6} : {status} (Confidence: {confidence:.2f})\n"

            if verbose and detection.get('is_valid', False):
                details = detection.get('details', '')
                if details:
                    output += f"          Details: {details}\n"

            if verbose and detection.get('error'):
                output += f"          Error: {detection['error']}\n"

        output += f"\nMost likely format: {result.get('most_likely_format', 'unknown').upper()}\n"

        return output


if __name__ == "__main__":
    app = DevKitZeroGUI()
    app.run()

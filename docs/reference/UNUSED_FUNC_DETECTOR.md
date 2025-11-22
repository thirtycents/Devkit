# Unused Function Detector

The **Unused Function Detector** is a static analysis tool designed to identify functions and methods in your Python project that are defined but never called. This helps in cleaning up the codebase and reducing technical debt.

## 🚀 Features

- **Static Analysis**: Analyzes source code without executing it.
- **Function & Method Detection**: Identifies both standalone functions and class methods.
- **Exclusion Support**: Automatically excludes common special methods (e.g., `__init__`, `__str__`) and test functions (`test_*`).
- **Configurable Exclusions**: Allows excluding specific directories (e.g., `venv`, `migrations`).
- **Multiple Output Formats**: Supports Text, JSON, and HTML reports.

## 📖 Usage

### Command Line Interface

You can run the tool via the `devkit-zero` CLI:

```bash
# Analyze the current directory
devkit-zero unused-func

# Analyze a specific project path
devkit-zero unused-func /path/to/your/project

# Exclude specific directories
devkit-zero unused-func -e venv,tests,migrations

# Output results to a JSON file
devkit-zero unused-func -f json -o report.json

# Generate an HTML report
devkit-zero unused-func -f html -o report.html
```

### Python API

You can also use the tool programmatically in your Python scripts:

```python
from devkit_zero.tools.unused_func_detector import detect_unused_functions
from pathlib import Path

# Define project path
project_path = Path("./my_project")

# Detect unused functions
unused_funcs = detect_unused_functions(
    project_path=project_path,
    exclude_dirs=["venv", ".git"]
)

# Process results
for func in unused_funcs:
    print(f"Unused: {func.full_name} in {func.file_path}:{func.line_no}")
```

## 🔍 How It Works

1.  **AST Parsing**: The tool parses all Python files in the project using the `ast` module.
2.  **Definition Collection**: It collects all function and method definitions.
3.  **Usage Analysis**: It scans the code for all function calls and attribute accesses.
4.  **Comparison**: It compares definitions against usages to find those with zero call counts.

## ⚠️ Limitations

- **Dynamic Calls**: Functions called dynamically (e.g., `getattr(obj, func_name)()`) may be falsely flagged as unused.
- **External Usage**: If a function is part of a public API used by other projects, it will be flagged as unused within the current project scope.
- **Same Name Issues**: If multiple functions have the same name in different files, usage of one might count as usage for all (depending on the resolution strategy, though this tool attempts to be smart about imports).

## 📊 Output Formats

- **Text**: Simple list of unused functions printed to the console.
- **JSON**: Structured data suitable for automated processing.
- **HTML**: A visual report with file grouping and highlighting.

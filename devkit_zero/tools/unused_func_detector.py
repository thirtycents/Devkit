import argparse
import ast
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict

class FunctionInfo:
    """Function information"""
    def __init__(self, name: str, file_path: str, line_no: int, 
                 is_method: bool = False, class_name: Optional[str] = None):
        self.name = name
        self.file_path = file_path
        self.line_no = line_no
        self.is_method = is_method
        self.class_name = class_name
        self.called_count = 0
    
    @property
    def full_name(self) -> str:
        """Return full function name"""
        if self.is_method and self.class_name:
            return f"{self.class_name}.{self.name}"
        return self.name
    
    def __repr__(self) -> str:
        return f"<FunctionInfo {self.full_name} at {self.file_path}:{self.line_no}>"


# =============================================================================
# AST Analyzer
# =============================================================================

class FunctionDefVisitor(ast.NodeVisitor):
    """Function definition visitor"""
    
    # Excluded special functions
    EXCLUDED_FUNCTIONS = {
        '__init__', '__str__', '__repr__', '__eq__', '__hash__',
        '__del__', '__enter__', '__exit__', '__call__',
        'main', 'setUp', 'tearDown', 'test_.*'  # Test functions
    }
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.functions: List[FunctionInfo] = []
        self.current_class: Optional[str] = None
    
    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Visit class definition"""
        old_class = self.current_class
        self.current_class = node.name
        self.generic_visit(node)
        self.current_class = old_class
    
    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Visit function definition"""
        # Check if should exclude
        if not self._should_exclude(node.name):
            func_info = FunctionInfo(
                name=node.name,
                file_path=self.file_path,
                line_no=node.lineno,
                is_method=self.current_class is not None,
                class_name=self.current_class
            )
            self.functions.append(func_info)
        
        self.generic_visit(node)
    
    def _should_exclude(self, func_name: str) -> bool:
        """Check if function should be excluded"""
        import re
        for pattern in self.EXCLUDED_FUNCTIONS:
            if re.match(pattern, func_name):
                return True
        return False


class FunctionCallVisitor(ast.NodeVisitor):
    """Function call visitor"""
    
    def __init__(self):
        self.calls: Set[str] = set()
    
    def visit_Call(self, node: ast.Call) -> None:
        """Visit function call"""
        # Handle simple call: func()
        if isinstance(node.func, ast.Name):
            self.calls.add(node.func.id)
        
        # Handle method call: obj.method()
        elif isinstance(node.func, ast.Attribute):
            self.calls.add(node.func.attr)
        
        self.generic_visit(node)


# =============================================================================
# Core Detection Logic
# =============================================================================

def analyze_file(file_path: Path) -> Tuple[List[FunctionInfo], Set[str]]:
    """
    Analyze a single Python file
    
    Args:
        file_path: Python file path
        
    Returns:
        (List of function definitions, Set of function calls)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        tree = ast.parse(content, filename=str(file_path))
        
        # Extract function definitions
        def_visitor = FunctionDefVisitor(str(file_path))
        def_visitor.visit(tree)
        
        # Extract function calls
        call_visitor = FunctionCallVisitor()
        call_visitor.visit(tree)
        
        return def_visitor.functions, call_visitor.calls
        
    except SyntaxError as e:
        print(f"Warning: Syntax error in {file_path}: {e}", file=sys.stderr)
        return [], set()
    except Exception as e:
        print(f"Warning: Error analyzing {file_path}: {e}", file=sys.stderr)
        return [], set()


def find_python_files(root_path: Path, exclude_patterns: List[str]) -> List[Path]:
    """
    Find all Python files
    
    Args:
        root_path: Root directory
        exclude_patterns: Excluded directory patterns
        
    Returns:
        List of Python files
    """
    python_files = []
    
    for py_file in root_path.rglob('*.py'):
        # Check if should exclude
        should_exclude = False
        for pattern in exclude_patterns:
            if pattern in str(py_file):
                should_exclude = True
                break
        
        if not should_exclude:
            python_files.append(py_file)
    
    return python_files


def detect_unused_functions(
    project_path: Path,
    exclude_dirs: Optional[List[str]] = None
) -> List[FunctionInfo]:
    """
    Detect unused functions in the project
    
    Args:
        project_path: Project root directory
        exclude_dirs: List of excluded directories
        
    Returns:
        List of unused functions
    """
    if exclude_dirs is None:
        exclude_dirs = ['venv', '__pycache__', '.git', 'build', 'dist', '.pytest_cache']
    
    # Find all Python files
    python_files = find_python_files(project_path, exclude_dirs)
    
    if not python_files:
        print(f"No Python files found in {project_path}")
        return []
    
    print(f"Analyzing {len(python_files)} Python files...")
    
    # Collect all function definitions and calls
    all_functions: Dict[str, FunctionInfo] = {}
    all_calls: Set[str] = set()
    
    for py_file in python_files:
        functions, calls = analyze_file(py_file)
        
        # Record function definitions
        for func in functions:
            key = f"{func.file_path}:{func.full_name}"
            all_functions[key] = func
        
        # Record function calls
        all_calls.update(calls)
    
    # Mark called functions
    for func_info in all_functions.values():
        if func_info.name in all_calls:
            func_info.called_count += 1
    
    # Return unused functions
    unused = [f for f in all_functions.values() if f.called_count == 0]
    
    return unused


# =============================================================================
# Report Generation
# =============================================================================

def format_text_report(unused_functions: List[FunctionInfo]) -> str:
    """Generate text report"""
    if not unused_functions:
        return "✅ No unused functions found!"
    
    report = []
    report.append(f"🔍 Found {len(unused_functions)} unused function(s):\n")
    report.append("=" * 80)
    
    # Group by file
    by_file: Dict[str, List[FunctionInfo]] = defaultdict(list)
    for func in unused_functions:
        by_file[func.file_path].append(func)
    
    for file_path in sorted(by_file.keys()):
        report.append(f"\n📄 File: {file_path}")
        report.append("-" * 80)
        
        for func in sorted(by_file[file_path], key=lambda f: f.line_no):
            func_type = "method" if func.is_method else "function"
            report.append(f"  Line {func.line_no:4d}: {func_type:8s} {func.full_name}")
    
    report.append("\n" + "=" * 80)
    report.append(f"Total: {len(unused_functions)} unused functions")
    
    return "\n".join(report)


def format_json_report(unused_functions: List[FunctionInfo]) -> str:
    """Generate JSON report"""
    import json
    
    data = {
        "total_count": len(unused_functions),
        "unused_functions": [
            {
                "name": f.full_name,
                "file": f.file_path,
                "line": f.line_no,
                "type": "method" if f.is_method else "function",
                "class": f.class_name
            }
            for f in unused_functions
        ]
    }
    
    return json.dumps(data, indent=2)


def format_html_report(unused_functions: List[FunctionInfo]) -> str:
    """Generate HTML report"""
    html = """
<!DOCTYPE html>
<html>
<head>
    <title>Unused Functions Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        h1 { color: #333; }
        .summary { background: #f0f0f0; padding: 10px; border-radius: 5px; }
        .file-section { margin: 20px 0; }
        .file-name { background: #4CAF50; color: white; padding: 10px; }
        .function-list { list-style: none; padding: 0; }
        .function-item { padding: 5px 10px; border-bottom: 1px solid #ddd; }
        .function-item:hover { background: #f9f9f9; }
        .line-no { color: #999; }
        .func-type { color: #666; font-style: italic; }
    </style>
</head>
<body>
    <h1>🔍 Unused Functions Report</h1>
"""
    
    if not unused_functions:
        html += "    <div class='summary'>✅ No unused functions found!</div>"
    else:
        html += f"    <div class='summary'>Found {len(unused_functions)} unused function(s)</div>"
        
        # Group by file
        by_file: Dict[str, List[FunctionInfo]] = defaultdict(list)
        for func in unused_functions:
            by_file[func.file_path].append(func)
        
        for file_path in sorted(by_file.keys()):
            html += f"""
    <div class='file-section'>
        <div class='file-name'>📄 {file_path}</div>
        <ul class='function-list'>
"""
            for func in sorted(by_file[file_path], key=lambda f: f.line_no):
                func_type = "method" if func.is_method else "function"
                html += f"""
            <li class='function-item'>
                <span class='line-no'>Line {func.line_no}</span> - 
                <span class='func-type'>{func_type}</span> 
                <strong>{func.full_name}</strong>
            </li>
"""
            html += "        </ul>\n    </div>"
    
    html += """
</body>
</html>
"""
    return html


# =============================================================================
# CLI Interface Function (Required)
# =============================================================================

def main_function(args: argparse.Namespace) -> int:
    """
    Main function of the tool - CLI entry point
    
    Args:
        args: Parsed command line arguments object
        
    Returns:
        Exit code (0=success, 1=error)
    """
    try:
        project_path = Path(args.path).resolve()
        
        if not project_path.exists():
            print(f"Error: Path does not exist: {project_path}", file=sys.stderr)
            return 1
        
        if not project_path.is_dir():
            print(f"Error: Path is not a directory: {project_path}", file=sys.stderr)
            return 1
        
        # Parse excluded directories
        exclude_dirs = args.exclude.split(',') if args.exclude else None
        
        # Detect unused functions
        if args.verbose:
            print(f"Scanning project: {project_path}")
            if exclude_dirs:
                print(f"Excluding directories: {', '.join(exclude_dirs)}")
        
        unused_functions = detect_unused_functions(project_path, exclude_dirs)
        
        # Generate report
        if args.format == 'json':
            report = format_json_report(unused_functions)
        elif args.format == 'html':
            report = format_html_report(unused_functions)
        else:
            report = format_text_report(unused_functions)
        
        # Output report
        if args.output:
            output_path = Path(args.output)
            output_path.write_text(report, encoding='utf-8')
            print(f"Report saved to: {output_path}")
        else:
            print(report)
        
        # Return None to avoid CLI printing exit code
        return None
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


def register_parser(subparsers) -> None:
    """
    Register CLI subcommand - Required function
    
    Args:
        subparsers: argparse subparsers collection
    """
    parser = subparsers.add_parser(
        'unused-func',
        help='Detect unused functions in project',
        description='Analyze Python project to find unused functions'
    )
    
    parser.add_argument(
        'path',
        nargs='?',
        default='.',
        help='Project path (default: current directory)'
    )
    
    parser.add_argument(
        '-e', '--exclude',
        type=str,
        help='Excluded directories (comma separated, default: venv,__pycache__,.git)'
    )
    
    parser.add_argument(
        '-f', '--format',
        choices=['text', 'json', 'html'],
        default='text',
        help='Output format (default: text)'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        help='Output file path (default: print to terminal)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Show verbose output'
    )
    
    # Set default handler
    parser.set_defaults(func=main_function)


def main():
    """Standalone entry point - Required function"""
    parser = argparse.ArgumentParser(
        description='Unused Function Detector',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                          # Analyze current directory
  %(prog)s /path/to/project         # Analyze specific project
  %(prog)s -f json -o report.json   # JSON output to file
  %(prog)s -e venv,tests            # Exclude specific directories
        """
    )
    
    subparsers = parser.add_subparsers(dest='command')
    register_parser(subparsers)
    
    args = parser.parse_args()
    sys.exit(main_function(args))


if __name__ == '__main__':
    main()
import argparse
import ast
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict

class FunctionInfo:
    """函数信息"""
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
        """返回完整的函数名称"""
        if self.is_method and self.class_name:
            return f"{self.class_name}.{self.name}"
        return self.name
    
    def __repr__(self) -> str:
        return f"<FunctionInfo {self.full_name} at {self.file_path}:{self.line_no}>"


# =============================================================================
# AST 分析器
# =============================================================================

class FunctionDefVisitor(ast.NodeVisitor):
    """函数定义访问器"""
    
    # 排除的特殊函数
    EXCLUDED_FUNCTIONS = {
        '__init__', '__str__', '__repr__', '__eq__', '__hash__',
        '__del__', '__enter__', '__exit__', '__call__',
        'main', 'setUp', 'tearDown', 'test_.*'  # 测试函数
    }
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.functions: List[FunctionInfo] = []
        self.current_class: Optional[str] = None
    
    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """访问类定义"""
        old_class = self.current_class
        self.current_class = node.name
        self.generic_visit(node)
        self.current_class = old_class
    
    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """访问函数定义"""
        # 检查是否应排除
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
        """检查函数是否应被排除"""
        import re
        for pattern in self.EXCLUDED_FUNCTIONS:
            if re.match(pattern, func_name):
                return True
        return False


class FunctionCallVisitor(ast.NodeVisitor):
    """函数调用访问器"""
    
    def __init__(self):
        self.calls: Set[str] = set()
    
    def visit_Call(self, node: ast.Call) -> None:
        """访问函数调用"""
        # 处理简单调用: func()
        if isinstance(node.func, ast.Name):
            self.calls.add(node.func.id)
        
        # 处理方法调用: obj.method()
        elif isinstance(node.func, ast.Attribute):
            self.calls.add(node.func.attr)
        
        self.generic_visit(node)


# =============================================================================
# 核心检测逻辑
# =============================================================================

def analyze_file(file_path: Path) -> Tuple[List[FunctionInfo], Set[str]]:
    """
    分析单个Python文件
    
    Args:
        file_path: Python文件路径
        
    Returns:
        (函数定义列表, 函数调用集合)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        tree = ast.parse(content, filename=str(file_path))
        
        # 提取函数定义
        def_visitor = FunctionDefVisitor(str(file_path))
        def_visitor.visit(tree)
        
        # 提取函数调用
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
    查找所有Python文件
    
    Args:
        root_path: 根目录
        exclude_patterns: 排除的目录模式
        
    Returns:
        Python文件列表
    """
    python_files = []
    
    for py_file in root_path.rglob('*.py'):
        # 检查是否应排除
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
    检测项目中未使用的函数
    
    Args:
        project_path: 项目根目录
        exclude_dirs: 排除的目录列表
        
    Returns:
        未使用函数列表
    """
    if exclude_dirs is None:
        exclude_dirs = ['venv', '__pycache__', '.git', 'build', 'dist', '.pytest_cache']
    
    # 查找所有Python文件
    python_files = find_python_files(project_path, exclude_dirs)
    
    if not python_files:
        print(f"No Python files found in {project_path}")
        return []
    
    print(f"Analyzing {len(python_files)} Python files...")
    
    # 收集所有函数定义和调用
    all_functions: Dict[str, FunctionInfo] = {}
    all_calls: Set[str] = set()
    
    for py_file in python_files:
        functions, calls = analyze_file(py_file)
        
        # 记录函数定义
        for func in functions:
            key = f"{func.file_path}:{func.full_name}"
            all_functions[key] = func
        
        # 记录函数调用
        all_calls.update(calls)
    
    # 标记被调用的函数
    for func_info in all_functions.values():
        if func_info.name in all_calls:
            func_info.called_count += 1
    
    # 返回未使用的函数
    unused = [f for f in all_functions.values() if f.called_count == 0]
    
    return unused


# =============================================================================
# 报告生成
# =============================================================================

def format_text_report(unused_functions: List[FunctionInfo]) -> str:
    """生成文本格式报告"""
    if not unused_functions:
        return "✅ No unused functions found!"
    
    report = []
    report.append(f"🔍 Found {len(unused_functions)} unused function(s):\n")
    report.append("=" * 80)
    
    # 按文件分组
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
    """生成JSON格式报告"""
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
    """生成HTML格式报告"""
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
        
        # 按文件分组
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
# CLI接口函数（必需）
# =============================================================================

def main_function(args: argparse.Namespace) -> int:
    """
    工具的主要功能函数 - CLI入口
    
    Args:
        args: 解析后的命令行参数对象
        
    Returns:
        退出代码 (0=成功, 1=错误)
    """
    try:
        project_path = Path(args.path).resolve()
        
        if not project_path.exists():
            print(f"Error: Path does not exist: {project_path}", file=sys.stderr)
            return 1
        
        if not project_path.is_dir():
            print(f"Error: Path is not a directory: {project_path}", file=sys.stderr)
            return 1
        
        # 解析排除目录
        exclude_dirs = args.exclude.split(',') if args.exclude else None
        
        # 检测未使用的函数
        if args.verbose:
            print(f"Scanning project: {project_path}")
            if exclude_dirs:
                print(f"Excluding directories: {', '.join(exclude_dirs)}")
        
        unused_functions = detect_unused_functions(project_path, exclude_dirs)
        
        # 生成报告
        if args.format == 'json':
            report = format_json_report(unused_functions)
        elif args.format == 'html':
            report = format_html_report(unused_functions)
        else:
            report = format_text_report(unused_functions)
        
        # 输出报告
        if args.output:
            output_path = Path(args.output)
            output_path.write_text(report, encoding='utf-8')
            print(f"Report saved to: {output_path}")
        else:
            print(report)
        
        # 返回 None 以避免 CLI 打印退出代码
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
    注册CLI子命令 - 必需函数
    
    Args:
        subparsers: argparse的子解析器集合
    """
    parser = subparsers.add_parser(
        'unused-func',
        help='检测项目中未使用的函数',
        description='分析Python项目，找出从未被调用的函数'
    )
    
    parser.add_argument(
        'path',
        nargs='?',
        default='.',
        help='项目路径（默认: 当前目录）'
    )
    
    parser.add_argument(
        '-e', '--exclude',
        type=str,
        help='排除的目录（逗号分隔，默认: venv,__pycache__,.git）'
    )
    
    parser.add_argument(
        '-f', '--format',
        choices=['text', 'json', 'html'],
        default='text',
        help='输出格式（默认: text）'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        help='输出文件路径（默认: 打印到终端）'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='显示详细输出'
    )
    
    # 设置默认处理函数
    parser.set_defaults(func=main_function)


def main():
    """独立运行入口 - 必需函数"""
    parser = argparse.ArgumentParser(
        description='未使用函数检测工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s                          # 分析当前目录
  %(prog)s /path/to/project         # 分析指定项目
  %(prog)s -f json -o report.json   # JSON格式输出到文件
  %(prog)s -e venv,tests            # 排除特定目录
        """
    )
    
    subparsers = parser.add_subparsers(dest='command')
    register_parser(subparsers)
    
    args = parser.parse_args()
    sys.exit(main_function(args))


if __name__ == '__main__':
    main()
import argparse
import ast
import os
from typing import List, Dict, Any


class CodeLinter:
    def __init__(self, config: dict = None):
        self.issues = []
        # 默认配置
        self.config = {
            'naming_convention': 'warning',
            'missing_docstring': 'info',
            'import_style': 'warning',
            'syntax_error': 'error',
            'mutable_default_argument': 'error'
        }
        if config:
            self.config.update(config)
    
    def check_python_file(self, file_path: str) -> List[Dict[str, Any]]:
        """检查 Python 文件"""
        self.issues = []
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return self.check_python_code(content, file_path)
    
    def check_python_code(self, code: str, filename: str = "<string>") -> List[Dict[str, Any]]:
        """检查 Python 代码"""
        self.issues = []
        
        try:
            tree = ast.parse(code, filename=filename)
            self.visit_node(tree)
        except SyntaxError as e:
            self.issues.append({
                'type': 'syntax_error',
                'message': f"语法错误: {e.msg}",
                'line': e.lineno,
                'column': e.offset,
                'severity': 'error'
            })
        
        return self.issues
    
    def visit_node(self, node: ast.AST):
        """访问 AST 节点"""
        # 检查函数定义
        if isinstance(node, ast.FunctionDef):
            self.check_function_def(node)
        
        # 检查类定义
        elif isinstance(node, ast.ClassDef):
            self.check_class_def(node)
        
        # 检查导入语句
        elif isinstance(node, ast.Import):
            self.check_import(node)
        
        elif isinstance(node, ast.ImportFrom):
            self.check_import_from(node)
        
        # 检查变量使用
        elif isinstance(node, ast.Name):
            self.check_name_usage(node)
        
        # 递归访问子节点
        for child in ast.iter_child_nodes(node):
            self.visit_node(child)
    
    def check_function_def(self, node: ast.FunctionDef):
        """检查函数定义"""
        # 检查函数名命名规范
        if not node.name.islower() and '_' not in node.name:
            if not node.name.startswith('_'):  # 忽略私有方法
                self.issues.append({
                    'type': 'naming_convention',
                    'message': f"函数名 '{node.name}' 应使用小写字母和下划线",
                    'line': node.lineno,
                    'column': node.col_offset,
                    'severity': 'warning'
                })
        
        # 检查函数是否有文档字符串
        if not ast.get_docstring(node):
            self.issues.append({
                'type': 'missing_docstring',
                'message': f"函数 '{node.name}' 缺少文档字符串",
                'line': node.lineno,
                'column': node.col_offset,
                'severity': 'info'
            })
        # 检查可变类型默认参数
        for arg in node.args.defaults:
            if isinstance(arg, (ast.List, ast.Dict, ast.Set)):
                self._add_issue(
                    'mutable_default_argument',
                    f"不应使用可变类型 (list, dict, set) 作为函数 '{node.name}' 的默认参数",
                    arg  # The node for the argument itself
                )
    
    def check_class_def(self, node: ast.ClassDef):
        """检查类定义"""
        # 检查类名命名规范
        if not node.name[0].isupper():
            self.issues.append({
                'type': 'naming_convention',
                'message': f"类名 '{node.name}' 应使用首字母大写的驼峰命名",
                'line': node.lineno,
                'column': node.col_offset,
                'severity': 'warning'
            })
    
    def check_import(self, node: ast.Import):
        """检查 import 语句"""
        for alias in node.names:
            if alias.name.startswith('*'):
                self.issues.append({
                    'type': 'import_style',
                    'message': "避免使用 'from module import *'",
                    'line': node.lineno,
                    'column': node.col_offset,
                    'severity': 'warning'
                })
    
    def check_import_from(self, node: ast.ImportFrom):
        """检查 from import 语句"""
        for alias in node.names:
            if alias.name == '*':
                self.issues.append({
                    'type': 'import_style',
                    'message': "避免使用 'from module import *'",
                    'line': node.lineno,
                    'column': node.col_offset,
                    'severity': 'warning'
                })
    
    def check_name_usage(self, node: ast.Name):
        """检查变量名使用"""
        # 检查变量命名规范
        if isinstance(node.ctx, ast.Store):  # 变量赋值
            name = node.id
            if name.isupper() and len(name) > 1:  # 可能是常量
                pass  # 常量使用大写是正确的
            elif not name.islower() and '_' not in name and not name.startswith('_'):
                self.issues.append({
                    'type': 'naming_convention',
                    'message': f"变量名 '{name}' 应使用小写字母和下划线",
                    'line': node.lineno,
                    'column': node.col_offset,
                    'severity': 'info'
                })


def lint_file(file_path: str) -> List[Dict[str, Any]]:
    """检查文件"""
    linter = CodeLinter()
    return linter.check_python_file(file_path)


def lint_code(code: str, filename: str = "<string>") -> List[Dict[str, Any]]:
    """检查代码"""
    linter = CodeLinter()
    return linter.check_python_code(code, filename)


def format_issues(issues: List[Dict[str, Any]]) -> str:
    """格式化检查结果"""
    if not issues:
        return "✅ 未发现问题"
    
    result = []
    result.append(f"发现 {len(issues)} 个问题:\n")
    
    for issue in issues:
        severity_icon = {
            'error': '❌',
            'warning': '⚠️',
            'info': 'ℹ️'
        }.get(issue['severity'], '•')
        
        line_info = f"第 {issue['line']} 行" if issue.get('line') else ""
        result.append(f"{severity_icon} {issue['type'].upper()}: {issue['message']} {line_info}")
    
    return '\n'.join(result)


def register_parser(subparsers):
    """注册 linter 命令的参数解析器"""
    parser = subparsers.add_parser('lint', help='代码静态检查工具')
    parser.add_argument('--file', '-f', help='要检查的文件路径')
    parser.add_argument('--code', '-c', help='要检查的代码')
    parser.add_argument('--format', choices=['detailed', 'summary'], default='detailed',
                       help='输出格式')
    parser.set_defaults(func=main)


def main(args):
    """linter 工具的主函数"""
    try:
        if args.file:
            issues = lint_file(args.file)
        elif args.code:
            issues = lint_code(args.code)
        else:
            raise ValueError("请提供要检查的文件 (--file) 或代码 (--code)")
        
        if args.format == 'summary':
            error_count = sum(1 for issue in issues if issue['severity'] == 'error')
            warning_count = sum(1 for issue in issues if issue['severity'] == 'warning')
            info_count = sum(1 for issue in issues if issue['severity'] == 'info')
            
            return f"检查完成: {error_count} 个错误, {warning_count} 个警告, {info_count} 个提示"
        else:
            return format_issues(issues)
            
    except Exception as e:
        raise RuntimeError(f"代码检查失败: {e}")


if __name__ == "__main__":
    # 测试代码
    test_code = """
def BadFunctionName():
    x = 1
    return x

class badClassName:
    pass

from os import *
"""
    
    print("代码检查测试:")
    issues = lint_code(test_code)
    print(format_issues(issues))
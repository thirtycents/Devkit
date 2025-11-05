import argparse
import ast
import os
import json
from typing import List, Dict, Any
from pathlib import Path


class CodeLinter:
    def __init__(self, config: dict = None):
        self.issues = []
        # 默认配置
        self.config = {
            'naming_convention': 'warning',
            'missing_docstring': 'info',
            'import_style': 'warning',
            'syntax_error': 'error',
            'mutable_default_argument': 'error',
            'line_too_long': 'warning',
            'unused_import': 'warning',
            'max_line_length': 120,
            'max_function_lines': 50,
            'complexity': 'warning'
        }
        if config:
            self.config.update(config)
    
    def _add_issue(self, issue_type: str, message: str, node: ast.AST):
        """Helper to add an issue with severity from config."""
        severity = self.config.get(issue_type, 'info')
        self.issues.append({
            'type': issue_type,
            'message': message,
            'line': node.lineno,
            'column': node.col_offset,
            'severity': severity
        })
    
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
            
            # 检查行长度
            self.check_line_lengths(code)
            
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
            if not node.name.startswith('_'):
                self._add_issue(
                    'naming_convention',
                    f"函数名 '{node.name}' 应使用小写字母和下划线",
                    node
                )
        
        # 检查函数是否有文档字符串
        if not ast.get_docstring(node):
            self._add_issue(
                'missing_docstring',
                f"函数 '{node.name}' 缺少文档字符串",
                node
            )
        
        # 检查可变类型默认参数
        for arg in node.args.defaults:
            if isinstance(arg, (ast.List, ast.Dict, ast.Set)):
                self._add_issue(
                    'mutable_default_argument',
                    f"不应使用可变类型 (list, dict, set) 作为函数 '{node.name}' 的默认参数",
                    arg
                )
        
        # 检查函数复杂度（通过统计节点数简单估计）
        complexity = self.calculate_complexity(node)
        if complexity > 10:
            self._add_issue(
                'complexity',
                f"函数 '{node.name}' 的复杂度过高 (复杂度: {complexity})",
                node
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
    
    def check_line_lengths(self, code: str):
        """检查行长度"""
        max_length = self.config.get('max_line_length', 120)
        lines = code.split('\n')
        
        for line_num, line in enumerate(lines, start=1):
            if len(line) > max_length:
                self.issues.append({
                    'type': 'line_too_long',
                    'message': f"行过长 ({len(line)} > {max_length} 字符)",
                    'line': line_num,
                    'column': max_length,
                    'severity': self.config.get('line_too_long', 'warning')
                })
    
    def calculate_complexity(self, node: ast.FunctionDef) -> int:
        """计算函数的圈复杂度"""
        complexity = 1  # 基础复杂度
        
        for child in ast.walk(node):
            # 增加复杂度的节点类型
            if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
            elif isinstance(child, (ast.And, ast.Or)):
                complexity += 1
        
        return complexity


def lint_file(file_path: str) -> List[Dict[str, Any]]:
    """检查文件"""
    linter = CodeLinter()
    return linter.check_python_file(file_path)


def lint_code(code: str, filename: str = "<string>") -> List[Dict[str, Any]]:
    """检查代码"""
    linter = CodeLinter()
    return linter.check_python_code(code, filename)


def lint_directory(directory: str, recursive: bool = True) -> Dict[str, List[Dict[str, Any]]]:
    """检查目录中的所有 Python 文件"""
    results = {}
    path = Path(directory)
    
    if not path.exists():
        raise FileNotFoundError(f"目录不存在: {directory}")
    
    pattern = "**/*.py" if recursive else "*.py"
    
    for py_file in path.glob(pattern):
        if py_file.is_file():
            try:
                issues = lint_file(str(py_file))
                results[str(py_file)] = issues
            except Exception as e:
                results[str(py_file)] = [{
                    'type': 'error',
                    'message': f"无法检查文件: {e}",
                    'line': 0,
                    'column': 0,
                    'severity': 'error'
                }]
    
    return results


def format_issues(issues: List[Dict[str, Any]]) -> str:
    """格式化检查结果"""
    if not issues:
        return "✅ 未发现问题"
    
    result = []
    result.append(f"发现 {len(issues)} 个问题:\n")
    
    # 按严重程度排序
    sorted_issues = sorted(issues, key=lambda x: {'error': 0, 'warning': 1, 'info': 2}.get(x['severity'], 3))
    
    for issue in sorted_issues:
        severity_icon = {
            'error': '❌',
            'warning': '⚠️',
            'info': 'ℹ️'
        }.get(issue['severity'], '•')
        
        line_info = f"第 {issue['line']} 行" if issue.get('line') else ""
        col_info = f":{issue['column']}" if issue.get('column') else ""
        result.append(f"{severity_icon} [{issue['severity'].upper()}] {issue['type']}: {issue['message']} ({line_info}{col_info})")
    
    return '\n'.join(result)


def format_issues_json(issues: List[Dict[str, Any]]) -> str:
    """以 JSON 格式输出检查结果"""
    return json.dumps(issues, indent=2, ensure_ascii=False)


def format_directory_results(results: Dict[str, List[Dict[str, Any]]], format_type: str = 'detailed') -> str:
    """格式化目录检查结果"""
    if format_type == 'json':
        return json.dumps(results, indent=2, ensure_ascii=False)
    
    output = []
    total_issues = 0
    total_errors = 0
    total_warnings = 0
    total_info = 0
    
    for file_path, issues in results.items():
        if issues:
            total_issues += len(issues)
            output.append(f"\n{'='*80}")
            output.append(f"📁 {file_path}")
            output.append('='*80)
            output.append(format_issues(issues))
            
            for issue in issues:
                if issue['severity'] == 'error':
                    total_errors += 1
                elif issue['severity'] == 'warning':
                    total_warnings += 1
                elif issue['severity'] == 'info':
                    total_info += 1
    
    if format_type == 'summary':
        summary = f"\n{'='*80}\n"
        summary += f"📊 检查摘要\n"
        summary += f"{'='*80}\n"
        summary += f"总文件数: {len(results)}\n"
        summary += f"总问题数: {total_issues}\n"
        summary += f"  - 错误: {total_errors}\n"
        summary += f"  - 警告: {total_warnings}\n"
        summary += f"  - 提示: {total_info}\n"
        return summary
    
    # detailed format
    summary = f"\n{'='*80}\n"
    summary += f"📊 检查摘要\n"
    summary += f"{'='*80}\n"
    summary += f"总文件数: {len(results)}\n"
    summary += f"总问题数: {total_issues}\n"
    summary += f"  - 错误: {total_errors}\n"
    summary += f"  - 警告: {total_warnings}\n"
    summary += f"  - 提示: {total_info}\n"
    output.append(summary)
    
    return '\n'.join(output)


def register_parser(subparsers):
    """注册 linter 命令的参数解析器"""
    parser = subparsers.add_parser('lint', help='代码静态检查工具')
    parser.add_argument('path', nargs='?', help='要检查的文件或目录路径')
    parser.add_argument('--file', '-f', help='要检查的文件路径')
    parser.add_argument('--dir', '-d', help='要检查的目录路径')
    parser.add_argument('--code', '-c', help='要检查的代码')
    parser.add_argument('--recursive', '-r', action='store_true', default=True,
                       help='递归检查目录（默认启用）')
    parser.add_argument('--no-recursive', dest='recursive', action='store_false',
                       help='不递归检查目录')
    parser.add_argument('--format', choices=['detailed', 'summary', 'json'], default='detailed',
                       help='输出格式')
    parser.add_argument(
        '--min-severity',
        choices=['info', 'warning', 'error'],
        default='warning',
        help='设置导致非零退出代码的最低严重级别'
    )
    parser.set_defaults(func=main_function)


def main_function(args):
    """linter 工具的主函数，返回退出代码"""
    try:
        issues = []
        output = ""
        
        # 确定检查目标
        if args.code:
            # 检查代码字符串
            issues = lint_code(args.code)
            if args.format == 'json':
                output = format_issues_json(issues)
            elif args.format == 'summary':
                error_count = sum(1 for issue in issues if issue['severity'] == 'error')
                warning_count = sum(1 for issue in issues if issue['severity'] == 'warning')
                info_count = sum(1 for issue in issues if issue['severity'] == 'info')
                output = f"检查完成: {error_count} 个错误, {warning_count} 个警告, {info_count} 个提示"
            else:
                output = format_issues(issues)
        
        elif args.file:
            # 检查单个文件
            issues = lint_file(args.file)
            if args.format == 'json':
                output = format_issues_json(issues)
            elif args.format == 'summary':
                error_count = sum(1 for issue in issues if issue['severity'] == 'error')
                warning_count = sum(1 for issue in issues if issue['severity'] == 'warning')
                info_count = sum(1 for issue in issues if issue['severity'] == 'info')
                output = f"检查完成: {error_count} 个错误, {warning_count} 个警告, {info_count} 个提示"
            else:
                output = format_issues(issues)
        
        elif args.dir:
            # 检查目录
            results = lint_directory(args.dir, args.recursive)
            output = format_directory_results(results, args.format)
            # 收集所有问题用于退出代码判断
            for file_issues in results.values():
                issues.extend(file_issues)
        
        elif args.path:
            # 根据路径类型自动判断
            path = Path(args.path)
            if path.is_file():
                issues = lint_file(args.path)
                if args.format == 'json':
                    output = format_issues_json(issues)
                else:
                    output = format_issues(issues)
            elif path.is_dir():
                results = lint_directory(args.path, args.recursive)
                output = format_directory_results(results, args.format)
                for file_issues in results.values():
                    issues.extend(file_issues)
            else:
                print(f"❌ 路径不存在: {args.path}")
                return 1
        
        else:
            print("❌ 请提供要检查的文件 (--file)、目录 (--dir)、路径或代码 (--code)")
            return 1
        
        # 输出结果
        print(output)
        
        # 根据严重级别决定退出代码
        severity_levels = {'info': 0, 'warning': 1, 'error': 2}
        min_level = severity_levels.get(args.min_severity, 1)
        
        for issue in issues:
            issue_level = severity_levels.get(issue['severity'], 0)
            if issue_level >= min_level:
                return 1
        
        return 0
            
    except Exception as e:
        print(f"❌ 代码检查失败: {e}")
        return 1


def main():
    """独立运行入口"""
    parser = argparse.ArgumentParser(description='代码静态检查工具')
    parser.add_argument('path', nargs='?', help='要检查的文件或目录路径')
    parser.add_argument('--file', '-f', help='要检查的文件路径')
    parser.add_argument('--dir', '-d', help='要检查的目录路径')
    parser.add_argument('--code', '-c', help='要检查的代码')
    parser.add_argument('--recursive', '-r', action='store_true', default=True,
                       help='递归检查目录（默认启用）')
    parser.add_argument('--no-recursive', dest='recursive', action='store_false',
                       help='不递归检查目录')
    parser.add_argument('--format', choices=['detailed', 'summary', 'json'], default='detailed',
                       help='输出格式')
    parser.add_argument(
        '--min-severity',
        choices=['info', 'warning', 'error'],
        default='warning',
        help='设置导致非零退出代码的最低严重级别'
    )
    
    args = parser.parse_args()
    exit_code = main_function(args)
    exit(exit_code)


if __name__ == "__main__":
    main()

import argparse
import ast
import os
import json
from typing import List, Dict, Any
from pathlib import Path


class CodeLinter:
    def __init__(self, config: dict = None):
        self.issues = []
        # Default configuration
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
        """Check Python file"""
        self.issues = []
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return self.check_python_code(content, file_path)
    
    def check_python_code(self, code: str, filename: str = "<string>") -> List[Dict[str, Any]]:
        """Check Python code"""
        self.issues = []
        
        try:
            tree = ast.parse(code, filename=filename)
            self.visit_node(tree)
            
            # Check line length
            self.check_line_lengths(code)
            
        except SyntaxError as e:
            self.issues.append({
                'type': 'syntax_error',
                'message': f"Syntax error: {e.msg}",
                'line': e.lineno,
                'column': e.offset,
                'severity': 'error'
            })
        
        return self.issues
    
    def visit_node(self, node: ast.AST):
        """Visit AST node"""
        # Check function definition
        if isinstance(node, ast.FunctionDef):
            self.check_function_def(node)
        
        # Check class definition
        elif isinstance(node, ast.ClassDef):
            self.check_class_def(node)
        
        # Check import statement
        elif isinstance(node, ast.Import):
            self.check_import(node)
        
        elif isinstance(node, ast.ImportFrom):
            self.check_import_from(node)
        
        # Check variable usage
        elif isinstance(node, ast.Name):
            self.check_name_usage(node)
        
        # Recursively visit child nodes
        for child in ast.iter_child_nodes(node):
            self.visit_node(child)
    
    def check_function_def(self, node: ast.FunctionDef):
        """Check function definition"""
        # Check function naming convention
        if not node.name.islower() and '_' not in node.name:
            if not node.name.startswith('_'):
                self._add_issue(
                    'naming_convention',
                    f"Function name '{node.name}' should use lowercase letters and underscores",
                    node
                )
        
        # Check docstring
        if not ast.get_docstring(node):
            self._add_issue(
                'missing_docstring',
                f"Function '{node.name}' missing docstring",
                node
            )
        
        # Check mutable default arguments
        for arg in node.args.defaults:
            if isinstance(arg, (ast.List, ast.Dict, ast.Set)):
                self._add_issue(
                    'mutable_default_argument',
                    f"Do not use mutable types (list, dict, set) as default arguments for function '{node.name}'",
                    arg
                )
        
        # Check complexity
        complexity = self.calculate_complexity(node)
        if complexity > 10:
            self._add_issue(
                'complexity',
                f"Function '{node.name}' is too complex (complexity: {complexity})",
                node
            )
    
    def check_class_def(self, node: ast.ClassDef):
        """Check class definition"""
        # Check class naming convention
        if not node.name[0].isupper():
            self.issues.append({
                'type': 'naming_convention',
                'message': f"Class name '{node.name}' should use CapWords convention",
                'line': node.lineno,
                'column': node.col_offset,
                'severity': 'warning'
            })
    
    def check_import(self, node: ast.Import):
        """Check import statement"""
        for alias in node.names:
            if alias.name.startswith('*'):
                self.issues.append({
                    'type': 'import_style',
                    'message': "Avoid using 'from module import *'",
                    'line': node.lineno,
                    'column': node.col_offset,
                    'severity': 'warning'
                })
    
    def check_import_from(self, node: ast.ImportFrom):
        """Check from import statement"""
        for alias in node.names:
            if alias.name == '*':
                self.issues.append({
                    'type': 'import_style',
                    'message': "Avoid using 'from module import *'",
                    'line': node.lineno,
                    'column': node.col_offset,
                    'severity': 'warning'
                })
    
    def check_name_usage(self, node: ast.Name):
        """Check variable usage"""
        # Check variable naming convention
        if isinstance(node.ctx, ast.Store):  # Variable assignment
            name = node.id
            if name.isupper() and len(name) > 1:  # Constant
                pass  # Constants using uppercase is correct
            elif not name.islower() and '_' not in name and not name.startswith('_'):
                self.issues.append({
                    'type': 'naming_convention',
                    'message': f"Variable name '{name}' should use lowercase letters and underscores",
                    'line': node.lineno,
                    'column': node.col_offset,
                    'severity': 'info'
                })
    
    def check_line_lengths(self, code: str):
        """Check line lengths"""
        max_length = self.config.get('max_line_length', 120)
        lines = code.split('\n')
        
        for line_num, line in enumerate(lines, start=1):
            if len(line) > max_length:
                self.issues.append({
                    'type': 'line_too_long',
                    'message': f"Line too long ({len(line)} > {max_length} characters)",
                    'line': line_num,
                    'column': max_length,
                    'severity': self.config.get('line_too_long', 'warning')
                })
    
    def calculate_complexity(self, node: ast.FunctionDef) -> int:
        """Calculate function cyclomatic complexity"""
        complexity = 1  # Base complexity
        
        for child in ast.walk(node):
            # Node types that increase complexity
            if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
            elif isinstance(child, (ast.And, ast.Or)):
                complexity += 1
        
        return complexity


def lint_file(file_path: str) -> List[Dict[str, Any]]:
    """Lint file"""
    linter = CodeLinter()
    return linter.check_python_file(file_path)


def lint_code(code: str, filename: str = "<string>") -> List[Dict[str, Any]]:
    """Lint code"""
    linter = CodeLinter()
    return linter.check_python_code(code, filename)


def lint_directory(directory: str, recursive: bool = True) -> Dict[str, List[Dict[str, Any]]]:
    """Lint all Python files in directory"""
    results = {}
    path = Path(directory)
    
    if not path.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")
    
    pattern = "**/*.py" if recursive else "*.py"
    
    for py_file in path.glob(pattern):
        if py_file.is_file():
            try:
                issues = lint_file(str(py_file))
                results[str(py_file)] = issues
            except Exception as e:
                results[str(py_file)] = [{
                    'type': 'error',
                    'message': f"Cannot lint file: {e}",
                    'line': 0,
                    'column': 0,
                    'severity': 'error'
                }]
    
    return results


def format_issues(issues: List[Dict[str, Any]]) -> str:
    """Format lint issues"""
    if not issues:
        return "✅ No issues found"
    
    result = []
    result.append(f"Found {len(issues)} issues:\n")
    
    # Sort by severity
    sorted_issues = sorted(issues, key=lambda x: {'error': 0, 'warning': 1, 'info': 2}.get(x['severity'], 3))
    
    for issue in sorted_issues:
        severity_icon = {
            'error': '❌',
            'warning': '⚠️',
            'info': 'ℹ️'
        }.get(issue['severity'], '•')
        
        line_info = f"Line {issue['line']}" if issue.get('line') else ""
        col_info = f":{issue['column']}" if issue.get('column') else ""
        result.append(f"{severity_icon} [{issue['severity'].upper()}] {issue['type']}: {issue['message']} ({line_info}{col_info})")
    
    return '\n'.join(result)


def format_issues_json(issues: List[Dict[str, Any]]) -> str:
    """Output lint issues in JSON format"""
    return json.dumps(issues, indent=2, ensure_ascii=False)


def format_directory_results(results: Dict[str, List[Dict[str, Any]]], format_type: str = 'detailed') -> str:
    """Format directory lint results"""
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
        summary += f"📊 Lint Summary\n"
        summary += f"{'='*80}\n"
        summary += f"Total files: {len(results)}\n"
        summary += f"Total issues: {total_issues}\n"
        summary += f"  - Errors: {total_errors}\n"
        summary += f"  - Warnings: {total_warnings}\n"
        summary += f"  - Infos: {total_info}\n"
        return summary
    
    # detailed format
    summary = f"\n{'='*80}\n"
    summary += f"📊 Lint Summary\n"
    summary += f"{'='*80}\n"
    summary += f"Total files: {len(results)}\n"
    summary += f"Total issues: {total_issues}\n"
    summary += f"  - Errors: {total_errors}\n"
    summary += f"  - Warnings: {total_warnings}\n"
    summary += f"  - Infos: {total_info}\n"
    output.append(summary)
    
    return '\n'.join(output)


def register_parser(subparsers):
    """Register linter command parser"""
    parser = subparsers.add_parser('lint', help='Static Code Analysis Tool')
    parser.add_argument('path', nargs='?', help='Path to file or directory to lint')
    parser.add_argument('--file', '-f', help='Path to file to lint')
    parser.add_argument('--dir', '-d', help='Path to directory to lint')
    parser.add_argument('--code', '-c', help='Code string to lint')
    parser.add_argument('--recursive', '-r', action='store_true', default=True,
                       help='Recursively lint directory (default: enabled)')
    parser.add_argument('--no-recursive', dest='recursive', action='store_false',
                       help='Do not recursively lint directory')
    parser.add_argument('--format', choices=['detailed', 'summary', 'json'], default='detailed',
                       help='Output format')
    parser.add_argument(
        '--min-severity',
        choices=['info', 'warning', 'error'],
        default='warning',
        help='Set minimum severity level for non-zero exit code'
    )
    parser.set_defaults(func=main_function)


def main_function(args):
    """linter tool main function, returns exit code"""
    try:
        issues = []
        output = ""
        
        # Determine lint target
        if args.code:
            # Lint code string
            issues = lint_code(args.code)
            if args.format == 'json':
                output = format_issues_json(issues)
            elif args.format == 'summary':
                error_count = sum(1 for issue in issues if issue['severity'] == 'error')
                warning_count = sum(1 for issue in issues if issue['severity'] == 'warning')
                info_count = sum(1 for issue in issues if issue['severity'] == 'info')
                output = f"Lint complete: {error_count} errors, {warning_count} warnings, {info_count} infos"
            else:
                output = format_issues(issues)
        
        elif args.file:
            # Lint single file
            issues = lint_file(args.file)
            if args.format == 'json':
                output = format_issues_json(issues)
            elif args.format == 'summary':
                error_count = sum(1 for issue in issues if issue['severity'] == 'error')
                warning_count = sum(1 for issue in issues if issue['severity'] == 'warning')
                info_count = sum(1 for issue in issues if issue['severity'] == 'info')
                output = f"Lint complete: {error_count} errors, {warning_count} warnings, {info_count} infos"
            else:
                output = format_issues(issues)
        
        elif args.dir:
            # Lint directory
            results = lint_directory(args.dir, args.recursive)
            output = format_directory_results(results, args.format)
            # Collect all issues for exit code
            for file_issues in results.values():
                issues.extend(file_issues)
        
        elif args.path:
            # Auto-detect path type
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
                print(f"❌ Path not found: {args.path}")
                return 1
        
        else:
            print("❌ Please provide file (--file), directory (--dir), path, or code (--code) to lint")
            return 1
        
        # Output result
        print(output)
        
        # Determine exit code based on severity
        severity_levels = {'info': 0, 'warning': 1, 'error': 2}
        min_level = severity_levels.get(args.min_severity, 1)
        
        for issue in issues:
            issue_level = severity_levels.get(issue['severity'], 0)
            if issue_level >= min_level:
                return 1
        
        return 0
            
    except Exception as e:
        print(f"❌ Lint failed: {e}")
        return 1


def main():
    """Standalone entry point"""
    parser = argparse.ArgumentParser(description='Static Code Analysis Tool')
    parser.add_argument('path', nargs='?', help='Path to file or directory to lint')
    parser.add_argument('--file', '-f', help='Path to file to lint')
    parser.add_argument('--dir', '-d', help='Path to directory to lint')
    parser.add_argument('--code', '-c', help='Code string to lint')
    parser.add_argument('--recursive', '-r', action='store_true', default=True,
                       help='Recursively lint directory (default: enabled)')
    parser.add_argument('--no-recursive', dest='recursive', action='store_false',
                       help='Do not recursively lint directory')
    parser.add_argument('--format', choices=['detailed', 'summary', 'json'], default='detailed',
                       help='Output format')
    parser.add_argument(
        '--min-severity',
        choices=['info', 'warning', 'error'],
        default='warning',
        help='Set minimum severity level for non-zero exit code'
    )
    
    args = parser.parse_args()
    exit_code = main_function(args)
    exit(exit_code)


if __name__ == "__main__":
    main()

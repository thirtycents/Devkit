"""
代码格式化工具

功能：格式化Python和JavaScript代码
负责人：lyh
优先级：高
"""

"""
代码格式化工具
支持 Python 和 JavaScript 代码格式化
"""

import argparse
import sys
import os
from typing import Optional


def format_python_code(code: str) -> str:
    """
    格式化 Python 代码
    使用内置的 ast 模块进行基础格式化
    """
    try:
        import ast
        # 验证代码语法正确性
        ast.parse(code)
        
        # 基础格式化 (这里可以后续集成 black)
        lines = code.split('\n')
        formatted_lines = []
        indent_level = 0
        
        for line in lines:
            stripped = line.strip()
            if not stripped:
                formatted_lines.append('')
                continue
                
            # 简单的缩进处理
            if stripped.endswith(':'):
                formatted_lines.append('    ' * indent_level + stripped)
                indent_level += 1
            elif stripped.startswith(('return', 'break', 'continue', 'pass')):
                formatted_lines.append('    ' * indent_level + stripped)
            else:
                if stripped.startswith(('def ', 'class ', 'if ', 'for ', 'while ', 'with ', 'try:')):
                    formatted_lines.append('    ' * indent_level + stripped)
                else:
                    formatted_lines.append('    ' * indent_level + stripped)
        
        return '\n'.join(formatted_lines)
    except SyntaxError as e:
        raise ValueError(f"Python 代码语法错误: {e}")


def format_javascript_code(code: str) -> str:
    """
    格式化 JavaScript 代码
    基础格式化实现
    """
    lines = code.split('\n')
    formatted_lines = []
    indent_level = 0
    
    for line in lines:
        stripped = line.strip()
        if not stripped:
            formatted_lines.append('')
            continue
            
        # 简单的 JS 格式化
        if stripped.endswith('{'):
            formatted_lines.append('  ' * indent_level + stripped)
            indent_level += 1
        elif stripped.startswith('}'):
            indent_level = max(0, indent_level - 1)
            formatted_lines.append('  ' * indent_level + stripped)
        else:
            formatted_lines.append('  ' * indent_level + stripped)
    
    return '\n'.join(formatted_lines)


def format_code(code: str, language: str) -> str:
    """
    格式化代码的主函数
    
    Args:
        code: 要格式化的代码字符串
        language: 编程语言 ('python' 或 'javascript')
        
    Returns:
        格式化后的代码字符串
    """
    if language.lower() in ['python', 'py']:
        return format_python_code(code)
    elif language.lower() in ['javascript', 'js']:
        return format_javascript_code(code)
    else:
        raise ValueError(f"不支持的编程语言: {language}")


def format_file(file_path: str, language: Optional[str] = None) -> str:
    """
    格式化文件
    
    Args:
        file_path: 文件路径
        language: 编程语言，如果不提供则从文件扩展名推断
        
    Returns:
        格式化后的代码字符串
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")
    
    # 从文件扩展名推断语言
    if language is None:
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.py':
            language = 'python'
        elif ext in ['.js', '.jsx']:
            language = 'javascript'
        else:
            raise ValueError(f"无法从扩展名推断语言: {ext}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()
    
    return format_code(code, language)


def register_parser(subparsers):
    """注册 formatter 命令的参数解析器"""
    parser = subparsers.add_parser('format', help='代码格式化工具')
    parser.add_argument('--file', '-f', help='要格式化的文件路径')
    parser.add_argument('--language', '-l', choices=['python', 'py', 'javascript', 'js'],
                       help='编程语言')
    parser.add_argument('--input', '-i', help='直接输入要格式化的代码')
    parser.add_argument('--output', '-o', help='输出文件路径 (可选)')
    parser.set_defaults(func=main)


def main(args):
    """formatter 工具的主函数"""
    try:
        if args.file:
            # 格式化文件
            formatted_code = format_file(args.file, args.language)
            
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(formatted_code)
                print(f"格式化完成，结果已保存到: {args.output}")
            else:
                return formatted_code
                
        elif args.input:
            # 格式化直接输入的代码
            if not args.language:
                raise ValueError("直接输入代码时必须指定语言 (--language)")
            
            formatted_code = format_code(args.input, args.language)
            
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(formatted_code)
                print(f"格式化完成，结果已保存到: {args.output}")
            else:
                return formatted_code
        else:
            raise ValueError("请提供要格式化的文件 (--file) 或直接输入代码 (--input)")
            
    except Exception as e:
        raise RuntimeError(f"格式化失败: {e}")


if __name__ == "__main__":
    # 用于独立测试
    test_python_code = """
def hello(name):
print(f"Hello, {name}!")
if name == "world":
return True
return False
"""
    
    print("Python 代码格式化测试:")
    print(format_python_code(test_python_code))
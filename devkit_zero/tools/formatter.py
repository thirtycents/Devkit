"""
代码格式化工具

功能：格式化Python和JavaScript代码
负责人：lyh
优先级：高
"""

import argparse
import sys
import os
import re
from typing import Optional, Tuple


def format_python_code(code: str, ignore_errors: bool = False) -> Tuple[str, Optional[str]]:
    """
    格式化 Python 代码
    使用智能的缩进和空格处理
    
    Args:
        code: 要格式化的代码字符串
        ignore_errors: 是否忽略语法错误,仍然尝试格式化
        
    Returns:
        (formatted_code, error_message) - 格式化后的代码和错误信息(如果有)
    """
    import ast
    
    error_msg = None
    
    # 先验证语法
    try:
        ast.parse(code)
    except SyntaxError as e:
        error_msg = f"Python 语法错误 (第{e.lineno}行): {e.msg}"
        if not ignore_errors:
            return code, error_msg
    
    try:
        lines = code.split('\n')
        formatted_lines = []
        indent_level = 0
        in_multiline_string = False
        string_delimiter = None
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            
            # 处理空行
            if not stripped:
                formatted_lines.append('')
                continue
            
            # 检测多行字符串
            if '"""' in stripped or "'''" in stripped:
                if not in_multiline_string:
                    in_multiline_string = True
                    string_delimiter = '"""' if '"""' in stripped else "'''"
                    formatted_lines.append('    ' * indent_level + stripped)
                    if stripped.count(string_delimiter) >= 2:
                        in_multiline_string = False
                    continue
                else:
                    formatted_lines.append('    ' * indent_level + stripped)
                    if string_delimiter in stripped:
                        in_multiline_string = False
                    continue
            
            # 在多行字符串内,保持原样
            if in_multiline_string:
                formatted_lines.append('    ' * indent_level + stripped)
                continue
            
            # 处理缩进减少的情况 (else, elif, except, finally, elif)
            if stripped.startswith(('else:', 'elif ', 'except:', 'except ', 'finally:', 'case ', 'case:')):
                indent_level = max(0, indent_level - 1)
                formatted_lines.append('    ' * indent_level + stripped)
                indent_level += 1
                continue
            
            # 处理右括号/大括号/中括号
            if stripped.startswith(('}', ']', ')')):
                indent_level = max(0, indent_level - 1)
            
            # 添加格式化的行
            formatted_lines.append('    ' * indent_level + stripped)
            
            # 处理缩进增加的情况
            if stripped.rstrip().endswith(':'):
                # 函数、类、if、for、while、with、try 等
                indent_level += 1
            elif stripped.rstrip().endswith(('{', '(')):
                indent_level += 1
            elif stripped.rstrip().endswith('[') and not stripped.rstrip().endswith('[]'):
                indent_level += 1
            
            # 处理缩进减少 - 单行语句后
            if indent_level > 0:
                # 检查是否是单行语句(pass, return, break, continue等)
                if any(stripped.startswith(kw) for kw in ['pass', 'return ', 'break', 'continue', 'raise ']):
                    # 检查下一行,如果不是同级或更深的缩进,则减少缩进
                    if i + 1 < len(lines):
                        next_line = lines[i + 1].strip()
                        if next_line and not next_line.startswith(('else:', 'elif ', 'except:', 'except ', 'finally:')):
                            # 如果下一行不是空的且不是控制流关键字,可能需要调整
                            pass
        
        # 后处理: 移除多余的空行,最多保留2个连续空行
        final_lines = []
        empty_count = 0
        for line in formatted_lines:
            if not line.strip():
                empty_count += 1
                if empty_count <= 2:
                    final_lines.append(line)
            else:
                empty_count = 0
                final_lines.append(line)
        
        # 添加运算符周围的空格
        result = '\n'.join(final_lines)
        
        # 格式化运算符空格 (简单版本)
        # = 周围加空格
        result = re.sub(r'(\w)=(\w)', r'\1 = \2', result)
        result = re.sub(r'(\w)=(\()', r'\1 = \2', result)
        
        # +, -, *, / 周围加空格
        result = re.sub(r'(\w)\+(\w)', r'\1 + \2', result)
        result = re.sub(r'(\w)-(\w)', r'\1 - \2', result)
        result = re.sub(r'(\w)\*(\w)', r'\1 * \2', result)
        result = re.sub(r'(\w)/(\w)', r'\1 / \2', result)
        
        # 逗号后加空格
        result = re.sub(r',(\w)', r', \1', result)
        
        return result, error_msg
        
    except Exception as e:
        if ignore_errors:
            return code, f"格式化出错: {str(e)}"
        return code, f"格式化失败: {str(e)}"


def format_javascript_code(code: str, ignore_errors: bool = False) -> Tuple[str, Optional[str]]:
    """
    格式化 JavaScript 代码
    智能的缩进和空格处理
    
    Args:
        code: 要格式化的代码字符串
        ignore_errors: 是否忽略错误继续格式化
        
    Returns:
        (formatted_code, error_message) - 格式化后的代码和错误信息(如果有)
    """
    try:
        lines = code.split('\n')
        formatted_lines = []
        indent_level = 0
        in_multiline_comment = False
        
        for line in lines:
            stripped = line.strip()
            
            # 处理空行
            if not stripped:
                formatted_lines.append('')
                continue
            
            # 处理多行注释
            if '/*' in stripped and '*/' not in stripped:
                in_multiline_comment = True
                formatted_lines.append('  ' * indent_level + stripped)
                continue
            elif '*/' in stripped:
                formatted_lines.append('  ' * indent_level + stripped)
                if in_multiline_comment:
                    in_multiline_comment = False
                continue
            elif in_multiline_comment:
                formatted_lines.append('  ' * indent_level + stripped)
                continue
            
            # 处理右大括号
            if stripped.startswith('}'):
                indent_level = max(0, indent_level - 1)
                formatted_lines.append('  ' * indent_level + stripped)
                # 处理 } else {, } catch {, } finally { 等
                if '{' in stripped:
                    indent_level += 1
                continue
            
            # 处理右括号和右中括号
            if stripped.startswith((']', ')')):
                indent_level = max(0, indent_level - 1)
            
            # 添加格式化的行
            formatted_lines.append('  ' * indent_level + stripped)
            
            # 处理缩进增加
            if stripped.rstrip().endswith('{'):
                indent_level += 1
            elif stripped.rstrip().endswith('(') and not stripped.startswith(('if', 'for', 'while', 'function')):
                indent_level += 1
            elif stripped.rstrip().endswith('[') and not stripped.rstrip().endswith('[]'):
                indent_level += 1
        
        # 后处理: 移除多余的空行
        final_lines = []
        empty_count = 0
        for line in formatted_lines:
            if not line.strip():
                empty_count += 1
                if empty_count <= 2:
                    final_lines.append(line)
            else:
                empty_count = 0
                final_lines.append(line)
        
        result = '\n'.join(final_lines)
        
        # 格式化运算符空格
        result = re.sub(r'(\w)=(\w)', r'\1 = \2', result)
        result = re.sub(r'(\w)\+(\w)', r'\1 + \2', result)
        result = re.sub(r'(\w)-(\w)', r'\1 - \2', result)
        result = re.sub(r'(\w)\*(\w)', r'\1 * \2', result)
        result = re.sub(r'(\w)/(\w)', r'\1 / \2', result)
        result = re.sub(r',(\w)', r', \1', result)
        
        return result, None
        
    except Exception as e:
        if ignore_errors:
            return code, f"格式化出错: {str(e)}"
        return code, f"格式化失败: {str(e)}"


def format_code(code: str, language: str, ignore_errors: bool = False) -> Tuple[str, Optional[str]]:
    """
    格式化代码的主函数
    
    Args:
        code: 要格式化的代码字符串
        language: 编程语言 ('python' 或 'javascript')
        ignore_errors: 是否忽略语法错误继续格式化
        
    Returns:
        (formatted_code, error_message) - 格式化后的代码和错误信息(如果有)
    """
    if language.lower() in ['python', 'py']:
        return format_python_code(code, ignore_errors)
    elif language.lower() in ['javascript', 'js']:
        return format_javascript_code(code, ignore_errors)
    else:
        return code, f"不支持的编程语言: {language}"


def format_file(file_path: str, language: Optional[str] = None, ignore_errors: bool = False) -> Tuple[str, Optional[str]]:
    """
    格式化文件
    
    Args:
        file_path: 文件路径
        language: 编程语言，如果不提供则从文件扩展名推断
        ignore_errors: 是否忽略语法错误继续格式化
        
    Returns:
        (formatted_code, error_message) - 格式化后的代码和错误信息(如果有)
    """
    if not os.path.exists(file_path):
        return "", f"文件不存在: {file_path}"
    
    # 从文件扩展名推断语言
    if language is None:
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.py':
            language = 'python'
        elif ext in ['.js', '.jsx']:
            language = 'javascript'
        else:
            return "", f"无法从扩展名推断语言: {ext}"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        return format_code(code, language, ignore_errors)
    except Exception as e:
        return "", f"读取文件失败: {str(e)}"


def register_parser(subparsers):
    """注册 formatter 命令的参数解析器"""
    parser = subparsers.add_parser(
        'format', 
        help='代码格式化工具',
        description='格式化 Python 和 JavaScript 代码,支持错误容忍模式'
    )
    parser.add_argument('--file', '-f', help='要格式化的文件路径')
    parser.add_argument('--language', '-l', choices=['python', 'py', 'javascript', 'js'],
                       help='编程语言 (python/js)')
    parser.add_argument('--input', '-i', help='直接输入要格式化的代码')
    parser.add_argument('--output', '-o', help='输出文件路径 (可选)')
    parser.add_argument('--ignore-errors', action='store_true', 
                       help='忽略语法错误,仍然尝试格式化代码')
    parser.add_argument('--in-place', action='store_true',
                       help='直接修改原文件 (仅对 --file 有效)')
    parser.set_defaults(func=main)


def main(args):
    """formatter 工具的主函数"""
    try:
        formatted_code = None
        error_msg = None
        
        if args.file:
            # 格式化文件
            formatted_code, error_msg = format_file(
                args.file, 
                args.language,
                args.ignore_errors
            )
            
            if error_msg and not args.ignore_errors:
                print(f"❌ {error_msg}")
                return 1
            
            # 决定输出位置
            output_path = args.file if args.in_place else args.output
            
            if output_path:
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(formatted_code)
                status = "⚠️ " if error_msg else "✓ "
                print(f"{status}格式化完成，结果已保存到: {output_path}")
                if error_msg:
                    print(f"警告: {error_msg}")
            else:
                # 输出到控制台
                if error_msg:
                    print(f"⚠️ 警告: {error_msg}\n")
                print(formatted_code)
                
        elif args.input:
            # 格式化直接输入的代码
            if not args.language:
                print("❌ 错误: 直接输入代码时必须指定语言 (--language python/js)")
                return 1
            
            formatted_code, error_msg = format_code(
                args.input, 
                args.language,
                args.ignore_errors
            )
            
            if error_msg and not args.ignore_errors:
                print(f"❌ {error_msg}")
                return 1
            
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(formatted_code)
                status = "⚠️ " if error_msg else "✓ "
                print(f"{status}格式化完成，结果已保存到: {args.output}")
                if error_msg:
                    print(f"警告: {error_msg}")
            else:
                # 输出到控制台
                if error_msg:
                    print(f"⚠️ 警告: {error_msg}\n")
                print(formatted_code)
        else:
            print("❌ 错误: 请提供要格式化的文件 (--file) 或直接输入代码 (--input)")
            return 1
        
        return 0
            
    except Exception as e:
        print(f"❌ 格式化失败: {e}")
        return 1


if __name__ == "__main__":
    # 用于独立测试
    test_python_code = """
def hello(name):
print(f"Hello, {name}!")
if name == "world":
return True
return False
"""
    
    print("=" * 60)
    print("Python 代码格式化测试")
    print("=" * 60)
    print("\n原始代码:")
    print(test_python_code)
    
    formatted, error = format_python_code(test_python_code, ignore_errors=True)
    
    print("\n格式化后:")
    print(formatted)
    
    if error:
        print(f"\n⚠️ 警告: {error}")
    
    # 测试 JavaScript
    test_js_code = """
function test(x){
if(x>0){
console.log("positive");
}else{
console.log("negative");
}
return x*2;
}
"""
    
    print("\n" + "=" * 60)
    print("JavaScript 代码格式化测试")
    print("=" * 60)
    print("\n原始代码:")
    print(test_js_code)
    
    formatted_js, error_js = format_javascript_code(test_js_code)
    
    print("\n格式化后:")
    print(formatted_js)
    
    if error_js:
        print(f"\n⚠️ 警告: {error_js}")


import argparse
import sys
import os
import re
from typing import Optional, Tuple


def format_python_code(code: str, ignore_errors: bool = False) -> Tuple[str, Optional[str]]:
    """
    Format Python code
    Use intelligent indentation and spacing
    
    Args:
        code: Code string to format
        ignore_errors: Whether to ignore syntax errors and attempt formatting
        
    Returns:
        (formatted_code, error_message) - Formatted code and error message (if any)
    """
    import ast
    
    error_msg = None
    
    # Validate syntax first
    try:
        ast.parse(code)
    except SyntaxError as e:
        error_msg = f"Python Syntax Error (Line {e.lineno}): {e.msg}"
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
            
            # Handle empty lines
            if not stripped:
                formatted_lines.append('')
                continue
            
            # Detect multiline strings
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
            
            # Inside multiline string, keep as is
            if in_multiline_string:
                formatted_lines.append('    ' * indent_level + stripped)
                continue
            
            # Handle indentation reduction (else, elif, except, finally, case)
            if stripped.startswith(('else:', 'elif ', 'except:', 'except ', 'finally:', 'case ', 'case:')):
                indent_level = max(0, indent_level - 1)
                formatted_lines.append('    ' * indent_level + stripped)
                indent_level += 1
                continue
            
            # Handle closing brackets/braces
            if stripped.startswith(('}', ']', ')')):
                indent_level = max(0, indent_level - 1)
            
            # Add formatted line
            formatted_lines.append('    ' * indent_level + stripped)
            
            # Handle indentation increase
            if stripped.rstrip().endswith(':'):
                # Function, class, if, for, while, with, try, etc.
                indent_level += 1
            elif stripped.rstrip().endswith(('{', '(')):
                indent_level += 1
            elif stripped.rstrip().endswith('[') and not stripped.rstrip().endswith('[]'):
                indent_level += 1
            
            # Handle indentation decrease - after single line statement
            if indent_level > 0:
                # Check if it is a single line statement (pass, return, break, continue, etc.)
                if any(stripped.startswith(kw) for kw in ['pass', 'return ', 'break', 'continue', 'raise ']):
                    # Check next line, if not same level or deeper indentation, decrease indentation
                    if i + 1 < len(lines):
                        next_line = lines[i + 1].strip()
                        if next_line and not next_line.startswith(('else:', 'elif ', 'except:', 'except ', 'finally:')):
                            # If next line is not empty and not control flow keyword, might need adjustment
                            pass
        
        # Post-processing: Remove excess empty lines, keep at most 2 consecutive empty lines
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
        
        # Add spaces around operators
        result = '\n'.join(final_lines)
        
        # Format operator spaces (simple version)
        # Add spaces around =
        result = re.sub(r'(\w)=(\w)', r'\1 = \2', result)
        result = re.sub(r'(\w)=(\()', r'\1 = \2', result)
        
        # Add spaces around +, -, *, /
        result = re.sub(r'(\w)\+(\w)', r'\1 + \2', result)
        result = re.sub(r'(\w)-(\w)', r'\1 - \2', result)
        result = re.sub(r'(\w)\*(\w)', r'\1 * \2', result)
        result = re.sub(r'(\w)/(\w)', r'\1 / \2', result)
        
        # Add space after comma
        result = re.sub(r',(\w)', r', \1', result)
        
        return result, error_msg
        
    except Exception as e:
        if ignore_errors:
            return code, f"Formatting error: {str(e)}"
        return code, f"Formatting failed: {str(e)}"


def format_javascript_code(code: str, ignore_errors: bool = False) -> Tuple[str, Optional[str]]:
    """
    Format JavaScript code
    Intelligent indentation and spacing handling
    
    Args:
        code: Code string to format
        ignore_errors: Whether to ignore errors and continue formatting
        
    Returns:
        (formatted_code, error_message) - Formatted code and error message (if any)
    """
    try:
        lines = code.split('\n')
        formatted_lines = []
        indent_level = 0
        in_multiline_comment = False
        
        for line in lines:
            stripped = line.strip()
            
            # Handle empty lines
            if not stripped:
                formatted_lines.append('')
                continue
            
            # Handle multiline comments
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
            
            # Handle closing braces
            if stripped.startswith('}'):
                indent_level = max(0, indent_level - 1)
                formatted_lines.append('  ' * indent_level + stripped)
                # Handle } else {, } catch {, } finally { etc.
                if '{' in stripped:
                    indent_level += 1
                continue
            
            # Handle closing brackets and parentheses
            if stripped.startswith((']', ')')):
                indent_level = max(0, indent_level - 1)
            
            # Add formatted line
            formatted_lines.append('  ' * indent_level + stripped)
            
            # Handle indentation increase
            if stripped.rstrip().endswith('{'):
                indent_level += 1
            elif stripped.rstrip().endswith('(') and not stripped.startswith(('if', 'for', 'while', 'function')):
                indent_level += 1
            elif stripped.rstrip().endswith('[') and not stripped.rstrip().endswith('[]'):
                indent_level += 1
        
        # Post-processing: Remove excess empty lines
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
        
        # Format operator spaces
        result = re.sub(r'(\w)=(\w)', r'\1 = \2', result)
        result = re.sub(r'(\w)\+(\w)', r'\1 + \2', result)
        result = re.sub(r'(\w)-(\w)', r'\1 - \2', result)
        result = re.sub(r'(\w)\*(\w)', r'\1 * \2', result)
        result = re.sub(r'(\w)/(\w)', r'\1 / \2', result)
        result = re.sub(r',(\w)', r', \1', result)
        
        return result, None
        
    except Exception as e:
        if ignore_errors:
            return code, f"Formatting error: {str(e)}"
        return code, f"Formatting failed: {str(e)}"


def format_code(code: str, language: str, ignore_errors: bool = False) -> Tuple[str, Optional[str]]:
    """
    Main function for code formatting
    
    Args:
        code: Code string to format
        language: Programming language ('python' or 'javascript')
        ignore_errors: Whether to ignore syntax errors and continue formatting
        
    Returns:
        (formatted_code, error_message) - Formatted code and error message (if any)
    """
    if language.lower() in ['python', 'py']:
        return format_python_code(code, ignore_errors)
    elif language.lower() in ['javascript', 'js']:
        return format_javascript_code(code, ignore_errors)
    else:
        return code, f"Unsupported programming language: {language}"


def format_file(file_path: str, language: Optional[str] = None, ignore_errors: bool = False) -> Tuple[str, Optional[str]]:
    """
    Format file
    
    Args:
        file_path: File path
        language: Programming language, inferred from file extension if not provided
        ignore_errors: Whether to ignore syntax errors and continue formatting
        
    Returns:
        (formatted_code, error_message) - Formatted code and error message (if any)
    """
    if not os.path.exists(file_path):
        return "", f"File not found: {file_path}"
    
    # Infer language from file extension
    if language is None:
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.py':
            language = 'python'
        elif ext in ['.js', '.jsx']:
            language = 'javascript'
        else:
            return "", f"Cannot infer language from extension: {ext}"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        return format_code(code, language, ignore_errors)
    except Exception as e:
        return "", f"Failed to read file: {str(e)}"


def register_parser(subparsers):
    """Register parser for formatter command"""
    parser = subparsers.add_parser(
        'format', 
        help='Code Formatting Tool',
        description='Format Python and JavaScript code, supports error tolerance mode'
    )
    parser.add_argument('--file', '-f', help='File path to format')
    parser.add_argument('--language', '-l', choices=['python', 'py', 'javascript', 'js'],
                       help='Programming language (python/js)')
    parser.add_argument('--input', '-i', help='Input code directly')
    parser.add_argument('--output', '-o', help='Output file path (optional)')
    parser.add_argument('--ignore-errors', action='store_true', 
                       help='Ignore syntax errors and try to format')
    parser.add_argument('--in-place', action='store_true',
                       help='Modify file in place (only for --file)')
    parser.set_defaults(func=main)


def main(args):
    """Main function for formatter tool"""
    try:
        formatted_code = None
        error_msg = None
        
        if args.file:
            # Format file
            formatted_code, error_msg = format_file(
                args.file, 
                args.language,
                args.ignore_errors
            )
            
            if error_msg and not args.ignore_errors:
                print(f"❌ {error_msg}")
                return 1
            
            # Determine output location
            output_path = args.file if args.in_place else args.output
            
            if output_path:
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(formatted_code)
                status = "⚠️ " if error_msg else "✓ "
                print(f"{status}Formatting complete, result saved to: {output_path}")
                if error_msg:
                    print(f"Warning: {error_msg}")
            else:
                # Output to console
                if error_msg:
                    print(f"⚠️ Warning: {error_msg}\n")
                print(formatted_code)
                
        elif args.input:
            # Format input code directly
            if not args.language:
                print("❌ Error: Language must be specified when inputting code directly (--language python/js)")
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
                print(f"{status}Formatting complete, result saved to: {args.output}")
                if error_msg:
                    print(f"Warning: {error_msg}")
            else:
                # Output to console
                if error_msg:
                    print(f"⚠️ Warning: {error_msg}\n")
                print(formatted_code)
        else:
            print("❌ Error: Please provide a file to format (--file) or input code directly (--input)")
            return 1
        
        return 0
            
    except Exception as e:
        print(f"❌ Formatting failed: {e}")
        return 1


if __name__ == "__main__":
    # For standalone testing
    test_python_code = """
def hello(name):
print(f"Hello, {name}!")
if name == "world":
return True
return False
"""
    
    print("=" * 60)
    print("Python Code Formatting Test")
    print("=" * 60)
    print("\nOriginal Code:")
    print(test_python_code)
    
    formatted, error = format_python_code(test_python_code, ignore_errors=True)
    
    print("\nFormatted:")
    print(formatted)
    
    if error:
        print(f"\n⚠️ Warning: {error}")
    
    # Test JavaScript
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
    print("JavaScript Code Formatting Test")
    print("=" * 60)
    print("\nOriginal Code:")
    print(test_js_code)
    
    formatted_js, error_js = format_javascript_code(test_js_code)
    
    print("\nFormatted:")
    print(formatted_js)
    
    if error_js:
        print(f"\n⚠️ Warning: {error_js}")
"""
文件差异比较工具

功能：比较两个文本/文件的差异
负责人：待分配
优先级：中
"""

import difflib
from typing import List, Tuple


def compare_text(text1: str, text2: str, context_lines: int = 3) -> str:
    """
    比较两个文本的差异
    
    Args:
        text1: 第一个文本
        text2: 第二个文本
        context_lines: 上下文行数
        
    Returns:
        差异报告字符串
    """
    lines1 = text1.splitlines(keepends=True)
    lines2 = text2.splitlines(keepends=True)
    
    diff = difflib.unified_diff(
        lines1, 
        lines2,
        fromfile='text1',
        tofile='text2',
        lineterm='',
        n=context_lines
    )
    
    return ''.join(diff)


def compare_files(file1: str, file2: str, context_lines: int = 3) -> str:
    """
    比较两个文件的差异
    
    Args:
        file1: 第一个文件路径
        file2: 第二个文件路径
        context_lines: 上下文行数
        
    Returns:
        差异报告字符串
    """
    try:
        with open(file1, 'r', encoding='utf-8') as f1:
            text1 = f1.read()
        with open(file2, 'r', encoding='utf-8') as f2:
            text2 = f2.read()
        
        lines1 = text1.splitlines(keepends=True)
        lines2 = text2.splitlines(keepends=True)
        
        diff = difflib.unified_diff(
            lines1,
            lines2,
            fromfile=file1,
            tofile=file2,
            lineterm='',
            n=context_lines
        )
        
        return ''.join(diff)
    except Exception as e:
        return f"错误: {str(e)}"


def get_similarity(text1: str, text2: str) -> float:
    """
    计算两个文本的相似度
    
    Args:
        text1: 第一个文本
        text2: 第二个文本
        
    Returns:
        相似度 (0-1)
    """
    return difflib.SequenceMatcher(None, text1, text2).ratio()


# GUI 使用的函数
def diff_text(text1: str, text2: str) -> dict:
    """
    比较两个文本并返回详细信息 (用于 GUI)
    
    Returns:
        包含差异信息的字典
    """
    diff = compare_text(text1, text2)
    similarity = get_similarity(text1, text2)
    
    return {
        'diff': diff,
        'similarity': similarity,
        'similarity_percent': f"{similarity * 100:.2f}%"
    }


def main_function(args):
    """CLI 主函数"""
    try:
        if args.file1 and args.file2:
            # 比较文件
            diff = compare_files(args.file1, args.file2, args.context)
            if diff:
                print(diff)
                # 计算相似度
                with open(args.file1, 'r', encoding='utf-8') as f1:
                    text1 = f1.read()
                with open(args.file2, 'r', encoding='utf-8') as f2:
                    text2 = f2.read()
                similarity = get_similarity(text1, text2)
                print(f"\n相似度: {similarity * 100:.2f}%")
            else:
                print("✓ 文件内容相同")
            return 0
            
        elif args.text1 and args.text2:
            # 比较文本
            diff = compare_text(args.text1, args.text2, args.context)
            if diff:
                print(diff)
                similarity = get_similarity(args.text1, args.text2)
                print(f"\n相似度: {similarity * 100:.2f}%")
            else:
                print("✓ 文本内容相同")
            return 0
        else:
            print("❌ 错误: 请提供要比较的文件 (--file1 --file2) 或文本 (--text1 --text2)")
            return 1
            
    except Exception as e:
        print(f"❌ 比较失败: {e}")
        return 1


def register_parser(subparsers):
    """注册 CLI 子命令"""
    parser = subparsers.add_parser(
        'diff',
        help='文本/文件差异比较工具',
        description='比较两个文本或文件的差异,显示详细的差异报告'
    )
    
    # 文件比较选项
    parser.add_argument('--file1', '-f1', help='第一个文件路径')
    parser.add_argument('--file2', '-f2', help='第二个文件路径')
    
    # 文本比较选项
    parser.add_argument('--text1', '-t1', help='第一个文本内容')
    parser.add_argument('--text2', '-t2', help='第二个文本内容')
    
    # 上下文行数
    parser.add_argument('--context', '-c', type=int, default=3,
                       help='显示的上下文行数 (默认: 3)')
    
    parser.set_defaults(func=main_function)

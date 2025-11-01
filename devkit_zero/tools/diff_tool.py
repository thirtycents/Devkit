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

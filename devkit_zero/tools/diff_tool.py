"""
File Difference Comparison Tool

Function: Compare differences between two texts/files
Owner: Unassigned
Priority: Medium
"""

import difflib
from typing import List, Tuple


def compare_text(text1: str, text2: str, context_lines: int = 3) -> str:
    """
    Compare differences between two texts
    
    Args:
        text1: First text
        text2: Second text
        context_lines: Number of context lines
        
    Returns:
        Difference report string
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
    Compare differences between two files
    
    Args:
        file1: First file path
        file2: Second file path
        context_lines: Number of context lines
        
    Returns:
        Difference report string
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
        return f"Error: {str(e)}"


def get_similarity(text1: str, text2: str) -> float:
    """
    Calculate similarity between two texts
    
    Args:
        text1: First text
        text2: Second text
        
    Returns:
        Similarity (0-1)
    """
    return difflib.SequenceMatcher(None, text1, text2).ratio()


def get_side_by_side_diff(text1: str, text2: str, width: int = 40) -> List[str]:
    """
    Generate side-by-side difference comparison
    
    Args:
        text1: First text
        text2: Second text
        width: Column width
        
    Returns:
        List of strings representing side-by-side diff
    """
    lines1 = text1.splitlines()
    lines2 = text2.splitlines()
    
    matcher = difflib.SequenceMatcher(None, lines1, lines2)
    result = []
    
    # Header
    fmt = f"{{:<{width}}} | {{:<{width}}} | {{}}"
    result.append(fmt.format("Text 1", "Text 2", "Op"))
    result.append("-" * (width * 2 + 10))
    
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':
            for k in range(i2 - i1):
                l1 = lines1[i1+k]
                l2 = lines2[j1+k]
                # Truncate if too long
                if len(l1) > width: l1 = l1[:width-3] + "..."
                if len(l2) > width: l2 = l2[:width-3] + "..."
                result.append(fmt.format(l1, l2, ""))
        elif tag == 'replace':
            max_len = max(i2-i1, j2-j1)
            for k in range(max_len):
                l1 = lines1[i1+k] if k < (i2-i1) else ""
                l2 = lines2[j1+k] if k < (j2-j1) else ""
                if len(l1) > width: l1 = l1[:width-3] + "..."
                if len(l2) > width: l2 = l2[:width-3] + "..."
                result.append(fmt.format(l1, l2, "MOD"))
        elif tag == 'delete':
            for k in range(i2-i1):
                l1 = lines1[i1+k]
                if len(l1) > width: l1 = l1[:width-3] + "..."
                result.append(fmt.format(l1, "", "DEL"))
        elif tag == 'insert':
            for k in range(j2-j1):
                l2 = lines2[j1+k]
                if len(l2) > width: l2 = l2[:width-3] + "..."
                result.append(fmt.format("", l2, "ADD"))
                
    return result


def analyze_changes(text1: str, text2: str) -> dict:
    """
    Analyze changes between two texts
    
    Args:
        text1: First text
        text2: Second text
        
    Returns:
        Dictionary with change statistics
    """
    lines1 = text1.splitlines()
    lines2 = text2.splitlines()
    matcher = difflib.SequenceMatcher(None, lines1, lines2)
    
    additions = 0
    deletions = 0
    modifications = 0
    
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'replace':
            modifications += max(i2-i1, j2-j1)
        elif tag == 'delete':
            deletions += (i2-i1)
        elif tag == 'insert':
            additions += (j2-j1)
            
    return {
        'total_lines_1': len(lines1),
        'total_lines_2': len(lines2),
        'additions': additions,
        'deletions': deletions,
        'modifications': modifications,
        'similarity': matcher.ratio(),
        'total_changes': additions + deletions + modifications
    }


# Function used by GUI
def diff_text(text1: str, text2: str) -> dict:
    """
    Compare two texts and return detailed info (for GUI)
    
    Returns:
        Dictionary containing difference info
    """
    diff = compare_text(text1, text2)
    similarity = get_similarity(text1, text2)
    
    return {
        'diff': diff,
        'similarity': similarity,
        'similarity_percent': f"{similarity * 100:.2f}%"
    }


def main_function(args):
    """CLI Main function"""
    try:
        if args.file1 and args.file2:
            # Compare files
            diff = compare_files(args.file1, args.file2, args.context)
            if diff:
                print(diff)
                # Calculate similarity
                with open(args.file1, 'r', encoding='utf-8') as f1:
                    text1 = f1.read()
                with open(args.file2, 'r', encoding='utf-8') as f2:
                    text2 = f2.read()
                similarity = get_similarity(text1, text2)
                print(f"\nSimilarity: {similarity * 100:.2f}%")
            else:
                print("✓ File contents are identical")
            return 0
            
        elif args.text1 and args.text2:
            # Compare texts
            diff = compare_text(args.text1, args.text2, args.context)
            if diff:
                print(diff)
                similarity = get_similarity(args.text1, args.text2)
                print(f"\nSimilarity: {similarity * 100:.2f}%")
            else:
                print("✓ Text contents are identical")
            return 0
        else:
            print("❌ Error: Please provide files (--file1 --file2) or texts (--text1 --text2) to compare")
            return 1
            
    except Exception as e:
        print(f"❌ Comparison failed: {e}")
        return 1


def register_parser(subparsers):
    """Register CLI subcommands"""
    parser = subparsers.add_parser(
        'diff',
        help='Text/File difference comparison tool',
        description='Compare differences between two texts or files, showing detailed difference report'
    )
    
    # File comparison options
    parser.add_argument('--file1', '-f1', help='First file path')
    parser.add_argument('--file2', '-f2', help='Second file path')
    
    # Text comparison options
    parser.add_argument('--text1', '-t1', help='First text content')
    parser.add_argument('--text2', '-t2', help='Second text content')
    
    # Context lines
    parser.add_argument('--context', '-c', type=int, default=3,
                       help='Number of context lines to show (default: 3)')
    
    parser.set_defaults(func=main_function)

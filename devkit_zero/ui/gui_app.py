"""
GUI主应用程序

这个模块实现Tkinter图形界面。
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import re
from typing import Dict, Any

class RegexTester:
    """Regular expression testing tool"""

    def __init__(self):
        self.match_history = []

    def test_pattern(self, pattern: str, text: str, flags: int = 0) -> Dict[str, Any]:
        """
        Test regular expression pattern
        Args:
            pattern: Regular expression pattern
            text: Text to match against
            flags: Regular expression flags
        Returns:
            Dictionary containing match results
        """
        try:
            # Compile regular expression
            regex = re.compile(pattern, flags)

            # Find all matches
            matches = list(regex.finditer(text))

            # Extract match information
            match_info = []
            for match in matches:
                match_info.append({
                    'start': match.start(),
                    'end': match.end(),
                    'group': match.group(),
                    'groups': match.groups()
                })

            # Test replacement functionality
            replaced_text = regex.sub(r'[MATCH]', text)

            result = {
                'success': True,
                'matches': match_info,
                'match_count': len(matches),
                'replaced_text': replaced_text,
                'pattern_valid': True
            }

        except re.error as e:
            result = {
                'success': False,
                'error': str(e),
                'matches': [],
                'match_count': 0,
                'replaced_text': text,
                'pattern_valid': False
            }

        # Save to history
        self.match_history.append({
            'pattern': pattern,
            'text': text,
            'result': result
        })

        return result


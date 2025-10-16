# Regular expression testing tool implementation
import re
from typing import List, Tuple, Dict, Any

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

    def get_common_patterns(self) -> Dict[str, str]:
        """Get common regular expression patterns"""
        return {
            'Email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'URL': r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+',
            'Phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            'IP Address': r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b',
            'Date (YYYY-MM-DD)': r'\b\d{4}-\d{2}-\d{2}\b',
            'HTML Tag': r'<[^>]+>',
            'Number': r'\b\d+\b'
        }

    def clear_history(self):
        """Clear match history"""
        self.match_history.clear()

# Create global instance
regex_tester = RegexTester()
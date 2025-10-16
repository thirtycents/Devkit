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
            # Email and Contact
            'Email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'Email (Simple)': r'\S+@\S+\.\S+',
            # URLs and Web
            'URL': r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+',
            'URL with Path': r'https?://[^\s/$.?#].[^\s]*',
            'Domain Name': r'\b([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}\b',
            # Phone Numbers
            'Phone (US)': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            'Phone (International)': r'\+\d{1,3}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}',
            'Phone (with Extension)': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\s*(?:ext\.?|x)\s*\d{1,5}',
            # Network
            'IP Address': r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b',
            'IP Address (with Port)': r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}:\d{1,5}\b',
            'MAC Address': r'([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})',
            'IPv6 Address': r'(?:[A-F0-9]{1,4}:){7}[A-F0-9]{1,4}',
        }

    def clear_history(self):
        """Clear match history"""
        self.match_history.clear()

# Create global instance
regex_tester = RegexTester()
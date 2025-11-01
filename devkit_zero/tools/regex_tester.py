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
            # Dates and Times
            'Date (YYYY-MM-DD)': r'\b\d{4}-\d{2}-\d{2}\b',
            'Date (MM/DD/YYYY)': r'\b(0[1-9]|1[0-2])/(0[1-9]|[12][0-9]|3[01])/\d{4}\b',
            'Date (DD/MM/YYYY)': r'\b(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}\b',
            'Time (24-hour)': r'\b(?:[01]?[0-9]|2[0-3]):[0-5][0-9](?::[0-5][0-9])?\b',
            'Time (12-hour)': r'\b(1[0-2]|0?[1-9]):[0-5][0-9]\s?(?:AM|PM)\b',
            'Timestamp': r'\d{4}-\d{2}-\d{2}[T\s]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})?',
            # Chinese Specific (if needed)
            'Chinese Characters': r'[\u4e00-\u9fff]+',
            'Chinese Mobile': r'\b1[3-9]\d{9}\b',
            'Chinese ID Card': r'\b[1-9]\d{5}(18|19|20)\d{2}((0[1-9])|(1[0-2]))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]\b',
        }

    def clear_history(self):
        """Clear match history"""
        self.match_history.clear()

# Create global instance
regex_tester = RegexTester()
import os
import sys
import json
import csv
import re
import tempfile
import shutil
from pathlib import Path
from xml.etree import ElementTree
from xml.parsers.expat import ExpatError
from io import StringIO

class FormatDetector:
    """
    Unified format detector class, supports JSON, XML, CSV format detection
    """
    
    class JSONDetector:
        """JSON format detector"""
        
        def detect(self, content):
            content = content.strip()
            
            if not content:
                return {
                    'is_valid': False,
                    'confidence': 0,
                    'error': 'Content is empty'
                }
            
            starts_with_brace = content.startswith('{') or content.startswith('[')
            
            try:
                parsed = json.loads(content)
                
                confidence = 0.9
                
                if starts_with_brace:
                    confidence += 0.05
                    
                if isinstance(parsed, (dict, list)):
                    confidence += 0.05
                    
                return {
                    'is_valid': True,
                    'confidence': min(confidence, 1.0),
                    'parsed_type': type(parsed).__name__,
                    'size': len(content),
                    'details': f'Valid {type(parsed).__name__}'
                }
                
            except json.JSONDecodeError as e:
                confidence = 0.0
                if starts_with_brace:
                    confidence = 0.3
                    
                return {
                    'is_valid': False,
                    'confidence': confidence,
                    'error': f'JSON parsing error: {str(e)}'
                }

    class XMLDetector:
        """XML format detector"""
        
        def detect(self, content):
            content = content.strip()
            
            if not content:
                return {
                    'is_valid': False,
                    'confidence': 0,
                    'error': 'Content is empty'
                }
            
            has_xml_declaration = content.startswith('<?xml')
            
            tag_pattern = r'<[^>]+>'
            tags = re.findall(tag_pattern, content)
            
            if not tags:
                return {
                    'is_valid': False,
                    'confidence': 0,
                    'error': 'No XML tags found'
                }
            
            try:
                root = ElementTree.fromstring(content)
                
                confidence = 0.8
                
                if has_xml_declaration:
                    confidence += 0.1
                    
                if len(tags) > 1:
                    confidence += 0.1
                    
                return {
                    'is_valid': True,
                    'confidence': min(confidence, 1.0),
                    'root_tag': root.tag,
                    'tag_count': len(list(root.iter())),
                    'details': f'Root element: {root.tag}, Total {len(list(root.iter()))} elements'
                }
                
            except ExpatError as e:
                confidence = 0.3 if has_xml_declaration or len(tags) > 1 else 0.1
                
                return {
                    'is_valid': False,
                    'confidence': confidence,
                    'error': f'XML parsing error: {str(e)}'
                }

    class CSVDetector:
        """CSV format detector"""
        
        def detect(self, content):
            content = content.strip()
            
            if not content:
                return {
                    'is_valid': False,
                    'confidence': 0,
                    'error': 'Content is empty'
                }
            
            lines = content.split('\n')
            if not lines:
                return {
                    'is_valid': False,
                    'confidence': 0,
                    'error': 'No data rows found'
                }
            
            comma_count = content.count(',')
            semicolon_count = content.count(';')
            tab_count = content.count('\t')
            pipe_count = content.count('|')
            
            delimiter_candidates = [
                (',', comma_count),
                (';', semicolon_count),
                ('\t', tab_count),
                ('|', pipe_count)
            ]
            most_common_delimiter = max(delimiter_candidates, key=lambda x: x[1])[0]
            
            try:
                reader = csv.reader(StringIO(content), delimiter=most_common_delimiter)
                rows = list(reader)
                
                if len(rows) < 1:
                    return {
                        'is_valid': False,
                        'confidence': 0,
                        'error': 'No valid data rows'
                    }
                
                confidence = 0.6
                
                if len(rows) > 1:
                    confidence += 0.2
                    
                col_counts = [len(row) for row in rows]
                if len(set(col_counts)) == 1 and col_counts[0] > 1:
                    confidence += 0.2
                    
                return {
                    'is_valid': True,
                    'confidence': min(confidence, 1.0),
                    'delimiter': most_common_delimiter,
                    'row_count': len(rows),
                    'column_count': len(rows[0]) if rows else 0,
                    'details': f'{len(rows)} rows × {len(rows[0]) if rows else 0} columns, delimiter: "{most_common_delimiter}"'
                }
                
            except Exception as e:
                confidence = 0.0
                if len(lines) > 1 and (comma_count > 0 or semicolon_count > 0 or tab_count > 0):
                    confidence = 0.4
                    
                return {
                    'is_valid': False,
                    'confidence': confidence,
                    'error': f'CSV parsing error: {str(e)}'
                }

    def __init__(self):
        """Initialize detector"""
        self.detectors = {
            'json': self.JSONDetector(),
            'xml': self.XMLDetector(),
            'csv': self.CSVDetector()
        }
    
    def detect_file(self, file_path):
        """Detect file format"""
        if not os.path.exists(file_path):
            return {'error': f'File does not exist: {file_path}'}
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return {'error': f'Cannot read file: {e}'}
        
        return self.detect_content(content, file_path)
    
    def detect_content(self, content, filename=None):
        """Detect content format"""
        if not content.strip():
            return {'error': 'Content is empty'}
        
        results = {
            'filename': filename,
            'content_preview': content[:200] + '...' if len(content) > 200 else content,
            'detections': {}
        }
        
        for format_name, detector in self.detectors.items():
            try:
                detection_result = detector.detect(content)
                results['detections'][format_name] = detection_result
            except Exception as e:
                results['detections'][format_name] = {
                    'is_valid': False,
                    'confidence': 0,
                    'error': str(e)
                }
        
        results['most_likely_format'] = self._get_most_likely_format(results['detections'])
        
        return results
    
    def _get_most_likely_format(self, detections):
        """Get most likely format"""
        valid_formats = {
            fmt: details['confidence'] 
            for fmt, details in detections.items() 
            if details.get('is_valid', False)
        }
        
        if not valid_formats:
            return 'unknown'
        
        return max(valid_formats.items(), key=lambda x: x[1])[0]

    def batch_detect(self, directory_path):
        """Batch detect files in directory"""
        directory = Path(directory_path)
        if not directory.exists() or not directory.is_dir():
            return {'error': f'Directory does not exist: {directory_path}'}
        
        results = {}
        supported_extensions = {'.txt', '.json', '.xml', '.csv', '.log', '.conf', '.config'}
        
        for file_path in directory.glob('*'):
            if file_path.is_file() and (file_path.suffix.lower() in supported_extensions or file_path.suffix == ''):
                try:
                    results[file_path.name] = self.detect_file(str(file_path))
                except Exception as e:
                    results[file_path.name] = {'error': str(e)}
        
        return results

    @staticmethod
    def print_detection_result(result, verbose=False):
        """Print detection result"""
        if 'error' in result:
            print(f"Error: {result['error']}")
            return
        
        print(f"File: {result.get('filename', 'N/A')}")
        print(f"Content preview: {result.get('content_preview', 'N/A')}")
        print("\nDetection results:")
        
        for format_name, detection in result['detections'].items():
            status = "✓ Valid" if detection.get('is_valid', False) else "✗ Invalid"
            confidence = detection.get('confidence', 0)
            print(f"  {format_name.upper():6} : {status} (confidence: {confidence:.2f})")
            
            if verbose and detection.get('is_valid', False):
                details = detection.get('details', '')
                if details:
                    print(f"          Details: {details}")
            
            if verbose and detection.get('error'):
                print(f"          Error: {detection['error']}")
        
        print(f"\nMost likely format: {result.get('most_likely_format', 'unknown').upper()}")


# Usage example
if __name__ == "__main__":
    # Create detector instance
    detector = FormatDetector()
    
    # Test content detection
    json_content = '{"name": "John", "age": 30}'
    result = detector.detect_content(json_content, "test.json")
    detector.print_detection_result(result, verbose=True)
    
    print("\n" + "="*50 + "\n")
    
    # Test file detection
    # detector.print_detection_result(detector.detect_file("example.json"))
    
    print("✅ Format detector class defined successfully!")

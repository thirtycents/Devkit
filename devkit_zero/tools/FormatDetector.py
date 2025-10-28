Complete Format Detector - Core Functionality
支持 JSON、XML、CSV 格式检测的核心类
"""

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


class CompleteFormatDetector:
    """
    完整格式检测器 - 核心功能
    支持 JSON、XML、CSV 格式检测
    """
    
    def __init__(self):
        self.supported_formats = ['json', 'xml', 'csv']
        self.test_results = {}
        
    def detect_json(self, content):
        """检测 JSON 格式"""
        content = content.strip()
        
        if not content:
            return {
                'is_valid': False,
                'confidence': 0,
                'error': '内容为空'
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
                'details': f'有效的 {type(parsed).__name__}'
            }
            
        except json.JSONDecodeError as e:
            confidence = 0.0
            if starts_with_brace:
                confidence = 0.3
                
            return {
                'is_valid': False,
                'confidence': confidence,
                'error': f'JSON 解析错误: {str(e)}'
            }
    
    def detect_xml(self, content):
        """检测 XML 格式"""
        content = content.strip()
        
        if not content:
            return {
                'is_valid': False,
                'confidence': 0,
                'error': '内容为空'
            }
        
        has_xml_declaration = content.startswith('<?xml')
        
        tag_pattern = r'<[^>]+>'
        tags = re.findall(tag_pattern, content)
        
        if not tags:
            return {
                'is_valid': False,
                'confidence': 0,
                'error': '未找到 XML 标签'
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
                'details': f'根元素: {root.tag}, 共 {len(list(root.iter()))} 个元素'
            }
            
        except ExpatError as e:
            confidence = 0.3 if has_xml_declaration or len(tags) > 1 else 0.1
            
            return {
                'is_valid': False,
                'confidence': confidence,
                'error': f'XML 解析错误: {str(e)}'
            }
    
    def detect_csv(self, content):
        """检测 CSV 格式"""
        content = content.strip()
        
        if not content:
            return {
                'is_valid': False,
                'confidence': 0,
                'error': '内容为空'
            }
        
        lines = content.split('\n')
        if not lines:
            return {
                'is_valid': False,
                'confidence': 0,
                'error': '未找到数据行'
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
                    'error': '无有效数据行'
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
                'details': f'{len(rows)} 行 × {len(rows[0]) if rows else 0} 列, 分隔符: "{most_common_delimiter}"'
            }
            
        except Exception as e:
            confidence = 0.0
            if len(lines) > 1 and (comma_count > 0 or semicolon_count > 0 or tab_count > 0):
                confidence = 0.4
                
            return {
                'is_valid': False,
                'confidence': confidence,
                'error': f'CSV 解析错误: {str(e)}'
            }
    
    def detect_content(self, content, filename=None):
        """
        检测文本内容的格式
        
        Args:
            content: 要分析的文本内容
            filename: 可选的文件名参考
            
        Returns:
            包含检测结果的字典
        """
        if not content.strip():
            return {'error': '内容为空'}
        
        results = {
            'filename': filename,
            'content_preview': content[:200] + '...' if len(content) > 200 else content,
            'detections': {}
        }
        
        # 检测每种格式
        detection_methods = {
            'json': self.detect_json,
            'xml': self.detect_xml,
            'csv': self.detect_csv
        }
        
        for format_name, detector in detection_methods.items():
            try:
                detection_result = detector(content)
                results['detections'][format_name] = detection_result
            except Exception as e:
                results['detections'][format_name] = {
                    'is_valid': False,
                    'confidence': 0,
                    'error': str(e)
                }
        
        # 确定最可能的格式
        results['most_likely_format'] = self._get_most_likely_format(results['detections'])
        
        return results
    
    def detect_file(self, file_path):
        """
        检测文件格式
        
        Args:
            file_path: 要分析的文件路径
            
        Returns:
            包含检测结果的字典
        """
        if not os.path.exists(file_path):
            return {'error': f'文件不存在: {file_path}'}
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            try:
                with open(file_path, 'r', encoding='latin-1') as f:
                    content = f.read()
            except Exception as e:
                return {'error': f'无法读取文件: {e}'}
        except Exception as e:
            return {'error': f'文件读取失败: {e}'}
        
        return self.detect_content(content, file_path)
    
    def batch_detect(self, directory_path):
        """
        批量检测目录中的文件格式
        
        Args:
            directory_path: 包含文件的目录路径
            
        Returns:
            以文件名为键，检测结果为值的字典
        """
        directory = Path(directory_path)
        if not directory.exists() or not directory.is_dir():
            return {'error': f'目录不存在: {directory_path}'}
        
        results = {}
        supported_extensions = {'.txt', '.json', '.xml', '.csv', '.log', '.conf', '.config'}
        
        for file_path in directory.glob('*'):
            if file_path.is_file() and (file_path.suffix.lower() in supported_extensions or file_path.suffix == ''):
                try:
                    results[file_path.name] = self.detect_file(str(file_path))
                except Exception as e:
                    results[file_path.name] = {'error': str(e)}
        
        return results
    
    def _get_most_likely_format(self, detections):
        """根据置信度分数确定最可能的格式"""
        valid_formats = {
            fmt: details['confidence'] 
            for fmt, details in detections.items() 
            if details.get('is_valid', False)
        }
        
        if not valid_formats:
            return 'unknown'
        
        return max(valid_formats.items(), key=lambda x: x[1])[0]
    
    def print_result(self, result, verbose=False):
        """打印格式化的检测结果"""
        if 'error' in result:
            print(f"错误: {result['error']}")
            return
        
        print(f"文件: {result.get('filename', 'N/A')}")
        print(f"内容预览: {result.get('content_preview', 'N/A')}")
        print("\n检测结果:")
        
        for format_name, detection in result['detections'].items():
            status = "✓ 有效" if detection.get('is_valid', False) else "✗ 无效"
            confidence = detection.get('confidence', 0)
            print(f"  {format_name.upper():6} : {status} (置信度: {confidence:.2f})")
            
            if verbose and detection.get('is_valid', False):
                details = detection.get('details', '')
                if details:
                    print(f"          详情: {details}")
            
            if verbose and detection.get('error'):
                print(f"          错误: {detection['error']}")
        
        print(f"\n最可能的格式: {result.get('most_likely_format', 'unknown').upper()}")

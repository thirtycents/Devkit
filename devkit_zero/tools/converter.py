"""
格式转换工具

功能：JSON/CSV/YAML格式互转
负责人：待分配
优先级：中
"""

# TODO: 实现格式转换功能
import argparse
import json
import csv
import os
from typing import Any, Dict, List


def json_to_csv(json_data: Any, output_path: str = None) -> str:
    """将 JSON 数据转换为 CSV 格式"""
    if isinstance(json_data, str):
        data = json.loads(json_data)
    else:
        data = json_data

    if not isinstance(data, list):
        raise ValueError("JSON 数据必须是列表格式才能转换为 CSV")

    if not data:
        return ""

    # 获取所有可能的字段
    fieldnames = set()
    for item in data:
        if isinstance(item, dict):
            fieldnames.update(item.keys())

    fieldnames = sorted(list(fieldnames))

    if output_path:
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        return f"CSV 文件已保存到: {output_path}"
    else:
        import io
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
        return output.getvalue()


def csv_to_json(csv_data: str, output_path: str = None) -> str:
    """将 CSV 数据转换为 JSON 格式"""
    import io

    if os.path.exists(csv_data):
        # 如果是文件路径
        with open(csv_data, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            data = list(reader)
    else:
        # 如果是 CSV 字符串
        reader = csv.DictReader(io.StringIO(csv_data))
        data = list(reader)

    json_str = json.dumps(data, ensure_ascii=False, indent=2)

    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(json_str)
        return f"JSON 文件已保存到: {output_path}"
    else:
        return json_str


def register_parser(subparsers):
    """注册 converter 命令的参数解析器"""
    parser = subparsers.add_parser('convert', help='数据格式转换工具')
    parser.add_argument('--input', '-i', required=True, help='输入文件或数据')
    parser.add_argument('--from', dest='from_format', required=True,
                        choices=['json', 'csv'], help='源格式')
    parser.add_argument('--to', dest='to_format', required=True,
                        choices=['json', 'csv'], help='目标格式')
    parser.add_argument('--output', '-o', help='输出文件路径')
    parser.set_defaults(func=main)


def main(args):
    """converter 工具的主函数"""
    try:
        if args.from_format == 'json' and args.to_format == 'csv':
            return json_to_csv(args.input, args.output)
        elif args.from_format == 'csv' and args.to_format == 'json':
            return csv_to_json(args.input, args.output)
        else:
            raise ValueError(f"不支持从 {args.from_format} 转换到 {args.to_format}")
    except Exception as e:
        raise RuntimeError(f"转换失败: {e}")


if __name__ == "__main__":
    # 测试代码
    test_json = '[{"name": "张三", "age": 25}, {"name": "李四", "age": 30}]'
    print("JSON to CSV:")
    print(json_to_csv(test_json))

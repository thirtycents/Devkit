"""
Format Conversion Tool

Function: JSON/CSV/YAML format conversion
Owner: Unassigned
Priority: Medium
"""

# TODO: Implement format conversion functionality
import argparse
import json
import csv
import os
from typing import Any, Dict, List


def json_to_csv(json_data: Any, output_path: str = None) -> str:
    """Convert JSON data to CSV format"""
    if isinstance(json_data, str):
        data = json.loads(json_data)
    else:
        data = json_data

    if not isinstance(data, list):
        raise ValueError("JSON data must be a list to convert to CSV")

    if not data:
        return ""

    # Get all possible fields
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
        return f"CSV file saved to: {output_path}"
    else:
        import io
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
        return output.getvalue()


def csv_to_json(csv_data: str, output_path: str = None) -> str:
    """Convert CSV data to JSON format"""
    import io

    if os.path.exists(csv_data):
        # If it is a file path
        with open(csv_data, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            data = list(reader)
    else:
        # If it is a CSV string
        reader = csv.DictReader(io.StringIO(csv_data))
        data = list(reader)

    json_str = json.dumps(data, ensure_ascii=False, indent=2)

    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(json_str)
        return f"JSON file saved to: {output_path}"
    else:
        return json_str


def register_parser(subparsers):
    """Register parser for converter command"""
    parser = subparsers.add_parser('convert', help='Data format conversion tool')
    parser.add_argument('--input', '-i', required=True, help='Input file or data')
    parser.add_argument('--from', dest='from_format', required=True,
                        choices=['json', 'csv'], help='Source format')
    parser.add_argument('--to', dest='to_format', required=True,
                        choices=['json', 'csv'], help='Target format')
    parser.add_argument('--output', '-o', help='Output file path')
    parser.set_defaults(func=main)


def main(args):
    """Main function for converter tool"""
    try:
        if args.from_format == 'json' and args.to_format == 'csv':
            return json_to_csv(args.input, args.output)
        elif args.from_format == 'csv' and args.to_format == 'json':
            return csv_to_json(args.input, args.output)
        else:
            raise ValueError(f"Conversion from {args.from_format} to {args.to_format} is not supported")
    except Exception as e:
        raise RuntimeError(f"Conversion failed: {e}")


if __name__ == "__main__":
    # Test code
    test_json = '[{"name": "Zhang San", "age": 25}, {"name": "Li Si", "age": 30}]'
    print("JSON to CSV:")
    print(json_to_csv(test_json))

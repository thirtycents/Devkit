"""
Robots Checker - Check website's robots.txt rules

Detailed Description:
- Input a URL to retrieve and parse the corresponding robots.txt rules
- Display allowed and disallowed crawler paths
- Extract sitemap information
- Show crawler restrictions such as delay

Author: Linjunyu
Creation Date: 2024-XX-XX
"""

import argparse
import sys
import re
import requests
from urllib.parse import urlparse, urljoin
from typing import Dict, List, Optional, Any


# =============================================================================
# Core Functionality
# =============================================================================

def core_logic(url: str, **options) -> Dict[str, Any]:
    """
    Core logic: Retrieve and parse robots.txt rules

    Args:
        url: URL of the website to check
       ** options: Optional parameters such as timeout

    Returns:
        Dictionary containing robots rules information

    Raises:
        ValueError: When input URL is invalid
        ConnectionError: When network connection fails
    """
    # Validate URL
    parsed_url = urlparse(url)
    if not parsed_url.scheme or not parsed_url.netloc:
        raise ValueError("Invalid URL, please include protocol (http/https) and domain name")

    # Construct robots.txt URL
    robots_url = urljoin(url, "/robots.txt")

    try:
        # Send request
        timeout = options.get('timeout', 10)
        response = requests.get(robots_url, timeout=timeout)

        if response.status_code != 200:
            return {
                'success': False,
                'message': f"Failed to retrieve robots.txt, status code: {response.status_code}",
                'url': robots_url,
                'content': None,
                'rules': None
            }

        # Parse content
        content = response.text
        rules = parse_robots(content)

        return {
            'success': True,
            'message': "Successfully retrieved robots.txt",
            'url': robots_url,
            'content': content,
            'rules': rules
        }

    except requests.exceptions.Timeout:
        raise ConnectionError(f"Connection timed out after {timeout} seconds")
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Network request error: {str(e)}")


def parse_robots(content: str) -> Dict[str, Any]:
    """Parse robots.txt content"""
    rules = {
        'user_agents': {},
        'sitemaps': [],
        'crawl_delay': None,
        'host': None
    }

    current_agent = None
    lines = [line.strip() for line in content.split('\n')]

    for line in lines:
        # Ignore comments and empty lines
        if not line or line.startswith('#'):
            continue

        # Split key-value pairs
        parts = re.split(r':\s*', line, 1)
        if len(parts) != 2:
            continue

        key, value = parts[0].lower(), parts[1]

        # Handle User-agent
        if key == 'user-agent':
            current_agent = value
            if current_agent not in rules['user_agents']:
                rules['user_agents'][current_agent] = {
                    'allow': [],
                    'disallow': []
                }

        # Handle Allow
        elif key == 'allow' and current_agent:
            rules['user_agents'][current_agent]['allow'].append(value)

        # Handle Disallow
        elif key == 'disallow' and current_agent:
            rules['user_agents'][current_agent]['disallow'].append(value)

        # Handle Crawl-delay
        elif key == 'crawl-delay' and current_agent:
            rules['crawl_delay'] = value

        # Handle Sitemap
        elif key == 'sitemap':
            rules['sitemaps'].append(value)

        # Handle Host
        elif key == 'host' and not rules['host']:
            rules['host'] = value

    return rules


# =============================================================================
# CLI Interface Functions (Required)
# =============================================================================

def validate_args(args: argparse.Namespace) -> bool:
    """Validate command line arguments"""
    if not args.url:
        return False

    # Simple URL format validation
    return re.match(r'^https?://', args.url) is not None


def main_function(args: argparse.Namespace) -> int:
    """
    Main tool function - CLI entry point

    Args:
        args: Parsed command line arguments object

    Returns:
        Exit code:
        - 0: Success
        - 1: General error
        - 2: Argument error
    """
    try:
        # 1. Validate arguments
        if not validate_args(args):
            print("Error: Invalid URL, please ensure it includes http:// or https://", file=sys.stderr)
            return 2

        # 2. Call core logic
        result = core_logic(
            args.url,
            timeout=args.timeout
        )

        # 3. Process output
        print(f"Check result: {result['message']}")
        print(f"Robots URL: {result['url']}\n")

        if result['success'] and result['content']:
            if args.raw:
                print("Raw content:")
                print("-" * 60)
                print(result['content'])
                print("-" * 60)
            else:
                # Display parsed rules
                rules = result['rules']

                if rules['host']:
                    print(f"Host: {rules['host']}")

                if rules['crawl_delay']:
                    print(f"Crawl delay: {rules['crawl_delay']} seconds")

                if rules['sitemaps']:
                    print("\nSitemaps:")
                    for sitemap in rules['sitemaps']:
                        print(f"- {sitemap}")

                print("\nUser agent rules:")
                for agent, agent_rules in rules['user_agents'].items():
                    print(f"\nUser-agent: {agent}")

                    if agent_rules['allow']:
                        print("  Allowed:")
                        for path in agent_rules['allow']:
                            print(f"    - {path}")

                    if agent_rules['disallow']:
                        print("  Disallowed:")
                        for path in agent_rules['disallow']:
                            print(f"    - {path}")

        return 0

    except ValueError as e:
        print(f"Argument error: {str(e)}", file=sys.stderr)
        return 2
    except ConnectionError as e:
        print(f"Connection error: {str(e)}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error occurred: {str(e)}", file=sys.stderr)
        return 1


def register_parser(subparsers) -> None:
    """Register CLI subcommand"""
    parser = subparsers.add_parser(
        'robots_checker',
        help='Check website robots.txt rules',
        description='Retrieve and parse robots.txt rules for specified website, showing allowed and disallowed crawler paths'
    )

    parser.add_argument(
        'url',
        help='URL of the website to check (including http:// or https://)'
    )

    parser.add_argument(
        '-t', '--timeout',
        type=int,
        default=10,
        help='Request timeout in seconds, default 10 seconds'
    )

    parser.add_argument(
        '-r', '--raw',
        action='store_true',
        help='Display raw robots.txt content without parsing'
    )
    
    # Set command handler function
    parser.set_defaults(func=main_function)

def main():
    """Standalone execution entry point"""
    parser = argparse.ArgumentParser(description='Robots Rules Checker Tool')
    register_parser(parser.add_subparsers(dest='command'))
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    sys.exit(main_function(args))


if __name__ == '__main__':
    main()
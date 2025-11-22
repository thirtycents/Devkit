"""
Port Checker Tool
Check port usage and corresponding processes
"""

import argparse
import socket
import subprocess
import sys
import os
from typing import List, Dict, Any, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed


def check_port(host: str, port: int, timeout: int = 3) -> Dict[str, Any]:
    """
    Check if port is in use
    Args:
        host: Host address
        port: Port number
        timeout: Connection timeout
    Returns:
        Port check result
    """
    result = {
        'host': host,
        'port': port,
        'is_open': False,
        'is_listening': False,
        'process_info': None
    }
    
    # Check if port is open
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        connection_result = sock.connect_ex((host, port))
        sock.close()
        result['is_open'] = _try_connect_all(host, port, timeout)
    except socket.error:
        result['is_open'] = False
    
    # Check if port is listening
    try:
        if sys.platform.startswith('win'):
            # Windows system
            cmd = f'netstat -ano | findstr :{port}'
            output = subprocess.check_output(cmd, shell=True, text=True, encoding='gbk')
            if output:
                result['is_listening'] = True
                result['process_info'] = parse_windows_netstat(output)
        else:
            # Linux system
            cmd = f'netstat -tulpn | grep :{port}'
            output = subprocess.check_output(cmd, shell=True, text=True)
            if output:
                result['is_listening'] = True
                result['process_info'] = parse_unix_netstat(output)
    except subprocess.CalledProcessError:
        pass
    except Exception:
        pass
    
    return result

def _try_connect_all(host: str, port: int, timeout: int) -> bool:
    # Try connecting to host:port for each address family (IPv4/IPv6), consider open if any succeeds
    try:
        infos = socket.getaddrinfo(host, port, 0, socket.SOCK_STREAM)
    except socket.gaierror:
        return False

    for family, socktype, proto, _, sockaddr in infos:
        try:
            s = socket.socket(family, socktype, proto)
            s.settimeout(timeout)
            ok = (s.connect_ex(sockaddr) == 0)
            s.close()
            if ok:
                return True
        except OSError:
            pass
    return False

def parse_windows_netstat(output: str) -> List[Dict[str, str]]:
    # Parse Windows netstat output
    processes = []
    lines = output.strip().split('\n')
    
    for line in lines:
        parts = line.split()
        if len(parts) >= 5:
            pid = parts[-1]
            try:
                # Get process name
                cmd = f'tasklist /FI "PID eq {pid}" /FO CSV /NH'
                task_output = subprocess.check_output(cmd, shell=True, text=True, encoding='gbk')
                if task_output:
                    process_name = task_output.split(',')[0].strip('"')
                else:
                    process_name = "Unknown"
            except:
                process_name = "Unknown"
            
            processes.append({
                'pid': pid,
                'name': process_name,
                'protocol': parts[0],
                'local_address': parts[1],
                'state': parts[3] if len(parts) > 3 else 'N/A'
            })
    
    return processes


def parse_unix_netstat(output: str) -> List[Dict[str, str]]:
    # Parse Unix/Linux netstat output
    processes = []
    lines = output.strip().split('\n')
    
    for line in lines:
        parts = line.split()
        if len(parts) >= 7:
            pid_program = parts[-1]
            if '/' in pid_program:
                pid, program = pid_program.split('/', 1)
            else:
                pid = pid_program
                program = "Unknown"
            
            processes.append({
                'pid': pid,
                'name': program,
                'protocol': parts[0],
                'local_address': parts[3],
                'state': parts[5] if len(parts) > 5 else 'N/A'
            })
    
    return processes

'''
def scan_ports(host: str, start_port: int, end_port: int) -> List[Dict[str, Any]]:
    """
    Scan port range
    
    Args:
        host: Host address
        start_port: Start port
        end_port: End port
        
    Returns:
        List of open ports
    """
    open_ports = []
    
    for port in range(start_port, end_port + 1):
        result = check_port(host, port, timeout=1)
        if result['is_open']:
            open_ports.append(result)
    
    return open_ports
'''
def _resolve_host_once(host):
    # Pre-resolve host, get (family, sockaddr_base) once for reuse
    infos = socket.getaddrinfo(host, None, 0, socket.SOCK_STREAM)
    seen = []
    for fam, socktype, proto, _, sockaddr in infos:
        addr = sockaddr[0]
        if (fam, addr) not in seen:
            seen.append((fam, addr))
    return seen

def _try_connect_family(family, addr, port, timeout):
    try:
        s = socket.socket(family, socket.SOCK_STREAM)
        s.settimeout(timeout)
        ok = (s.connect_ex((addr, port)) == 0)
        s.close()
        return ok
    except OSError:
        return False

def scan_ports(host: str, start_port: int, end_port: int, *,
               timeout: float = 0.4, max_workers: int = 200):
    # Concurrent port scanning
    if end_port < start_port:
        raise ValueError("End port must be greater than start port")
    families = _resolve_host_once(host)

    def check_one(p):
        for fam, addr in families:
            if _try_connect_family(fam, addr, p, timeout):
                # Only fill core information
                return {'host': host, 'port': p, 'is_open': True,
                        'is_listening': False, 'process_info': None}
        return None

    open_ports = []
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futs = {ex.submit(check_one, p): p for p in range(start_port, end_port+1)}
        for fut in as_completed(futs):
            res = fut.result()
            if res:
                open_ports.append(res)
    # If process_info is needed, call check_port(host, p, timeout) again for each open port
    return open_ports

def get_common_ports() -> Dict[int, str]:
    # Get common ports and their services
    return {
        21: "FTP",
        22: "SSH", 
        23: "Telnet",
        25: "SMTP",
        53: "DNS",
        80: "HTTP",
        110: "POP3",
        143: "IMAP",
        443: "HTTPS",
        993: "IMAPS",
        995: "POP3S",
        1433: "SQL Server",
        3306: "MySQL",
        3389: "RDP",
        5432: "PostgreSQL",
        6379: "Redis",
        8080: "HTTP Alt",
        8443: "HTTPS Alt",
        9200: "Elasticsearch",
        27017: "MongoDB"
    }


def format_port_result(result: Dict[str, Any]) -> str:
    # Format port check result
    lines = []
    
    host = result['host']
    port = result['port']
    
    # Get common port service name
    common_ports = get_common_ports()
    service = common_ports.get(port, "Unknown Service")
    
    lines.append(f"Host: {host}")
    lines.append(f"Port: {port} ({service})")
    
    if result['is_open']:
        lines.append("Port Status: Open")
        lines.append("Listening Status: Listening" if result['is_listening'] else "👂 Listening Status: Not Listening")
        
        if result['process_info']:
            lines.append("\nProcess Info:")
            for proc in result['process_info']:
                lines.append(f"  • PID: {proc['pid']}")
                lines.append(f"  • Process Name: {proc['name']}")
                lines.append(f"  • Protocol: {proc['protocol']}")
                lines.append(f"  • Local Address: {proc['local_address']}")
                lines.append(f"  • State: {proc['state']}")
                lines.append("")
    else:
        lines.append("Port Status: Closed or No Response")
        lines.append("Listening Status: Not Listening")
    
    return '\n'.join(lines)


def format_scan_results(results: List[Dict[str, Any]]) -> str:
    """Format port scan results"""
    if not results:
        return "No open ports found in scan range"
    
    lines = []
    lines.append(f"Found {len(results)} open ports:\n")
    
    common_ports = get_common_ports()
    
    for result in results:
        port = result['port']
        service = common_ports.get(port, "Unknown")
        lines.append(f"Port {port} - {service}")
        
        if result['process_info']:
            for proc in result['process_info']:
                lines.append(f"    {proc['name']} (PID: {proc['pid']})")
    
    return '\n'.join(lines)


def register_parser(subparsers):
    # Register port-checker command parser
    parser = subparsers.add_parser('port', help='Port Checker Tool')
    
    subcommands = parser.add_subparsers(dest='action', help='Operation Type')
    
    # Check single port
    check_parser = subcommands.add_parser('check', help='Check specific port')
    check_parser.add_argument('port', type=int, help='Port number')
    check_parser.add_argument('--host', default='localhost', help='Host address (default: localhost)')
    check_parser.add_argument('--timeout', type=int, default=3, help='Connection timeout (seconds)')
    
    # Scan port range
    scan_parser = subcommands.add_parser('scan', help='Scan port range')
    scan_parser.add_argument('--host', default='localhost', help='Host address (default: localhost)')
    scan_parser.add_argument('--start', type=int, default=1, help='Start port (default: 1)')
    scan_parser.add_argument('--end', type=int, default=1000, help='End port (default: 1000)')
    
    # List common ports
    subcommands.add_parser('list', help='List common ports')
    
    parser.set_defaults(func=main)


def main(args):
    # port-checker tool main function
    try:
        if args.action == 'check':
            result = check_port(args.host, args.port, args.timeout)
            return format_port_result(result)
            
        elif args.action == 'scan':
            if args.end <= args.start:
                raise ValueError("End port must be greater than start port")
            
            results = scan_ports(args.host, args.start, args.end)
            return format_scan_results(results)
            
        elif args.action == 'list':
            common_ports = get_common_ports()
            lines = ["Common Ports List:\n"]
            for port in sorted(common_ports):
                lines.append(f"  {port:>5}  - {common_ports[port]}")
            
            return '\n'.join(lines)
            
        else:
            raise ValueError("Please select operation type: check, scan, list")
            
    except Exception as e:
        raise RuntimeError(f"Port check failed: {e}")


if __name__ == "__main__":
    # Test
    print("Port Checker Tool Test:")
    result = check_port('localhost', 80)
    print(format_port_result(result))

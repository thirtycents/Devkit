
# tests/test_tools/test_port_checker.py
# 说明：
# - 使用 unittest（不依赖 pytest），与目录中其它基于类的测试风格一致；
# - 支持：直接运行 `python tests/test_tools/test_port_checker.py`，或 `python -m unittest -v`；
# - 不依赖 netstat/tasklist，仅验证端口连通性与格式化，避免在 CI/课堂环境卡住。

import sys
import time
import socket
import threading
import unittest
from pathlib import Path

from devkit_zero.tools import port_checker


def _start_tcp_server(host="127.0.0.1"):
    """启动一个极小的 TCP 服务：接受连接后立即关闭。
    返回 (port, stop_event, thread)。"""
    srv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv_sock.bind((host, 0))  # 0 表示让操作系统分配临时端口
    srv_sock.listen(5)
    port = srv_sock.getsockname()[1]

    stop = threading.Event()

    def _serve():
        srv_sock.settimeout(0.2)
        try:
            while not stop.is_set():
                try:
                    conn, _ = srv_sock.accept()
                except socket.timeout:
                    continue
                try:
                    conn.close()
                except Exception:
                    pass
        finally:
            try:
                srv_sock.close()
            except Exception:
                pass

    t = threading.Thread(target=_serve, daemon=True)
    t.start()
    return port, stop, t


def _pick_closed_port(host="127.0.0.1"):
    """申请一个空闲端口后立刻释放，作为“很可能关闭”的端口用于测试。"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, 0))
    port = s.getsockname()[1]
    s.close()
    return port


class TestPortChecker(unittest.TestCase):

    def test_check_port_open(self):
        # 准备：启动本地临时 TCP 服务
        port, stop, th = _start_tcp_server()
        try:
            result = port_checker.check_port("127.0.0.1", port, timeout=1)
            self.assertTrue(result.get("is_open"), msg=f"期望端口开放，结果：{result}")
            # 结果格式化 smoke test（不依赖 netstat）
            text = port_checker.format_port_result(result)
            self.assertIn("开放", text)
        finally:
            stop.set()
            th.join(timeout=1)

    def test_check_port_closed(self):
        closed_port = _pick_closed_port()
        time.sleep(0.05)  # 让端口完全释放
        result = port_checker.check_port("127.0.0.1", closed_port, timeout=0.5)
        self.assertFalse(result.get("is_open"), msg=f"期望端口关闭，结果：{result}")
        text = port_checker.format_port_result(result)
        self.assertIn("关闭或未响应", text)

    def test_scan_ports_find_server(self):
        # 为了避免扫描慢，这里把范围设置为 [port, port]
        port, stop, th = _start_tcp_server()
        try:
            results = port_checker.scan_ports("127.0.0.1", port, port)  # 仅扫描 1 个端口
            found = {r["port"] for r in results}
            self.assertIn(port, found)
            out = port_checker.format_scan_results(results)
            self.assertIn("开放端口", out)
        finally:
            stop.set()
            th.join(timeout=1)

    def test_common_ports_mapping(self):
        common = port_checker.get_common_ports()
        self.assertIn(8080, common)
        self.assertIsInstance(common[8080], str)

    def test_main_list_branch(self):
        # 模拟 argparse.Namespace
        class Args: pass
        args = Args()
        args.action = "list"
        out = port_checker.main(args)
        self.assertIn("常见端口列表", out)


if __name__ == "__main__":
    # 允许单文件直接运行：python tests/test_tools/test_port_checker.py
    unittest.main(verbosity=2)

# -*- coding: utf-8 -*-
import sys, unittest, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[0]  
# 检查上级目录的上级目录是否在系统路径中（确保能导入devkit_zero相关模块）
if str(ROOT.parent.parent) not in sys.path:
    # 假设目录结构：tests/test_tools 与 devkit_zero/ 处于同级目录
    # 将devkit_zero的父目录添加到系统路径
    sys.path.insert(0, str(ROOT.parent.parent)) 

# 为了支持预览功能，需要以模块形式导入（直接按文件名导入会失效）
# 实际项目中，应将该文件移至 devkit_zero/tools/api_contract_diff.py
# 此处仅通过模拟导入路径，验证目标函数是否存在
try:
    from devkit_zero.tools import api_contract_diff as api
except Exception:
    # 降级方案：当仅运行当前文件时，从指定路径导入（需用户确保文件位置正确）
    import importlib.util, os
    p = os.path.join(os.path.dirname(__file__), "..", "..", "devkit_zero", "tools", "api_contract_diff.py")
    spec = importlib.util.spec_from_file_location("api", p)
    api = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(api)

def _v1():
    return {
        "apis": [
            {
                "name": "GetUser",
                "method": "GET",
                "path": "/users/{id}",
                "params": [{"in":"path","name":"id","type":"string","required":True}],
                "responses": {
                    "200": {"type":"object","required":["id"],"properties":{
                        "id":{"type":"string"}, "name":{"type":"string"}
                    }}
                }
            },
            {
                "name": "ListUsers",
                "method": "GET",
                "path": "/users",
                "query": [{"name":"active","type":"boolean","required":False}],
                "responses": {"200":{"type":"object","properties":{"items":{"type":"array","items":{"type":"object","properties":{"id":{"type":"string"}}}}}}}
            }
        ]
    }

def _v2():
    return {
        "apis": [
            {
                "name": "GetUser",
                "method": "GET",
                "path": "/users/{id}",
                "params": [{"in":"path","name":"id","type":"string","required":True}],
                "responses": {"200":{"type":"object","required":["id"],"properties":{"id":{"type":"string"},"email":{"type":"string"}}}}
            },
            {
                "name": "ListUsers",
                "method": "GET",
                "path": "/users",
                "query": [
                    {"name":"active","type":"boolean","required":False},
                    {"name":"page","type":"integer","required":True}
                ],
                "responses": {"200":{"type":"object","properties":{"items":{"type":"array","items":{"type":"object","properties":{"id":{"type":"string"}}}}}}}
            },
            {"name":"CreateUser","method":"POST","path":"/users",
             "request":{"type":"object","required":["name"],"properties":{"name":{"type":"string"}}},
             "responses":{"201":{"type":"object","properties":{"id":{"type":"string"}}}}}
        ]
    }

class TestApiDiff(unittest.TestCase):
    def test_compare(self):
        old = api.parse_contract(text=json.dumps(_v1(), ensure_ascii=False))
        new = api.parse_contract(text=json.dumps(_v2(), ensure_ascii=False))
        rpt = api.compare_contracts(old, new)
        txt = api.format_report_text(rpt)
        self.assertGreater(rpt["summary"]["breaking"], 0)
        self.assertGreater(rpt["summary"]["non_breaking"], 0)
        self.assertIn("POST /users", rpt["added_endpoints"])
        self.assertIn("新增端点", txt)
        self.assertIn("删除字段", txt)

    def test_format_md_json(self):
        old = api.parse_contract(text=json.dumps(_v1(), ensure_ascii=False))
        new = api.parse_contract(text=json.dumps(_v2(), ensure_ascii=False))
        rpt = api.compare_contracts(old, new)
        self.assertTrue(api.format_report_md(rpt).startswith("# 接口契约对比结果"))
        self.assertIn('"breaking"', api.format_report_json(rpt))

if __name__ == "__main__":
    unittest.main(verbosity=2)


# -*- coding: utf-8 -*-
import sys, unittest, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[0]  # adjust when copying into repo
if str(ROOT.parent.parent) not in sys.path:
    # assume structure: tests/test_tools alongside devkit_zero/
    sys.path.insert(0, str(ROOT.parent.parent))

# For download preview we import module as a loose file name won't work; in project move to devkit_zero/tools/api_contract_diff.py
# Here we just verify functions exist by emulating import path.
try:
    from devkit_zero.tools import api_contract_diff as api
except Exception:
    # Fallback when running only this file: import from same dir if user places it there
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

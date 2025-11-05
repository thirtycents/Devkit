# devkit_zero/tools/api_contract_diff.py
from __future__ import annotations

"""
接口契约对比器 (API Contract Diff & Compatibility Check)

- 支持两种输入：
  1) “简化契约 JSON”：{ "apis": [ {method, path, params/query/headers, request, responses}, ... ] }
  2) OpenAPI/Swagger JSON：自动识别并转换为上面的简化结构再对比

- 兼容性规则（简化且保守）：
  * 端点：新增 -> 非破坏；删除 -> 破坏
  * 参数/请求体字段：
      - 新增必填 -> 破坏；新增可选 -> 非破坏；删除 -> 破坏
      - required False->True -> 破坏；True->False -> 非破坏
      - 类型变化 -> 破坏（唯一“放宽”例外：请求/参数里 integer->number 视为非破坏；响应里仍视为破坏）
  * 响应体字段：删除 -> 破坏；新增 -> 非破坏；类型变化 -> 破坏
"""

import json
from typing import Dict, Any, List, Optional


# ---------- 基础IO ----------

def load_json_file(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ---------- OpenAPI 识别与转换 ----------

def _is_openapi_doc(data: dict) -> bool:
    """非常宽松的判定：有 paths 即认为是 OpenAPI 风格 JSON。"""
    return isinstance(data, dict) and "paths" in data


def _resolve_ref(root: dict, ref: str) -> dict:
    """解析本地 $ref（形如 #/components/...）。找不到则返回 {}。"""
    if not isinstance(ref, str) or not ref.startswith("#/"):
        return {}
    node = root
    for key in ref.lstrip("#/").split("/"):
        node = node.get(key, {})
        if not isinstance(node, dict):
            return {}
    return node


def _oas_schema_to_simple(root: dict, schema: dict) -> dict:
    """
    将 OpenAPI schema 转为“简化契约”的 schema（仅保留 type/required/properties/items）。
    处理：$ref、allOf（浅合并）/ object / array / 原子类型
    """
    if not isinstance(schema, dict):
        return {}

    # $ref
    if "$ref" in schema:
        schema = _resolve_ref(root, schema["$ref"])

    # allOf -> 浅合并为 object
    if "allOf" in schema and isinstance(schema["allOf"], list):
        merged = {"type": "object", "properties": {}, "required": []}
        for part in schema["allOf"]:
            part = _oas_schema_to_simple(root, part)
            if not isinstance(part, dict):
                continue
            if part.get("type") == "object":
                merged["properties"].update(part.get("properties", {}) or {})
                merged["required"].extend(part.get("required", []) or [])
        if merged["required"]:
            merged["required"] = sorted(set(merged["required"]))
        schema = merged

    typ = schema.get("type")

    # object
    if (typ == "object") or ("properties" in schema) or ("required" in schema):
        props = {}
        for name, sub in (schema.get("properties") or {}).items():
            props[name] = _oas_schema_to_simple(root, sub)
        out = {"type": "object"}
        if props:
            out["properties"] = props
        if schema.get("required"):
            out["required"] = list(schema["required"])
        return out

    # array
    if typ == "array":
        items = schema.get("items", {})
        return {"type": "array", "items": _oas_schema_to_simple(root, items)}

    # 原子类型
    if typ in ("string", "number", "integer", "boolean"):
        return {"type": typ}

    # 兜底：当作 object
    return {"type": "object"}


def openapi_to_simple(oas: dict) -> dict:
    """OpenAPI JSON -> 简化契约 JSON（{ "apis": [...] }）"""
    apis = []

    # 预处理：为参数 $ref 做简单解引用
    def _dereference_param(p: dict) -> dict:
        if "$ref" in p:
            return _resolve_ref(oas, p["$ref"]) or {}
        return p

    for path, item in (oas.get("paths") or {}).items():
        if not isinstance(item, dict):
            continue

        # 路径级参数
        path_params = [ _dereference_param(p) for p in (item.get("parameters") or []) ]

        for method in ("get", "post", "put", "patch", "delete", "options", "head"):
            op = item.get(method)
            if not isinstance(op, dict):
                continue

            # 方法级参数
            params_all = path_params + [ _dereference_param(p) for p in (op.get("parameters") or []) ]
            params_simple = []
            for p in params_all:
                p_in   = p.get("in")
                p_name = p.get("name")
                if not p_in or not p_name:
                    continue
                sch = p.get("schema") or {}
                if "$ref" in sch:
                    sch = _resolve_ref(oas, sch["$ref"])
                p_type = (sch.get("type") or "string")
                params_simple.append({
                    "in": p_in,
                    "name": p_name,
                    "type": p_type,
                    "required": bool(p.get("required", False)),
                })

            # requestBody（取 application/json）
            req_schema_simple = None
            req = op.get("requestBody")
            if isinstance(req, dict):
                if "$ref" in req:
                    req = _resolve_ref(oas, req["$ref"])
                content = req.get("content") or {}
                if "application/json" in content:
                    s = content["application/json"].get("schema")
                    if isinstance(s, dict):
                        req_schema_simple = _oas_schema_to_simple(oas, s)

            # responses（取 application/json）
            resps_simple = {}
            for code, resp in (op.get("responses") or {}).items():
                if not isinstance(resp, dict):
                    continue
                if "$ref" in resp:
                    resp = _resolve_ref(oas, resp["$ref"])
                content = resp.get("content") or {}
                if "application/json" in content:
                    s = content["application/json"].get("schema")
                    if isinstance(s, dict):
                        resps_simple[str(code)] = _oas_schema_to_simple(oas, s)

            apis.append({
                "name":     op.get("operationId") or f"{method.upper()} {path}",
                "method":   method.upper(),
                "path":     path,
                "params":   params_simple,
                "request":  req_schema_simple,
                "responses": resps_simple,
            })

    return {"apis": apis}


# ---------- 解析与归一化 ----------

def parse_contract(*, text: Optional[str] = None, path: Optional[str] = None) -> Dict[str, Any]:
    """
    解析契约（简化 JSON 或 OpenAPI JSON），并归一化为内部结构：
    {
      "endpoints": {
        "GET /users/{id}": {
          "params":   { "path.id": {...}, "query.q": {...}, ... },
          "request":  { "name": {...}, "items[]": {...}, "items[].sku": {...}, ... },
          "responses":{ "200": { ... }, "400": { ... } }
        }, ...
      }
    }
    """
    if text is None and path is None:
        raise ValueError("parse_contract: 必须提供 text 或 path 之一")

    data = load_json_file(path) if path else json.loads(text)

    # 自动识别 OpenAPI（含 paths）
    if _is_openapi_doc(data):
        data = openapi_to_simple(data)

    if not isinstance(data, dict) or "apis" not in data or not isinstance(data["apis"], list):
        raise ValueError("契约 JSON 格式不正确：根对象应包含 'apis' 列表（或传入 OpenAPI JSON）")

    endpoints: Dict[str, Dict[str, Any]] = {}

    for api in data["apis"]:
        method = str(api.get("method", "")).upper()
        pathv  = str(api.get("path", ""))
        if not method or not pathv:
            continue

        key = f"{method} {pathv}"

        # 参数（path/query/header）
        params_map: Dict[str, Dict[str, Any]] = {}

        def _add_param(scope: str, item: Dict[str, Any]):
            name = item.get("name")
            if not name:
                return
            t   = str(item.get("type", "string"))
            req = bool(item.get("required", False))
            params_map[f"{scope}.{name}"] = {"type": t, "required": req}

        for p in api.get("params", []) or []:
            _add_param(str(p.get("in", "query")), p)
        for p in api.get("query", []) or []:
            _add_param("query", p)
        for p in api.get("headers", []) or []:
            _add_param("header", p)
        for p in api.get("pathParams", []) or []:
            _add_param("path", p)

        # 请求体
        req_fields = flatten_schema(api.get("request")) if api.get("request") else {}

        # 响应体（按状态码展开）
        resps: Dict[str, Dict[str, Dict[str, Any]]] = {}
        responses = api.get("responses") or {}
        if isinstance(responses, dict):
            for code, schema in responses.items():
                resps[str(code)] = flatten_schema(schema) if schema else {}

        endpoints[key] = {
            "method":    method,
            "path":      pathv,
            "params":    params_map,
            "request":   req_fields,
            "responses": resps,
            "name":      api.get("name", key),
        }

    return {"endpoints": endpoints}


def flatten_schema(schema: Optional[Dict[str, Any]], prefix: str = "") -> Dict[str, Dict[str, Any]]:
    """
    将 object/array schema 展平成 {field_path: {"type":..., "required":bool}}。
    数组用 '[]' 表示，如 items[]、items[].id。
    """
    result: Dict[str, Dict[str, Any]] = {}
    if not schema or not isinstance(schema, dict):
        return result

    t = schema.get("type")

    if t == "object":
        props    = schema.get("properties", {}) or {}
        required = set(schema.get("required", []) or [])
        for name, sub in props.items():
            is_req = name in required
            if not isinstance(sub, dict):
                continue
            sub_t = sub.get("type")
            field = f"{prefix}{name}" if not prefix else f"{prefix}.{name}"
            if sub_t == "object":
                result.update(flatten_schema(sub, field))
            elif sub_t == "array":
                items = sub.get("items", {})
                arr   = f"{field}[]"
                if isinstance(items, dict) and items.get("type") == "object":
                    result.update(flatten_schema(items, arr))
                else:
                    itype = items.get("type", "any") if isinstance(items, dict) else "any"
                    result[arr] = {"type": f"array<{itype}>", "required": is_req}
            else:
                result[field] = {"type": sub_t or "any", "required": is_req}

    elif t == "array":
        items = schema.get("items", {})
        name  = f"{prefix}[]".rstrip(".")
        if isinstance(items, dict) and items.get("type") == "object":
            result.update(flatten_schema(items, name))
        else:
            itype = items.get("type", "any") if isinstance(items, dict) else "any"
            result[name] = {"type": f"array<{itype}>", "required": False}

    else:
        base = prefix or "value"
        result[base] = {"type": t or "any", "required": False}

    return result


# ---------- 对比与兼容性判定 ----------

def _is_non_breaking_widen(old_type: str, new_type: str, *, response_mode: bool) -> bool:
    """
    非破坏“放宽”判断：仅在请求/参数中允许 integer -> number 。
    响应中一律保守，视为破坏。
    """
    if response_mode:
        return False
    return old_type == "integer" and new_type == "number"


def _diff_field_maps(
    breaking: List[str],
    non_breaking: List[str],
    *,
    category: str,
    old_map: Dict[str, Dict[str, Any]],
    new_map: Dict[str, Dict[str, Any]],
    on_add_required_breaking: bool,
    on_remove_breaking: bool,
    response_mode: bool = False,
):
    """比较两个 {field: {type, required}}，生成变更描述。"""
    old_keys = set(old_map)
    new_keys = set(new_map)

    # 删除 / 新增
    for f in sorted(old_keys - new_keys):
        if on_remove_breaking:
            breaking.append(f"{category} 删除字段: {f}")
        else:
            non_breaking.append(f"{category} 删除字段: {f}（非破坏）")

    for f in sorted(new_keys - old_keys):
        req = bool(new_map[f].get("required", False))
        if req and on_add_required_breaking:
            breaking.append(f"{category} 新增必填字段: {f}")
        else:
            non_breaking.append(f"{category} 新增字段: {f}")

    # 交集：required 与 type 变化
    for f in sorted(old_keys & new_keys):
        o = old_map[f]
        n = new_map[f]
        o_req, n_req = bool(o.get("required", False)), bool(n.get("required", False))
        if (not o_req) and n_req:
            breaking.append(f"{category} 字段改为必填: {f}")
        elif o_req and (not n_req):
            non_breaking.append(f"{category} 字段由必填改为可选: {f}")

        ot, nt = str(o.get("type", "any")), str(n.get("type", "any"))
        if ot != nt:
            if _is_non_breaking_widen(ot, nt, response_mode=response_mode):
                non_breaking.append(f"{category} 字段类型放宽: {f} {ot} -> {nt}")
            else:
                breaking.append(f"{category} 字段类型改变: {f} {ot} -> {nt}")


def compare_contracts(old: Dict[str, Any], new: Dict[str, Any]) -> Dict[str, Any]:
    """对比两个归一化契约，返回报告 dict。"""
    old_eps = old.get("endpoints", {})
    new_eps = new.get("endpoints", {})

    breaking: List[str] = []
    non_breaking: List[str] = []
    notes: List[str] = []

    old_keys = set(old_eps)
    new_keys = set(new_eps)

    # 端点增删
    removed = sorted(old_keys - new_keys)
    added   = sorted(new_keys - old_keys)
    for k in removed:
        breaking.append(f"删除端点: {k}")
    for k in added:
        non_breaking.append(f"新增端点: {k}")

    # 端点内部变化
    for k in sorted(old_keys & new_keys):
        o, n = old_eps[k], new_eps[k]

        _diff_field_maps(
            breaking, non_breaking, category=f"[参数] {k}",
            old_map=o.get("params", {}), new_map=n.get("params", {}),
            on_add_required_breaking=True, on_remove_breaking=True
        )
        _diff_field_maps(
            breaking, non_breaking, category=f"[请求体] {k}",
            old_map=o.get("request", {}), new_map=n.get("request", {}),
            on_add_required_breaking=True, on_remove_breaking=True
        )

        old_resps = o.get("responses", {})
        new_resps = n.get("responses", {})
        for code in sorted(set(old_resps) | set(new_resps)):
            if code not in old_resps and code in new_resps:
                non_breaking.append(f"[响应 {code}] {k} 新增状态码")
                continue
            if code in old_resps and code not in new_resps:
                breaking.append(f"[响应 {code}] {k} 删除状态码")
                continue
            _diff_field_maps(
                breaking, non_breaking, category=f"[响应 {code}] {k}",
                old_map=old_resps.get(code, {}), new_map=new_resps.get(code, {}),
                on_add_required_breaking=False, on_remove_breaking=True,
                response_mode=True
            )

    return {
        "breaking": breaking,
        "non_breaking": non_breaking,
        "notes": notes,
        "summary": {
            "breaking": len(breaking),
            "non_breaking": len(non_breaking),
            "removed_endpoints": len(removed),
            "added_endpoints": len(added),
        },
        "added_endpoints": added,
        "removed_endpoints": removed,
    }


# ---------- 报告渲染 ----------

def format_report_text(report: Dict[str, Any]) -> str:
    parts = []
    s = report.get("summary", {})
    parts.append("接口契约对比结果")
    parts.append(f"- 破坏性变更: {s.get('breaking', 0)}")
    parts.append(f"- 非破坏性变更: {s.get('non_breaking', 0)}")
    parts.append("")
    if report.get("breaking"):
        parts.append("【破坏性变更】")
        parts.extend(f"  - {x}" for x in report["breaking"])
        parts.append("")
    if report.get("non_breaking"):
        parts.append("【非破坏性变更】")
        parts.extend(f"  - {x}" for x in report["non_breaking"])
        parts.append("")
    if report.get("removed_endpoints"):
        parts.append("【删除的端点】")
        parts.extend(f"  - {x}" for x in report["removed_endpoints"])
        parts.append("")
    if report.get("added_endpoints"):
        parts.append("【新增的端点】")
        parts.extend(f"  - {x}" for x in report["added_endpoints"])
        parts.append("")
    return "\n".join(parts).rstrip() + "\n"


def format_report_md(report: Dict[str, Any]) -> str:
    s = report.get("summary", {})
    out = [
        "# 接口契约对比结果",
        f"- **破坏性变更**: {s.get('breaking', 0)}",
        f"- **非破坏性变更**: {s.get('non_breaking', 0)}",
        "",
    ]
    if report.get("breaking"):
        out.append("## 破坏性变更")
        out.extend(f"- {x}" for x in report["breaking"])
        out.append("")
    if report.get("non_breaking"):
        out.append("## 非破坏性变更")
        out.extend(f"- {x}" for x in report["non_breaking"])
        out.append("")
    if report.get("removed_endpoints"):
        out.append("## 删除的端点")
        out.extend(f"- {x}" for x in report["removed_endpoints"])
        out.append("")
    if report.get("added_endpoints"):
        out.append("## 新增的端点")
        out.extend(f"- {x}" for x in report["added_endpoints"])
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def format_report_json(report: Dict[str, Any]) -> str:
    return json.dumps(report, ensure_ascii=False, indent=2)


# ---------- CLI 接入 ----------

def register_parser(subparsers):
    parser = subparsers.add_parser("api-diff", help="接口契约对比器")
    sub = parser.add_subparsers(dest="action", help="动作")

    cmp_parser = sub.add_parser("compare", help="对比两份契约（简化 JSON 或 OpenAPI JSON）")
    cmp_parser.add_argument("--old", required=True, help="旧版契约 JSON 文件路径")
    cmp_parser.add_argument("--new", required=True, help="新版契约 JSON 文件路径")
    cmp_parser.add_argument("--format", choices=["text", "json", "md"], default="text", help="输出格式")
    cmp_parser.set_defaults(func=main)


def main(args):
    if getattr(args, "action", None) != "compare":
        raise RuntimeError("用法：api-diff compare --old v1.json --new v2.json [--format text|json|md]")

    old_c = parse_contract(path=args.old)
    new_c = parse_contract(path=args.new)
    report = compare_contracts(old_c, new_c)
    fmt = getattr(args, "format", "text")
    if fmt == "json":
        return format_report_json(report)
    if fmt == "md":
        return format_report_md(report)
    return format_report_text(report)

# devkit_zero/tools/api_contract_diff.py
from __future__ import annotations

"""
API Contract Diff & Compatibility Check

- Supports two types of input:
  1) "Simplified Contract JSON": { "apis": [ {method, path, params/query/headers, request, responses}, ... ] }
  2) OpenAPI/Swagger JSON: Automatically identified and converted to the simplified structure above for comparison

- Compatibility Rules (Simplified and Conservative):
  * Endpoints: Added -> Non-breaking; Removed -> Breaking
  * Parameters/Request Body Fields:
      - Added required -> Breaking; Added optional -> Non-breaking; Removed -> Breaking
      - required False->True -> Breaking; True->False -> Non-breaking
      - Type change -> Breaking (Only "relaxation" exception: integer->number in request/params is considered non-breaking; still breaking in response)
  * Response Body Fields: Removed -> Breaking; Added -> Non-breaking; Type change -> Breaking
"""

import json
from typing import Dict, Any, List, Optional


# ---------- Basic IO ----------

def load_json_file(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ---------- OpenAPI Identification & Conversion ----------

def _is_openapi_doc(data: dict) -> bool:
    """Very loose check: if it has 'paths', consider it OpenAPI style JSON."""
    return isinstance(data, dict) and "paths" in data


def _resolve_ref(root: dict, ref: str) -> dict:
    """Resolve local $ref (e.g. #/components/...). Return {} if not found."""
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
    Convert OpenAPI schema to "Simplified Contract" schema (keep only type/required/properties/items).
    Handle: $ref, allOf (shallow merge) / object / array / atomic types
    """
    if not isinstance(schema, dict):
        return {}

    # $ref
    if "$ref" in schema:
        schema = _resolve_ref(root, schema["$ref"])

    # allOf -> shallow merge as object
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

    # atomic types
    if typ in ("string", "number", "integer", "boolean"):
        return {"type": typ}

    # fallback: treat as object
    return {"type": "object"}


def openapi_to_simple(oas: dict) -> dict:
    """OpenAPI JSON -> Simplified Contract JSON ({ "apis": [...] })"""
    apis = []

    # Preprocessing: Simple dereference for parameter $ref
    def _dereference_param(p: dict) -> dict:
        if "$ref" in p:
            return _resolve_ref(oas, p["$ref"]) or {}
        return p

    for path, item in (oas.get("paths") or {}).items():
        if not isinstance(item, dict):
            continue

        # Path-level parameters
        path_params = [ _dereference_param(p) for p in (item.get("parameters") or []) ]

        for method in ("get", "post", "put", "patch", "delete", "options", "head"):
            op = item.get(method)
            if not isinstance(op, dict):
                continue

            # Method-level parameters
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

            # requestBody (take application/json)
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

            # responses (take application/json)
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


# ---------- Parsing & Normalization ----------

def parse_contract(*, text: Optional[str] = None, path: Optional[str] = None) -> Dict[str, Any]:
    """
    Parse contract (Simplified JSON or OpenAPI JSON) and normalize to internal structure:
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
        raise ValueError("parse_contract: Must provide either text or path")

    data = load_json_file(path) if path else json.loads(text)

    # Auto-detect OpenAPI (contains paths)
    if _is_openapi_doc(data):
        data = openapi_to_simple(data)

    if not isinstance(data, dict) or "apis" not in data or not isinstance(data["apis"], list):
        raise ValueError("Invalid contract JSON format: Root object should contain 'apis' list (or provide OpenAPI JSON)")

    endpoints: Dict[str, Dict[str, Any]] = {}

    for api in data["apis"]:
        method = str(api.get("method", "")).upper()
        pathv  = str(api.get("path", ""))
        if not method or not pathv:
            continue

        key = f"{method} {pathv}"

        # Params (path/query/header)
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

        # Request body
        req_fields = flatten_schema(api.get("request")) if api.get("request") else {}

        # Response body (expand by status code)
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
    Flatten object/array schema into {field_path: {"type":..., "required":bool}}.
    Arrays are represented by '[]', e.g. items[], items[].id.
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


# ---------- Comparison and Compatibility Judgment ----------

def _is_non_breaking_widen(old_type: str, new_type: str, *, response_mode: bool) -> bool:
    """
    Non-breaking "widening" check: allow integer -> number only in requests/parameters.
    In responses, be conservative and treat it as breaking.
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
    """Compare two {field: {type, required}} maps and generate change description."""
    old_keys = set(old_map)
    new_keys = set(new_map)

    # Remove / Add
    for f in sorted(old_keys - new_keys):
        if on_remove_breaking:
            breaking.append(f"{category} Removed field: {f}")
        else:
            non_breaking.append(f"{category} Removed field: {f} (non-breaking)")

    for f in sorted(new_keys - old_keys):
        req = bool(new_map[f].get("required", False))
        if req and on_add_required_breaking:
            breaking.append(f"{category} Added required field: {f}")
        else:
            non_breaking.append(f"{category} Added field: {f}")

    # Intersection: required and type changes
    for f in sorted(old_keys & new_keys):
        o = old_map[f]
        n = new_map[f]
        o_req, n_req = bool(o.get("required", False)), bool(n.get("required", False))
        if (not o_req) and n_req:
            breaking.append(f"{category} Field changed to required: {f}")
        elif o_req and (not n_req):
            non_breaking.append(f"{category} Field changed from required to optional: {f}")

        ot, nt = str(o.get("type", "any")), str(n.get("type", "any"))
        if ot != nt:
            if _is_non_breaking_widen(ot, nt, response_mode=response_mode):
                non_breaking.append(f"{category} Field type widened: {f} {ot} -> {nt}")
            else:
                breaking.append(f"{category} Field type changed: {f} {ot} -> {nt}")


def compare_contracts(old: Dict[str, Any], new: Dict[str, Any]) -> Dict[str, Any]:
    """Compare two normalized contracts, return report dict."""
    old_eps = old.get("endpoints", {})
    new_eps = new.get("endpoints", {})

    breaking: List[str] = []
    non_breaking: List[str] = []
    notes: List[str] = []

    old_keys = set(old_eps)
    new_keys = set(new_eps)

    # Endpoint add/remove
    removed = sorted(old_keys - new_keys)
    added   = sorted(new_keys - old_keys)
    for k in removed:
        breaking.append(f"Removed endpoint: {k}")
    for k in added:
        non_breaking.append(f"Added endpoint: {k}")

    # Endpoint internal changes
    for k in sorted(old_keys & new_keys):
        o, n = old_eps[k], new_eps[k]

        _diff_field_maps(
            breaking, non_breaking, category=f"[Params] {k}",
            old_map=o.get("params", {}), new_map=n.get("params", {}),
            on_add_required_breaking=True, on_remove_breaking=True
        )
        _diff_field_maps(
            breaking, non_breaking, category=f"[Request Body] {k}",
            old_map=o.get("request", {}), new_map=n.get("request", {}),
            on_add_required_breaking=True, on_remove_breaking=True
        )

        old_resps = o.get("responses", {})
        new_resps = n.get("responses", {})
        for code in sorted(set(old_resps) | set(new_resps)):
            if code not in old_resps and code in new_resps:
                non_breaking.append(f"[Response {code}] {k} Added status code")
                continue
            if code in old_resps and code not in new_resps:
                breaking.append(f"[Response {code}] {k} Removed status code")
                continue
            _diff_field_maps(
                breaking, non_breaking, category=f"[Response {code}] {k}",
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


# ---------- Report Rendering ----------

def format_report_text(report: Dict[str, Any]) -> str:
    parts = []
    s = report.get("summary", {})
    parts.append("API Contract Diff Results")
    parts.append(f"- Breaking changes: {s.get('breaking', 0)}")
    parts.append(f"- Non-breaking changes: {s.get('non_breaking', 0)}")
    parts.append("")
    if report.get("breaking"):
        parts.append("[Breaking Changes]")
        parts.extend(f"  - {x}" for x in report["breaking"])
        parts.append("")
    if report.get("non_breaking"):
        parts.append("[Non-breaking Changes]")
        parts.extend(f"  - {x}" for x in report["non_breaking"])
        parts.append("")
    if report.get("removed_endpoints"):
        parts.append("[Removed Endpoints]")
        parts.extend(f"  - {x}" for x in report["removed_endpoints"])
        parts.append("")
    if report.get("added_endpoints"):
        parts.append("[Added Endpoints]")
        parts.extend(f"  - {x}" for x in report["added_endpoints"])
        parts.append("")
    return "\n".join(parts).rstrip() + "\n"


def format_report_md(report: Dict[str, Any]) -> str:
    s = report.get("summary", {})
    out = [
        "# API Contract Diff Results",
        f"- **Breaking changes**: {s.get('breaking', 0)}",
        f"- **Non-breaking changes**: {s.get('non_breaking', 0)}",
        "",
    ]
    if report.get("breaking"):
        out.append("## Breaking Changes")
        out.extend(f"- {x}" for x in report["breaking"])
        out.append("")
    if report.get("non_breaking"):
        out.append("## Non-breaking Changes")
        out.extend(f"- {x}" for x in report["non_breaking"])
        out.append("")
    if report.get("removed_endpoints"):
        out.append("## Removed Endpoints")
        out.extend(f"- {x}" for x in report["removed_endpoints"])
        out.append("")
    if report.get("added_endpoints"):
        out.append("## Added Endpoints")
        out.extend(f"- {x}" for x in report["added_endpoints"])
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def format_report_json(report: Dict[str, Any]) -> str:
    return json.dumps(report, ensure_ascii=False, indent=2)


# ---------- CLI Integration ----------

def register_parser(subparsers):
    parser = subparsers.add_parser("api-diff", help="API Contract Diff Tool")
    sub = parser.add_subparsers(dest="action", help="Action")

    cmp_parser = sub.add_parser("compare", help="Compare two contracts (Simplified JSON or OpenAPI JSON)")
    cmp_parser.add_argument("--old", required=True, help="Old contract JSON file path")
    cmp_parser.add_argument("--new", required=True, help="New contract JSON file path")
    cmp_parser.add_argument("--format", choices=["text", "json", "md"], default="text", help="Output format")
    cmp_parser.set_defaults(func=main)


def main(args):
    if getattr(args, "action", None) != "compare":
        raise RuntimeError("Usage: api-diff compare --old v1.json --new v2.json [--format text|json|md]")

    old_c = parse_contract(path=args.old)
    new_c = parse_contract(path=args.new)
    report = compare_contracts(old_c, new_c)
    fmt = getattr(args, "format", "text")
    if fmt == "json":
        return format_report_json(report)
    if fmt == "md":
        return format_report_md(report)
    return format_report_text(report)

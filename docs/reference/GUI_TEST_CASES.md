# DevKit-Zero GUI 测试用例指南

本文档提供了可以直接复制粘贴到 DevKit-Zero GUI 各个工具中的测试数据。请按照以下说明进行手动测试。

## 1. Code Formatter (代码格式化)

**设置:**

- **Language:** Python
- **Input Type:** Direct Input

**测试数据 (Code Input):**

def  calculate_sum( a,b ):
 result=a+b
 return  result

print( calculate_sum( 10,20 ) )

**预期结果:**
代码应该被格式化，去除多余空格，规范缩进。

---

## 2. Random Generator (随机数生成)

**设置:**

- **Type:** String
- **Length:** 16
- **Options:** 勾选 Include Numbers, Uppercase, Lowercase

**操作:**
点击 "Generate" 按钮。

**预期结果:**
Result Output 区域显示一个 16 位的随机字符串。

---

## 3. Text Diff (文本对比)

**设置:**

- **Output Format:** Side-by-Side (或 Unified)

**测试数据 (Text 1):**

```text
DevKit-Zero is a developer toolkit.
It has no external dependencies.
It is very fast.
```

**测试数据 (Text 2):**

```text
DevKit-Zero is a great developer toolkit.
It has zero external dependencies.
It is extremely fast.
```

**预期结果:**
显示两段文本的差异对比。

---

## 4. Format Converter (格式转换)

**设置:**

- **From Format:** JSON
- **To Format:** CSV

**测试数据 (Input Data):**

```json
[
  {
    "id": 1,
    "name": "Alice",
    "role": "Admin"
  },
  {
    "id": 2,
    "name": "Bob",
    "role": "User"
  }
]
```

**预期结果:**
显示转换后的 CSV 数据：

```csv
id,name,role
1,Alice,Admin
2,Bob,User
```

---

## 5. Code Linter (代码检查)

**设置:**

- **Input Type:** Direct Input

**测试数据 (Code Input):**

```python
import sys
import os

def my_function():
    x = 1
    y = 2
    print("Hello") 
```

**预期结果:**
显示 Lint 报告，指出未使用的导入 (`sys`, `os`) 和未使用的变量 (`x`, `y`)。

---

## 6. Regex Tester (正则测试)

**设置:**

- **Custom Pattern:** `\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b`
- **Options:** 勾选 Ignore Case

**测试数据 (Test Text):**

```text
Please contact support@example.com for assistance.
You can also reach out to sales@company.org.
Invalid emails like test@.com should not match.
```

**预期结果:**

- Match Result: 2 matches
- Match Details: 显示 `support@example.com` 和 `sales@company.org`。

---

## 7. Port Checker (端口检查)

**设置:**

- **Action Type:** Check

**测试数据:**

- **Host:** `google.com`
- **Port:** `443`
- **Timeout:** `3`

**预期结果:**
显示端口 443 是 Open (开放) 的状态。

---

## 8. API Contract Diff (API 契约对比)

**设置:**

- **Output Format:** Text

**测试数据 (Contract v1) - 旧版本:**

```json
{
  "apis": [
    {
      "name": "GetUser",
      "method": "GET",
      "path": "/users",
      "params": [
        {
          "name": "page",
          "in": "query",
          "type": "integer",
          "required": false
        }
      ],
      "responses": {
        "200": {
          "type": "array",
          "items": {
            "type": "object"
          }
        }
      }
    }
  ]
}
```

**测试数据 (Contract v2) - 新版本:**

```json
{
  "apis": [
    {
      "name": "GetUser",
      "method": "GET",
      "path": "/users",
      "params": [
        {
          "name": "page",
          "in": "query",
          "type": "integer",
          "required": true
        }
      ],
      "responses": {
        "200": {
          "type": "array",
          "items": {
            "type": "object"
          }
        }
      }
    }
  ]
}
```

**操作步骤:**

1. 选择 **API Contract Diff** 工具。
2. 将 **Contract v1** 代码粘贴到左边的文本框。
3. 将 **Contract v2** 代码粘贴到右边的文本框。
4. 点击 **Compare Contracts** 按钮。

**预期结果:**
显示 API 变更报告，指出 `page` 参数的 `required` 属性从 `false` 变更为 `true`。

---

## 8.1 API Contract Diff - 复杂变更示例

**测试数据 (Contract v1) - 旧版本:**

```json
{
  "apis": [
    {
      "name": "ListUsers",
      "method": "GET",
      "path": "/users",
      "params": [],
      "responses": {
        "200": {
          "type": "object",
          "properties": {
            "items": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "id": {
                    "type": "string"
                  }
                }
              }
            }
          }
        }
      }
    }
  ]
}
```

**测试数据 (Contract v2) - 新版本:**

```json
{
  "apis": [
    {
      "name": "ListUsers",
      "method": "GET",
      "path": "/users",
      "params": [
        {
          "name": "active",
          "in": "query",
          "type": "boolean",
          "required": false
        },
        {
          "name": "page",
          "in": "query",
          "type": "integer",
          "required": true
        }
      ],
      "responses": {
        "200": {
          "type": "object",
          "properties": {
            "items": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "id": {
                    "type": "string"
                  },
                  "email": {
                    "type": "string"
                  }
                }
              }
            }
          }
        }
      }
    },
    {
      "name": "CreateUser",
      "method": "POST",
      "path": "/users",
      "request": {
        "type": "object",
        "required": ["name"],
        "properties": {
          "name": {
            "type": "string"
          },
          "age": {
            "type": "integer"
          }
        }
      },
      "responses": {
        "201": {
          "type": "object",
          "properties": {
            "id": {
              "type": "string"
            }
          }
        }
      }
    }
  ]
}
```

**操作步骤:**

1. 将旧版本代码粘贴到 **Contract v1**。
2. 将新版本代码粘贴到 **Contract v2**。
3. 点击 **Compare Contracts**。

**预期结果:**
显示详细的 API 变更报告，包括：

- 新增查询参数：`active`（可选）、`page`（必需）
- 响应对象新增字段：`email`
- 新增 API 端点：`CreateUser` (POST /users)

---

## 8.2 快速演示 - 点击 "Fill Example" 按钮

**操作:**

1. 选择 **API Contract Diff** 工具。
2. 点击 **Fill Example** 按钮（自动填充示例数据）。
3. 点击 **Compare Contracts** 按钮。

**预期结果:**
自动加载示例数据并显示对比结果，演示：

- 字段属性变更（`name` -> `email`）
- 新增查询参数（`page`）
- 新增 API 端点（`CreateUser`）

---

## 9. Robots Checker (Robots 协议检查)

**设置:**

- **Timeout:** 10

**测试数据 (Website URL):**
`https://www.github.com`

**预期结果:**
显示 GitHub 的 robots.txt 解析规则（Allow/Disallow 路径）。

---

## 10. Format Detector (格式检测)

**设置:**

- **Detection Mode:** Content

**测试数据 (Input Content):**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<note>
  <to>Tove</to>
  <from>Jani</from>
  <heading>Reminder</heading>
  <body>Don't forget me this weekend!</body>
</note>
```

**预期结果:**

- Most likely format: XML
- XML: ✓ Valid

---

## 11. Unused Function (未使用函数检测)

**注意:** 此工具需要选择文件夹。

**操作:**

1. 在 `Project Path` 点击 `Select Dir`。
2. 选择当前的 `devkit_zero` 文件夹。
3. 点击 `Detect Unused Functions`。

**预期结果:**
显示项目中未被调用的函数列表（如果有）。

---

## 12. Batch Processor (批量处理)

**注意:** 此工具建议在临时文件夹测试。

**操作:**

1. 创建一个临时文件夹 `temp_test`。
2. 在其中创建几个文件：`test1.txt`, `test2.txt`。
3. 在 GUI 中选择 `Operation Type: Rename`。
4. **Directory Path:** 选择 `temp_test` 文件夹。
5. **Find Pattern:** `test`
6. **Replace With:** `demo`
7. 点击 `Execute Operation` (Preview Mode 默认开启)。

**预期结果:**
预览显示 `test1.txt -> demo1.txt` 等重命名操作。

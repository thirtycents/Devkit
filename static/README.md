# 🎨 Static 目录

本目录用于存放静态资源文件,主要用于GUI界面。

## 📂 目录结构

```
static/
├── css/                    # 样式文件
│   ├── main.css           # 主样式
│   ├── themes/            # 主题样式
│   │   ├── light.css
│   │   └── dark.css
│   └── components/        # 组件样式
│
├── js/                     # JavaScript文件(如需要)
│   ├── main.js
│   └── utils.js
│
├── html/                   # HTML模板
│   ├── tool_panel.html
│   └── result_view.html
│
└── config/                 # UI配置文件
    ├── themes.json        # 主题配置
    └── layout.json        # 布局配置
```

## 📋 文件类型说明

### CSS样式文件

#### main.css
主样式文件,定义全局样式:

```css
/* 全局样式 */
:root {
    --primary-color: #007bff;
    --secondary-color: #6c757d;
    --bg-color: #ffffff;
    --text-color: #212529;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
}

/* 按钮样式 */
.btn {
    padding: 8px 16px;
    border-radius: 4px;
    cursor: pointer;
}
```

#### 主题文件

**light.css** - 亮色主题
```css
:root {
    --bg-color: #ffffff;
    --text-color: #212529;
    --panel-bg: #f8f9fa;
}
```

**dark.css** - 暗色主题
```css
:root {
    --bg-color: #1e1e1e;
    --text-color: #d4d4d4;
    --panel-bg: #252526;
}
```

### HTML模板

用于动态生成GUI内容:

```html
<!-- tool_panel.html -->
<div class="tool-panel">
    <h2>{{tool_name}}</h2>
    <div class="tool-options">
        {{tool_options}}
    </div>
    <button class="btn-run">运行</button>
</div>
```

### JavaScript文件(可选)

如果GUI使用Web技术(如Electron):

```javascript
// main.js
function runTool(toolName, options) {
    // 调用Python后端
    window.pywebview.api.runTool(toolName, options)
        .then(result => displayResult(result));
}
```

### 配置文件

#### themes.json
```json
{
    "themes": [
        {
            "name": "Light",
            "file": "css/themes/light.css",
            "default": true
        },
        {
            "name": "Dark",
            "file": "css/themes/dark.css"
        }
    ]
}
```

#### layout.json
```json
{
    "mainWindow": {
        "width": 1024,
        "height": 768,
        "minWidth": 800,
        "minHeight": 600
    },
    "panels": {
        "toolList": {
            "width": 200,
            "position": "left"
        }
    }
}
```

## 🔧 在代码中使用

### tkinter GUI示例

```python
import tkinter as tk
from pathlib import Path

# 获取static目录
STATIC_DIR = Path(__file__).parent.parent / 'static'

# 加载配置
import json
with open(STATIC_DIR / 'config' / 'layout.json') as f:
    layout = json.load(f)

# 创建窗口
root = tk.Tk()
root.geometry(f"{layout['mainWindow']['width']}x{layout['mainWindow']['height']}")
```

### 加载CSS(如使用Web视图)

```python
import webview
from pathlib import Path

STATIC_DIR = Path(__file__).parent.parent / 'static'

# 读取CSS
with open(STATIC_DIR / 'css' / 'main.css') as f:
    css = f.read()

# 创建窗口
webview.create_window('DevKit-Zero', html=html_content, css=css)
```

### 使用HTML模板

```python
from pathlib import Path
from string import Template

STATIC_DIR = Path(__file__).parent.parent / 'static'

# 读取模板
with open(STATIC_DIR / 'html' / 'tool_panel.html') as f:
    template = Template(f.read())

# 渲染模板
html = template.substitute(
    tool_name='Code Formatter',
    tool_options='<input type="text" />'
)
```

## 🎨 样式指南

### 颜色方案

```css
/* 主色调 */
--primary: #007bff;      /* 主要操作按钮 */
--success: #28a745;      /* 成功状态 */
--warning: #ffc107;      /* 警告状态 */
--danger: #dc3545;       /* 危险/错误 */
--info: #17a2b8;         /* 信息提示 */

/* 中性色 */
--gray-100: #f8f9fa;
--gray-200: #e9ecef;
--gray-300: #dee2e6;
--gray-400: #ced4da;
--gray-500: #adb5bd;
```

### 字体

```css
/* 主要字体 */
font-family: -apple-system, BlinkMacSystemFont, 
             'Segoe UI', Roboto, Oxygen, Ubuntu, 
             sans-serif;

/* 等宽字体(代码) */
font-family: 'Consolas', 'Monaco', 'Courier New', 
             monospace;
```

### 间距

```css
/* 使用8px基准 */
--spacing-xs: 4px;
--spacing-sm: 8px;
--spacing-md: 16px;
--spacing-lg: 24px;
--spacing-xl: 32px;
```

## 📐 响应式设计

### 断点

```css
/* 小屏幕 */
@media (max-width: 768px) {
    .tool-panel {
        width: 100%;
    }
}

/* 中等屏幕 */
@media (min-width: 769px) and (max-width: 1024px) {
    .tool-panel {
        width: 48%;
    }
}

/* 大屏幕 */
@media (min-width: 1025px) {
    .tool-panel {
        width: 30%;
    }
}
```

## 🚫 不应该放在这里的文件

- ❌ Python代码
- ❌ 编译产物
- ❌ 用户数据
- ❌ 日志文件
- ❌ 缓存文件

## 📦 静态资源优化

### CSS优化
```bash
# 压缩CSS(生产环境)
# 使用工具如 cssnano 或在线工具
```

### 图片优化
- 小图标考虑使用CSS绘制或SVG
- 避免在CSS中使用大图片
- 使用雪碧图(sprite)合并小图标

### 文件组织
```css
/* 不好: 一个巨大的CSS文件 */
main.css (3000 lines)

/* 好: 模块化的CSS */
main.css (基础样式)
components/button.css
components/input.css
themes/light.css
themes/dark.css
```

## 🔄 主题切换实现

### Python代码

```python
class ThemeManager:
    def __init__(self):
        self.current_theme = 'light'
        self.load_themes()
    
    def load_themes(self):
        """加载主题配置"""
        with open(STATIC_DIR / 'config' / 'themes.json') as f:
            self.themes = json.load(f)['themes']
    
    def switch_theme(self, theme_name):
        """切换主题"""
        for theme in self.themes:
            if theme['name'] == theme_name:
                css_path = STATIC_DIR / theme['file']
                # 加载CSS...
                self.current_theme = theme_name
```

## 📚 相关资源

- [CSS文档](https://developer.mozilla.org/zh-CN/docs/Web/CSS)
- [tkinter文档](https://docs.python.org/3/library/tkinter.html)
- [配色工具](https://coolors.co/)
- [字体资源](https://fonts.google.com/)

---

**注意**: 
- GUI开发是可选功能,优先确保CLI功能完善
- 选择合适的GUI框架(tkinter/PyQt/Web)
- 保持样式简洁一致

**最后更新**: 2025-XX-XX

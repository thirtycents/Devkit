# 📁 Assets 目录

本目录用于存放项目的资源文件。

## 📂 目录结构

```
assets/
├── icons/          # 图标文件
│   ├── app-icon.png
│   ├── tool-icons/
│   └── ui-icons/
│
├── images/         # 图片资源
│   ├── logo.png
│   ├── screenshots/
│   └── diagrams/
│
├── fonts/          # 字体文件(如需要)
│
└── data/           # 示例数据文件
    └── samples/
```

## 📋 资源类型说明

### Icons (图标)
- **应用图标**: 主程序图标,各种尺寸
- **工具图标**: 各个工具的特色图标
- **UI图标**: 界面元素图标

**格式要求**:
- PNG格式,透明背景
- 推荐尺寸: 16x16, 32x32, 64x64, 128x128, 256x256

### Images (图片)
- **Logo**: 项目Logo
- **截图**: 功能演示截图
- **架构图**: 系统架构图

**格式要求**:
- PNG或SVG格式
- 文件名使用小写+连字符: `my-screenshot.png`

### Fonts (字体)
如果GUI需要特殊字体,放在这里

**注意**:
- 确保字体有使用许可
- 优先使用系统字体

### Data (数据)
示例数据文件,用于:
- 测试工具功能
- 文档中的示例
- 演示数据

## 🔧 使用方式

### 在代码中引用资源

```python
from pathlib import Path

# 获取assets目录路径
ASSETS_DIR = Path(__file__).parent.parent / 'assets'

# 加载图标
icon_path = ASSETS_DIR / 'icons' / 'app-icon.png'

# 加载图片
logo_path = ASSETS_DIR / 'images' / 'logo.png'

# 读取示例数据
sample_file = ASSETS_DIR / 'data' / 'samples' / 'example.txt'
```

### 在文档中引用

```markdown
![Logo](../assets/images/logo.png)
![Screenshot](../assets/images/screenshots/main-window.png)
```

## 📝 命名规范

- 使用小写字母
- 单词间用连字符分隔: `my-icon.png`
- 有意义的文件名: `formatter-tool-icon.png` 而非 `icon1.png`
- 版本号放在文件名后: `logo-v2.png`

## 🚫 不应该放在这里的文件

- ❌ 临时文件
- ❌ 编译产物
- ❌ 用户生成的内容
- ❌ 缓存文件
- ❌ 大型视频文件(考虑外部托管)

## 📦 资源优化

### 图片优化
- 使用适当的分辨率
- 压缩PNG文件: 使用 TinyPNG 或 ImageOptim
- 考虑使用SVG替代光栅图(可缩放)

### 文件大小
- 单个文件建议不超过 5MB
- 大文件考虑使用 Git LFS

## 🔗 相关链接

- [免费图标资源](https://fontawesome.com/)
- [免费图片资源](https://unsplash.com/)
- [图片压缩工具](https://tinypng.com/)

---

**注意**: 添加资源文件后,记得在 `.gitignore` 中确认不会忽略它们。

**最后更新**: 2025-XX-XX

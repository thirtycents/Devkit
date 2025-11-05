"""
DevKit-Zero 安装配置
"""

from setuptools import setup, find_packages
from pathlib import Path

# 读取README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding='utf-8') if readme_file.exists() else ""

setup(
    name="devkit-zero",
    version="0.1.0",
    author="DevKit-Zero Team",
    author_email="your-team@example.com",
    description="A lightweight, zero-dependency developer toolkit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/devkit",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        # 零依赖！只使用Python标准库
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "devkit-zero=devkit_zero.cli:main",
        ],
        "gui_scripts": [
            "devkit-zero-gui=devkit_zero.gui_main:main",
        ],
    },
)

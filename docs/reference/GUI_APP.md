# DevKit-Zero GUI Application

The **DevKit-Zero GUI** provides a user-friendly graphical interface for all the developer tools included in the DevKit-Zero library. It allows users to access formatting, linting, conversion, and other utilities without using the command line.

## Features

The GUI includes the following tools:

1.  **Code Formatter**: Format Python and JavaScript code.
2.  **Random Generator**: Generate UUIDs, passwords, random strings, numbers, and colors.
3.  **Text Diff**: Compare two text blocks and see differences side-by-side or in unified format.
4.  **Format Converter**: Convert data between JSON and CSV formats.
5.  **Code Linter**: Static analysis for Python code to find potential issues.
6.  **Unused Function Detector**: Analyze projects to find functions that are never called.
7.  **Port Checker**: Check if a port is open or scan a range of ports.
8.  **API Contract Diff**: Compare two API contracts (JSON/OpenAPI) to detect breaking changes.
9.  **Regex Tester**: Test regular expressions against sample text with real-time feedback.
10. **Robots Checker**: Parse and validate `robots.txt` files from URLs.
11. **Batch Processor**: Rename, copy, or move files in bulk using patterns.
12. **Format Detector**: Identify file formats (JSON, XML, YAML, etc.) from file paths or content.

## How to Run

You can launch the GUI using the following command from the project root:

```bash
python -m devkit_zero.ui.gui_app
```

Or if you have the package installed:

```bash
devkit-gui
```

## Requirements

-   **Python 3.6+**
-   **Tkinter**: This is usually included with standard Python installations.
    -   *Linux users*: You may need to install it manually (e.g., `sudo apt-get install python3-tk`).

## Usage Guide

1.  **Select a Tool**: Use the radio buttons at the top "Tool Selection" panel to switch between different utilities.
2.  **Configure Parameters**: The "Control Panel" on the left will update to show options relevant to the selected tool.
3.  **Input Data**: Enter text directly into the input boxes or use the "Select File" buttons to load content.
4.  **Execute**: Click the action button (e.g., "Format Code", "Generate") at the bottom of the control panel.
5.  **View Results**: The output will appear in the "Result Output" panel on the right.

## Troubleshooting

-   **GUI looks too small/large**: This can happen on high-DPI displays. The application attempts to handle scaling, but you may need to adjust your system's DPI settings if issues persist.
-   **"Module not found"**: Ensure you are running the command from the root directory of the project, or that the package is installed in your environment.

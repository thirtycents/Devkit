"""
DevKit-Zero GUI Main Entry Point
"""

import sys
import os
from typing import Optional


def main(argv: Optional[list] = None) -> int:
    """GUI Main Entry Function"""
    try:
        # Lazy import tkinter to avoid errors in non-GUI environments
        try:
            import tkinter as tk
        except ImportError:
            print("Error: Cannot import tkinter. Please ensure Python tkinter support is installed.", file=sys.stderr)
            print("On some Linux distributions, you may need to install the python3-tkinter package.", file=sys.stderr)
            return 1
        
        # Support two running modes: run as package (relative import) and run file directly (no parent package)
        try:
            from .ui.gui_app import DevKitZeroGUI
        except Exception:
            # When running directly with `python devkit_zero/gui_main.py`, it will show
            # "attempted relative import with no known parent package".
            # In this case, try to use absolute import as fallback.
            from devkit_zero.ui.gui_app import DevKitZeroGUI
        
        app = DevKitZeroGUI()
        app.run()
        return 0
        
    except KeyboardInterrupt:
        return 130
        
    except Exception as e:
        print(f"GUI Startup Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
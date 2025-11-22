import os
import pytest
from pathlib import Path
from devkit_zero.tools.unused_func_detector import detect_unused_functions

class TestUnusedFuncDetector:
    
    @pytest.fixture
    def sample_project(self, tmp_path):
        """Create a sample project for testing"""
        # Create project structure
        project_dir = tmp_path / "sample_project"
        project_dir.mkdir()
        
        # File 1: Definitions
        (project_dir / "lib.py").write_text("""
def used_function():
    return "I am used"

def unused_function():
    return "I am unused"

class MyClass:
    def used_method(self):
        pass
        
    def unused_method(self):
        pass
""", encoding="utf-8")

        # File 2: Usages
        (project_dir / "main.py").write_text("""
from lib import used_function, MyClass

def main():
    used_function()
    obj = MyClass()
    obj.used_method()

if __name__ == "__main__":
    main()
""", encoding="utf-8")

        return project_dir

    def test_detect_unused_functions(self, sample_project):
        """Test detecting unused functions"""
        unused = detect_unused_functions(sample_project)
        
        # Convert to set of names for easier checking
        unused_names = {f.name for f in unused}
        
        assert "unused_function" in unused_names
        assert "unused_method" in unused_names
        assert "used_function" not in unused_names
        assert "used_method" not in unused_names
        assert "main" not in unused_names  # main is usually excluded or used

    def test_exclude_directories(self, sample_project):
        """Test excluding directories"""
        # Create an excluded directory with unused functions
        exclude_dir = sample_project / "exclude_me"
        exclude_dir.mkdir()
        (exclude_dir / "ignored.py").write_text("""
def ignored_unused():
    pass
""", encoding="utf-8")
        
        unused = detect_unused_functions(sample_project, exclude_dirs=["exclude_me"])
        unused_names = {f.name for f in unused}
        
        assert "ignored_unused" not in unused_names

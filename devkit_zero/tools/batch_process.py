import os
import shutil
import re
from pathlib import Path

class BatchFileProcessor:
    def __init__(self, preview=False):
        self.preview = preview
        self.operations = []
    
    def rename_files(self, directory, pattern, replacement, regex=False, case_sensitive=True, extension_filter=None):
        """Batch rename files"""
        directory = Path(directory)
        if not directory.exists():
            print(f"Error: Directory '{directory}' does not exist")
            return
        
        renamed_count = 0
        for file_path in directory.iterdir():
            if file_path.is_file():
                # Check extension filter
                if extension_filter and file_path.suffix.lower() != extension_filter.lower():
                    continue
                
                old_name = file_path.name
                
                # Generate new filename based on pattern
                if regex:
                    flags = 0 if case_sensitive else re.IGNORECASE
                    new_name = re.sub(pattern, replacement, old_name, flags=flags)
                else:
                    if case_sensitive:
                        new_name = old_name.replace(pattern, replacement)
                    else:
                        new_name = old_name.lower().replace(pattern.lower(), replacement)
                
                # If filename changed, execute rename
                if new_name != old_name:
                    new_path = directory / new_name
                    
                    if self.preview:
                        print(f"[Preview] Rename: '{old_name}' -> '{new_name}'")
                        self.operations.append(("rename", str(file_path), str(new_path)))
                    else:
                        try:
                            file_path.rename(new_path)
                            print(f"Rename: '{old_name}' -> '{new_name}'")
                            renamed_count += 1
                        except Exception as e:
                            print(f"Error: Cannot rename '{old_name}': {e}")
        
        if not self.preview:
            print(f"Done! Renamed {renamed_count} files")
    
    def copy_files(self, source_dir, target_dir, pattern="*", recursive=False, overwrite=False):
        """Batch copy files"""
        source_dir = Path(source_dir)
        target_dir = Path(target_dir)
        
        if not source_dir.exists():
            print(f"Error: Source directory '{source_dir}' does not exist")
            return
        
        # Create target directory (if not exists)
        if not self.preview:
            target_dir.mkdir(parents=True, exist_ok=True)
        
        copied_count = 0
        search_pattern = "**/" + pattern if recursive else pattern
        
        for file_path in source_dir.glob(search_pattern):
            if file_path.is_file():
                target_path = target_dir / file_path.name
                
                # Check if target file exists
                if target_path.exists() and not overwrite:
                    print(f"Skip: '{file_path.name}' already exists in target directory")
                    continue
                
                if self.preview:
                    print(f"[Preview] Copy: '{file_path}' -> '{target_path}'")
                    self.operations.append(("copy", str(file_path), str(target_path)))
                else:
                    try:
                        shutil.copy2(file_path, target_path)
                        print(f"Copy: '{file_path.name}'")
                        copied_count += 1
                    except Exception as e:
                        print(f"Error: Cannot copy '{file_path.name}': {e}")
        
        if not self.preview:
            print(f"Done! Copied {copied_count} files")
    
    def move_files(self, source_dir, target_dir, pattern="*", recursive=False, overwrite=False):
        """Batch move files"""
        source_dir = Path(source_dir)
        target_dir = Path(target_dir)
        
        if not source_dir.exists():
            print(f"Error: Source directory '{source_dir}' does not exist")
            return
        
        # Create target directory (if not exists)
        if not self.preview:
            target_dir.mkdir(parents=True, exist_ok=True)
        
        moved_count = 0
        search_pattern = "**/" + pattern if recursive else pattern
        
        for file_path in source_dir.glob(search_pattern):
            if file_path.is_file():
                target_path = target_dir / file_path.name
                
                # Check if target file exists
                if target_path.exists() and not overwrite:
                    print(f"Skip: '{file_path.name}' already exists in target directory")
                    continue
                
                if self.preview:
                    print(f"[Preview] Move: '{file_path}' -> '{target_path}'")
                    self.operations.append(("move", str(file_path), str(target_path)))
                else:
                    try:
                        shutil.move(str(file_path), str(target_path))
                        print(f"Move: '{file_path.name}'")
                        moved_count += 1
                    except Exception as e:
                        print(f"Error: Cannot move '{file_path.name}': {e}")
        
        if not self.preview:
            print(f"Done! Moved {moved_count} files")
    
    def execute_operations(self):
        """Execute previewed operations"""
        if not self.operations:
            print("No operations to execute")
            return
        
        print(f"\nReady to execute {len(self.operations)} operations:")
        for i, (op_type, src, dst) in enumerate(self.operations, 1):
            print(f"{i}. {op_type}: '{src}' -> '{dst}'")
        
        confirm = input("\nConfirm execution? (y/N): ")
        if confirm.lower() == 'y':
            for op_type, src, dst in self.operations:
                try:
                    if op_type == "rename":
                        Path(src).rename(dst)
                    elif op_type == "copy":
                        shutil.copy2(src, dst)
                    elif op_type == "move":
                        shutil.move(src, dst)
                    print(f"Execute: {op_type} '{src}' -> '{dst}'")
                except Exception as e:
                    print(f"Error: Cannot execute {op_type} '{src}': {e}")
            print("All operations completed")
        else:
            print("Operation cancelled")

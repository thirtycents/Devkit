import os
import shutil
import re
from pathlib import Path

class BatchFileProcessor:
    def __init__(self, preview=False):
        self.preview = preview
        self.operations = []
    
    def rename_files(self, directory, pattern, replacement, regex=False, case_sensitive=True, extension_filter=None):
        """批量重命名文件"""
        directory = Path(directory)
        if not directory.exists():
            print(f"错误: 目录 '{directory}' 不存在")
            return
        
        renamed_count = 0
        for file_path in directory.iterdir():
            if file_path.is_file():
                # 检查扩展名过滤
                if extension_filter and file_path.suffix.lower() != extension_filter.lower():
                    continue
                
                old_name = file_path.name
                
                # 根据模式生成新文件名
                if regex:
                    flags = 0 if case_sensitive else re.IGNORECASE
                    new_name = re.sub(pattern, replacement, old_name, flags=flags)
                else:
                    if case_sensitive:
                        new_name = old_name.replace(pattern, replacement)
                    else:
                        new_name = old_name.lower().replace(pattern.lower(), replacement)
                
                # 如果文件名有变化，则执行重命名
                if new_name != old_name:
                    new_path = directory / new_name
                    
                    if self.preview:
                        print(f"[预览] 重命名: '{old_name}' -> '{new_name}'")
                        self.operations.append(("rename", str(file_path), str(new_path)))
                    else:
                        try:
                            file_path.rename(new_path)
                            print(f"重命名: '{old_name}' -> '{new_name}'")
                            renamed_count += 1
                        except Exception as e:
                            print(f"错误: 无法重命名 '{old_name}': {e}")
        
        if not self.preview:
            print(f"完成! 共重命名 {renamed_count} 个文件")
    
    def copy_files(self, source_dir, target_dir, pattern="*", recursive=False, overwrite=False):
        """批量复制文件"""
        source_dir = Path(source_dir)
        target_dir = Path(target_dir)
        
        if not source_dir.exists():
            print(f"错误: 源目录 '{source_dir}' 不存在")
            return
        
        # 创建目标目录（如果不存在）
        if not self.preview:
            target_dir.mkdir(parents=True, exist_ok=True)
        
        copied_count = 0
        search_pattern = "**/" + pattern if recursive else pattern
        
        for file_path in source_dir.glob(search_pattern):
            if file_path.is_file():
                target_path = target_dir / file_path.name
                
                # 检查目标文件是否已存在
                if target_path.exists() and not overwrite:
                    print(f"跳过: '{file_path.name}' 已存在于目标目录")
                    continue
                
                if self.preview:
                    print(f"[预览] 复制: '{file_path}' -> '{target_path}'")
                    self.operations.append(("copy", str(file_path), str(target_path)))
                else:
                    try:
                        shutil.copy2(file_path, target_path)
                        print(f"复制: '{file_path.name}'")
                        copied_count += 1
                    except Exception as e:
                        print(f"错误: 无法复制 '{file_path.name}': {e}")
        
        if not self.preview:
            print(f"完成! 共复制 {copied_count} 个文件")
    
    def move_files(self, source_dir, target_dir, pattern="*", recursive=False, overwrite=False):
        """批量移动文件"""
        source_dir = Path(source_dir)
        target_dir = Path(target_dir)
        
        if not source_dir.exists():
            print(f"错误: 源目录 '{source_dir}' 不存在")
            return
        
        # 创建目标目录（如果不存在）
        if not self.preview:
            target_dir.mkdir(parents=True, exist_ok=True)
        
        moved_count = 0
        search_pattern = "**/" + pattern if recursive else pattern
        
        for file_path in source_dir.glob(search_pattern):
            if file_path.is_file():
                target_path = target_dir / file_path.name
                
                # 检查目标文件是否已存在
                if target_path.exists() and not overwrite:
                    print(f"跳过: '{file_path.name}' 已存在于目标目录")
                    continue
                
                if self.preview:
                    print(f"[预览] 移动: '{file_path}' -> '{target_path}'")
                    self.operations.append(("move", str(file_path), str(target_path)))
                else:
                    try:
                        shutil.move(str(file_path), str(target_path))
                        print(f"移动: '{file_path.name}'")
                        moved_count += 1
                    except Exception as e:
                        print(f"错误: 无法移动 '{file_path.name}': {e}")
        
        if not self.preview:
            print(f"完成! 共移动 {moved_count} 个文件")
    
    def execute_operations(self):
        """执行预览的操作"""
        if not self.operations:
            print("没有操作需要执行")
            return
        
        print(f"\n准备执行 {len(self.operations)} 个操作:")
        for i, (op_type, src, dst) in enumerate(self.operations, 1):
            print(f"{i}. {op_type}: '{src}' -> '{dst}'")
        
        confirm = input("\n确认执行这些操作? (y/N): ")
        if confirm.lower() == 'y':
            for op_type, src, dst in self.operations:
                try:
                    if op_type == "rename":
                        Path(src).rename(dst)
                    elif op_type == "copy":
                        shutil.copy2(src, dst)
                    elif op_type == "move":
                        shutil.move(src, dst)
                    print(f"执行: {op_type} '{src}' -> '{dst}'")
                except Exception as e:
                    print(f"错误: 无法执行 {op_type} '{src}': {e}")
            print("所有操作已完成")
        else:
            print("操作已取消")

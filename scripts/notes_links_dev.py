import os
import re
import html
import datetime
from dataclasses import dataclass
from typing import List, Optional
import glob
from pathlib import Path


@dataclass
class NoteFile:
    """表示一个笔记文件的类"""
    filepath: str  # 文件完整路径
    title: str     # 笔记标题
    date: datetime.datetime  # 笔记日期
    url: str       # 笔记的URL

    @property
    def filename(self) -> str:
        """返回文件名（不含路径）"""
        return os.path.basename(self.filepath)


class NotesManager:
    """笔记管理类"""
    
    def __init__(self, notes_dir: str, output_dir: str, url_base: str = ""):
        """
        初始化笔记管理器
        
        Args:
            notes_dir: 笔记文件所在目录
            output_dir: 生成的HTML文件目录
            url_base: URL基础路径，用于构建笔记链接
        """
        self.notes_dir = notes_dir
        self.output_dir = output_dir
        self.url_base = url_base
        self.notes: List[NoteFile] = []
    
    def scan_notes(self, extensions: List[str] = [".md", ".txt"]):
        """扫描笔记目录，找到所有笔记文件"""
        self.notes = []
        for ext in extensions:
            for filepath in glob.glob(f"{self.notes_dir}/**/*{ext}", recursive=True):
                # 获取文件修改时间作为笔记日期
                mod_time = datetime.datetime.fromtimestamp(os.path.getmtime(filepath))
                
                # 提取标题（使用文件名，移除扩展名）
                filename = os.path.basename(filepath)
                title = os.path.splitext(filename)[0]
                
                # 构建URL
                rel_path = os.path.relpath(filepath, self.notes_dir)
                url_path = os.path.splitext(rel_path)[0] + ".html"  # 假设输出为HTML
                url = f"{self.url_base}/{url_path}"
                
                self.notes.append(NoteFile(
                    filepath=filepath,
                    title=title,
                    date=mod_time,
                    url=url
                ))
    
    def get_recent_notes(self, limit: int = 10) -> List[NoteFile]:
        """获取最近更新的笔记"""
        return sorted(self.notes, key=lambda note: note.date, reverse=True)[:limit]
    
    def generate_recent_notes_html(self, limit: int = 10) -> str:
        """生成最近更新笔记的HTML代码"""
        recent_notes = self.get_recent_notes(limit)
        content = ''
        
        for note in recent_notes:
            safe_title = html.escape(note.title)
            safe_date = html.escape(note.date.strftime('%Y-%m-%d'))
            content += f'- <div class="recent-notes"><a href="{note.url}">{safe_title}</a><small>{safe_date}</small></div>\n'
        
        return content
    
    def process_markdown_file(self, filepath: str, placeholder: str = "<!-- RECENT NOTES -->"):
        """处理Markdown文件，替换占位符为最近笔记链接"""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        recent_notes_html = self.generate_recent_notes_html()
        updated_content = content.replace(placeholder, recent_notes_html)
        
        # 保存处理后的文件
        output_path = os.path.join(self.output_dir, os.path.basename(filepath))
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        return output_path
    
    def process_all_templates(self, template_dir: str, placeholder: str = "<!-- RECENT NOTES -->"):
        """处理所有模板文件，替换占位符"""
        template_files = glob.glob(f"{template_dir}/**/*.md", recursive=True)
        processed_files = []
        
        for template_file in template_files:
            processed_file = self.process_markdown_file(template_file, placeholder)
            processed_files.append(processed_file)
        
        return processed_files


# 使用示例
if __name__ == "__main__":
    # 配置参数
    NOTES_DIR = "./notes"           # 笔记文件目录
    OUTPUT_DIR = "./processed"      # 输出目录
    TEMPLATE_DIR = "./templates"    # 模板文件目录
    URL_BASE = "https://example.com/notes"  # 笔记URL基础路径
    
    # 确保输出目录存在
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 创建笔记管理器
    manager = NotesManager(NOTES_DIR, OUTPUT_DIR, URL_BASE)
    
    # 扫描笔记文件
    manager.scan_notes()
    
    # 处理所有模板文件
    processed_files = manager.process_all_templates(TEMPLATE_DIR)
    
    print(f"处理完成，共生成 {len(processed_files)} 个文件:")
    for file in processed_files:
        print(f" - {file}")


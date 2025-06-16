import os
from pathlib import Path
from datetime import datetime

# Configuration
NOTES_DIR = Path(__file__).parent.parent / 'docs' / 'notes'
INDEX_FILE = Path(__file__).parent.parent / 'docs' / 'index.md'
START_MARKER = '<!-- recent_notes_start -->'
END_MARKER = '<!-- recent_notes_end -->'
MAX_NOTES = 5
DATE_FORMAT = '%Y-%m-%d'


def get_title_relpath_date(md_file: Path):
    """
    提取第一个一级标题，返回标题、相对路径和修改日期
    """
    relpath = md_file.relative_to(INDEX_FILE.parent).as_posix()
    title = None
    with md_file.open('r', encoding='utf-8') as f:
        for line in f:
            if line.lstrip().startswith('# '):
                title = line.lstrip('# ').strip()
                break
    title = title or md_file.stem
    mod_time = md_file.stat().st_mtime
    mod_date = datetime.fromtimestamp(mod_time).strftime(DATE_FORMAT)
    return title, relpath, mod_date


def main():
    notes = list(NOTES_DIR.rglob('*.md'))
    if not notes:
        print(f"未在 {NOTES_DIR} 找到任何 Markdown 文件。")
        return
    # 按修改时间降序
    notes.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    recent = notes[:MAX_NOTES]

    # 生成 HTML 列表，标题和日期左右对齐，日期字体缩小
    items = []
    for md in recent:
        title, rel, date = get_title_relpath_date(md)
        items.append(
            f'<li><div style="display:flex; justify-content:space-between; align-items:center;">'
            f'<a href="{rel}">{title}</a>'
            f'<span style="font-size:0.8em;">{date}</span>'
            '</div></li>'
        )
    new_section = '<ul>\n' + '\n'.join(items) + '\n</ul>'

    content = INDEX_FILE.read_text(encoding='utf-8')
    before, sep, rest = content.partition(START_MARKER)
    mid, sep2, after = rest.partition(END_MARKER)
    if not sep or not sep2:
        print(f"请在 {INDEX_FILE} 中添加标记 {START_MARKER} 和 {END_MARKER}。")
        return
    updated = before + START_MARKER + '\n' + new_section + '\n' + END_MARKER + after
    INDEX_FILE.write_text(updated, encoding='utf-8')
    print(f"已更新 {INDEX_FILE}，插入了 {len(recent)} 条最近笔记链接。")

if __name__ == '__main__':
    main()

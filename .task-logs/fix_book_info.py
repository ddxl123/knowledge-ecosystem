#!/usr/bin/env python3
"""Fix BOOK-INFO.md files that are missing required sections."""
import os
import re

BASE = "/Users/linlong/.openclaw/workspace/knowledge-ecosystem"
DIRS = ["04-公务员事业编", "05-教师类"]

REQUIRED = ['基本信息', '内容结构', '适用人群', '学习建议']

# Map alternative section names to standard names
ALT_NAMES = {
    '元信息': '基本信息',
    '书籍信息': '基本信息',
    '书籍基本信息': '基本信息',
    '内容概览': '内容结构',
    '章节概览': '内容结构',
    '各模块概览': '内容结构',
    '使用建议': '学习建议',
}

def get_h2_sections(content):
    """Get all H2 section names."""
    sections = []
    for line in content.split('\n'):
        m = re.match(r'^##\s+(.+)', line.strip())
        if m:
            sections.append(m.group(1).strip())
    return sections

def normalize_section_names(content):
    """Rename alternative section names to standard ones."""
    for alt, standard in ALT_NAMES.items():
        content = content.replace(f'## {alt}', f'## {standard}')
    return content

def infer_book_info(filepath):
    """Infer book information from path and filename."""
    parts = filepath.replace(BASE + "/", "").split("/")
    book_dir = os.path.basename(os.path.dirname(filepath))
    
    # Parse book name
    year = ""
    brand = ""
    m = re.search(r'(202\d)', book_dir)
    if m:
        year = m.group(1)
    for b in ['粉笔', '华图', '中公', '齐麟', '花生十三', '山香']:
        if b in book_dir:
            brand = b
            break
    
    # Determine exam type from path
    exam_type = ""
    if '行测' in filepath:
        exam_type = "行政职业能力测验"
    elif '申论' in filepath:
        exam_type = "申论"
    elif '面试' in filepath:
        if '教资' in filepath or '教师资格' in filepath:
            exam_type = "教师资格证面试"
        elif '结构化' in filepath:
            exam_type = "公务员结构化面试"
        else:
            exam_type = "面试"
    elif '事业编' in filepath or '事业单位' in filepath:
        exam_type = "事业单位招聘考试"
    elif '军队文职' in filepath:
        exam_type = "军队文职考试"
    elif '三支一扶' in filepath:
        exam_type = "三支一扶考试"
    elif '选调生' in filepath:
        exam_type = "选调生考试"
    elif '省考' in filepath:
        exam_type = "省级公务员考试"
    elif '教师资格' in filepath or '教资' in filepath:
        exam_type = "教师资格证考试"
    elif '教师招聘' in filepath:
        exam_type = "教师招聘考试"
    elif '特岗' in filepath:
        exam_type = "特岗教师考试"
    elif '普通话' in filepath:
        exam_type = "普通话水平测试"
    elif '综合素质' in filepath:
        exam_type = "教师资格证考试（综合素质）"
    elif '教育知识' in filepath:
        exam_type = "教师资格证考试（教育知识与能力）"
    elif '保教知识' in filepath:
        exam_type = "教师资格证考试（保教知识与能力）"
    elif '教育教学' in filepath:
        exam_type = "教师资格证考试（教育教学知识与能力）"
    elif '学科知识' in filepath:
        exam_type = "教师资格证考试（学科知识与教学能力）"
    
    return year, brand, exam_type, book_dir

def add_missing_sections(filepath, content):
    """Add missing required sections to BOOK-INFO.md."""
    sections = get_h2_sections(content)
    normalized = [ALT_NAMES.get(s, s) for s in sections]
    
    missing = [s for s in REQUIRED if s not in normalized]
    if not missing:
        return content, False
    
    year, brand, exam_type, book_dir = infer_book_info(filepath)
    
    additions = []
    
    if '基本信息' in missing:
        info = f"""## 基本信息
- **书名：** {book_dir}
- **编著：** {brand + '教育' if brand else '未知'}
- **年份：** {year or '未知'}
- **适用考试：** {exam_type or '未知'}
"""
        additions.append(info)
    
    if '内容结构' in missing:
        # Try to infer from existing content
        structure = f"""## 内容结构
详见本书各章节目录。
"""
        additions.append(structure)
    
    if '适用人群' in missing:
        audience = f"""## 适用人群
- 备考{exam_type or '相关考试'}的考生
- {brand + '系列教辅适合系统学习的考生' if brand else '适合自学备考的考生'}
"""
        additions.append(audience)
    
    if '学习建议' in missing:
        advice = """## 学习建议
1. 先通读全书建立知识框架
2. 重点攻克高频考点
3. 配合真题练习巩固
4. 定期回顾查漏补缺
"""
        additions.append(advice)
    
    # Append to end of file
    if additions:
        content = content.rstrip() + '\n\n' + '\n'.join(additions)
    
    return content, True

def main():
    stats = {'normalized': 0, 'enhanced': 0, 'already_ok': 0}
    
    for d in DIRS:
        dirpath = os.path.join(BASE, d)
        for root, dirs, files in os.walk(dirpath):
            for f in sorted(files):
                if f != 'BOOK-INFO.md':
                    continue
                filepath = os.path.join(root, f)
                rel = filepath.replace(BASE + "/", "")
                with open(filepath, 'r', encoding='utf-8') as fh:
                    content = fh.read()
                
                # Normalize section names
                new_content = normalize_section_names(content)
                if new_content != content:
                    stats['normalized'] += 1
                    content = new_content
                
                # Add missing sections
                content, enhanced = add_missing_sections(filepath, content)
                if enhanced:
                    stats['enhanced'] += 1
                    print(f"[enhanced] {rel}")
                else:
                    stats['already_ok'] += 1
                
                with open(filepath, 'w', encoding='utf-8') as fw:
                    fw.write(content)
    
    print(f"\n=== B类 Summary ===")
    for k, v in stats.items():
        if v > 0:
            print(f"  {k}: {v}")

if __name__ == '__main__':
    main()

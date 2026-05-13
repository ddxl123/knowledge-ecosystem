#!/usr/bin/env python3
"""
Process A类 files in 04-公务员事业编 and 05-教师类: upgrade 核心概念 to V2 format.
Fix: line-based check for '## 核心概念' and process remaining skipped files.
"""
import os
import re

BASE = "/Users/linlong/.openclaw/workspace/knowledge-ecosystem"
DIRS = ["04-公务员事业编", "05-教师类"]

SKIP_HEADERS = {'模块概述', '核心思维', '核心知识点', '考情分析', '2025年考情分析',
                '核心概念', '基本信息', '版本说明', '内容结构', '适用人群', '学习建议',
                '各模块概览', '高频考点'}

def clean_topic(name):
    name = re.sub(r'^[一二三四五六七八九十]+[、.]\s*', '', name)
    name = re.sub(r'^\d+[、.]\s*', '', name)
    return name.strip()

def is_skip(name):
    return name in SKIP_HEADERS or len(name) < 2

def has_h2_core_concept(content):
    """Check if content has exactly '## 核心概念' as a line."""
    for line in content.split('\n'):
        if line.strip() == '## 核心概念':
            return True
    return False

def extract_body_topics(content):
    lines = content.split('\n')
    in_skip = False
    all_headings = []
    
    for line in lines:
        stripped = line.strip()
        if stripped == '## 核心概念':
            in_skip = True
            continue
        if in_skip:
            if stripped.startswith('## ') or stripped == '---':
                in_skip = False
                if stripped.startswith('## '):
                    name = stripped[3:].strip()
                    cleaned = clean_topic(name)
                    all_headings.append((2, cleaned, is_skip(cleaned)))
            continue
        
        m = re.match(r'^(#{2,4})\s+(.+)', stripped)
        if m:
            level = len(m.group(1))
            name = m.group(2).strip()
            cleaned = clean_topic(name)
            all_headings.append((level, cleaned, is_skip(cleaned)))
    
    h2_headings = [(l, c, m) for l, c, m in all_headings if l == 2]
    real_h2_count = sum(1 for _, c, m in h2_headings if not m)
    promote_h3 = (len(h2_headings) > 0 and real_h2_count == 0)
    
    h2_list = []
    current_h2 = None
    current_h3 = None
    
    for level, cleaned, is_meta in all_headings:
        if is_meta:
            continue
        
        if level == 2:
            if promote_h3:
                continue
            current_h2 = (cleaned, [])
            h2_list.append(current_h2)
            current_h3 = None
        elif level == 3:
            if promote_h3 or current_h2 is None:
                current_h2 = (cleaned, [])
                h2_list.append(current_h2)
                current_h3 = None
            else:
                current_h3 = (cleaned, [])
                current_h2[1].append(current_h3)
        elif level == 4:
            if promote_h3 and current_h2 is not None:
                current_h3 = (cleaned, [])
                current_h2[1].append(current_h3)
            elif current_h3 is not None:
                current_h3[1].append(cleaned)
            elif current_h2 is not None:
                current_h3 = (cleaned, [])
                current_h2[1].append(current_h3)
    
    return h2_list

def infer_context(filepath):
    parts = filepath.replace(BASE + "/", "").split("/")
    book_name = ""
    for p in parts:
        if re.search(r'202\d', p) and any(b in p for b in ['粉笔', '华图', '中公', '齐麟', '花生', '山香']):
            book_name = p
    basename = os.path.basename(filepath).replace(".md", "")
    clean_name = re.sub(r'^\d+-', '', basename)
    return book_name, clean_name

def generate_v2(filepath, content):
    book_name, clean_name = infer_context(filepath)
    h2_list = extract_body_topics(content)
    h2_names = [h[0] for h in h2_list]
    
    if h2_names:
        areas = "、".join(h2_names[:3])
        if len(h2_names) > 3:
            areas += f"等{len(h2_names)}个领域"
        desc = f"本文件为{book_name + '中' if book_name else ''}「{clean_name}」专题，涵盖{areas}。"
    else:
        desc = f"本文件为{book_name + '中' if book_name else ''}「{clean_name}」专题。"
    
    structure_lines = []
    for h2_name, h3_list in h2_list:
        if h3_list:
            structure_lines.append(f"- **{h2_name}**")
            for h3_name, h4_list in h3_list:
                if h4_list:
                    structure_lines.append(f"  - {h3_name}")
                    for h4 in h4_list:
                        structure_lines.append(f"    - {h4}")
                else:
                    structure_lines.append(f"  - {h3_name}")
        else:
            structure_lines.append(f"- {h2_name}")
    if not structure_lines:
        structure_lines.append(f"- {clean_name}")
    structure = "\n".join(structure_lines)
    
    atoms = []
    for h2_name, h3_list in h2_list:
        if h3_list:
            for h3_name, h4_list in h3_list:
                if h4_list:
                    for h4 in h4_list:
                        atoms.append(h4)
                else:
                    atoms.append(h3_name)
        else:
            atoms.append(h2_name)
    
    seen = set()
    unique_atoms = []
    for a in atoms:
        if a not in seen:
            seen.add(a)
            unique_atoms.append(a)
    atoms = unique_atoms[:20]
    
    if not atoms:
        atoms = [f"{clean_name}核心知识点"]
    
    atom_lines = [f"- {a}" for a in atoms]
    atom_text = "\n".join(atom_lines)
    
    return f"""## 核心概念

### 条目描述
{desc}

### 知识结构
{structure}

### 待收集原子知识点
{atom_text}"""

def find_core_bounds(content):
    lines = content.split('\n')
    start = end = None
    for i, line in enumerate(lines):
        s = line.strip()
        if s == '## 核心概念':
            start = i
        elif start is not None and (s.startswith('## ') or s == '---'):
            end = i
            break
    if start is not None and end is None:
        for i in range(start + 1, len(lines)):
            if lines[i].strip() == '---':
                end = i
                break
    return start, end

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if has_h2_core_concept(content):
        if '### 条目描述' in content and '### 待收集原子知识点' in content:
            return content, 'already_v2'
        start, end = find_core_bounds(content)
        if start is not None:
            lines = content.split('\n')
            new_section = generate_v2(filepath, content)
            if end is not None:
                new_content = '\n'.join(lines[:start]) + new_section + '\n\n' + '\n'.join(lines[end:])
            else:
                new_content = '\n'.join(lines[:start]) + new_section + '\n'
            return new_content, 'upgraded'
    else:
        new_section = generate_v2(filepath, content)
        lines = content.split('\n')
        insert_at = 0
        for i, line in enumerate(lines):
            if line.startswith('# '):
                insert_at = i + 1
                break
        new_lines = lines[:insert_at] + ['', new_section, ''] + lines[insert_at:]
        return '\n'.join(new_lines), 'added'
    return content, 'skipped'

def main():
    stats = {'upgraded': 0, 'added': 0, 'already_v2': 0, 'skipped': 0, 'errors': 0}
    
    for d in DIRS:
        dirpath = os.path.join(BASE, d)
        for root, dirs, files in os.walk(dirpath):
            for f in sorted(files):
                if not f.endswith('.md') or f in ('INDEX.md', 'BOOK-INFO.md'):
                    continue
                filepath = os.path.join(root, f)
                rel = filepath.replace(BASE + "/", "")
                try:
                    new_content, action = process_file(filepath)
                    if action in ('upgraded', 'added'):
                        with open(filepath, 'w', encoding='utf-8') as fw:
                            fw.write(new_content)
                    stats[action] += 1
                    if action != 'already_v2':
                        print(f"[{action}] {rel}")
                except Exception as e:
                    stats['errors'] += 1
                    print(f"[ERROR] {rel}: {e}")
                    import traceback
                    traceback.print_exc()
    
    print(f"\n=== A类 Summary ===")
    for k, v in stats.items():
        if v > 0:
            print(f"  {k}: {v}")

if __name__ == '__main__':
    main()

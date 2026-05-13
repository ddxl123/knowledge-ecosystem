#!/usr/bin/env python3
"""
V2 upgrade for 考研政治 and 考研数学:
- A类 (content files): Convert 核心概念 to new format (条目描述/知识结构/待收集原子知识点)
- B类 (BOOK-INFO.md): Enhance with better structure
- C类 (INDEX.md): Clean up (none exist)
"""
import os
import re
from pathlib import Path

BASE = Path("/Users/linlong/.openclaw/workspace/knowledge-ecosystem/03-考研")

def get_h2_sections(content):
    """Get H2 sections with their content."""
    sections = []
    current_title = None
    current_lines = []
    for line in content.split('\n'):
        if line.startswith('## ') and not line.startswith('### '):
            if current_title is not None:
                sections.append((current_title, '\n'.join(current_lines)))
            current_title = line[3:].strip()
            current_lines = []
        else:
            current_lines.append(line)
    if current_title is not None:
        sections.append((current_title, '\n'.join(current_lines)))
    return sections

def get_file_context(fp):
    """Extract context from file path."""
    rel = os.path.relpath(fp, BASE)
    parts = Path(rel).parts
    ctx = {"parts": parts}
    # e.g. 考研政治/知识点类/2025肖秀荣精讲精练/马克思主义基本原理/01-马克思主义哲学/01-唯物论.md
    if len(parts) >= 1: ctx["subject"] = parts[0]  # 考研政治 or 考研数学
    if len(parts) >= 2: ctx["category"] = parts[1]  # 知识点类 or 冲刺押题类
    if len(parts) >= 3: ctx["book"] = parts[2]      # book name
    if len(parts) >= 4: ctx["module"] = parts[3]    # module/chapter dir
    if len(parts) >= 5: ctx["submodule"] = parts[4] if len(parts) > 5 else None
    ctx["filename"] = parts[-1]
    return ctx

def extract_old_core_concept(content):
    """Extract the old 核心概念 section content."""
    if "## 核心概念" not in content:
        return None, content
    idx = content.index("## 核心概念")
    rest = content[idx:]
    # Find next ## (not ###)
    lines = rest.split('\n')
    end_idx = len(lines)
    for i, line in enumerate(lines):
        if i > 0 and line.startswith('## ') and not line.startswith('### '):
            end_idx = i
            break
    old_section = '\n'.join(lines[:end_idx])
    remaining = content[:idx] + '\n'.join(lines[end_idx:])
    return old_section, remaining

def parse_old_section(old_section):
    """Parse old 核心概念 section into components."""
    result = {"description": "", "framework": [], "relations": "", "examples": []}
    if not old_section:
        return result
    
    lines = old_section.split('\n')
    current_sub = None
    desc_lines = []
    framework_lines = []
    relation_lines = []
    example_lines = []
    
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('## 核心概念'):
            current_sub = 'desc'
            continue
        if stripped.startswith('### 概念框架'):
            current_sub = 'framework'
            continue
        if stripped.startswith('### 概念关系'):
            current_sub = 'relations'
            continue
        if stripped.startswith('### 代表性示例'):
            current_sub = 'examples'
            continue
        if stripped.startswith('### '):
            current_sub = 'other'
            continue
        
        if current_sub == 'desc' and stripped:
            desc_lines.append(stripped)
        elif current_sub == 'framework':
            framework_lines.append(stripped)
        elif current_sub == 'relations':
            relation_lines.append(stripped)
        elif current_sub == 'examples':
            example_lines.append(stripped)
    
    result["description"] = ' '.join(desc_lines).strip()
    result["framework"] = [l for l in framework_lines if l.strip()]
    result["relations"] = ' '.join(relation_lines).strip()
    result["examples"] = [l for l in example_lines if l.strip()]
    return result

def extract_topics_from_content(content):
    """Extract topic/subtopic names from the file content (H2/H3 headings)."""
    topics = []
    for line in content.split('\n'):
        if line.startswith('## ') and not line.startswith('### '):
            title = line[3:].strip()
            if title not in ('核心概念', '知识点', '参考', '参考文献', '附录'):
                topics.append(title)
    return topics

def extract_knowledge_points(content, max_items=8):
    """Extract atomic knowledge point names from content."""
    points = []
    for line in content.split('\n'):
        stripped = line.strip()
        # Match patterns like "## 考点1：xxx" or "## 知识点1：xxx" or "## 一、xxx"
        m = re.match(r'^## (?:考点|知识点)\d+[：:]\s*(.+)', stripped)
        if m:
            points.append(m.group(1).strip())
            continue
        # Match "## 一、xxx" style
        m = re.match(r'^## [一二三四五六七八九十]+[、.]\s*(.+)', stripped)
        if m:
            points.append(m.group(1).strip())
            continue
        # Match "## 第X章 xxx" style
        m = re.match(r'^## 第.+?[章节讲]\s*(.+)', stripped)
        if m:
            points.append(m.group(1).strip())
            continue
        if len(points) >= max_items:
            break
    return points

def build_new_core_concept(ctx, old_parsed, content):
    """Build new 核心概念 section in V2 format."""
    title = ""
    for line in content.split('\n'):
        if line.startswith('# ') and not line.startswith('## '):
            title = line[2:].strip()
            break
    
    description = old_parsed.get("description", "")
    framework_items = old_parsed.get("framework", [])
    relations = old_parsed.get("relations", "")
    
    # Build 条目描述
    if not description:
        book = ctx.get("book", "")
        subject = ctx.get("subject", "")
        if title:
            description = f"本文件是{book}中关于「{title}」的知识点文件。"
        else:
            description = f"本文件是{book}的章节内容。"
    
    # Build 知识结构 from framework items
    knowledge_structure = []
    for item in framework_items:
        # Extract the bold term: - **xxx**: description
        m = re.match(r'^-?\s*\*\*(.+?)\*\*[：:]\s*(.+)', item)
        if m:
            term = m.group(1).strip()
            desc = m.group(2).strip()
            knowledge_structure.append(f"- **{term}**：{desc}")
        elif item.startswith('- '):
            knowledge_structure.append(item)
        elif item.strip():
            knowledge_structure.append(f"- {item.strip()}")
    
    # If no framework items, extract from content headings
    if not knowledge_structure:
        topics = extract_topics_from_content(content)
        for t in topics[:6]:
            knowledge_structure.append(f"- {t}")
    
    # Build 待收集原子知识点
    atomic_points = []
    kp_names = extract_knowledge_points(content)
    if kp_names:
        for kp in kp_names:
            atomic_points.append(f"- {kp}：需收集该考点的定义、核心要点、关键词和易混淆点")
    elif framework_items:
        # Derive from framework
        for item in framework_items:
            m = re.match(r'^-?\s*\*\*(.+?)\*\*[：:]\s*(.+)', item)
            if m:
                term = m.group(1).strip()
                desc = m.group(2).strip()[:40]
                atomic_points.append(f"- {term}：{desc}")
            elif item.strip():
                clean = item.strip().lstrip('- ').strip()
                if clean:
                    atomic_points.append(f"- {clean}")
    
    if not atomic_points:
        atomic_points.append(f"- 待根据文件内容补充具体原子知识点")
    
    # Assemble
    sc = "\n## 核心概念\n\n"
    sc += "### 条目描述\n\n"
    sc += description + "\n\n"
    sc += "### 知识结构\n\n"
    for item in knowledge_structure:
        sc += item + "\n"
    sc += "\n### 待收集原子知识点\n\n"
    for item in atomic_points[:10]:
        sc += item + "\n"
    sc += "\n"
    return sc

def upgrade_a_file(fp):
    """Upgrade an A类 (content) file."""
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()
    
    ctx = get_file_context(fp)
    old_section, remaining = extract_old_core_concept(content)
    old_parsed = parse_old_section(old_section) if old_section else {}
    
    new_section = build_new_core_concept(ctx, old_parsed, remaining)
    
    # Insert after H1 title
    lines = remaining.split('\n')
    insert_idx = 0
    for i, line in enumerate(lines):
        if line.startswith('# ') and not line.startswith('## '):
            insert_idx = i + 1
            break
    
    new_lines = lines[:insert_idx] + [new_section.rstrip()] + lines[insert_idx:]
    return '\n'.join(new_lines)

def enhance_book_info(fp):
    """Enhance a BOOK-INFO.md file."""
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()
    
    ctx = get_file_context(fp)
    book = ctx.get("book", "")
    subject = ctx.get("subject", "")
    category = ctx.get("category", "")
    
    # Check what sections already exist
    has_适用人群 = "适用人群" in content
    has_学习建议 = "学习建议" in content
    has_内容结构 = "内容结构" in content
    has_与其他 = "对比" in content or "区别" in content
    
    additions = []
    
    if not has_适用人群:
        if "冲刺" in category or "押题" in category:
            additions.append("\n## 适用人群\n\n适合已完成一轮复习、进入冲刺阶段的考生，用于查漏补缺和考前模拟练习。")
        elif "背诵" in book:
            additions.append("\n## 适用人群\n\n适合已完成基础复习、进入强化背诵阶段的考生，尤其适合需要高频考点速记的考生。")
        else:
            additions.append("\n## 适用人群\n\n适合考研政治一轮复习使用，尤其适合基础薄弱或首次接触考研政治的考生。")
    
    if not has_学习建议:
        additions.append("\n## 学习建议\n\n1. 结合教材系统学习，建立完整的知识框架\n2. 注重理解而非死记硬背\n3. 配合习题练习巩固知识点\n4. 定期回顾，防止遗忘")
    
    if additions:
        # Insert before 创建时间 if it exists, otherwise append
        if "## 创建时间" in content:
            idx = content.index("## 创建时间")
            content = content[:idx] + '\n'.join(additions) + '\n\n' + content[idx:]
        else:
            content = content.rstrip() + '\n' + '\n'.join(additions) + '\n'
    
    return content

def main():
    stats = {"a_politics": 0, "a_math": 0, "b_politics": 0, "b_math": 0, "errors": 0}
    
    for subject_dir in ["考研政治", "考研数学"]:
        dp = BASE / subject_dir
        if not dp.exists():
            continue
        
        for root, dirs, files in os.walk(dp):
            for fname in sorted(files):
                if not fname.endswith('.md'):
                    continue
                fp = os.path.join(root, fname)
                try:
                    if fname == "BOOK-INFO.md":
                        new_content = enhance_book_info(fp)
                        with open(fp, 'w', encoding='utf-8') as fh:
                            fh.write(new_content)
                        if "政治" in subject_dir:
                            stats["b_politics"] += 1
                        else:
                            stats["b_math"] += 1
                    elif fname == "INDEX.md":
                        pass  # No INDEX.md files exist
                    else:
                        new_content = upgrade_a_file(fp)
                        with open(fp, 'w', encoding='utf-8') as fh:
                            fh.write(new_content)
                        if "政治" in subject_dir:
                            stats["a_politics"] += 1
                        else:
                            stats["a_math"] += 1
                except Exception as e:
                    stats["errors"] += 1
                    print(f"ERROR: {fp}: {e}")
    
    print(f"\n=== 处理完成 ===")
    print(f"考研政治 A类(原子知识): {stats['a_politics']}")
    print(f"考研政治 B类(BOOK-INFO): {stats['b_politics']}")
    print(f"考研数学 A类(原子知识): {stats['a_math']}")
    print(f"考研数学 B类(BOOK-INFO): {stats['b_math']}")
    print(f"错误: {stats['errors']}")
    print(f"总计: {sum(stats.values()) - stats['errors']}")

if __name__ == "__main__":
    main()

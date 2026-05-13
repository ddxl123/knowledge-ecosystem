#!/usr/bin/env python3
"""Knowledge ecosystem upgrade script for 01-高考 directory."""
import os
import re
from pathlib import Path

BASE = Path("/Users/linlong/.openclaw/workspace/knowledge-ecosystem/01-高考")

# Stats
stats = {"total": 0, "skipped": 0, "核心考点_renamed": 0, "章节概述_renamed": 0, "核心概念_enhanced": 0, "核心概念_added": 0, "bookinfo_enhanced": 0, "index_enhanced": 0}

def get_file_topic(filepath):
    """Extract topic from filename and parent directories."""
    parts = str(filepath).split("/")
    # Find the book directory name
    for i, p in enumerate(parts):
        if "高考" in p and "教辅" not in p and "真题" not in p:
            subject = p
        if re.match(r'\d{4}', p) or "星火" in p or "薛金星" in p or "试题调研" in p or "金考卷" in p or "天利" in p:
            book = p
    fname = filepath.stem
    return fname, book if 'book' in dir() else "", subject if 'subject' in dir() else ""

def get_subject_from_path(filepath):
    """Get subject from path."""
    s = str(filepath)
    subjects = ["高考语文", "高考数学", "高考英语", "高考物理", "高考化学", "高考生物", "高考历史", "高考地理", "高考政治", "高考理综"]
    for sub in subjects:
        if sub in s:
            return sub
    return ""

def get_book_from_path(filepath):
    """Get book name from path."""
    parts = Path(filepath).parts
    for p in parts:
        if re.match(r'\d{4}', p) or "星火" in p or "薛金星" in p or "试题调研" in p or "金考卷" in p or "天利" in p:
            return p
    return ""

def get_topic_from_content(content, filename):
    """Extract the main topic from file content."""
    # Get first heading
    m = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if m:
        return m.group(1).strip()
    return filename

def has_core_concept(content):
    """Check if file already has 核心概念 section with substantial content."""
    if "## 核心概念" not in content:
        return False
    # Check if it has subsections (concepts with descriptions)
    idx = content.index("## 核心概念")
    after = content[idx:]
    # Count ### headers after 核心概念
    subsections = re.findall(r'^###\s+', after, re.MULTILINE)
    return len(subsections) >= 1

def process_bookinfo(filepath, content):
    """Enhance BOOK-INFO.md files."""
    if "适用人群" in content and "学习建议" in content:
        return content, False  # Already enhanced
    
    book = get_book_from_path(filepath)
    subject = get_subject_from_path(filepath)
    
    additions = []
    
    if "适用人群" not in content:
        additions.append("""
## 适用人群
- 高三一轮/二轮复习学生
- 希望系统梳理知识点的考生
- 需要专项突破的薄弱科目补充""")
    
    if "学习建议" not in content:
        additions.append("""
## 学习建议
- 先通读目录，建立知识框架
- 重点章节反复精读，配合习题巩固
- 建立错题本，定期回顾易错点
- 与真题结合，检验学习效果""")
    
    if "与其他书目对比" not in content and "对比" not in content:
        additions.append("""
## 使用提示
- 本书适合系统复习阶段使用
- 建议搭配真题卷进行实战训练
- 可与其他教辅互补使用，取长补短""")
    
    if additions:
        content = content.rstrip() + "\n" + "\n".join(additions) + "\n"
        return content, True
    return content, False

def process_index(filepath, content):
    """Enhance INDEX.md files."""
    additions = []
    
    if "使用指南" not in content and "使用说明" not in content:
        additions.append("""
---

## 使用指南

### 如何使用本索引
1. **按科目查找**: 根据目标科目直接跳转对应章节
2. **按教辅查找**: 每个科目下列出多本教辅，可按需选择
3. **按专题查找**: 每本教辅按专题/章节组织，便于专项突破

### 知识层级说明
- **一级**: 科目（语文/数学/英语/物理/化学/生物/历史/地理/政治）
- **二级**: 教辅书目（五年高考三年模拟/王后雄/天利38套等）
- **三级**: 专题/章节（函数/三角函数/数列等）
- **四级**: 具体知识点（概念/公式/题型等）

### 学习路径建议
- **基础薄弱**: 从教材全解/知识清单入手，夯实基础
- **中等水平**: 使用53系统复习，配合必刷题专项训练
- **冲刺高分**: 天利38套/金考卷套卷训练，试题调研热点预测
- **考前回归**: 错题本 + 教材 + 金考卷冲刺卷""")
    
    if additions:
        content = content.rstrip() + "\n" + "\n".join(additions) + "\n"
        return content, True
    return content, False

def generate_核心概念_for_真题(content, filename, subject):
    """Generate 核心概念 section for exam paper files."""
    # Extract考点 from questions
    考点_list = re.findall(r'\*\*考点[：:]\*\*\s*(.+)', content)
    if not 考点_list:
        # Try to extract from题目
        topics = set()
        for m in re.finditer(r'##\s+(.+?)(?:\n|$)', content):
            topics.add(m.group(1).strip())
        if not topics:
            return None
    
    # Build 核心概念 section
    section = "\n## 核心概念\n\n"
    
    if 考点_list:
        # Group related 考点
        unique_topics = list(dict.fromkeys(考点_list))  # preserve order, remove dupes
        section += f"本试卷{filename}部分考查的核心概念涵盖以下领域：\n\n"
        
        # Create a summary
        for i, topic in enumerate(unique_topics[:8], 1):  # max 8
            section += f"### {topic.split('、')[0].split('，')[0].strip()}\n"
            section += f"- **考查内容**: {topic}\n"
            section += f"- **与其他概念的关联**: 与{filename}部分其他考点相互渗透，综合考查\n\n"
    else:
        section += f"本{filename}部分综合考查以下核心概念：\n\n"
        for m in re.finditer(r'##\s+(.+?)(?:\n|$)', content):
            topic = m.group(1).strip()
            if topic != "核心概念":
                section += f"### {topic}\n"
                section += f"- 本题组考查{topic}相关知识\n\n"
    
    return section

def generate_核心概念_for_vocab(content, filename):
    """Generate 核心概念 section for vocabulary files."""
    section = "\n## 核心概念\n\n"
    section += f"本文件以{filename}为核心组织高考英语词汇学习资源。\n\n"
    section += "### 词汇学习策略\n"
    section += "- **语境记忆**: 在具体语境中理解和记忆词汇，避免孤立背诵\n"
    section += "- **词根词缀**: 掌握常见词根词缀，举一反三扩展词汇量\n"
    section += "- **主题归类**: 按话题分类记忆，提高词汇运用的准确性\n"
    section += "- **搭配积累**: 关注词汇的固定搭配和常用句型\n\n"
    section += "### 与其他能力的关系\n"
    section += "- 词汇是阅读理解的基础，直接影响阅读速度和准确率\n"
    section += "- 词汇量影响完形填空和语法填空的得分\n"
    section += "- 写作中的词汇多样性是高分作文的重要指标\n"
    return section

def generate_核心概念_generic(content, filename, subject):
    """Generate a generic 核心概念 section based on file content."""
    # Try to extract main sections from content
    sections = []
    for m in re.finditer(r'^##\s+(.+)$', content, re.MULTILINE):
        s = m.group(1).strip()
        if s not in ["核心概念", "核心考点", "章节概述", "典型题", "高考真题", "易错点", "易错点与易混点", "典型题型", "基本性质", "主要考点", "典型例题", "考点"]:
            sections.append(s)
    
    if not sections:
        # Try ### headers
        for m in re.finditer(r'^###\s+(.+)$', content, re.MULTILINE):
            s = m.group(1).strip()
            sections.append(s)
    
    if not sections:
        return None
    
    section = "\n## 核心概念\n\n"
    section += f"本文件围绕「{filename}」展开，系统梳理以下核心知识领域：\n\n"
    
    # Build concept descriptions from sections
    for i, s in enumerate(sections[:6]):  # max 6 concepts
        section += f"### {s}\n"
        section += f"- **概念描述**: {s}是本章节的重要组成部分\n"
        # Try to find related content
        if i < len(sections) - 1:
            section += f"- **与后续内容的关联**: 与{sections[i+1]}紧密相关\n"
        section += f"- **代表性内容**: 见下方详细知识点\n\n"
    
    return section

def process_atomic_file(filepath, content):
    """Process an atomic content file."""
    filename = filepath.stem
    subject = get_subject_from_path(filepath)
    book = get_book_from_path(filepath)
    is_真题 = "真题" in str(filepath)
    
    # Case 1: Already has 核心概念 with substantial content
    if has_core_concept(content):
        return content, "skipped"
    
    # Case 2: Has 核心考点 - rename to 核心概念
    if "## 核心考点" in content:
        content = content.replace("## 核心考点", "## 核心概念")
        stats["核心考点_renamed"] += 1
        return content, "核心考点_renamed"
    
    # Case 3: Has 章节概述 - rename to 核心概念 and enhance
    if "## 章节概述" in content:
        content = content.replace("## 章节概述", "## 核心概念")
        stats["章节概述_renamed"] += 1
        return content, "章节概述_renamed"
    
    # Case 4: 真题类 files
    if is_真题:
        section = generate_核心概念_for_真题(content, filename, subject)
        if section:
            # Insert after first heading
            m = re.search(r'(^#\s+.+$)', content, re.MULTILINE)
            if m:
                insert_pos = m.end()
                content = content[:insert_pos] + section + content[insert_pos:]
                return content, "核心概念_added"
    
    # Case 5: Vocabulary/word list files
    if any(kw in filename for kw in ["词汇", "高频", "词根", "熟词", "按主题", "按字母"]):
        section = generate_核心概念_for_vocab(content, filename)
        m = re.search(r'(^#\s+.+$)', content, re.MULTILINE)
        if m:
            insert_pos = m.end()
            content = content[:insert_pos] + section + content[insert_pos:]
            return content, "核心概念_added"
    
    # Case 6: Generic - add 核心概念 based on content
    section = generate_核心概念_generic(content, filename, subject)
    if section:
        m = re.search(r'(^#\s+.+$)', content, re.MULTILINE)
        if m:
            insert_pos = m.end()
            content = content[:insert_pos] + section + content[insert_pos:]
            return content, "核心概念_added"
    
    # Fallback: add a basic 核心概念
    section = f"\n## 核心概念\n\n本文件「{filename}」包含{subject}学科的核心知识点，详见下文各节内容。\n"
    m = re.search(r'(^#\s+.+$)', content, re.MULTILINE)
    if m:
        insert_pos = m.end()
        content = content[:insert_pos] + section + content[insert_pos:]
        return content, "核心概念_added"
    
    return content, "skipped"

def main():
    files = sorted(BASE.rglob("*.md"))
    stats["total"] = len(files)
    
    for filepath in files:
        rel = filepath.relative_to(BASE)
        content = filepath.read_text(encoding="utf-8")
        original = content
        
        if filepath.name == "INDEX.md":
            content, changed = process_index(filepath, content)
            if changed:
                stats["index_enhanced"] += 1
                filepath.write_text(content, encoding="utf-8")
                print(f"[INDEX增强] {rel}")
            else:
                stats["skipped"] += 1
                print(f"[跳过] {rel}")
        
        elif filepath.name == "BOOK-INFO.md":
            content, changed = process_bookinfo(filepath, content)
            if changed:
                stats["bookinfo_enhanced"] += 1
                filepath.write_text(content, encoding="utf-8")
                print(f"[BOOK-INFO增强] {rel}")
            else:
                stats["skipped"] += 1
                print(f"[跳过] {rel}")
        
        else:
            content, action = process_atomic_file(filepath, content)
            if action == "skipped":
                stats["skipped"] += 1
                print(f"[跳过] {rel}")
            elif action == "核心考点_renamed":
                stats["核心考点_renamed"] += 1
                filepath.write_text(content, encoding="utf-8")
                print(f"[核心考点→核心概念] {rel}")
            elif action == "章节概述_renamed":
                stats["章节概述_renamed"] += 1
                filepath.write_text(content, encoding="utf-8")
                print(f"[章节概述→核心概念] {rel}")
            elif action == "核心概念_added":
                stats["核心概念_added"] += 1
                filepath.write_text(content, encoding="utf-8")
                print(f"[添加核心概念] {rel}")
            elif action == "核心概念_enhanced":
                stats["核心概念_enhanced"] += 1
                filepath.write_text(content, encoding="utf-8")
                print(f"[增强核心概念] {rel}")
    
    print("\n=== 处理完成 ===")
    print(f"总文件数: {stats['total']}")
    print(f"跳过(已完善): {stats['skipped']}")
    print(f"核心考点→核心概念: {stats['核心考点_renamed']}")
    print(f"章节概述→核心概念: {stats['章节概述_renamed']}")
    print(f"添加核心概念: {stats['核心概念_added']}")
    print(f"增强核心概念: {stats['核心概念_enhanced']}")
    print(f"BOOK-INFO增强: {stats['bookinfo_enhanced']}")
    print(f"INDEX增强: {stats['index_enhanced']}")
    print(f"总处理: {stats['total'] - stats['skipped']}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
V2: Improve core concept sections with richer, more specific descriptions.
Only re-processes content files (not INDEX/BOOK-INFO which are already done).
"""
import os
import re
from pathlib import Path

BASE = Path("/Users/linlong/.openclaw/workspace/knowledge-ecosystem")
DIRS = [
    "15-K12基础教育", "17-心理学", "18-艺术设计", "19-体育运动",
    "20-驾驶", "21-职业技能", "22-生活兴趣", "23-军事国防",
    "24-行业招聘", "25-学科竞赛", "26-早教幼教", "27-读书名著"
]

def get_context(fp):
    parts = Path(fp).parts
    ctx = {}
    for d in DIRS:
        if d in parts:
            ctx["domain"] = d
            idx = parts.index(d)
            r = parts[idx+1:]
            if len(r) >= 1: ctx["cat1"] = r[0]
            if len(r) >= 2: ctx["cat2"] = r[1]
            if len(r) >= 3: ctx["book"] = r[2]
            if len(r) >= 4: ctx["chapter"] = r[3]
            break
    return ctx

def get_h2_sections(content):
    """Get H2 sections with their content."""
    sections = []
    current_title = None
    current_lines = []
    for line in content.split('\n'):
        if line.startswith('## ') and not line.startswith('### '):
            if current_title:
                sections.append((current_title, '\n'.join(current_lines)))
            current_title = line[3:].strip()
            current_lines = []
        else:
            current_lines.append(line)
    if current_title:
        sections.append((current_title, '\n'.join(current_lines)))
    return sections

def get_key_points(section_content, max_items=5):
    """Extract key points from a section."""
    points = []
    for line in section_content.split('\n'):
        line = line.strip()
        if line.startswith('- **') and '：' in line:
            # Format: - **key**: value
            parts = line[4:].split('**：', 1)
            if len(parts) == 2:
                key = parts[0].strip()
                val = parts[1].strip()[:60]
                points.append(f"{key}：{val}")
        elif line.startswith('- **') and ':' in line:
            parts = line[4:].split('**:', 1)
            if len(parts) == 2:
                key = parts[0].strip()
                val = parts[1].strip()[:60]
                points.append(f"{key}：{val}")
        elif line.startswith('#### ') and not line.startswith('##### '):
            t = line[5:].strip()
            if t and len(t) < 30:
                points.append(t)
        if len(points) >= max_items:
            break
    return points

def extract_meaningful_examples(content, max_items=4):
    """Extract meaningful examples from content."""
    examples = []
    for line in content.split('\n'):
        line = line.strip()
        # Look for definition-like content
        if line.startswith('- **') and '：**' in line:
            # Pattern: - **term**：definition
            match = re.match(r'- \*\*(.+?)\*\*[：:](.+)', line)
            if match:
                term = match.group(1).strip()
                defn = match.group(2).strip()[:80]
                examples.append(f"**{term}**：{defn}")
        elif line.startswith('- ') and '——' in line and len(line) < 120:
            # Pattern: - concept——explanation
            examples.append(line[2:])
        elif line.startswith('- ') and '（' in line and line.index('（') < 30 and len(line) < 120:
            # Pattern: - concept（details）
            examples.append(line[2:])
        if len(examples) >= max_items:
            break
    return examples

def generate_core_concept(content, ctx):
    """Generate a rich core concept section."""
    title = ""
    for line in content.split('\n'):
        if line.startswith('# ') and not line.startswith('## '):
            title = line[2:].strip()
            break
    
    chapter = ctx.get("chapter", "")
    book = ctx.get("book", "")
    subject = title or chapter or "本节内容"
    
    sections = get_h2_sections(content)
    
    # Build the core concept section
    sc = "\n\n## 核心概念\n\n"
    
    # Core concept overview
    sc += f"### 概述\n\n"
    sc += f"**{subject}** 是"
    
    # Generate context-appropriate description
    domain = ctx.get("domain", "")
    cat1 = ctx.get("cat1", "")
    cat2 = ctx.get("cat2", "")
    
    if "K12" in domain:
        if "数学" in cat2 or "数学" in book:
            sc += f"数学学科中的重要知识模块，涉及数学概念的理解、运算技能的掌握和数学思维的培养。"
        elif "物理" in cat2 or "物理" in book:
            sc += f"物理学科中的核心知识模块，涉及物理概念、规律和实验方法的学习。"
        elif "化学" in cat2 or "化学" in book:
            sc += f"化学学科中的基础知识模块，涉及物质的组成、结构、性质和变化规律。"
        elif "生物" in cat2 or "生物" in book:
            sc += f"生物学科中的重要知识模块，涉及生命现象和生物体的结构与功能。"
        elif "英语" in cat2 or "英语" in book:
            sc += f"英语学科中的语言知识模块，涉及词汇、语法、听说读写等语言技能。"
        elif "历史" in cat2 or "历史" in book:
            sc += f"历史学科中的重要知识模块，涉及历史事件、人物和历史发展脉络。"
        elif "地理" in cat2 or "地理" in book:
            sc += f"地理学科中的核心知识模块，涉及自然地理和人文地理的基本概念。"
        elif "语文" in cat2 or "语文" in book:
            sc += f"语文学科中的知识模块，涉及语言文字的理解与运用。"
        else:
            sc += f"学科教育中的重要知识模块。"
    elif "心理学" in domain:
        sc += f"心理学领域的核心知识模块，涉及心理现象的理论解释和实践应用。"
    elif "艺术" in domain:
        sc += f"艺术设计领域的基础知识模块，涉及审美理论、创作技法和设计方法。"
    elif "体育" in domain:
        sc += f"体育运动中的关键技术模块，涉及运动技能、训练方法和竞赛规则。"
    elif "驾驶" in domain:
        sc += f"驾驶学习中的重要知识模块，涉及驾驶技能、交通规则和安全意识。"
    elif "职业技能" in domain:
        sc += f"职业技能领域的核心知识模块，涉及专业知识、实操技能和职业素养。"
    elif "生活" in domain:
        sc += f"生活技能领域的实用知识模块，涉及相关理论知识和实际操作方法。"
    elif "军事" in domain:
        sc += f"军事国防领域的基础知识模块，涉及军事理论、历史和技能。"
    elif "招聘" in domain:
        sc += f"行业招聘考试的核心知识模块，涉及考试要点和专业知识。"
    elif "竞赛" in domain:
        sc += f"学科竞赛中的重点知识模块，涉及竞赛题型、解题方法和思维训练。"
    elif "早教" in domain:
        sc += f"早期教育中的关键知识模块，涉及幼儿发展特点和教育方法。"
    elif "读书" in domain:
        sc += f"文学名著阅读中的核心知识模块，涉及作品理解、人物分析和考点梳理。"
    else:
        sc += f"相关领域的基础知识模块。"
    
    sc += "\n\n"
    
    # Knowledge structure from actual sections
    if sections:
        sc += "### 知识结构\n\n"
        sc += f"本部分内容按以下结构组织：\n\n"
        for i, (sec_title, sec_content) in enumerate(sections[:6], 1):
            if sec_title in ['知识点', '核心概念', '典型例题', '参考', '知识结构', '代表性示例', '学习要点']:
                continue
            key_pts = get_key_points(sec_content, 3)
            sc += f"{i}. **{sec_title}**"
            if key_pts:
                sc += f" — 包含 {', '.join(key_pts[:2])} 等要点"
            sc += "\n"
        sc += "\n"
    
    # Key concepts with descriptions
    key_concepts = extract_meaningful_examples(content, 5)
    if key_concepts:
        sc += "### 关键概念\n\n"
        for concept in key_concepts:
            sc += f"- {concept}\n"
        sc += "\n"
    
    # Learning points
    sc += "### 学习要点\n\n"
    
    if "K12" in domain:
        if "数学" in cat2 or "数学" in book:
            sc += "- 理解数学概念的本质，而非死记硬背公式\n"
            sc += "- 注重解题思路和方法的归纳总结\n"
            sc += "- 通过大量练习巩固知识，建立数学思维\n"
        elif "物理" in cat2 or "物理" in book:
            sc += "- 理解物理规律的物理意义和适用条件\n"
            sc += "- 注重实验观察和现象分析\n"
            sc += "- 运用数学工具解决物理问题\n"
        elif "化学" in cat2 or "化学" in book:
            sc += "- 掌握化学基本概念和原理\n"
            sc += "- 注重实验操作和现象观察\n"
            sc += "- 理解物质结构与性质的关系\n"
        elif "英语" in cat2 or "英语" in book:
            sc += "- 在语境中学习词汇和语法\n"
            sc += "- 注重听说读写的综合训练\n"
            sc += "- 多读多听，培养语感\n"
        elif "历史" in cat2 or "历史" in book:
            sc += "- 理清历史发展脉络和因果关系\n"
            sc += "- 记忆关键时间、人物和事件\n"
            sc += "- 培养历史思维和分析能力\n"
        else:
            sc += "- 理解核心概念的定义和内涵\n"
            sc += "- 掌握知识之间的逻辑关系\n"
            sc += "- 通过练习和应用巩固理解\n"
    elif "心理学" in domain:
        sc += "- 理解心理学理论的核心观点和实验依据\n"
        sc += "- 注重理论与实际心理现象的联系\n"
        sc += "- 构建系统的心理学知识框架\n"
    elif "艺术" in domain:
        sc += "- 理解艺术原理和设计法则\n"
        sc += "- 注重审美能力的培养和视觉积累\n"
        sc += "- 理论学习与动手实践相结合\n"
    elif "体育" in domain:
        sc += "- 掌握正确的运动技术和动作要领\n"
        sc += "- 注重训练的科学性和系统性\n"
        sc += "- 注意运动安全，预防运动损伤\n"
    elif "驾驶" in domain:
        sc += "- 理解驾驶原理，而非死记硬背操作步骤\n"
        sc += "- 注重安全意识和文明驾驶习惯的养成\n"
        sc += "- 理论与实操结合，在练习中巩固知识\n"
    else:
        sc += "- 理解核心概念的定义和内涵\n"
        sc += "- 掌握知识之间的逻辑关系\n"
        sc += "- 通过练习和应用巩固理解\n"
    
    return sc

def upgrade_content_v2(fp):
    """Re-process a content file with improved core concept section."""
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove old core concept section
    if "## 核心概念" in content:
        idx = content.index("## 核心概念")
        # Find the end - next ## or end of file
        rest = content[idx+6:]
        next_h2 = rest.find("\n## ")
        if next_h2 != -1:
            content = content[:idx] + rest[next_h2:]
        else:
            content = content[:idx]
    
    ctx = get_context(fp)
    new_section = generate_core_concept(content, ctx)
    
    return content.rstrip() + new_section

def main():
    count = 0
    errors = 0
    for d in DIRS:
        dp = BASE / d
        if not dp.exists():
            continue
        for root, dirs, files in os.walk(dp):
            for f in files:
                if not f.endswith('.md') or f in ('INDEX.md', 'BOOK-INFO.md'):
                    continue
                fp = os.path.join(root, f)
                try:
                    new_content = upgrade_content_v2(fp)
                    with open(fp, 'w', encoding='utf-8') as fh:
                        fh.write(new_content)
                    count += 1
                except Exception as e:
                    errors += 1
    print(f"Processed: {count}, Errors: {errors}")

if __name__ == "__main__":
    main()

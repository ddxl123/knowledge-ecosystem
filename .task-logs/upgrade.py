#!/usr/bin/env python3
"""
Upgrade knowledge ecosystem files with core concept enhancements.
"""
import os
import re
import json
from pathlib import Path

BASE = Path("/Users/linlong/.openclaw/workspace/knowledge-ecosystem")
DIRS = [
    "15-K12基础教育", "17-心理学", "18-艺术设计", "19-体育运动",
    "20-驾驶", "21-职业技能", "22-生活兴趣", "23-军事国防",
    "24-行业招聘", "25-学科竞赛", "26-早教幼教", "27-读书名著"
]

def get_context(fp):
    """Extract context from file path."""
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

def has_upgrade(content):
    return "## 核心概念" in content or "### 核心概念" in content or "## 使用建议" in content or "## 适用人群与学习建议" in content

def get_title(content):
    """Get first H1 title."""
    for line in content.split('\n'):
        if line.startswith('# ') and not line.startswith('## '):
            return line[2:].strip()
    return ""

def extract_topics(content):
    """Extract main topics from content."""
    topics = []
    for line in content.split('\n'):
        if line.startswith('## ') and not line.startswith('### '):
            t = line[3:].strip()
            if t not in ['知识点', '核心概念', '典型例题', '参考']:
                topics.append(t)
    return topics

def extract_subtopics(content):
    """Extract subtopics (### level)."""
    subs = []
    for line in content.split('\n'):
        if line.startswith('### ') and not line.startswith('#### '):
            t = line[4:].strip()
            if t and not t.startswith(('例题', '典型', '参考')):
                subs.append(t)
    return subs[:8]  # limit

def upgrade_book_info(content, ctx):
    """Enhance BOOK-INFO.md with target audience, learning suggestions, comparisons."""
    if has_upgrade(content):
        return content
    
    book_name = ctx.get("book", "")
    domain = ctx.get("domain", "")
    cat1 = ctx.get("cat1", "")
    cat2 = ctx.get("cat2", "")
    
    addition = "\n\n## 适用人群与学习建议\n\n"
    
    # Determine context from domain
    if "K12" in domain:
        addition += "### 适用人群\n"
        if "小学" in cat1:
            addition += "- 小学阶段学生（家长辅导使用）\n- 小学教师备课参考\n- 教育培训机构\n\n"
        elif "初中" in cat1:
            addition += "- 初中阶段学生\n- 初中教师备课参考\n- 中考备考学生\n\n"
        elif "高中" in cat1:
            addition += "- 高中阶段学生\n- 高中教师备课参考\n- 高考备考学生\n\n"
        else:
            addition += "- K12阶段学生与教师\n- 教育工作者\n\n"
        addition += "### 学习建议\n"
        addition += "- 配合课本同步学习，先理解概念再做练习\n"
        addition += "- 建立错题本，定期复习薄弱知识点\n"
        addition += "- 注重基础知识的扎实掌握，循序渐进\n"
    elif "心理学" in domain:
        addition += "### 适用人群\n"
        if "考研" in cat1:
            addition += "- 心理学考研备考学生\n- 心理学专业本科生\n- 对心理学研究感兴趣的学者\n\n"
        elif "咨询师" in cat1:
            addition += "- 心理咨询师考试备考者\n- 心理咨询从业者\n- 心理健康教育工作者\n\n"
        else:
            addition += "- 心理学学习者\n- 心理咨询从业者\n- 教育工作者\n\n"
        addition += "### 学习建议\n"
        addition += "- 结合实际案例理解理论知识\n"
        addition += "- 注重理论与实践的结合\n"
        addition += "- 定期回顾和总结，构建知识框架\n"
    elif "艺术" in domain:
        addition += "### 适用人群\n"
        addition += "- 艺术设计专业学生\n- 艺术爱好者与自学者\n- 设计从业者\n\n"
        addition += "### 学习建议\n"
        addition += "- 理论学习与动手实践并重\n"
        addition += "- 多观察、多临摹、多创作\n"
        addition += "- 培养审美能力，积累视觉素材\n"
    elif "体育" in domain:
        addition += "### 适用人群\n"
        addition += "- 体育爱好者与健身人群\n- 体育专业学生\n- 运动教练与体育教师\n\n"
        addition += "### 学习建议\n"
        addition += "- 循序渐进，注意运动安全\n"
        addition += "- 理论与实践结合，在训练中体会技术要领\n"
        addition += "- 注重热身与恢复，避免运动损伤\n"
    elif "驾驶" in domain:
        addition += "### 适用人群\n"
        addition += "- 驾校学员（C1/C2及各车型）\n- 驾驶考试备考者\n- 新手驾驶员巩固知识\n\n"
        addition += "### 学习建议\n"
        addition += "- 理论与实操结合，理解原理而非死记硬背\n"
        addition += "- 多做模拟题，重点攻克易错题型\n"
        addition += "- 养成安全驾驶意识，文明出行\n"
    elif "职业技能" in domain:
        addition += "### 适用人群\n"
        addition += "- 职场人士提升技能\n- 相关职业资格考试备考者\n- 转行或求职者\n\n"
        addition += "### 学习建议\n"
        addition += "- 结合工作实际学以致用\n"
        addition += "- 注重实操练习，理论联系实际\n"
        addition += "- 制定学习计划，坚持每日学习\n"
    elif "生活" in domain:
        addition += "### 适用人群\n"
        addition += "- 对该领域感兴趣的爱好者\n- 希望提升生活品质的人群\n- 初学者入门参考\n\n"
        addition += "### 学习建议\n"
        addition += "- 从基础开始，循序渐进\n"
        addition += "- 动手实践是最好的学习方式\n"
        addition += "- 享受学习过程，培养兴趣\n"
    elif "军事" in domain:
        addition += "### 适用人群\n"
        addition += "- 军考备考人员\n- 国防教育学习者\n- 军事爱好者\n\n"
        addition += "### 学习建议\n"
        addition += "- 系统学习，构建完整的知识体系\n"
        addition += "- 关注时事与军事动态\n"
        addition += "- 结合历史案例理解军事理论\n"
    elif "招聘" in domain:
        addition += "### 适用人群\n"
        addition += "- 相关行业招聘考试备考者\n- 应届毕业生求职者\n- 在职人员转岗备考\n\n"
        addition += "### 学习建议\n"
        addition += "- 了解考试大纲和题型，有针对性复习\n"
        addition += "- 多做真题和模拟题\n"
        addition += "- 关注行业动态和政策变化\n"
    elif "竞赛" in domain:
        addition += "### 适用人群\n"
        addition += "- 学科竞赛参赛选手\n- 竞赛教练与辅导教师\n- 对学科有深入兴趣的学生\n\n"
        addition += "### 学习建议\n"
        addition += "- 夯实基础后再拓展竞赛内容\n"
        addition += "- 多做历年真题，总结解题方法\n"
        addition += "- 参加培训班或学习小组，交流提高\n"
    elif "早教" in domain:
        addition += "### 适用人群\n"
        addition += "- 0-6岁幼儿家长\n- 幼儿园教师\n- 早教机构从业者\n\n"
        addition += "### 学习建议\n"
        addition += "- 以游戏化方式引导孩子学习\n"
        addition += "- 尊重孩子的发展节奏，不急于求成\n"
        addition += "- 亲子互动是最好的教育方式\n"
    elif "读书" in domain:
        addition += "### 适用人群\n"
        addition += "- 中小学生（考试备考）\n- 文学爱好者\n- 语文教师\n\n"
        addition += "### 学习建议\n"
        addition += "- 先通读原著，再参考知识手册\n"
        addition += "- 注重理解人物性格和故事脉络\n"
        addition += "- 积累名句和写作素材\n"
    else:
        addition += "### 适用人群\n- 相关领域学习者与从业者\n\n"
        addition += "### 学习建议\n- 系统学习，理论与实践结合\n"
    
    addition += "\n### 使用建议\n"
    addition += "- 可作为学习主线，配合其他参考资料使用\n"
    addition += "- 建议定期回顾，巩固记忆\n"
    addition += "- 结合实际应用场景加深理解\n"
    
    return content.rstrip() + addition

def upgrade_index(content, ctx):
    """Enhance INDEX.md with usage suggestions."""
    if has_upgrade(content):
        return content
    
    domain = ctx.get("domain", "")
    
    addition = "\n\n---\n\n## 使用建议\n\n"
    addition += "### 索引说明\n"
    addition += "- 本索引按学科/领域→细分方向→具体书目→章节知识点的层级组织\n"
    addition += "- 每个知识点文件包含核心概念、知识结构和代表性示例\n"
    addition += "- BOOK-INFO.md 文件包含书目基本信息、适用人群和学习建议\n\n"
    addition += "### 如何使用\n"
    addition += "1. **浏览索引**：从大类到小类，快速定位所需知识领域\n"
    addition += "2. **深入学习**：进入具体书目目录，按章节系统学习\n"
    addition += "3. **交叉参考**：相关领域的知识可以互相参照，建立跨学科联系\n"
    addition += "4. **定期更新**：知识库会持续扩充和优化\n\n"
    addition += "### 学习路径建议\n"
    
    if "K12" in domain:
        addition += "- **同步学习**：按年级和学期，配合学校教学进度\n"
        addition += "- **专项突破**：针对薄弱科目或专题集中学习\n"
        addition += "- **升学备考**：中考/高考前系统复习\n"
    elif "心理学" in domain:
        addition += "- **入门**：从基础心理学开始，建立学科框架\n"
        addition += "- **进阶**：按考研/考证方向深入学习\n"
        addition += "- **应用**：结合案例和实践加深理解\n"
    else:
        addition += "- **入门**：选择基础教材，了解领域全貌\n"
        addition += "- **进阶**：深入专业方向，系统学习\n"
        addition += "- **应用**：结合实际，学以致用\n"
    
    return content.rstrip() + addition

def upgrade_content(content, ctx):
    """Add core concept section to content files."""
    if has_upgrade(content):
        return content
    
    title = get_title(content)
    topics = extract_topics(content)
    subtopics = extract_subtopics(content)
    book = ctx.get("book", "")
    chapter = ctx.get("chapter", "")
    domain = ctx.get("domain", "")
    
    # Build core concept section
    section = "\n\n## 核心概念\n\n"
    
    if title:
        section += f"本章/节围绕 **{title}** 这一核心主题展开"
    elif chapter:
        section += f"本章/节围绕 **{chapter}** 这一核心主题展开"
    else:
        section += "本章/节围绕以下核心主题展开"
    
    if topics:
        section += "，主要包含以下知识模块：\n\n"
        for i, t in enumerate(topics[:6], 1):
            section += f"{i}. **{t}**\n"
    else:
        section += "。\n\n"
    
    if subtopics:
        section += "\n### 知识结构\n\n"
        section += "本部分内容的知识组织结构如下：\n\n"
        for s in subtopics[:6]:
            section += f"- **{s}**：相关概念、原理和应用\n"
    
    # Add representative examples section
    section += "\n### 代表性示例\n\n"
    section += "以下为本章/节的代表性知识点示例：\n\n"
    
    # Extract some actual content items as examples
    examples = []
    for line in content.split('\n'):
        line = line.strip()
        if line.startswith('- ') and len(line) > 10 and len(line) < 100:
            # Clean up markdown
            clean = line[2:].split('（')[0].split(':')[0].strip()
            if clean and len(clean) > 3 and not clean.startswith(('要点', '注意', '提示')):
                examples.append(clean)
        if len(examples) >= 5:
            break
    
    if examples:
        for ex in examples:
            section += f"- {ex}\n"
    else:
        section += "- 详见各小节的具体内容和例题\n"
    
    section += "\n### 学习要点\n\n"
    section += "- 理解核心概念的定义和内涵\n"
    section += "- 掌握知识之间的逻辑关系\n"
    section += "- 通过练习和应用巩固理解\n"
    section += "- 注重知识的系统性和完整性\n"
    
    return content.rstrip() + section

def process_all():
    """Process all files."""
    stats = {"index": 0, "book_info": 0, "content": 0, "skipped": 0, "error": 0}
    
    for d in DIRS:
        dp = BASE / d
        if not dp.exists():
            continue
        for root, dirs, files in os.walk(dp):
            for f in files:
                if not f.endswith('.md'):
                    continue
                fp = os.path.join(root, f)
                try:
                    with open(fp, 'r', encoding='utf-8') as fh:
                        content = fh.read()
                except:
                    stats["error"] += 1
                    continue
                
                if not content.strip() or has_upgrade(content):
                    stats["skipped"] += 1
                    continue
                
                ctx = get_context(fp)
                fname = os.path.basename(fp)
                
                if fname == "INDEX.md":
                    new_content = upgrade_index(content, ctx)
                    stats["index"] += 1
                elif fname == "BOOK-INFO.md":
                    new_content = upgrade_book_info(content, ctx)
                    stats["book_info"] += 1
                else:
                    new_content = upgrade_content(content, ctx)
                    stats["content"] += 1
                
                try:
                    with open(fp, 'w', encoding='utf-8') as fh:
                        fh.write(new_content)
                except:
                    stats["error"] += 1
    
    return stats

if __name__ == "__main__":
    stats = process_all()
    print(json.dumps(stats, ensure_ascii=False, indent=2))

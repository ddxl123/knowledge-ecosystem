#!/usr/bin/env python3
"""Generate sub-agent task prompts for missing .knowledge files."""
import os
import json
from collections import defaultdict

BASE = "/Users/linlong/.openclaw/workspace/knowledge-ecosystem"

def scan():
    md_files = []
    for root, dirs, files in os.walk(BASE):
        if ".git" in root or ".task-logs" in root or ".task-scripts" in root:
            continue
        for f in files:
            if f.endswith(".md") and f not in ("INDEX.md", "BOOK-INFO.md"):
                md_files.append(os.path.join(root, f))

    knowledge_bases = set()
    for root, dirs, files in os.walk(BASE):
        if ".git" in root or ".task-logs" in root or ".task-scripts" in root:
            continue
        for f in files:
            if f.endswith(".knowledge"):
                knowledge_bases.add(os.path.join(root, f).replace(".knowledge", ""))

    missing = []
    for mf in sorted(md_files):
        if mf.replace(".md", "") not in knowledge_bases:
            missing.append(mf)
    return missing

def group_by_dir(files):
    by_dir = defaultdict(list)
    for f in files:
        d = os.path.dirname(f)
        by_dir[d].append(f)
    return by_dir

def generate_task_prompt(md_path, knowledge_path):
    """Generate the task prompt for a single sub-agent."""
    return f"""你是知识收集专家。请为以下源文件生成权威的原子知识集文件。

## 任务
1. 读取源文件：`{md_path}`
2. 深度理解其中的「收集指南」部分
3. 根据收集指南中的"待收集原子知识点"，通过web搜索收集权威、准确的知识内容
4. 将收集到的知识写入：`{knowledge_path}`

## 输出格式要求
.knowledge文件格式参考：
- 以 `# [标题] · 知识集` 开头
- 包含来源信息引用块
- 按知识结构分节（一、二、三...）
- 每个知识点包含：核心概念定义、公式定理（如有）、典型应用、易错点
- 使用Markdown格式，数学公式使用LaTeX（$...$）

## 约束
- 所有知识必须准确、权威，符合最新行业标准与学术共识
- 绝对禁止编造知识点
- 严格遵循源文件的收集指南范围，不得跨目录/跨文件引用
- 如果源文件已有部分内容（非收集指南），可参考但需扩展为完整权威知识

## 工作流
1. 先用 read 工具读取源文件
2. 理解收集指南中的条目描述、知识结构、待收集原子知识点
3. 用 web_search 搜索每个知识点的权威内容（多个搜索）
4. 综合整理为结构化的 .knowledge 文件
5. 用 write 工具写入目标路径

请立即开始工作，不要向用户提问。"""

if __name__ == "__main__":
    missing = scan()
    print(f"Total missing: {len(missing)}")
    
    # Generate task list grouped by directory
    by_dir = group_by_dir(missing)
    
    # Save task prompts
    tasks = []
    for d in sorted(by_dir.keys()):
        for mf in sorted(by_dir[d]):
            kp = mf.replace(".md", ".knowledge")
            tasks.append({
                "md_path": mf,
                "knowledge_path": kp,
                "prompt": generate_task_prompt(mf, kp)
            })
    
    with open(os.path.join(BASE, ".task-scripts", "all_tasks.json"), "w") as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)
    
    print(f"Generated {len(tasks)} task prompts")
    print(f"Saved to .task-scripts/all_tasks.json")

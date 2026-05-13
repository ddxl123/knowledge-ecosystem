#!/usr/bin/env python3
"""
Knowledge Ecosystem File Processor
Processes .md files for core concept level upgrades.
"""

import os
import re
import json
from pathlib import Path

BASE_DIR = Path("/Users/linlong/.openclaw/workspace/knowledge-ecosystem")
TARGET_DIRS = [
    "15-K12基础教育", "17-心理学", "18-艺术设计", "19-体育运动",
    "20-驾驶", "21-职业技能", "22-生活兴趣", "23-军事国防",
    "24-行业招聘", "25-学科竞赛", "26-早教幼教", "27-读书名著"
]

def get_file_type(filepath):
    """Determine file type: INDEX, BOOK-INFO, or CONTENT"""
    name = os.path.basename(filepath)
    if name == "INDEX.md":
        return "INDEX"
    elif name == "BOOK-INFO.md":
        return "BOOK_INFO"
    else:
        return "CONTENT"

def get_subject_context(filepath):
    """Extract subject/book context from file path"""
    parts = Path(filepath).parts
    context = {}
    
    # Find the target directory
    for td in TARGET_DIRS:
        if td in parts:
            context["domain"] = td
            idx = parts.index(td)
            remaining = parts[idx+1:]
            if len(remaining) >= 1:
                context["category"] = remaining[0]  # e.g., "初中", "心理咨询师"
            if len(remaining) >= 2:
                context["subcategory"] = remaining[1]  # e.g., "数学", "心理咨询师"
            if len(remaining) >= 3:
                context["book"] = remaining[2]  # e.g., "2025人教版高中数学必修一"
            if len(remaining) >= 4:
                context["chapter"] = remaining[3]  # e.g., "函数"
            break
    
    return context

def has_core_concept(content):
    """Check if file already has core concept section"""
    return "## 核心概念" in content or "### 核心概念" in content

def get_content_stats(content):
    """Get basic stats about file content"""
    lines = content.strip().split('\n')
    total_lines = len(lines)
    headers = [l for l in lines if l.startswith('#')]
    return {
        "total_lines": total_lines,
        "headers": headers,
        "has_content": total_lines > 5
    }

def process_file(filepath):
    """Process a single file and return (action_taken, description)"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return "ERROR", str(e)
    
    if not content.strip():
        return "SKIP", "Empty file"
    
    file_type = get_file_type(filepath)
    context = get_subject_context(filepath)
    
    if has_core_concept(content):
        return "SKIP", "Already has core concept section"
    
    stats = get_content_stats(content)
    if stats["total_lines"] < 3:
        return "SKIP", "Too short to process"
    
    return file_type, context

def main():
    """List all files and their processing status"""
    results = {"SKIP": 0, "INDEX": 0, "BOOK_INFO": 0, "CONTENT": 0, "ERROR": 0}
    file_list = []
    
    for td in TARGET_DIRS:
        dir_path = BASE_DIR / td
        if not dir_path.exists():
            continue
        for root, dirs, files in os.walk(dir_path):
            for f in files:
                if f.endswith('.md'):
                    filepath = os.path.join(root, f)
                    result = process_file(filepath)
                    results[result[0]] = results.get(result[0], 0) + 1
                    file_list.append({
                        "path": filepath,
                        "type": result[0],
                        "detail": result[1] if result[0] == "SKIP" else ""
                    })
    
    print(json.dumps({"results": results, "total": len(file_list)}, ensure_ascii=False, indent=2))
    
    # Write file list for batch processing
    with open(BASE_DIR / ".task-logs" / "file_list.json", 'w', encoding='utf-8') as f:
        json.dump(file_list, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()

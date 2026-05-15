#!/usr/bin/env python3
"""
Extract knowledge atoms from .md files and generate .knowledge files.
Format: {{知识点名称}}title{{知识点内容}}content
Atoms separated by ▮, last atom has no trailing ▮.
"""
import os
import re
import sys

def extract_knowledge_atoms(content):
    """Extract knowledge atoms from markdown content."""
    lines = content.split('\n')
    
    # Find where the 收集指南 section ends
    in_guide = False
    content_start = 0
    
    for i, line in enumerate(lines):
        if '收集指南' in line and line.strip().startswith('#'):
            in_guide = True
            continue
        if in_guide:
            # Guide ends when we hit a new ## or # section that's not part of the guide
            # Guide sections: 条目描述, 知识结构, 待收集原子知识点
            if line.startswith('# ') or (line.startswith('## ') and not any(
                marker in line for marker in ['条目描述', '知识结构', '待收集', '收集指南']
            )):
                content_start = i
                in_guide = False
                break
            # Also end on --- separator
            if line.strip() == '---':
                content_start = i + 1
                in_guide = False
                break
    
    if in_guide:
        # Never found end of guide, skip
        return []
    
    # Get content lines after guide
    content_lines = lines[content_start:]
    
    # Parse knowledge atoms from content
    atoms = []
    current_title = None
    current_content = []
    
    for line in content_lines:
        # Match headers at ### or #### level (knowledge atom level)
        # Also match ## level if it has numbered sub-items
        match = re.match(r'^(#{2,4})\s+(.+)', line)
        if match:
            level = len(match.group(1))
            title = match.group(2).strip()
            
            # Save previous atom if exists
            if current_title and current_content:
                content_text = '\n'.join(current_content).strip()
                if content_text and len(content_text) > 5:
                    atoms.append((current_title, content_text))
            
            current_title = title
            current_content = []
        elif line.strip() and not line.startswith('---'):
            # Skip meta sections
            if any(marker in line for marker in ['## 2025 Updates', '## Exam Tips', '## Common Mistakes', '## 考试技巧', '## 备考建议']):
                if current_title and current_content:
                    content_text = '\n'.join(current_content).strip()
                    if content_text and len(content_text) > 5:
                        atoms.append((current_title, content_text))
                    current_title = None
                    current_content = []
                continue
            current_content.append(line.strip())
    
    # Don't forget the last atom
    if current_title and current_content:
        content_text = '\n'.join(current_content).strip()
        if content_text and len(content_text) > 5:
            atoms.append((current_title, content_text))
    
    return atoms

def format_knowledge(atoms):
    """Format atoms into .knowledge format."""
    if not atoms:
        return ""
    
    parts = []
    for title, content in atoms:
        # Clean up content - remove markdown formatting
        content = re.sub(r'\*\*(.+?)\*\*', r'\1', content)  # Remove bold
        content = re.sub(r'\*(.+?)\*', r'\1', content)  # Remove italic
        content = re.sub(r'^\s*[-*]\s+', '', content, flags=re.MULTILINE)  # Remove list markers
        content = re.sub(r'^\s*\d+\.\s+', '', content, flags=re.MULTILINE)  # Remove numbered lists
        content = re.sub(r'\n{2,}', '；', content)  # Replace multiple newlines
        content = content.replace('\n', '；')
        content = re.sub(r'[；:：]+$', '', content)  # Clean trailing
        content = re.sub(r'^[；:：]+', '', content)  # Clean leading
        content = content.strip()
        
        if content and len(content) > 3:
            parts.append(f'{{{{知识点名称}}}}{title}{{{{知识点内容}}}}{content}')
    
    return '▮'.join(parts)

def process_file(md_path):
    """Process a single .md file and generate .knowledge file."""
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if it's mostly placeholders
    if content.count('待补充') > len(content) / 100:
        return None, "Skipped: too many placeholders"
    
    atoms = extract_knowledge_atoms(content)
    
    if not atoms:
        return None, "Skipped: no atoms extracted"
    
    knowledge_content = format_knowledge(atoms)
    if not knowledge_content:
        return None, "Skipped: empty knowledge content"
    
    knowledge_path = md_path[:-3] + '.knowledge'
    with open(knowledge_path, 'w', encoding='utf-8') as f:
        f.write(knowledge_content)
    
    return knowledge_path, f"Generated {len(atoms)} atoms"

if __name__ == '__main__':
    if len(sys.argv) > 1:
        for path in sys.argv[1:]:
            result, msg = process_file(path)
            print(f"{path}: {msg}")

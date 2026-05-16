#!/usr/bin/env python3
"""
Knowledge file generator for knowledge-ecosystem.
Usage: python3 .gen_knowledge.py <directory_path>

Generates a .knowledge file in the specified directory based on its path structure.
"""
import os
import sys
import re

def parse_path_info(path):
    """Parse the directory path to extract domain, subject, book info, etc."""
    base = "/Users/linlong/.openclaw/workspace/knowledge-ecosystem"
    rel = path.replace(base + '/', '')
    parts = rel.split('/')
    
    info = {
        'domain': parts[0] if len(parts) > 0 else '',
        'subject': parts[1] if len(parts) > 1 else '',
        'category': parts[2] if len(parts) > 2 else '',
        'book': parts[3] if len(parts) > 3 else '',
        'chapter': parts[4] if len(parts) > 4 else '',
        'section': parts[5] if len(parts) > 5 else '',
        'leaf_name': parts[-1] if parts else '',
        'full_path': rel,
    }
    
    # Extract year from book name
    year_match = re.search(r'(20\d{2})', info['book'])
    info['year'] = year_match.group(1) if year_match else ''
    
    # Extract book title (remove year prefix)
    info['book_title'] = re.sub(r'^20\d{2}', '', info['book']).strip() if info['book'] else ''
    
    return info

def get_knowledge_filename(info):
    """Generate the .knowledge filename based on path info."""
    leaf = info['leaf_name']
    # Use leaf directory name as filename
    return f"{leaf}.knowledge"

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 .gen_knowledge.py <directory_path>")
        sys.exit(1)
    
    path = sys.argv[1]
    info = parse_path_info(path)
    filename = get_knowledge_filename(info)
    
    print(f"Path: {info['full_path']}")
    print(f"Domain: {info['domain']}")
    print(f"Subject: {info['subject']}")
    print(f"Book: {info['book']} ({info['book_title']})")
    print(f"Chapter: {info['chapter']}")
    print(f"Leaf: {info['leaf_name']}")
    print(f"Output: {filename}")

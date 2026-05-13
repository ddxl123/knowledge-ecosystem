#!/usr/bin/env python3
"""Fix 冲刺押题类 files where knowledge structure incorrectly shows question numbers."""
import os
import re
from pathlib import Path

BASE = Path("/Users/linlong/.openclaw/workspace/knowledge-ecosystem/03-考研")

def fix_politics_exam_file(fp, content, fname):
    """Fix a 考研政治 exam file (选择题.md or 分析题.md)."""
    is_选择题 = "选择题" in fname
    is_分析题 = "分析题" in fname
    is_套卷 = "套卷" in fp
    
    # Get book name from path
    parts = Path(fp).parts
    book_name = ""
    for p in parts:
        if "肖秀荣" in p or "徐涛" in p or "腿姐" in p or "米鹏" in p:
            book_name = p
            break
    
    # Determine paper number from directory
    paper_num = ""
    for p in parts:
        m = re.match(r'套卷(\d+)', p)
        if m:
            paper_num = m.group(1)
            break
    
    if is_选择题:
        new_concept = """## 核心概念

### 条目描述

本文件是{book}第{num}套的客观题部分，包含单选题和多选题，用于考查考研政治各模块的基础知识掌握程度和辨析能力。

### 知识结构

- **马克思主义基本原理**（约24分）：唯物论、辩证法、认识论、唯物史观、政治经济学、科学社会主义
- **毛泽东思想和中国特色社会主义理论体系概论**（约24分）：毛泽东思想、邓小平理论、"三个代表"、科学发展观、习近平新时代思想
- **中国近现代史纲要**（约14分）：旧民主主义革命、新民主主义革命、社会主义革命和建设、改革开放
- **思想道德与法治**（约16分）：人生观、理想信念、中国精神、核心价值观、道德修养、法治思维

### 待收集原子知识点

- 马原高频考点：哲学基本概念辨析、剩余价值理论、唯物史观基本原理
- 毛中特高频考点：各理论的核心内容和历史地位、新时代思想要点
- 史纲高频考点：重要时间节点、会议、文献的意义
- 思法高频考点：人生观价值观、道德与法治的核心概念
""".format(book=book_name, num=paper_num)
    elif is_分析题:
        new_concept = """## 核心概念

### 条目描述

本文件是{book}第{num}套的主观题部分，共5道分析题，分别对应考研政治五大模块，考查综合分析和论述能力。

### 知识结构

- **第34题（马原）**：运用马克思主义哲学原理分析现实问题
- **第35题（毛中特）**：中国特色社会主义理论体系的实践应用
- **第36题（史纲）**：历史事件的意义和经验启示
- **第37题（思法）**：思想道德与法治的现实意义
- **第38题（时政）**：当代世界经济与政治热点分析

### 待收集原子知识点

- 马原分析题：唯物辩证法、认识论、唯物史观的原理及方法论
- 毛中特分析题：新时代中国特色社会主义的核心论述
- 史纲分析题：重要历史事件的背景、过程、意义
- 思法分析题：理想信念、中国精神、核心价值观的现实意义
- 时政分析题：当年重大时政热点与理论结合
""".format(book=book_name, num=paper_num)
    else:
        return content
    
    # Replace the old 核心概念 section
    if "## 核心概念" in content:
        idx = content.index("## 核心概念")
        rest = content[idx:]
        # Find next ## (not ###)
        end_idx = len(rest)
        for i, line in enumerate(rest.split('\n')):
            if i > 0 and line.startswith('## ') and not line.startswith('### '):
                end_idx = content.index("## 核心概念") + sum(len(l)+1 for l in rest.split('\n')[:i])
                break
        else:
            end_idx = len(content)
        
        # More robust: find the position after the 核心概念 section
        lines = content.split('\n')
        start_line = None
        end_line = None
        for i, line in enumerate(lines):
            if line.startswith('## 核心概念'):
                start_line = i
            elif start_line is not None and line.startswith('## ') and not line.startswith('### '):
                end_line = i
                break
        if start_line is not None:
            if end_line is None:
                end_line = len(lines)
            new_lines = lines[:start_line] + [new_concept.rstrip()] + lines[end_line:]
            return '\n'.join(new_lines)
    
    return content

def fix_math_exam_file(fp, content, fname):
    """Fix a 考研数学 exam file (试题.md)."""
    parts = Path(fp).parts
    book_name = ""
    for p in parts:
        if "李林" in p or "合工大" in p or "张宇" in p or "汤家凤" in p:
            book_name = p
            break
    
    paper_num = ""
    for p in parts:
        m = re.match(r'套卷(\d+)', p)
        if m:
            paper_num = m.group(1)
            break
    
    # Check if it's 合工大 (only has 试题.md, no 选择题/填空题 split)
    is_hegongda = "合工大" in fp
    
    new_concept = """## 核心概念

### 条目描述

本文件是{book}第{num}套的试题部分，用于考研数学冲刺阶段的模拟训练，帮助考生检验复习效果和查漏补缺。

### 知识结构

- **高等数学**（约56%）：函数极限连续、一元微分学、一元积分学、多元微分学、重积分、常微分方程、无穷级数、空间解析几何
- **线性代数**（约22%）：行列式、矩阵、向量、线性方程组、特征值与特征向量、二次型
- **概率论与数理统计**（约22%）：随机事件与概率、随机变量及其分布、多维随机变量、数字特征、大数定律与中心极限定理、数理统计、参数估计

### 待收集原子知识点

- 高数核心考点：极限计算、中值定理应用、积分计算与应用、级数敛散性判断
- 线代核心考点：矩阵运算与变换、线性方程组求解、特征值与相似对角化
- 概率核心考点：概率计算、常见分布、数字特征、参数估计方法
""".format(book=book_name, num=paper_num)
    
    # Replace
    lines = content.split('\n')
    start_line = None
    end_line = None
    for i, line in enumerate(lines):
        if line.startswith('## 核心概念'):
            start_line = i
        elif start_line is not None and line.startswith('## ') and not line.startswith('### '):
            end_line = i
            break
    if start_line is not None:
        if end_line is None:
            end_line = len(lines)
        new_lines = lines[:start_line] + [new_concept.rstrip()] + lines[end_line:]
        return '\n'.join(new_lines)
    return content

def main():
    count = 0
    for subject_dir in ["考研政治", "考研数学"]:
        dp = BASE / subject_dir / "冲刺押题类"
        if not dp.exists():
            continue
        for root, dirs, files in os.walk(dp):
            for fname in sorted(files):
                if not fname.endswith('.md') or fname == "BOOK-INFO.md":
                    continue
                fp = os.path.join(root, fname)
                with open(fp, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if "## 核心概念" not in content:
                    continue
                
                if "政治" in subject_dir:
                    if "选择题" in fname or "分析题" in fname:
                        new_content = fix_politics_exam_file(fp, content, fname)
                    elif "套卷" in fname:
                        # 米鹏 style - single file per paper
                        # These might be ok already, check
                        continue
                    else:
                        continue
                else:
                    if "试题" in fname:
                        new_content = fix_math_exam_file(fp, content, fname)
                    else:
                        continue
                
                if new_content != content:
                    with open(fp, 'w', encoding='utf-8') as fh:
                        fh.write(new_content)
                    count += 1
    
    print(f"Fixed {count} 冲刺押题类 files")

if __name__ == "__main__":
    main()

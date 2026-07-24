---
name: learning-notes
description: Create and update learning notes in the Learning/ folder. Use when user says "创建学习笔记", "学到个新概念", "写个学习笔记到 Learning", "记录这个知识点", or discusses fundamental concepts that need detailed explanation with derivations, examples, and intuitive understanding. Learning/ is for foundational knowledge (math basics, derivations, intuitive explanations) while Concepts/ is for research field concepts managed by paper-agent.
---

# Learning Notes Skill

Create and update learning notes in the Learning/ folder.

## Step 0: 读取共享配置

先读取 `../_shared/user_config.py`，如果 `../_shared/user-config.local.json` 存在，再用它覆盖默认值。

显式生成并在后续统一使用这些变量：

- `VAULT_PATH` — Obsidian vault 根目录
- `LEARNING_PATH` — Learning 笔记目录（默认 `{VAULT_PATH}/Learning`）

## When to Use

- User wants to record a foundational concept they learned
- Need to document derivation process or intuitive understanding
- Creating notes with examples and step-by-step explanations
- User explicitly mentions Learning folder

## Learning/ vs Concepts/

| Aspect | Learning/ | Concepts/ |
|--------|-----------|-----------|
| Purpose | Foundational knowledge, learning notes | Research concepts dictionary |
| Content | Derivations, examples, intuitive understanding | Definitions, paper links, method comparisons |
| Style | Full learning path with examples | Concise definition + references |
| Structure | Flat, no categories | Organized (1-Foundations, 2-Methods...) |
| Links | Few, mainly ML concepts | Many links to papers, related concepts |

## Workflow

### 1. Create New Note

```bash
# Generate filename: Concept_Name.md (underscores for spaces)
FILE="{LEARNING_PATH}/<Concept_Name>.md"
```

### 2. Frontmatter Template

```yaml
---
title: "<Concept Name>"
created: <YYYY-MM-DD>
source: "<来源：文章链接/课程/讨论>"
tags: [<relevant>, <tags>]
---
```

### 3. Note Structure

```markdown
# <Concept Name>

## 一句话定义
<简洁的定义>

## 直观理解
<例子、类比、图示>

## 数学形式
<推导过程、公式>

$$
\text{LaTeX 公式}
$$

## 应用场景
<在什么情况下用>

## 相关概念
- [[xxx]]
```

### 4. Git Commit & Push

```bash
cd {VAULT_PATH}
git add Learning/<filename>
git commit -m "Add learning note: <concept_name>"
git push
```

## Example

Input: "写个学习笔记关于向量叉乘"

Output file: `{LEARNING_PATH}/Cross_Product.md`

```markdown
---
title: 向量叉乘
created: 2026-05-02
source: 线性代数学习
tags: [math, linear-algebra, 3d]
---

# 向量叉乘

## 一句话定义
叉乘 = 垂直于两向量的第三个向量，大小等于平行四边形面积。

## 直观理解
右手定则：四指从 a 转向 b，拇指指向叉乘结果。

...

## 数学形式
$$
\mathbf{a} \times \mathbf{b} = |a||b|\sin(\theta)\hat{n}
$$

## 应用场景
- 计算平面法向量
- 机器人运动学（力矩计算）

## 相关概念
- [[Dot_Product_as_Projection]]
- [[Linear_Algebra]]
```

## Notes

- LaTeX formulas render normally in Obsidian - no need to convert to images
- Use Obsidian-style links: `[[Concept_Name]]`
- Keep examples concrete and relatable
- Include ASCII diagrams when helpful
- Ask user for clarification if the concept is ambiguous

---
name: reader-notes
description: |
  添加解释和评论到论文笔记。当用户请求"写到笔记里"、"加个解释"、"添加 Reader's Notes"、"帮我记下来"时使用。
  
  功能：
  - 局部解释 (Explain by Reader) - 在某个 section 后追加解释
  - 整体评论 (Reader's Notes) - 在笔记末尾追加阅读笔记
  
  自动 git commit & push 到 ObsidianVault。

metadata:
  { "openclaw": { "requires": { "bins": [], "env": [] } } }
---

# Reader Notes Skill

让 vault-reader agent 能够在论文笔记中添加解释和评论。

## 触发条件

当用户明确请求时：
- "在这里加个解释"
- "写到笔记里"
- "帮我记下来"
- "添加 Reader's Notes"

## 功能

### 0. 论文评估 (Paper Verdict)

**场景**：用户读完论文后讨论质量，请求添加评估

**格式**：插入在笔记开头 metadata 之后、`## 一句话总结` 之前

```markdown
## 🏷️ Paper Verdict

> **再读价值**: ⭐⭐⭐ / ⭐⭐⭐⭐⭐
> **证据强度**: 强 / 中 / 弱
> **一句话评价**: [为什么值得/不值得再读]

### 优点
- ...

### 局限
- ...

### 适用场景
- 什么情况下这篇论文有参考价值

— Eve, YYYY-MM-DD
```

**再读价值评分标准**：
| 评分 | 含义 |
|------|------|
| ⭐⭐⭐⭐⭐ | 必读，方法/发现有开创性 |
| ⭐⭐⭐⭐ | 值得再读，有明确贡献 |
| ⭐⭐⭐ | 可选，有参考价值但局限明显 |
| ⭐⭐ | 一般，问题有价值但支撑不足 |
| ⭐ | 不推荐，结论不可靠 |

**证据强度**：
- **强**：多任务/多设置验证，结论稳健
- **中**：部分验证，有一定说服力
- **弱**：单一任务/设置，结论待验证

**触发词**：
- "这篇论文怎么样"
- "值不值得再读"
- "加个评估"
- "帮我标记一下质量"

### 1. 局部解释 (Explain by Reader)

**场景**：用户对某部分不理解，让 agent 解释后请求写入笔记

**格式**：
```markdown
### 某某概念解释

原文内容...

#### 💡 Explain by Reader
> [解释内容]
> 
> — vault-reader, 2026-04-07
```

**位置**：紧跟在问题部分之后

### 2. Reader's Notes (整体评论)

**场景**：用户请求添加整体性的阅读笔记

**格式**：
```markdown
---

## 📖 Reader's Notes

### 要点总结
- 要点1
- 要点2

### 与其他论文的联系
- [[Paper_A]] 的方法类似...
- 与 [[Paper_B]] 的区别在于...

### 个人见解
> [用户的见解或评论]
> 
> — Eve, 2026-04-07
```

**位置**：笔记末尾，在最后的 `---` 之前

### 3. Q&A 讨论记录

**场景**：用户和 agent 进行了深入的 Q&A 讨论，用户请求写入笔记

**格式**：
```markdown
---

## 📖 Reader's Notes

### Q&A 讨论记录（YYYY-MM-DD）

#### Q1: 问题标题？
回答内容，可以包含代码块、公式、表格...

#### Q2: 问题标题？
回答内容...

### 与其他论文的联系
- [[Paper_A]] 的方法类似...

— Eve, YYYY-MM-DD
```

**位置**：笔记末尾，在最后的 `---` 之前

**特点**：
- 每个 Q&A 独立成段，标题用 `#### Qn:` 格式
- 回答可以用代码块、公式、表格等丰富格式
- 鼓励在回答中包含具体的例子和类比
- 最后附上与其他论文的联系

### 4. 更新 Mermaid 架构图

**场景**：在 Q&A 讨论中，用户对模型架构有了更深的理解，需要更新笔记中的 mermaid 图

**触发条件**：
- 用户说"更新图"、"改 mermaid"、"画个图"
- Q&A 讨论中发现原有 mermaid 图不准确或不完整
- 用户确认"写到笔记里"且内容涉及架构

**操作**：
1. 找到笔记中现有的 mermaid 图
2. 根据讨论内容更新 mermaid 图（更详细、更准确）
3. 保持 mermaid 语法正确（所有标签加引号，subgraph 用 `ID["Label"]` 格式）

**注意事项**：
- mermaid 图中的中文标签必须加引号
- 特殊字符（括号、下划线等）用引号包裹
- subgraph 格式：`subgraph ID["Label"]`（不要直接写中文作为 ID）
- 更新后确认图能在 Obsidian 中正常渲染

## 工作流程

### 添加论文评估

1. 用户读完论文并讨论后，请求添加评估
2. Agent 根据讨论内容和论文质量生成评估
3. Agent 执行：
   - 找到第一个 `---` 分隔线之后的位置（metadata 结束处）
   - 在 `## 一句话总结` 之前插入 `## 🏷️ Paper Verdict` section
   - 包含评分、优缺点、适用场景
4. Git commit & push

**位置示意**：
```markdown
---
title: "论文名"
...metadata...
---

## 🏷️ Paper Verdict        ← 插在这里
> **再读价值**: ⭐⭐⭐
...

## 一句话总结                ← 在这之前
```

### 添加解释

1. 用户指出不理解的部分（可能引用原文或描述位置）
2. Agent 解释该部分
3. 用户确认："写到笔记里"
4. Agent 执行：
   - 找到该部分在笔记中的位置
   - 在其后插入 `#### 💡 Explain by Reader` section
   - 包含解释内容和署名

### 添加 Reader's Notes

1. 用户请求添加阅读笔记
2. Agent 确认内容（可能是之前讨论的总结）
3. Agent 执行：
   - 检查笔记是否已有 `## 📖 Reader's Notes` section
   - 如果没有，在末尾创建
   - 追加内容，包含署名

### 添加 Q&A 讨论记录

1. 用户和 agent 进行了深入 Q&A 讨论
2. 用户请求写入笔记（"写到笔记里"、"记录一下"等）
3. Agent 执行：
   - 整理讨论中的 Q&A 内容
   - 检查笔记是否已有 `## 📖 Reader's Notes` section
   - 如果没有，在末尾创建
   - 写入 Q&A 格式的内容（`#### Qn:` 格式）
   - 附上与其他论文的联系
4. 如果 Q&A 涉及模型架构，**主动询问用户是否需要更新 mermaid 图**
5. Git commit & push

**Q&A 整理原则**：
- 每个独立问题做成一个 Q&A
- 回答要清晰，可以用代码块/公式/表格
- 包含具体的例子和类比
- 如果讨论中有"写到笔记里"的明确请求，直接写入

### 更新 Mermaid 图

1. 用户请求更新图（"更新图"、"改 mermaid"）
2. Agent 执行：
   - 找到现有 mermaid 图
   - 根据讨论内容更新（更详细、更准确）
   - 确保语法正确（中文标签加引号，特殊字符用引号包裹）
3. Git commit & push

## 操作指令

### 添加论文评估

```
add_verdict <paper_name> <rating> <evidence_strength> <summary> <strengths> <weaknesses> <use_cases>
```

示例：
```
add_verdict AtomicProbe rating:3 evidence:weak summary:"问题有价值但只在一个任务上验证" strengths:"首次提出技能更新治理问题;方法论清晰" weaknesses:"主导技能效应只在T6观察到;T2-T5原子成功率全0" use_cases:"研究技能组合稳定性的参考;skill-update governance方向"
```

### 添加局部解释

```
add_explanation <paper_name> <section_locator> <explanation>
```

参数：
- `paper_name`: 论文笔记名称（不含 .md）
- `section_locator`: 定位方式
  - `section:XXX` - 找到 `## XXX` 或 `### XXX` section
  - `keyword:XXX` - 找到包含关键词的段落
- `explanation`: 解释内容

示例：
```
add_explanation CLARE section:模型架构 这里的FFN层存储知识是因为...
```

### 添加 Reader's Notes

```
add_reader_notes <paper_name> <content> [--append]
```

参数：
- `paper_name`: 论文笔记名称
- `content`: 笔记内容（Markdown 格式）
- `--append`: 追加到现有 Reader's Notes section（如果已存在）

示例：
```
add_reader_notes CLARE "
### 关键洞察
- 动态扩展策略很巧妙，避免无限制增长

### 与其他论文的联系
- [[MoE-Adapters]] 也用了类似思想
"
```

### 添加 Q&A 讨论记录

```
add_qa_notes <paper_name> <qa_content> [--update-mermaid <mermaid_content>]
```

参数：
- `paper_name`: 论文笔记名称
- `qa_content`: Q&A 内容（Markdown 格式，用 `#### Qn:` 分隔）
- `--update-mermaid`: 可选，同时更新 mermaid 图

示例：
```
add_qa_notes HOVER "
#### Q1: HOVER 是运动跟踪吗？
不是。HOVER 是全身控制器...

#### Q2: Mask 是什么？
Mask 是一个 one-hot 向量...
"
```

### 更新 Mermaid 图

```
update_mermaid <paper_name> <mermaid_content>
```

参数：
- `paper_name`: 论文笔记名称
- `mermaid_content`: mermaid 图内容（不含 ```mermaid 标记）

示例：
```
update_mermaid HOVER "
graph TB
    subgraph Phase1[\"Phase 1\"]
        A[\"AMASS\"] --> B[\"Oracle\"]
    end
"
```

## 执行方式

### 查找位置

```bash
# 找到 section 位置
grep -n "## 模型架构" Papers/*/CLARE.md

# 找到关键词位置
grep -n "FFN 层存储" Papers/*/CLARE.md
```

### 插入解释

使用 `edit` 工具，在目标位置后插入：

```xml
<parameter name="file_path">/path/to/paper.md</parameter>
<parameter name="oldText">原始段落内容</parameter>
<parameter name="newText">原始段落内容

#### 💡 Explain by Reader
> 解释内容
> 
> — vault-reader, 2026-04-07</parameter>
```

### 追加 Reader's Notes

1. 先检查是否已有该 section
2. 如果有，追加内容
3. 如果没有，在笔记末尾 `---` 前插入

## 格式规范

### 署名格式

- Agent 解释：`— vault-reader, YYYY-MM-DD`
- 用户见解：`— Eve, YYYY-MM-DD`

### 引用格式

- 论文链接：`[[Paper_Name]]`
- 概念链接：`[[Concept_Name]]`

### 内容风格

- 解释要清晰、有针对性
- 避免过度展开，保持简洁
- 必要时引用相关论文或概念

## 示例对话

**用户**: CLARE 的模型架构这块我不太理解，为什么 FFN 层可以存储知识？

**Agent**: FFN 层之所以能存储知识，是因为它的参数矩阵可以看作是一个巨大的键值存储...

**用户**: 帮我把这个解释写到笔记里，就在模型架构那部分旁边

**Agent**: 好的，我来添加解释到 CLARE 笔记的模型架构部分。
[执行 add_explanation 操作]

**用户**: 帮我加个 Reader's Notes，总结一下 CLARE 和 MoE-Adapters 的对比

**Agent**: 
[执行 add_reader_notes 操作]

## Git 操作

添加笔记后，自动提交并推送到 ObsidianVault repo。

### 提交格式

```bash
git add <modified_file>
git commit -m "Add reader notes to <paper_name>"
git push
```

### 执行时机

每次添加解释或 Reader's Notes 后立即执行：
1. `git add` 修改的文件
2. `git commit` 并附上清晰的 commit message
3. `git push` 到远程

### Vault 位置

`{VAULT_PATH}`（从 config 读取）

所有 git 操作都在此目录下执行。

## 注意事项

1. **不要覆盖原有内容**：总是在原文后追加或插入新 section
2. **保持格式一致**：使用和原笔记相同的 Markdown 风格
3. **标注来源**：区分 agent 解释和用户见解
4. **日期格式**：统一使用 YYYY-MM-DD
5. **立即推送**：添加笔记后立即 git commit 和 push

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

## 工作流程

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

## 操作指令

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

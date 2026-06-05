# Vault Reader Skills

轻量级论文阅读 & 讨论 agent 的专用技能集。

## Skills

| Skill | 用途 |
|-------|------|
| `latex-render` | LaTeX 公式渲染为 PNG（Discord 专用） |
| `learning-notes` | 基础知识学习笔记（Learning/ 目录） |
| `reader-notes` | 论文笔记追加解释和评论 |
| `spark-manager` | 灵感管理器（记录/追踪/演化研究想法） |

## 配置

所有路径从 `_shared/user-config.json` 读取，支持 `user-config.local.json` 覆盖。

```json
{
  "VAULT_PATH": "/path/to/ObsidianVault",
  "LEARNING_PATH": "/path/to/ObsidianVault/Learning",
  "LATEX_CACHE_PATH": "/path/to/latex-cache",
  "SPARK_PATH": "/path/to/ObsidianVault/灵光一现",
  "GIT_COMMIT_ENABLED": true,
  "GIT_PUSH_ENABLED": true
}
```

## 安装

将此目录放到 agent 的 skills 目录下，确保 `_shared/` 目录包含 `user-config.json`。

## 依赖

- Python 3.8+
- 标准库 only（无第三方依赖）

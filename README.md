# Vault Reader Skills

轻量级论文阅读 & 讨论 agent 的专用技能集。

## Skills

| Skill | 用途 |
|-------|------|
| `learning-notes` | 基础知识学习笔记（Learning/ 目录） |
| `reader-notes` | 论文笔记追加解释和评论 |
| `spark-manager` | 灵感管理器（记录/追踪/演化研究想法） |

## 配置

所有配置在 `_shared/user_config.py` 的 `DEFAULT_CONFIG` 中定义。如需覆盖，创建 `_shared/user-config.local.json`。

```python
DEFAULT_CONFIG = {
    "VAULT_PATH": "/path/to/ObsidianVault",
    "LEARNING_PATH": "/path/to/ObsidianVault/Learning",
    "SPARK_PATH": "/path/to/ObsidianVault/灵光一现",
    "GIT_COMMIT_ENABLED": True,
    "GIT_PUSH_ENABLED": True,
}
```

## 安装

将此目录放到 agent 的 skills 目录下。

## 依赖

- Python 3.8+
- 标准库 only（无第三方依赖）

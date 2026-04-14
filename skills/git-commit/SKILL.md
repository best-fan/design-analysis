---
name: git-commit
description: 此技能用于生成符合项目规范的 git commit。当用户请求提交代码、运行 /git-commit 命令、或完成代码修改后需要提交时触发此技能。技能会分析 git 变更，生成多个候选 commit 消息供用户选择，确认后执行 git add 和 git commit，并询问是否推送远程仓库。
metadata:
  version: 1.1.0
  updatedAt: 2026-04-14
---

# Git Commit Skill

生成符合项目规范的 git commit。

## 执行步骤

1. 运行 `git status` 查看未提交的文件
2. 运行 `git diff --stat` 查看修改统计
3. 运行 `git log --oneline -5` 查看最近的 commit 消息风格
4. 分析修改内容，生成 **多个候选 commit 消息**供用户选择
5. **使用 AskUserQuestion 展示候选消息，让用户选择确认**
6. 用户确认后，使用 `git add` 添加修改的文件
7. 使用 `git commit` 创建提交
8. **使用 AskUserQuestion 让用户确认是否推送远程**
9. 用户确认推送后，执行 `git push`

## Commit 消息格式

```
<type>(<scope>): <subject>

<body>

Authored-By: Claude Code AI
```

## Commit 类型

| 类型 | 说明 |
|------|------|
| feat | 新功能 |
| fix | 修复问题 |
| docs | 文档变更 |
| style | 代码格式调整（不影响功能） |
| refactor | 重构代码 |
| perf | 性能优化 |
| test | 测试相关 |
| chore | 构建/工具相关 |

## 注意事项

- 使用 HEREDOC 格式传递 commit 消息，避免换行问题
- commit 消息末尾添加 `Authored-By` 标识
- 只 commit 用户明确请求的文件
- 不要使用 `--no-verify` 跳过 hooks
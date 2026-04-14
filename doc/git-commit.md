# Git Commit 技能文档

## 使用时机

在以下情况使用此技能：

- 用户请求提交代码
- 手动调用 `/git-commit` 命令
- 完成代码修改后需要提交
- 需要生成规范的 commit 消息

---

## 核心功能

- 分析 git 变更内容（status、diff）
- 查看项目 commit 消息风格
- 生成多个候选 commit 消息供用户选择
- 执行 git add 和 git commit
- 询问是否推送远程仓库

---

## 执行步骤

### 步骤 1：查看变更状态

```bash
git status              # 查看未提交的文件
git diff --stat         # 查看修改统计
git log --oneline -5    # 查看最近的 commit 消息风格
```

---

### 步骤 2：生成候选消息

分析修改内容，生成 **多个候选 commit 消息**供用户选择。

---

### 步骤 3：用户确认

使用 `AskUserQuestion` 展示候选消息，让用户选择确认。

---

### 步骤 4：执行提交

```bash
# 添加修改的文件
git add {文件路径}

# 创建提交（使用 HEREDOC 格式）
git commit -m "$(cat <<'EOF'
<type>(<scope>): <subject>

<body>

Authored-By: Claude Code AI
EOF
)"
```

---

### 步骤 5：推送确认

使用 `AskUserQuestion` 让用户确认是否推送远程。

用户确认推送后，执行 `git push`。

---

## Commit 消息格式

```
<type>(<scope>): <subject>

<body>

Authored-By: Claude Code AI
```

### 格式说明

| 部分 | 说明 | 示例 |
|------|------|------|
| type | commit 类型 | `feat`、`fix`、`docs` |
| scope | 影响范围（可选） | `skills`、`build` |
| subject | 简短描述 | `添加 git-commit 技能` |
| body | 详细说明（可选） | 多行描述 |
| Authored-By | AI 标识 | 固定值 |

---

## Commit 类型

| 类型 | 说明 | 适用场景 |
|------|------|----------|
| feat | 新功能 | 添加新技能、新特性 |
| fix | 修复问题 | 修复 bug、错误 |
| docs | 文档变更 | 更新文档、README |
| style | 代码格式调整 | 不影响功能的格式修改 |
| refactor | 重构代码 | 代码重构、优化 |
| perf | 性能优化 | 性能改进 |
| test | 测试相关 | 添加或修改测试 |
| chore | 构建/工具相关 | 构建配置、工具更新 |

---

## 注意事项

| 注意点 | 说明 |
|--------|------|
| HEREDOC 格式 | 使用 HEREDOC 传递 commit 消息，避免换行问题 |
| Authored-By 标识 | commit 消息末尾添加 `Authored-By: Claude Code AI` |
| 文件选择 | 只 commit 用户明确请求的文件 |
| hooks | 不要使用 `--no-verify` 跳过 hooks |
| 多候选消息 | 提供多个选项让用户选择，不自动决定 |

---

## 示例输出

```
📝 Git 提交分析完成

**变更文件**：3 个
- README.md（修改）
- doc/git-commit.md（新增）
- skills/git-commit/SKILL.md（新增）

**候选 commit 消息**：

1. feat(skills): 添加 git-commit 技能并更新 README
2. docs: 新增 git-commit 技能文档
3. chore: 添加 git-commit 技能配置

请选择 commit 消息：[1/2/3/其他]

是否推送远程仓库？[是/否]
```

---

## 技能文件结构

```
skills/git-commit/
└── SKILL.md              # 技能入口定义
```

---

## 版本信息

- 当前版本：1.1.0
- 更新日期：2026-04-14
# Agent Skills

Claude Code 技能仓库，提供可复用的自动化工作流。

## 技能列表

| 技能 | 版本 | 说明 |
|------|------|------|
| [design-analysis](#design-analysis) | 1.26.1 | 设计稿分析，产出 UI 分析清单 |
| [frontend-code-review](#frontend-code-review) | 1.2.0 | 前端代码审查，输出结构化报告 |
| [build-frontend-zip](#build-frontend-zip) | 1.0.0 | 前端项目打包，生成 zip 分发包 |
| [git-commit](#git-commit) | 1.1.0 | Git 提交，生成规范 commit 消息 |

---

### design-analysis

通用设计稿分析技能，支持 `.pen`、Figma、MasterGo 设计稿及本地图片。

**核心功能：**
- 建立 UI 布局结构
- 提取文字、图片、布局、层级信息
- 汇总样式规范（颜色、字体、圆角、间距等）
- 产出标准化 UI 分析清单文档

**使用方式：** `/design-analysis`

**详细文档：** [doc/design-analysis.md](doc/design-analysis.md)

---

### frontend-code-review

前端代码审查技能，适用于 Vue 3 + TypeScript + pnpm 项目。

**核心功能：**
- 运行 ESLint、TypeScript 静态检查
- 代码质量、类型安全、Vue 规范审查
- npm 依赖安全审计
- 输出结构化审查报告

**使用方式：** `/frontend-code-review`

**详细文档：** [doc/frontend-code-review.md](doc/frontend-code-review.md)

---

### build-frontend-zip

前端项目打包技能，将构建产物压缩为可分发的 zip 文件。

**核心功能：**
- 自动检测项目路径和包管理器
- 运行构建命令并打包 dist 目录
- 输出构建汇总信息（分支、耗时、文件数量等）
- 生成带时间戳的 zip 文件

**使用方式：** `/build-frontend-zip`

**详细文档：** [doc/build-frontend-zip.md](doc/build-frontend-zip.md)

---

### git-commit

Git 提交技能，生成符合项目规范的 commit 消息。

**核心功能：**
- 分析 git 变更内容
- 根据项目 commit 风格生成多个候选消息
- 用户选择确认后执行提交
- 询问是否推送远程仓库

**使用方式：** `/git-commit`

**详细文档：** [doc/git-commit.md](doc/git-commit.md)

---

## 安装说明

### 方法一：网络拉取（推荐）

使用 `npx skills add` 从远程仓库直接安装：

```bash
# 安装 design-analysis 技能
npx skills add https://github.com/best-fan/agent-skills/tree/main/skills/design-analysis

# 安装 frontend-code-review 技能
npx skills add https://github.com/best-fan/agent-skills/tree/main/skills/frontend-code-review

# 安装 build-frontend-zip 技能
npx skills add https://github.com/best-fan/agent-skills/tree/main/skills/build-frontend-zip

# 安装 git-commit 技能
npx skills add https://github.com/best-fan/agent-skills/tree/main/skills/git-commit
```

### 方法二：复制到项目

将需要的技能文件夹复制到项目的 `.claude/skills/` 目录：

```bash
# 安装 design-analysis 技能
cp -r skills/design-analysis /path/to/your/project/.claude/skills/

# 安装 frontend-code-review 技能
cp -r skills/frontend-code-review /path/to/your/project/.claude/skills/

# 安装 build-frontend-zip 技能
cp -r skills/build-frontend-zip /path/to/your/project/.claude/skills/

# 安装 git-commit 技能
cp -r skills/git-commit /path/to/your/project/.claude/skills/
```

### 方法三：全局安装

将技能文件夹复制到 Claude Code 全局配置目录：

```bash
# Windows
cp -r skills/design-analysis %USERPROFILE%\.claude\skills\

# macOS / Linux
cp -r skills/design-analysis ~/.claude/skills/
```

### 验证安装

安装后，在 Claude Code 中运行：

```
/design-analysis
```

或

```
/build-frontend-zip
```

技能将自动加载并执行。

---

## 目录结构

```
agent-skills/
├── README.md                    # 本文件
├── CLAUDE.md                    # 项目级 Claude Code 配置
├── doc/                         # 详细文档
│   ├── design-analysis.md       # 设计稿分析技能详细文档
│   ├── frontend-code-review.md  # 前端代码审查技能详细文档
│   ├── build-frontend-zip.md    # 前端打包技能详细文档
│   └── git-commit.md            # Git 提交技能详细文档
└── skills/                      # 技能定义
    ├── design-analysis/
    │   ├── SKILL.md             # 技能入口
    │   ├── references/          # 参考文档
    │   ├── scripts/             # 工具脚本
    │   └── assets/              # 示例资源
    ├── frontend-code-review/
    │   ├── SKILL.md             # 技能入口
    │   └── references/          # 参考文档
    ├── build-frontend-zip/
    │   ├── SKILL.md             # 技能入口
    │   └── scripts/             # 工具脚本
    └── git-commit/
        └── SKILL.md             # 技能入口
```

---

## 扩展阅读

- [Claude Code 技能开发指南](https://docs.anthropic.com/claude-code/skills)
- [提交问题或建议](https://github.com/anthropics/claude-code/issues)
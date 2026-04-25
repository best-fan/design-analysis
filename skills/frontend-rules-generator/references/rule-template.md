# Rules 文件模板结构

## YAML Frontmatter 格式

```yaml
---
paths:
  - "src/xxx/**/*.ts"
  - "src/yyy/**/*.vue"
---
```

- **paths**: 必填字段，使用 glob 模式匹配文件路径
- 多个路径使用数组形式
- 支持 `**` 通配符匹配多层目录

## Markdown 内容模板

```markdown
# {模块名} 开发规范

## 开发前检查流程

**在编写新{内容类型}前，必须按以下顺序检查：**

### 1. 检查全局是否已存在类似{内容类型}

**必须先搜索 `src/{模块}/` 目录**，确认没有可复用的{内容类型}：

```bash
# 搜索现有{内容类型}
ls src/{模块}/
grep -r "{关键词}" src/{模块}/
```

**常见全局{内容类型}清单**：

| {名称} | 文件 | {功能说明} |
|--------|------|------------|
| ... | ... | ... |

### 2. 判断{内容类型}归属

| 条件 | 归属目录 | 示例 |
|------|----------|------|
| 多个模块共用 | `src/{模块}/` | ... |
| 单个页面独用 | 页面内定义 | ... |

### 3. 评估是否应添加到全局

**满足以下条件之一，应添加到全局{模块}**：

- ✅ {条件1}
- ✅ {条件2}
- ✅ {条件3}

**不应添加到全局的情况**：

- ❌ {反条件1}
- ❌ {反条件2}

### 4. 扩展现有{内容类型}

如果全局存在类似{内容类型}，优先**扩展现有{内容类型}**：

```typescript
// ✅ 扩展现有{内容类型}
// {路径}
export const existing = ...

// 新增内容
export const newContent = ...

// ❌ 新建重复{内容类型}
```

## 文件组织

### 文件命名
- 格式：{命名规则}
- 示例：`{示例1}`、`{示例2}`

### 目录结构
```
src/{模块}/
├── {文件1}
├── {文件2}
└── index.ts
```

## 命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| ... | ... | ... |

## 代码模板示例

```typescript
// 正确示例
```

```typescript
// 错误示例
```

## 禁止事项

1. ❌ 禁止{事项1}
2. ❌ 禁止{事项2}
3. ❌ 禁止{事项3}
```

## 常见模块 Rules 模板

### Vue 组件 Rules

```yaml
---
paths:
  - "src/components/**/*"
  - "src/pages/**/*"
---
```

### Services/API Rules

```yaml
---
paths:
  - "src/services/*.ts"
---
```

### Store Rules (Pinia/Vuex)

```yaml
---
paths:
  - "src/store/**/*.ts"
---
```

### Composables/Hooks Rules

Vue Composables:
```yaml
---
paths:
  - "src/composables/**/*.ts"
  - "src/pages/**/composables/*.ts"
---
```

React Hooks:
```yaml
---
paths:
  - "src/hooks/**/*.ts"
---
```

### Types Rules

```yaml
---
paths:
  - "src/types/**/*.ts"
---
```

### Utils Rules

```yaml
---
paths:
  - "src/utils/*.ts"
---
```

### Router Rules

```yaml
---
paths:
  - "src/router/*.ts"
---
```

### Style Rules

```yaml
---
paths:
  - 'src/**/*.scss'
  - 'src/**/*.vue'
---
```

### 通用代码质量 Rules

```yaml
---
paths:
  - "src/**/*.ts"
  - "src/**/*.vue"
---
```
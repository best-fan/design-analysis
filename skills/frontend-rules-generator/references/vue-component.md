# Vue 组件规范模板

此模板用于生成 Vue 项目的 `vue-component.md` 规则文件。

## YAML Frontmatter

```yaml
---
paths:
  - "src/components/**/*.vue"
  - "src/pages/**/*.vue"
---
```

## 完整模板示例

```markdown
---
paths:
  - "src/components/**/*.vue"
  - "src/pages/**/*.vue"
---
# Vue 组件开发规范

## 开发前检查流程

**在编写新组件前，必须按以下顺序检查：**

### 1. 检查全局是否已存在类似组件

**必须先搜索 `src/components/` 目录**，确认没有可复用的组件：

```bash
# 搜索现有组件
ls src/components/
grep -r "关键词" src/components/
```

**常见全局组件清单**：

| 组件名 | 文件 | 功能 |
|--------|------|------|
| Button | `Button.vue` | 基础按钮 |
| Input | `Input.vue` | 输入框 |
| Table | `Table.vue` | 表格 |
| Modal | `Modal.vue` | 弹窗 |
| Card | `Card.vue` | 卡片容器 |

### 2. 判断组件归属

| 条件 | 归属目录 | 示例 |
|------|----------|------|
| 多个页面共用 | `src/components/` | Button、Modal |
| 单个页面独用 | 页面内定义 | UserCard 只在 UserProfile 页面用 |
| 业务模块共用 | `src/components/{module}/` | OrderCard 只在订单模块用 |

### 3. 评估是否应添加到全局

**满足以下条件之一，应添加到全局 components**：

- ✅ 3个及以上页面需要使用
- ✅ 通用 UI 功能（按钮、输入、弹窗等）
- ✅ 可能有其他模块未来需要

**不应添加到全局的情况**：

- ❌ 仅单个页面使用
- ❌ 强依赖特定业务数据结构
- ❌ 包含复杂业务逻辑

### 4. 扩展现有组件

如果全局存在类似组件，优先**扩展现有组件**：

```vue
<!-- ✅ 扩展 Button.vue -->
<!-- src/components/Button.vue -->
<template>
  <button :class="['btn', variantClass]">
    <slot />
  </button>
</template>

<script setup lang="ts">
// 新增 variant prop
defineProps<{
  variant?: 'primary' | 'secondary' | 'danger'
}>()
</script>

<!-- ❌ 新建重复 MyButton.vue -->
```

## 文件组织

### 文件命名

| 类型 | 规范 | 示例 |
|------|------|------|
| 组件文件 | PascalCase | `UserCard.vue` |
| 组件目录 | kebab-case 或 PascalCase | `user-card/` 或 `UserCard/` |
| 样式文件 | 同组件名 | `UserCard.scss`（分离时） |

### 目录结构

**单文件组件**：
```
src/components/
├── Button.vue
├── Input.vue
└── index.ts    # 统一导出
```

**复杂组件（带逻辑/样式分离）**：
```
src/components/
└── UserCard/
    ├── index.vue      # 主组件入口
    ├── UserCard.vue   # 组件实现
    ├── useUserCard.ts # 组合式函数（可选）
    ├── UserCard.scss  # 样式（可选）
    └── types.ts       # 类型定义（可选）
```

## 命名规范

### 组件命名

| 类型 | 规范 | 示例 |
|------|------|------|
| 组件名 | PascalCase | `UserCard`, `OrderList` |
| 组件注册名 | PascalCase 或 kebab-case | `<UserCard />` 或 `<user-card />` |
| Props | camelCase | `userList`, `isLoading` |
| Events | kebab-case | `@update:model-value`, `@click` |

### 组合式函数命名

| 类型 | 规范 | 示例 |
|------|------|------|
| 返回响应式状态 | `use{功能}` | `useUserList`, `useForm` |
| 纯计算函数 | 不用 use 前缀 | `formatDate`, `calcTotal` |
| 事件处理 | `handle{动作}` | `handleClick`, `handleSubmit` |

## 代码模板示例

### Composition API（推荐）

```vue
<!-- ✅ 正确：使用 <script setup> -->
<template>
  <div class="user-card">
    <span>{{ user.name }}</span>
    <Button @click="handleEdit">编辑</Button>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import Button from '@/components/Button.vue'

// Props 定义
const props = defineProps<{
  user: User
}>()

// Events 定义
const emit = defineEmits<{
  edit: [user: User]
}>()

// 响应式状态
const isEditing = ref(false)

// 计算属性
const displayName = computed(() => props.user.name)

// 方法
function handleEdit() {
  emit('edit', props.user)
}
</script>

<style scoped>
.user-card {
  /* 样式 */
}
</style>
```

### Options API（遗留代码）

```vue
<!-- 仅用于遗留项目，新项目禁用 -->
<script lang="ts">
export default {
  name: 'UserCard',
  props: {
    user: { type: Object, required: true }
  },
  emits: ['edit'],
  data() {
    return { isEditing: false }
  },
  methods: {
    handleEdit() {
      this.$emit('edit', this.user)
    }
  }
}
</script>
```

### 禁止事项

```vue
<!-- ❌ 禁止：内联样式 -->
<template>
  <div style="color: red">...</div>
</template>

<!-- ❌ 禁止：未使用 scoped -->
<style>
/* 全局样式污染 */
.user-card { }
</style>

<!-- ❌ 禁止：直接修改 props -->
<script setup>
props.user.name = 'new'  // 禁止
</script>

<!-- ❌ 禁止：大型组件（>300行） -->
<!-- 拆分为子组件或组合式函数 -->

<!-- ❌ 禁止：任何 类型 -->
<script setup>
const user: any = {}  // 禁止
</script>
```

## 禁止事项清单

1. ❌ 禁止内联 style 属性
2. ❌ 禁止未使用 scoped 的组件样式
3. ❌ 禁止直接修改 props
4. ❌ 禁止组件超过 300 行（需拆分）
5. ❌ 禁止使用 `any` 类型
6. ❌ 禁止在组件内定义复杂业务逻辑（移至 composables）
7. ❌ 禁止 Options API（仅遗留代码允许）
8. ❌ 禁止重复创建已存在的组件
```

## 样式规范补充

### Scoped 样式最佳实践

```vue
<style scoped>
/* ✅ 使用 scoped 避免污染全局 */
.user-card {
  padding: 16px;
}

/* ✅ 子元素样式 */
.user-card .title {
  font-size: 14px;
}

/* ✅ 深度选择器（修改子组件样式） */
.user-card :deep(.btn) {
  margin-left: 8px;
}
</style>
```

### CSS 变量使用

```vue
<style scoped>
.user-card {
  /* ✅ 使用 CSS 变量 */
  --card-padding: var(--spacing-md, 16px);
  padding: var(--card-padding);
}
</style>
```

## 组件通信模式

### Props 传递

```vue
<!-- ✅ 正确：明确的 Props 定义 -->
<script setup lang="ts">
defineProps<{
  title: string
  count?: number
}>()
</script>

<!-- ❌ 禁止：无类型 Props -->
<script setup>
defineProps(['title', 'count'])  // 禁止
</script>
```

### Events 发送

```vue
<script setup lang="ts">
// ✅ 正确：类型化的 Events
const emit = defineEmits<{
  update: [value: string]
  close: []
}>()

function handleClose() {
  emit('close')
}
</script>
```

### Provide/Inject（跨层级）

```vue
<!-- Provider -->
<script setup lang="ts">
import { provide, ref } from 'vue'

const theme = ref('light')
provide('theme', theme)
</script>

<!-- Consumer -->
<script setup lang="ts">
import { inject } from 'vue'

const theme = inject<Ref<string>>('theme')
</script>
```
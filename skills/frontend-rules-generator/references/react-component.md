# React 组件规范模板

此模板用于生成 React 项目的 `react-component.md` 规则文件。

## YAML Frontmatter

```yaml
---
paths:
  - "src/components/**/*.tsx"
  - "src/components/**/*.jsx"
  - "src/pages/**/*.tsx"
---
```

## 完整模板示例

```markdown
---
paths:
  - "src/components/**/*.tsx"
  - "src/components/**/*.jsx"
  - "src/pages/**/*.tsx"
---
# React 组件开发规范

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
| Button | `Button.tsx` | 基础按钮 |
| Input | `Input.tsx` | 输入框 |
| Table | `Table.tsx` | 表格 |
| Modal | `Modal.tsx` | 弹窗 |
| Card | `Card.tsx` | 卡片容器 |

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

```tsx
// ✅ 扩展 Button.tsx
// src/components/Button.tsx
interface ButtonProps {
  children: React.ReactNode
  onClick?: () => void
  variant?: 'primary' | 'secondary' | 'danger'  // 新增 variant
}

export function Button({ children, onClick, variant = 'primary' }: ButtonProps) {
  return (
    <button 
      className={`btn btn-${variant}`}
      onClick={onClick}
    >
      {children}
    </button>
  )
}

// ❌ 新建重复 MyButton.tsx
```

## 文件组织

### 文件命名

| 类型 | 规范 | 示例 |
|------|------|------|
| 组件文件 | PascalCase.tsx | `UserCard.tsx` |
| 组件目录 | kebab-case 或 PascalCase | `user-card/` 或 `UserCard/` |
| 样式文件 | 同组件名 | `UserCard.css` 或 `UserCard.module.css` |
| 类型文件 | 同组件名 | `UserCard.types.ts` |

### 目录结构

**单文件组件**：
```
src/components/
├── Button.tsx
├── Input.tsx
└── index.ts    # 统一导出
```

**复杂组件（带逻辑/样式分离）**：
```
src/components/
└── UserCard/
    ├── index.tsx        # 主组件入口
    ├── UserCard.tsx     # 组件实现
    ├── useUserCard.ts   # 自定义 Hook
    ├── UserCard.module.css  # CSS Modules
    └── UserCard.types.ts    # 类型定义
```

## 命名规范

### 组件命名

| 类型 | 规范 | 示例 |
|------|------|------|
| 组件名 | PascalCase | `UserCard`, `OrderList` |
| Props 类型 | PascalCase + Props | `UserCardProps` |
| 事件处理 | handle{动作} | `handleClick`, `handleSubmit` |
| 渲染函数 | render{内容} | `renderHeader`, `renderItem` |

### Hooks 命名

| 类型 | 规范 | 示例 |
|------|------|------|
| 自定义 Hook | use{功能} | `useUserList`, `useForm` |
| 状态 Hook | useState 返回 | `[state, setState]` |
| Ref Hook | useRef 返回 | `inputRef` |

## 代码模板示例

### 函数组件（推荐）

```tsx
// ✅ 正确：函数组件 + TypeScript
// src/components/UserCard.tsx
import { useState, useCallback } from 'react'
import { Button } from '@/components/Button'
import type { User } from '@/types'

interface UserCardProps {
  user: User
  onEdit?: (user: User) => void
}

export function UserCard({ user, onEdit }: UserCardProps) {
  // 状态
  const [isEditing, setIsEditing] = useState(false)
  
  // 事件处理
  const handleEdit = useCallback(() => {
    onEdit?.(user)
    setIsEditing(true)
  }, [user, onEdit])
  
  return (
    <div className="user-card">
      <span>{user.name}</span>
      <Button onClick={handleEdit}>编辑</Button>
    </div>
  )
}

// 默认导出（可选）
export default UserCard
```

### 带 Hooks 的组件

```tsx
// src/components/UserList.tsx
import { useUserList } from '@/hooks/useUserList'

interface UserListProps {
  filter?: string
}

export function UserList({ filter }: UserListProps) {
  // 使用自定义 Hook
  const { users, loading, error, refetch } = useUserList(filter)
  
  if (loading) return <Spinner />
  if (error) return <ErrorMessage error={error} />
  
  return (
    <ul className="user-list">
      {users.map(user => (
        <li key={user.id}>
          <UserCard user={user} />
        </li>
      ))}
    </ul>
  )
}
```

### 组件拆分示例

```tsx
// ✅ 正确：复杂组件拆分
// src/components/UserProfile/index.tsx
export { UserProfile } from './UserProfile'
export { UserProfileHeader } from './UserProfileHeader'
export { UserProfileBody } from './UserProfileBody'

// src/components/UserProfile/UserProfile.tsx
import { UserProfileHeader } from './UserProfileHeader'
import { UserProfileBody } from './UserProfileBody'

export function UserProfile({ user }: UserProfileProps) {
  return (
    <div className="user-profile">
      <UserProfileHeader user={user} />
      <UserProfileBody user={user} />
    </div>
  )
}
```

### 禁止事项

```tsx
// ❌ 禁止：内联样式对象
<div style={{ color: 'red' }}>...</div>

// ❌ 禁止：未提取的复杂渲染逻辑
export function ComplexComponent() {
  return (
    <div>
      {/* 100+ 行的 JSX */}
    </div>
  )
}

// ❌ 禁止：直接修改 props
function Component({ user }: Props) {
  user.name = 'new'  // 禁止
}

// ❌ 禁止：大型组件（>300行）
// 拆分为子组件或提取 Hooks

// ❌ 禁止：any 类型
const user: any = {}  // 禁止

// ❌ 禁止：类组件（仅遗留代码允许）
class UserCard extends React.Component { }
```

## 禁止事项清单

1. ❌ 禁止内联 style 对象（提取为 CSS Modules 或 Tailwind）
2. ❌ 禁止直接修改 props
3. ❌ 禁止组件超过 300 行（需拆分）
4. ❌ 禁止使用 `any` 类型
5. ❌ 禁止在组件内定义复杂业务逻辑（移至 hooks）
6. ❌ 禁止类组件（仅遗留代码允许）
7. ❌ 禁止重复创建已存在的组件
8. ❌ 禁止 useEffect 中直接写异步函数（提取为 async function）
```

## 样式规范补充

### CSS Modules（推荐）

```tsx
// src/components/UserCard.module.css
.userCard {
  padding: 16px;
}

.title {
  font-size: 14px;
}

// src/components/UserCard.tsx
import styles from './UserCard.module.css'

export function UserCard() {
  return (
    <div className={styles.userCard}>
      <span className={styles.title}>Title</span>
    </div>
  )
}
```

### Tailwind CSS（如项目使用）

```tsx
// src/components/UserCard.tsx
export function UserCard() {
  return (
    <div className="p-4 rounded-lg shadow-md">
      <span className="text-sm font-medium">Title</span>
    </div>
  )
}
```

### Styled Components（如项目使用）

```tsx
// src/components/UserCard.tsx
import styled from 'styled-components'

const CardContainer = styled.div`
  padding: 16px;
`

export function UserCard() {
  return <CardContainer>...</CardContainer>
}
```

## Hooks 规范

### 自定义 Hook 模板

```tsx
// src/hooks/useUserList.ts
import { useState, useEffect } from 'react'
import type { User } from '@/types'

interface UseUserListResult {
  users: User[]
  loading: boolean
  error: Error | null
  refetch: () => void
}

export function useUserList(filter?: string): UseUserListResult {
  const [users, setUsers] = useState<User[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<Error | null>(null)
  
  useEffect(() => {
    fetchUsers(filter)
      .then(setUsers)
      .catch(setError)
      .finally(() => setLoading(false))
  }, [filter])
  
  const refetch = useCallback(() => {
    setLoading(true)
    fetchUsers(filter)
      .then(setUsers)
      .catch(setError)
      .finally(() => setLoading(false))
  }, [filter])
  
  return { users, loading, error, refetch }
}
```

### useEffect 规范

```tsx
// ✅ 正确：清理副作用
useEffect(() => {
  const subscription = subscribe()
  
  return () => {
    subscription.unsubscribe()
  }
}, [])

// ✅ 正确：提取 async 函数
useEffect(() => {
  async function fetchData() {
    const data = await fetch()
    setState(data)
  }
  fetchData()
}, [])

// ❌ 禁止：直接 async useEffect
useEffect(async () => {
  const data = await fetch()  // 禁止
  setState(data)
}, [])
```

## Props 传递模式

### 基础 Props

```tsx
// ✅ 正确：明确类型定义
interface ButtonProps {
  children: React.ReactNode
  onClick?: () => void
  disabled?: boolean
  variant?: 'primary' | 'secondary'
}

export function Button({ 
  children, 
  onClick, 
  disabled = false,
  variant = 'primary'
}: ButtonProps) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`btn btn-${variant}`}
    >
      {children}
    </button>
  )
}
```

### Render Props / Children as Function

```tsx
interface ListProps<T> {
  items: T[]
  children: (item: T, index: number) => React.ReactNode
}

export function List<T>({ items, children }: ListProps<T>) {
  return (
    <ul>
      {items.map((item, index) => (
        <li key={index}>{children(item, index)}</li>
      ))}
    </ul>
  )
}

// 使用
<List items={users}>
  {(user, index) => <UserCard user={user} />}
</List>
```

### Context 跨层级传递

```tsx
// src/context/UserContext.tsx
import { createContext, useContext } from 'react'

interface UserContextValue {
  user: User | null
  setUser: (user: User) => void
}

const UserContext = createContext<UserContextValue | null>(null)

export function UserProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  
  return (
    <UserContext.Provider value={{ user, setUser }}>
      {children}
    </UserContext.Provider>
  )
}

export function useUser() {
  const context = useContext(UserContext)
  if (!context) {
    throw new Error('useUser must be used within UserProvider')
  }
  return context
}
```
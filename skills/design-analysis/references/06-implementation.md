---
title: 实现建议
impact: HIGH
impactDescription: 主流网页设计常识和常见错误模式，实现时需遵循
tags: implementation, guidelines, errors, layout
---

# 实现建议

## 核心原则

**实现时应遵循主流网页设计常识，避免反审美的效果。**

看到设计稿时，默认不会出现以下反审美的效果：
- 右侧大片留白
- 列表留空白
- 元素截断
- 换行后列宽不一致

---

## 页面容器宽度

### ❌ 错误做法

**不应写死 `max-width`** 导致右侧大片留白。

```css
/* 错误：固定宽度导致右侧大片留白 */
.container {
  max-width: 1200px;
  margin: 0 auto;
}
```

### ✅ 正确做法

**页面应自适应视口宽度**。

```css
/* 正确：自适应视口宽度 */
.container {
  width: 100%;
  padding: 0 132px;
}
```

---

## 横向列表布局

### ❌ 错误做法

- 不应限制一行几个元素而留空白
- 不应出现元素被截断

### ✅ 正确做法

- 应铺满可用宽度，能放几个放几个
- 换行后应保持列宽一致（使用 Grid 而非 Flex）

### 布局选择指导

#### Grid：适合等列宽、多行一致

```css
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 24px;
  width: 100%; /* 重要：确保 Grid 容器有明确宽度 */
}
```

#### Flex：适合自适应但每行独立计算

```css
.flex {
  display: flex;
  flex-wrap: wrap;
  gap: 24px;
}

.flex-item {
  flex-grow: 1; /* 允许增长 */
  flex-basis: 300px;
}
```

---

## 元素展示完整性

### ❌ 错误做法

**不应展示不完整的元素**（如半截卡片、被裁切的按钮）。

### ✅ 正确做法

**要么完整展示，要么完全不展示**。

```css
.container {
  overflow: hidden;
}

.item {
  flex: 0 0 calc(33.333% - 16px);
}
```

---

## 对齐方式

### 图标与文本的对齐

```css
.icon-text {
  display: flex;
  align-items: center; /* 垂直居中 */
  gap: 8px;
}
```

---

## 常见错误模式

| 错误模式 | 原因 | 避免方法 |
|---------|------|----------|
| **Grid 一行只有一个** | Grid 容器宽度不确定 | 确保 Grid 容器有明确宽度（`width: 100%`） |
| **Flex 不铺满、留空白** | 使用了 `flex: 0 1 fixed-width` | 使用 `flex-grow: 1` |
| **换行后列宽不一致** | Flex 布局每行独立计算 | 使用 Grid 保证列宽一致 |
| **组件样式被覆盖** | 页面级样式覆盖组件样式 | 使用更具体的选择器或 CSS Modules |
| **对齐方式错误** | 默认使用了 `flex-start` | 明确设置 `align-items: center` |
| **按钮尺寸不对** | 未用浏览器实际查看 | **必须用浏览器工具查看实际渲染效果** |

---

## 必须用浏览器验证的细节

以下细节**必须用浏览器工具实际查看渲染效果**：

- ⚠️ **按钮高度、宽度**
- ⚠️ **对齐效果**
- ⚠️ **hover/active 状态**
- ⚠️ **响应式表现**

---

## 实现检查清单

- [ ] Grid 容器有明确宽度（如 `width: 100%`）
- [ ] Flex 布局使用 `flex-grow: 1` 允许增长
- [ ] 需要列宽一致时使用 Grid 而非 Flex
- [ ] 组件样式使用更具体的选择器或 CSS Modules
- [ ] 对齐方式明确设置（如 `align-items: center`）
- [ ] 按钮尺寸用浏览器工具实际查看

---

## 搜索关键词

| 搜索关键词 | 定位内容 |
|-----------|---------|
| `Grid\|Flex\|布局` | 布局选择 |
| `留白\|截断` | 常见问题 |
| `对齐\|align-items` | 对齐方式 |
| `错误模式\|避免方法` | 错误模式表格 |
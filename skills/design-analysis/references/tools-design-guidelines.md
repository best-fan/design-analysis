---
title: 设计稿工具使用指南
impact: HIGH
impactDescription: 根据设计稿类型选择 Pencil MCP 或 Figma MCP 或 MasterGo MCP 获取布局与节点信息
tags: tools, design, pencil, figma, MasterGo 
---

# 设计稿工具使用指南

## 概述

根据设计稿类型选择相应的工具，获取设计稿的结构、截图、布局和节点信息。


**支持的设计稿类型**：
- `.pen` 文件 → 使用 **Pencil MCP**
- **Figma 链接** → 使用 **Figma MCP**
- **MasterGo 链接** → 使用 **MasterGo MCP**
- **本地图片**（截图/UI 图片）→ 使用 **大模型视觉识别**

## 设计稿类型与工具选择

### .pen（Pencil 设计稿）

**工具**：Pencil MCP

**可用功能**：
- `mcp__pencil__open_document` - 打开 .pen 文件（使用设计稿前必须先执行）
- `mcp__pencil__get_editor_state` - 获取当前编辑器状态和用户选中的节点
- `mcp__pencil__snapshot_layout` - 获取布局快照，查看整体结构
- `mcp__pencil__get_screenshot` - 获取节点截图
- `mcp__pencil__batch_get` - 批量获取节点详细信息
- `mcp__pencil__get_variables` - 获取变量和主题定义

**使用步骤**：
1. **打开设计稿** - 使用 `mcp__pencil__open_document(filePath)` 打开 .pen 文件
2. **获取编辑器状态** - 使用 `mcp__pencil__get_editor_state` 查看顶层节点和选中状态
3. **获取整体布局** - 使用 `mcp__pencil__snapshot_layout` 获取整体布局结构
4. **获取截图** - 使用 `mcp__pencil__get_screenshot` 获取页面截图用于视觉分析
5. **获取节点详情** - 使用 `mcp__pencil__batch_get` 获取具体节点的详细信息

**示例**：
```javascript
// 1. 打开 .pen 文件（必须首先执行）
mcp__pencil__open_document({ filePathOrTemplate: "path/to/design.pen" })

// 2. 获取编辑器状态，查看顶层节点
mcp__pencil__get_editor_state({ include_schema: true })

// 3. 获取布局快照（filePath 为可选参数，若已打开文档可省略）
mcp__pencil__snapshot_layout({ filePath: "path/to/design.pen", maxDepth: 2 })

// 4. 获取特定节点的截图
mcp__pencil__get_screenshot({ filePath: "path/to/design.pen", nodeId: "node-id" })

// 5. 批量获取节点详细信息
mcp__pencil__batch_get({
  filePath: "path/to/design.pen",
  nodeIds: ["node1", "node2"],
  readDepth: 2
})

// 6. 获取变量和主题
mcp__pencil__get_variables({ filePath: "path/to/design.pen" })
```

**重要参数说明**：
- `filePath` - .pen 文件的绝对路径（大部分工具都需要）
- `nodeId` - 节点的唯一标识符
- `maxDepth` / `readDepth` - 读取深度，控制获取多少层子节点
- `include_schema` - 是否包含 schema 信息

### Figma 链接

**工具**：Figma MCP

**可用功能**：
- `mcp__Framelink_Figma_MCP__get_figma_data` - 获取 Figma 文件的全面数据，包括布局、内容、视觉效果和组件信息
- `mcp__Framelink_Figma_MCP__download_figma_images` - 下载 Figma 文件中使用的 SVG 和 PNG 图像

**使用步骤**：
1. 从 Figma 链接中解析 file key 和 node id
   - URL 格式：`https://www.figma.com/file/{fileKey}/{fileName}?node-id={nodeId}` 或 `https://www.figma.com/design/{fileKey}/{fileName}?node-id={nodeId}`
   - nodeId 格式：`'1234:5678'` 或 `'I5666:180910;1:10515;1:10336'`（多个节点）
2. 使用 `mcp__Framelink_Figma_MCP__get_figma_data` 获取设计稿的结构、布局和节点信息
3. 使用 `mcp__Framelink_Figma_MCP__download_figma_images` 下载所需的图像资源（SVG/PNG）

**示例**：
```javascript
// 获取设计稿数据
mcp__Framelink_Figma_MCP__get_figma_data({ fileKey, nodeId, depth })

// 下载图像资源
mcp__Framelink_Figma_MCP__download_figma_images({ fileKey, localPath, nodes, pngScale })
```

**使用流程**：
1. 先用 `mcp__Framelink_Figma_MCP__get_figma_data` 获取设计稿数据，识别需要的节点
2. 用 `mcp__Framelink_Figma_MCP__download_figma_images` 下载所需的图像资源

---

### MasterGo 链接

**工具**：MasterGo MCP

**可用功能**：
- `mcp__mastergo-magic-mcp__mcp__getDsl` - 获取 DSL（领域特定语言）数据，分析设计结构、组件层次、提取设计属性
- `mcp__mastergo-magic-mcp__mcp__getComponentLink` - 获取组件文档数据（当 DSL 数据包含 componentDocumentLinks 时使用）
- `mcp__mastergo-magic-mcp__mcp__getMeta` - 获取网站或页面的元数据信息和规则
- `mcp__mastergo-magic-mcp__mcp__getComponentGenerator` - 获取组件开发工作流程（用于生成代码）

**使用步骤**：
1. 从 MasterGo 链接中解析 fileId 和 layerId
   - URL 格式：`https://{domain}/file/{fileId}/{name}?layer_id={layerId}`
   - 或使用短链接：`https://{domain}/goto/{shortLink}`
2. 使用 `mcp__mastergo-magic-mcp__mcp__getDsl` 获取设计稿的结构、组件和样式数据
3. 如有组件文档链接，使用 `mcp__mastergo-magic-mcp__mcp__getComponentLink` 获取详细文档
4. 如需生成代码，使用 `mcp__mastergo-magic-mcp__mcp__getComponentGenerator`

**分析脚本**：

为提高分析效率和准确性，提供配套分析脚本：

| 脚本 | 路径 | 功能 |
|------|------|------|
| MasterGo DSL 分析器 | `scripts/mastergo-dsl-analyzer.py` | 统计主要区域、提取文字和样式 |

**使用分析脚本**：

```bash
# 1. 先使用 MCP 工具获取 DSL 数据，保存到文件
# mcp__mastergo-magic-mcp__mcp__getDsl 返回的数据

# 2. 使用脚本分析
python scripts/mastergo-dsl-analyzer.py dsl_data.json --format markdown

# 3. 脚本输出
# - 主要区域数量（用于校验零）
# - 所有区域列表（按 y,x 排序）
# - 文字节点列表
# - 颜色/字体规范
```

**脚本参数**：
- `--format json/markdown`：输出格式
- `--output <file>`：输出到文件
- `--url <url>`：设计稿链接（用于 Markdown 输出）
- `--name <name>`：模块名称（用于 Markdown 输出）

**示例**：
```javascript
// 获取 DSL 数据
mcp__mastergo-magic-mcp__mcp__getDsl({ fileId, layerId })
// 或使用短链接
mcp__mastergo-magic-mcp__mcp__getDsl({ shortLink })

// 获取组件文档
mcp__mastergo-magic-mcp__mcp__getComponentLink({ url })

// 获取元数据
mcp__mastergo-magic-mcp__mcp__getMeta({ fileId, layerId })

// 获取组件生成器工作流程
mcp__mastergo-magic-mcp__mcp__getComponentGenerator({ fileId, layerId, rootPath })
```

## 扫描顺序

**按「从上到下、再从左到右」扫描**：
- 先按 y 从大到小（或从 0 起向下）确定所有横向区域顺序
- 再在同一行内按 x 从左到右读取
- 使用 Pencil MCP 工具（`mcp__pencil__snapshot_layout`、`mcp__pencil__batch_get`）时也按此顺序逐层获取布局与节点信息

详见 `analysis-order.md`。

## 本地图片处理（设计稿截图 / UI 图片）

当用户提供本地图片文件（如设计稿截图、UI 界面图片等）时，使用大模型的视觉识别能力进行分析。

### 使用步骤

1. **读取图片**
   - 使用模型自身能力视觉能力识别图片内容

2. **视觉分析（遵守 analysis-order.md 顺序）**

   按「**从上到下、从左到右、从外到里**」的顺序分析图片：

   - **从上到下**：先识别页面顶部区域，逐行向下扫描
   - **从左到右**：同一行内从左到右识别元素
   - **从外到里**：每个区域内先识别外层容器，再深入内部元素

   提取信息包括：
   - 整体布局（页面类型、尺寸比例、结构）
   - 区域划分（按顺序记录各区域位置和内容）
   - 文字内容（按区域记录文字、字号、颜色）
   - 图片与图标（位置、尺寸）
   - 样式规范（主色、背景色、圆角、间距）
   - 交互元素（按钮、输入框等）
   - 层级关系（模块嵌套）

3. **信息结构化**
   - 将识别结果按 analysis-order.md 顺序整理
   - 建立布局 Map（参考 `workflow-layout-map.md`）
   - 整理样式规范

4. **补充确认**
   - 识别结果为估算值（颜色、尺寸），关键数值需与用户确认
   - 多状态截图需分别分析

### 注意事项

- 视觉识别无法获取精确像素值，需标注为「估算值」
- 颜色识别为近似值，需标注为「约 #XXXXXX」
- 遵循 `analysis-order.md` 的「从上到下、从左到右、从外到里」顺序

## 获取内容

使用工具时，需要获取以下内容：

### 布局信息
- 整体尺寸（宽度、高度）
- 区域列表（x, y, w, h）
- 区域间间距

### 节点信息
- 文字内容、字体、字号、字重、颜色、行高
- 图片尺寸、位置、比例、圆角
- 布局参数（padding, gap, margin, align-items, justifyContent）
- 层级关系（嵌套、父子、兄弟）

详见 `workflow-layout-map.md` 和 `workflow-element-extraction.md`。

## 注意事项

1. **多状态设计稿**：如有多个 frame（如「有数据 / 无数据」），分别获取每个状态的布局和节点信息
2. **顶层 frame**：确认顶层 frame，确保获取的是正确的设计稿区域
3. **节点 ID**：记录重要节点的 ID，便于后续获取详细信息
4. **截图对比**：使用截图与实现页面对比时，确保截图区域与实现页面区域一致
5. **本地图片识别**：视觉识别结果存在估算误差，关键数值需与需求方确认

## 相关规则

- `analysis-order.md` - 分析顺序（必守）
- `workflow-layout-map.md` - 第一步：建立布局 Map（使用这些工具）
- `workflow-element-extraction.md` - 第二步：区域与元素提取（使用这些工具）

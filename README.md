# Design Analysis

通用设计稿分析工具集，用于分析设计稿并产出 UI 分析清单文档，供开发实现或验收对照使用。

## 功能特性

- **多格式支持**：支持 `.pen`、Figma、MasterGo 设计稿，以及本地图片
- **标准化输出**：产出结构化的 UI 分析清单，包含九大章节
- **严格校验**：十项校验机制确保分析结果准确无误
- **强制执行**：内置检查清单，防止遗漏和错误

## 项目结构

```
design-analysis/
├── README.md
└── skills/
    └── design-analysis/
        ├── SKILL.md                          # 技能定义文件
        ├── assets/
        │   └── example-ui-checklist.md       # UI 分析清单示例
        ├── references/                       # 参考文档
        │   ├── analysis-order.md             # 分析顺序规则
        │   ├── analysis-priorities.md        # 四类重中之重
        │   ├── enforcement-mechanism.md      # 强制执行机制
        │   ├── workflow-layout-map.md        # 建立布局 Map
        │   ├── workflow-element-extraction.md # 区域与元素提取
        │   ├── workflow-style-summary.md     # 样式规范汇总
        │   ├── workflow-output-checklist.md  # 输出文档要求
        │   ├── workflow-module-verification.md # 区域检查验证
        │   ├── output-analysis-checklist.md  # UI 分析清单模板
        │   ├── implementation-guidelines.md  # 实现建议
        │   ├── implementation-common-errors.md # 常见错误模式
        │   ├── checklist-common-misses.md    # 常见遗漏检查点
        │   └── tools-design-guidelines.md    # 工具使用指南
        └── scripts/
            ├── mastergo-dsl-analyzer.py      # MasterGo DSL 分析脚本
            └── detailed_region_analysis.py   # 区域详细分析脚本
```

## 使用方法

### 作为 Claude Code Skill 使用

在 Claude Code 中，当需要分析设计稿时，系统会自动调用此技能：

```
请分析这个 Figma 设计稿：https://www.figma.com/file/xxxxx
```

### 分析流程

1. **建立布局 Map** - 获取设计稿结构、页面状态、整体尺寸、区域划分
2. **区域与元素提取** - 对每个区域按「从外到里」逐项提取
3. **样式规范汇总** - 汇总颜色、字体、圆角、间距、阴影等
4. **输出 UI 分析清单** - 按标准模板输出文档
5. **区域检查与对比完善** - 验证分析结果准确性

### 核心原则

**分析顺序**：从上到下 → 从左到右 → 从外到里

**四类重中之重**（不允许出错或遗漏）：
- **文字**：所有可见文案、字体、字号、颜色等
- **图片**：所有图片、占位图、图标区域等
- **布局**：位置、尺寸、间距、对齐、排列方向
- **层级**：嵌套关系、先后顺序、叠放关系

## 输出产物

| 产出物 | 路径 | 用途 |
|--------|------|------|
| UI 分析清单 | `openspec/ui-checklist/{序号}-{模块名}.md` | 开发实现、验收对照 |

### 文档结构

UI 分析清单包含九大章节：

1. 文档说明
2. 设计稿整体分析
3. 区域详细分析
4. 样式规范汇总
5. 交互状态分析
6. 占位元素说明
7. 常见遗漏检查点
8. 实现建议
9. 验证检查清单

## 校验机制

分析完成后必须执行十项校验：

| 校验项 | 说明 |
|--------|------|
| 校验零 | 区域数量校验 |
| 校验一 | 区域顺序校验 |
| 校验二 | 区域详细分析顺序校验 |
| 校验三 | 标题文字一致性校验 |
| 校验四 | 模块存在性验证 |
| 校验五 | 区域列表一致性校验 |
| 校验六 | 表格列标题专项校验 |
| 校验七 | 子元素一致性校验 |
| 校验八 | 子元素排序校验 |
| 校验九 | 子元素归属校验 |
| 校验十 | 层级结构校验 |

## 工具脚本

### MasterGo DSL 分析器

用于解析 MasterGo 设计稿 DSL 数据：

```bash
python scripts/mastergo-dsl-analyzer.py <dsl_json_file> [options]

参数：
  --output, -o    输出文件路径
  --format, -f    输出格式：json / markdown
  --url           设计稿链接（用于 Markdown 输出）
  --name          模块名称（用于 Markdown 输出）
  --titles        提取卡片标题
```

## 支持的设计稿类型

| 类型 | 工具 | 说明 |
|------|------|------|
| `.pen` 文件 | Pencil MCP | Pencil 设计文件 |
| Figma | Figma MCP | Figma 设计链接 |
| MasterGo | MasterGo MCP | MasterGo 设计链接 |
| 本地图片 | 视觉识别 | 设计稿截图、UI 图片 |

## 版本信息

- 当前版本：1.5.0
- 更新日期：2026-03

## 许可证

MIT License
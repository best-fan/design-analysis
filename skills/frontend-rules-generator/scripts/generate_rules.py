#!/usr/bin/env python3
"""
前端 Rules 生成器脚本
分析前端项目结构，生成 .claude/rules/ 目录下的开发规范文件
"""

import os
import json
import argparse
from pathlib import Path
from typing import Optional


def detect_project_type(src_dir: Path) -> str:
    """检测项目类型（Vue/React/其他）"""
    # 检查 package.json
    package_json = src_dir.parent / "package.json"
    if package_json.exists():
        with open(package_json, "r", encoding="utf-8") as f:
            pkg = json.load(f)
            deps = pkg.get("dependencies", {})
            if "vue" in deps or "@vue/runtime-core" in deps:
                return "vue"
            if "react" in deps or "react-dom" in deps:
                return "react"

    # 检查文件扩展名
    vue_files = list(src_dir.glob("**/*.vue"))
    jsx_files = list(src_dir.glob("**/*.jsx")) + list(src_dir.glob("**/*.tsx"))

    if vue_files:
        return "vue"
    if jsx_files:
        return "react"

    return "unknown"


def scan_modules(src_dir: Path, project_type: str) -> dict:
    """扫描项目模块"""
    modules = {}

    # 标准前端模块
    standard_modules = {
        "components": "组件",
        "services": "API服务",
        "api": "API服务",
        "store": "状态管理",
        "utils": "工具函数",
        "types": "类型定义",
        "hooks": "Hooks",
        "composables": "组合式函数",
        "router": "路由",
        "pages": "页面",
        "views": "页面",
        "styles": "样式",
        "layouts": "布局",
        "config": "配置",
    }

    for module_name, module_desc in standard_modules.items():
        module_path = src_dir / module_name
        if module_path.exists() and module_path.is_dir():
            modules[module_name] = {
                "path": str(module_path),
                "description": module_desc,
                "files": list(module_path.glob("**/*.*"))
            }

    return modules


def extract_naming_patterns(files: list) -> dict:
    """从文件列表提取命名模式"""
    patterns = {
        "file_naming": [],  # 文件命名风格
        "has_index": False,  # 是否有 index.ts 导出
        "has_subdirs": False,  # 是否使用子目录
        "style_separate": False,  # 是否分离样式文件
    }

    for file in files:
        name = file.name
        if name == "index.ts" or name == "index.js":
            patterns["has_index"] = True
        if name.endswith(".scss") or name.endswith(".css"):
            patterns["style_separate"] = True
        if file.parent != file.parents[1]:
            patterns["has_subdirs"] = True

        # 文件命名风格
        if name[0].isupper():
            patterns["file_naming"].append("PascalCase")
        elif "-" in name:
            patterns["file_naming"].append("kebab-case")
        else:
            patterns["file_naming"].append("camelCase")

    # 统计最常见的命名风格
    if patterns["file_naming"]:
        from collections import Counter
        counter = Counter(patterns["file_naming"])
        patterns["file_naming"] = counter.most_common(1)[0][0]
    else:
        patterns["file_naming"] = "camelCase"

    return patterns


def generate_rule_content(module_name: str, module_info: dict, project_type: str) -> str:
    """生成 rules 文件内容"""

    module_desc = module_info["description"]
    patterns = extract_naming_patterns(module_info["files"])

    # 根据模块类型选择路径模式
    path_patterns = get_path_patterns(module_name, project_type)

    content = f"""---
paths:
{path_patterns}
---
# {module_desc}开发规范

## 开发前检查流程

**在编写新{module_desc}前，必须按以下顺序检查：**

### 1. 检查全局是否已存在类似{module_desc}

**必须先搜索 `src/{module_name}/` 目录**，确认没有可复用的{module_desc}：

```bash
# 搜索现有{module_desc}
ls src/{module_name}/
grep -r "关键词" src/{module_name}/
```

### 2. 判断{module_desc}归属

| 条件 | 归属目录 | 示例 |
|------|----------|------|
| 多个模块共用 | `src/{module_name}/` | ... |
| 单个页面独用 | 页面内定义 | ... |

### 3. 评估是否应添加到全局

**满足以下条件之一，应添加到全局{module_name}**：

- ✅ 多个模块需要使用
- ✅ 通用功能
- ✅ 可能有其他模块未来需要

**不应添加到全局的情况**：

- ❌ 仅单个页面使用
- ❌ 强依赖特定业务逻辑

### 4. 扩展现有{module_desc}

如果全局存在类似{module_desc}，优先扩展现有{module_desc}：

```typescript
// ✅ 扩展
export const existing = ...

// 新增
export const newContent = ...

// ❌ 新建重复
```

## 文件组织

### 文件命名
- 格式：{patterns["file_naming"]}
- 示例：根据实际项目填写

### 目录结构
"""
    if patterns["has_index"]:
        content += "- 有统一导出 `index.ts`\n"
    if patterns["has_subdirs"]:
        content += "- 使用子目录组织\n"
    if patterns["style_separate"]:
        content += "- 样式文件分离\n"

    content += """
## 禁止事项

1. ❌ 禁止重复创建
2. ❌ 禁止命名不规范
"""

    return content


def get_path_patterns(module_name: str, project_type: str) -> str:
    """获取模块的路径匹配模式"""

    patterns_map = {
        "components": '''  - "src/components/**/*"''',
        "services": '''  - "src/services/*.ts"''',
        "api": '''  - "src/api/*.ts"''',
        "store": '''  - "src/store/**/*.ts"''',
        "utils": '''  - "src/utils/*.ts"''',
        "types": '''  - "src/types/**/*.ts"''',
        "hooks": '''  - "src/hooks/**/*.ts"''',
        "composables": '''  - "src/composables/**/*.ts"\n  - "src/pages/**/composables/*.ts"''',
        "router": '''  - "src/router/*.ts"''',
        "pages": '''  - "src/pages/**/*"''',
        "views": '''  - "src/views/**/*"''',
        "styles": '''  - 'src/**/*.scss'\n  - 'src/**/*.vue'''',
        "layouts": '''  - "src/layouts/**/*"''',
        "config": '''  - "src/config/*.ts"''',
    }

    return patterns_map.get(module_name, f'''  - "src/{module_name}/**/*"''')


def generate_rules(src_dir: Path, output_dir: Path, project_type: str = None) -> list:
    """生成 rules 文件"""

    if project_type is None:
        project_type = detect_project_type(src_dir)

    modules = scan_modules(src_dir, project_type)
    generated_files = []

    # 确保 output_dir 存在
    output_dir.mkdir(parents=True, exist_ok=True)

    for module_name, module_info in modules.items():
        content = generate_rule_content(module_name, module_info, project_type)

        # 确定 rules 文件名
        rule_filename = f"{module_name}.md"
        if module_name == "components":
            rule_filename = f"{project_type}-component.md"
        elif module_name in ["services", "api"]:
            rule_filename = "services.md"

        rule_path = output_dir / rule_filename

        with open(rule_path, "w", encoding="utf-8") as f:
            f.write(content)

        generated_files.append(str(rule_path))

    # 生成通用代码质量规范
    code_quality_content = '''---
paths:
  - "src/**/*.ts"
  - "src/**/*.vue"
---
# 代码质量规范

## 命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| 组件 | PascalCase | `UserCard.vue` |
| 函数 | camelCase | `getUserInfo` |
| 常量 | SCREAMING_SNAKE_CASE | `MAX_COUNT` |
| 类型/接口 | PascalCase | `UserInfo` |

## 禁止事项

1. ❌ 禁止 `any` 类型
2. ❌ 禁止未使用的变量/函数/导入
'''

    code_quality_path = output_dir / "code-quality.md"
    with open(code_quality_path, "w", encoding="utf-8") as f:
        f.write(code_quality_content)
    generated_files.append(str(code_quality_path))

    return generated_files


def main():
    parser = argparse.ArgumentParser(description="生成前端项目 rules 文件")
    parser.add_argument("src_dir", help="源码目录路径（如 src/）")
    parser.add_argument("--output", "-o", default=".claude/rules", help="输出目录")
    parser.add_argument("--type", "-t", choices=["vue", "react"], help="项目类型")

    args = parser.parse_args()

    src_dir = Path(args.src_dir)
    output_dir = Path(args.output)

    if not src_dir.exists():
        print(f"错误：源码目录不存在 - {src_dir}")
        return

    generated = generate_rules(src_dir, output_dir, args.type)

    print(f"成功生成 {len(generated)} 个 rules 文件：")
    for f in generated:
        print(f"  - {f}")


if __name__ == "__main__":
    main()
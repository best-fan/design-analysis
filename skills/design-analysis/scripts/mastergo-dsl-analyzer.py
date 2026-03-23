#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MasterGo DSL 分析脚本
用于解析 MasterGo 设计稿 DSL 数据，提取区域和文字信息

使用方法：
    python mastergo-dsl-analyzer.py <dsl_json_file> [options]

参数：
    dsl_json_file: MCP 工具返回的 DSL JSON 文件路径
    --output: 输出文件路径（默认输出到控制台）
    --format: 输出格式，支持 json/markdown（默认 json）

功能：
    1. 统计设计稿顶层区域数量（用于校验零）
    2. 提取所有区域信息（按 y,x 排序）
    3. 提取所有文字节点
    4. 提取样式规范（颜色、字体）
"""

import json
import argparse
from datetime import datetime
from typing import Any, Optional
from collections import OrderedDict


def load_dsl_data(file_path: str) -> dict:
    """加载 DSL JSON 数据"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 解析外层 JSON
    data = json.loads(content)

    # MCP 工具返回格式: [{"type": "text", "text": "..."}]
    if isinstance(data, list) and len(data) > 0:
        if data[0].get('type') == 'text':
            text_content = data[0].get('text', '')
            return json.loads(text_content)

    return data


def extract_styles(dsl_data: dict) -> dict:
    """提取样式定义"""
    styles = {}
    if 'dsl' in dsl_data and 'styles' in dsl_data['dsl']:
        for style_id, style_value in dsl_data['dsl']['styles'].items():
            styles[style_id] = style_value.get('value', [])
    return styles


def extract_root_node(dsl_data: dict) -> dict:
    """提取根节点"""
    if 'dsl' in dsl_data and 'nodes' in dsl_data['dsl']:
        nodes = dsl_data['dsl']['nodes']
        if isinstance(nodes, list) and len(nodes) > 0:
            return nodes[0]
    return {}


def get_style_value(styles: dict, style_ref: str) -> Any:
    """通过样式引用获取样式值"""
    if style_ref in styles:
        return styles[style_ref]
    return None


def parse_color_from_style(style_value: Any) -> str:
    """从样式值解析颜色"""
    if isinstance(style_value, list):
        for item in style_value:
            if isinstance(item, str):
                if item.startswith('#') or item.startswith('rgb') or item.startswith('linear'):
                    return item
    return ''


def parse_node(node: dict, styles: dict, depth: int = 0, parent_x: float = 0, parent_y: float = 0) -> dict:
    """递归解析节点"""
    result = {
        'id': node.get('id', ''),
        'name': node.get('name', ''),
        'type': node.get('type', ''),
        'depth': depth,
        'children': [],
        'layout': {},
        'text': None,
        'fills': [],
    }

    # 解析布局样式
    layout_style = node.get('layoutStyle', {})
    if layout_style:
        # 相对坐标（处理 None 值）
        rel_x = layout_style.get('relativeX') or 0
        rel_y = layout_style.get('relativeY') or 0
        width = layout_style.get('width') or 0
        height = layout_style.get('height') or 0

        # 绝对坐标
        abs_x = parent_x + rel_x
        abs_y = parent_y + rel_y

        result['layout'] = {
            'x': abs_x,
            'y': abs_y,
            'relativeX': rel_x,
            'relativeY': rel_y,
            'width': width,
            'height': height,
        }

        # 更新父坐标用于子节点
        parent_x = abs_x
        parent_y = abs_y

    # 解析填充
    if 'fill' in node:
        fill = node['fill']
        if isinstance(fill, list):
            for f in fill:
                if 'paint' in f:
                    color = parse_color_from_style(get_style_value(styles, f['paint']))
                    if color:
                        result['fills'].append(color)

    # 解析文字内容
    if node.get('type') == 'TEXT':
        text_field = node.get('text', [])
        text_content = ''
        font_info = {}

        if text_field and len(text_field) > 0:
            text_content = text_field[0].get('text', '')
            font_ref = text_field[0].get('font', '')

            if font_ref and font_ref in styles:
                font_style = styles[font_ref]
                if isinstance(font_style, dict):
                    font_info['font_family'] = font_style.get('family', 'Source Han Sans')
                    font_info['font_size'] = font_style.get('size', 14)
                    font_info['line_height'] = font_style.get('lineHeight', '22')

        result['text'] = {
            'content': text_content,
            **font_info
        }

    # 递归解析子节点
    if 'children' in node:
        for child in node['children']:
            child_result = parse_node(child, styles, depth + 1, parent_x, parent_y)
            result['children'].append(child_result)

    return result


def get_main_regions(root: dict) -> list:
    """
    获取主要区域（根节点的直接子节点）
    用于"校验零：区域数量校验"
    """
    main_regions = []

    if 'children' in root:
        for child in root['children']:
            layout = child.get('layout', {})
            node_type = child.get('type', '')
            width = layout.get('width', 0) or 0
            height = layout.get('height', 0) or 0

            # 过滤条件：有实际尺寸的 FRAME/GROUP/INSTANCE
            # 注意：不过滤接近页面宽度的区域，避免遗漏底部表格
            if node_type in ['FRAME', 'GROUP', 'INSTANCE'] and width >= 100 and height >= 50:
                main_regions.append({
                    'id': child.get('id', ''),
                    'name': child.get('name', ''),
                    'type': node_type,
                    'x': layout.get('relativeX', 0) or 0,
                    'y': layout.get('relativeY', 0) or 0,
                    'width': width,
                    'height': height,
                })

    # 按 y 坐标排序，y 相同时按 x 排序
    main_regions.sort(key=lambda r: (r['y'], r['x']))

    return main_regions


def get_all_regions(node: dict, regions: list, min_width: int = 100, min_height: int = 50, exclude_root: bool = True):
    """
    获取所有区域节点（递归）
    用于详细分析
    """
    layout = node.get('layout', {})
    width = layout.get('width', 0) or 0
    height = layout.get('height', 0) or 0
    node_type = node.get('type', '')
    depth = node.get('depth', 0)

    # 判断是否为有效区域
    # 排除根节点（depth=0）
    if not exclude_root or depth > 0:
        if node_type in ['FRAME', 'GROUP', 'INSTANCE'] and width >= min_width and height >= min_height:
            regions.append(node)

    # 递归处理子节点
    for child in node.get('children', []):
        get_all_regions(child, regions, min_width, min_height, exclude_root)


def get_text_nodes(node: dict, texts: list):
    """收集所有文字节点"""
    if node.get('text') and node['text'].get('content'):
        texts.append(node)

    for child in node.get('children', []):
        get_text_nodes(child, texts)


def analyze_dsl(dsl_data: dict) -> dict:
    """分析 DSL 数据"""
    styles = extract_styles(dsl_data)
    root_node = extract_root_node(dsl_data)

    # 解析根节点
    root = parse_node(root_node, styles)

    # 获取页面尺寸
    root_layout = root.get('layout', {})
    page_width = root_layout.get('width', 1920)
    page_height = root_layout.get('height', 900)

    # 获取主要区域（根节点直接子节点）- 用于校验零
    main_regions = get_main_regions(root)

    # 获取所有区域（递归）
    all_regions = []
    get_all_regions(root, all_regions)
    all_regions.sort(key=lambda r: (r['layout'].get('y', 0), r['layout'].get('x', 0)))

    # 获取文字节点
    texts = []
    get_text_nodes(root, texts)
    texts.sort(key=lambda t: (t['layout'].get('y', 0), t['layout'].get('x', 0)))

    # 提取颜色规范
    color_map = OrderedDict()
    for style_id, style_value in styles.items():
        if style_id.startswith('paint_'):
            color = parse_color_from_style(style_value)
            if color and color.startswith('#'):
                color_map[color] = style_id

    # 提取字体规范
    font_map = OrderedDict()
    for style_id, style_value in styles.items():
        if style_id.startswith('font_') and isinstance(style_value, dict):
            size = style_value.get('size', 14)
            if size not in font_map:
                font_map[size] = style_value

    return {
        'page': {
            'width': page_width,
            'height': page_height,
        },
        'main_regions': main_regions,  # 用于校验零
        'all_regions': all_regions,
        'texts': texts,
        'colors': list(color_map.keys()),
        'fonts': font_map,
        'root': root,
    }


def output_json(analysis: dict) -> str:
    """输出 JSON 格式"""
    # 简化输出，只保留关键信息
    output = {
        'page': analysis['page'],
        'verification': {
            'main_region_count': len(analysis['main_regions']),
            'main_regions': [
                {
                    'name': r['name'],
                    'y': r['y'],
                    'size': f"{r['width']}x{r['height']}"
                }
                for r in analysis['main_regions']
            ]
        },
        'regions_count': len(analysis['all_regions']),
        'texts_count': len(analysis['texts']),
        'colors': analysis['colors'][:20],
        'fonts': [
            {
                'size': size,
                'family': info.get('family', 'Source Han Sans')
            }
            for size, info in sorted(analysis['fonts'].items())
        ]
    }
    return json.dumps(output, ensure_ascii=False, indent=2)


def extract_card_titles(dsl_data: dict, output_file: str = None) -> list:
    """
    提取所有卡片标题（用于校验三：标题文字一致性校验）
    强制使用文件输出，避免控制台编码问题

    参数:
        dsl_data: DSL 数据
        output_file: 输出文件路径，默认为 openspec/output/card_titles.json

    返回:
        标题列表
    """
    if output_file is None:
        output_file = 'openspec/output/card_titles.json'

    styles = extract_styles(dsl_data)
    root_node = extract_root_node(dsl_data)
    root = parse_node(root_node, styles)

    titles = []

    for child in root.get('children', []):
        layout = child.get('layout', {})
        y = layout.get('y', 0)
        x = layout.get('x', 0)
        w = layout.get('width', 0)
        node_name = child.get('name', '')

        # 过滤主要区域（有实际尺寸的）
        if w >= 500 and y in [0, 112, 552, 992]:
            def find_first_text(node):
                """找到第一个文字节点"""
                if node.get('text') and node['text'].get('content'):
                    return node['text']['content']
                for c in node.get('children', []):
                    result = find_first_text(c)
                    if result:
                        return result
                return None

            title = find_first_text(child)
            titles.append({
                'y': y,
                'x': x,
                'region_name': node_name,
                'card_title': title
            })

    # 保存到文件（强制）
    output_path = output_file
    import os
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(titles, f, ensure_ascii=False, indent=2)

    return titles


def output_markdown(analysis: dict, design_url: str = '', module_name: str = '设计稿') -> str:
    """输出 Markdown 格式的校验报告"""
    lines = []

    lines.append(f"# {module_name} - 设计稿分析报告")
    lines.append("")
    lines.append(f"> 分析时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"> 设计稿链接：{design_url}")
    lines.append("")
    lines.append("---")
    lines.append("")

    # 校验零：区域数量校验
    lines.append("## 校验零：区域数量校验")
    lines.append("")
    lines.append(f"- **页面尺寸**：{analysis['page']['width']} x {analysis['page']['height']} px")
    lines.append(f"- **主要区域数量**：{len(analysis['main_regions'])} 个")
    lines.append("")
    lines.append("### 主要区域列表（根节点直接子节点，按 y,x 排序）")
    lines.append("")
    lines.append("| 序号 | 区域名称 | y 坐标 | 尺寸 | 类型 |")
    lines.append("|------|----------|--------|------|------|")

    for i, r in enumerate(analysis['main_regions']):
        lines.append(f"| {i+1} | {r['name']} | {r['y']} | {r['width']}x{r['height']} | {r['type']} |")

    lines.append("")
    lines.append("### 校验提示")
    lines.append("")
    lines.append("```")
    lines.append(f"设计稿主要区域数：{len(analysis['main_regions'])} 个")
    lines.append("文档区域列表行数：___ 行")
    lines.append("是否一致：___")
    lines.append("```")
    lines.append("")

    # 区域详情
    lines.append("---")
    lines.append("")
    lines.append("## 区域详情")
    lines.append("")
    lines.append(f"- 总区域数：{len(analysis['all_regions'])} 个")
    lines.append(f"- 文字节点数：{len(analysis['texts'])} 个")
    lines.append("")

    # 颜色规范
    lines.append("---")
    lines.append("")
    lines.append("## 颜色规范")
    lines.append("")
    lines.append("| 用途 | 颜色值 |")
    lines.append("|------|--------|")
    for color in analysis['colors'][:15]:
        lines.append(f"| 颜色 | `{color}` |")

    lines.append("")

    # 字体规范
    lines.append("---")
    lines.append("")
    lines.append("## 字体规范")
    lines.append("")
    lines.append("| 字号 | 字体族 |")
    lines.append("|------|--------|")
    for size, info in sorted(analysis['fonts'].items()):
        lines.append(f"| {size}px | {info.get('family', 'Source Han Sans')} |")

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='MasterGo DSL 分析脚本')
    parser.add_argument('dsl_file', help='DSL JSON 文件路径')
    parser.add_argument('--output', '-o', help='输出文件路径')
    parser.add_argument('--format', '-f', choices=['json', 'markdown'], default='json', help='输出格式')
    parser.add_argument('--url', help='设计稿链接（用于 Markdown 输出）')
    parser.add_argument('--name', help='模块名称（用于 Markdown 输出）')
    parser.add_argument('--titles', action='store_true', help='提取卡片标题（用于校验三）')

    args = parser.parse_args()

    try:
        dsl_data = load_dsl_data(args.dsl_file)

        # 标题提取模式（用于校验三）
        if args.titles:
            titles = extract_card_titles(dsl_data, args.output)
            print(f"卡片标题已保存到: {args.output or 'openspec/output/card_titles.json'}")
            print(f"共提取 {len(titles)} 个标题")
            return 0

        analysis = analyze_dsl(dsl_data)

        if args.format == 'markdown':
            result = output_markdown(analysis, args.url or '', args.name or '设计稿')
        else:
            result = output_json(analysis)

        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(result)
            print(f"输出已保存到：{args.output}")
        else:
            print(result)

        # 控制台输出关键统计
        print("\n" + "="*50, file=__import__('sys').stderr)
        print("【校验零统计】", file=__import__('sys').stderr)
        print(f"  主要区域数量：{len(analysis['main_regions'])} 个", file=__import__('sys').stderr)
        print(f"  页面尺寸：{analysis['page']['width']} x {analysis['page']['height']} px", file=__import__('sys').stderr)
        print("="*50, file=__import__('sys').stderr)

    except Exception as e:
        print(f"错误：{e}", file=__import__('sys').stderr)
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == '__main__':
    exit(main())
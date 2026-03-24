#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
详细区域分析脚本
用于深入分析每个区域的子元素、图表类型等
"""

import json
import sys
from collections import OrderedDict


def load_dsl_data(file_path: str) -> dict:
    """加载 DSL JSON 数据"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    data = json.loads(content)
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


def get_style_value(styles: dict, style_ref: str):
    """通过样式引用获取样式值"""
    if style_ref in styles:
        return styles[style_ref]
    return None


def parse_color_from_style(style_value) -> str:
    """从样式值解析颜色"""
    if isinstance(style_value, list):
        for item in style_value:
            if isinstance(item, str):
                if item.startswith('#') or item.startswith('rgb') or item.startswith('linear'):
                    return item
    return ''


def parse_node_full(node: dict, styles: dict, depth: int = 0, parent_x: float = 0, parent_y: float = 0) -> dict:
    """递归解析节点（完整版）"""
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
        rel_x = layout_style.get('relativeX') or 0
        rel_y = layout_style.get('relativeY') or 0
        width = layout_style.get('width') or 0
        height = layout_style.get('height') or 0

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
            child_result = parse_node_full(child, styles, depth + 1, parent_x, parent_y)
            result['children'].append(child_result)

    return result


def find_all_texts(node: dict, texts: list, max_depth: int = 10):
    """收集所有文字节点"""
    if node.get('text') and node['text'].get('content'):
        texts.append({
            'content': node['text']['content'],
            'font_size': node['text'].get('font_size', 14),
            'font_family': node['text'].get('font_family', 'Source Han Sans'),
            'x': node['layout'].get('x', 0),
            'y': node['layout'].get('y', 0),
            'node_name': node.get('name', ''),
            'node_id': node.get('id', ''),
        })

    if node.get('depth', 0) < max_depth:
        for child in node.get('children', []):
            find_all_texts(child, texts, max_depth)


def find_chart_nodes(node: dict, charts: list, max_depth: int = 10):
    """识别图表节点（通过节点名称判断）"""
    name = node.get('name', '').lower()
    name_original = node.get('name', '')  # 保留原始名称用于精确匹配
    node_type = node.get('type', '')
    layout = node.get('layout', {})

    # 图表类型关键词（优先级从高到低）
    # 注意：Stacked area chart 需要精确匹配，避免被 line 关键词错误匹配
    chart_keywords_priority = [
        ('stacked area', '堆叠面积图'),
        ('stacked bar', '堆叠柱状图'),
        ('堆叠面积', '堆叠面积图'),
        ('堆叠柱状', '堆叠柱状图'),
        ('堆叠', '堆叠图'),
        ('分组柱状', '分组柱状图'),
        ('环形图', '环形图'),
        ('饼图', '饼图'),
        ('雷达图', '雷达图'),
        ('仪表盘', '仪表盘'),
        ('面积图', '面积图'),
        ('柱状图', '柱状图'),
        ('折线图', '折线图'),
        ('散点图', '散点图'),
        ('直方图', '直方图'),
        ('bar', '柱状图'),
        ('line', '折线图'),
        ('pie', '饼图'),
        ('area', '面积图'),
        ('scatter', '散点图'),
        ('radar', '雷达图'),
        ('gauge', '仪表盘'),
        ('chart', '图表'),
        ('graph', '图表'),
        ('折线', '折线图'),
        ('柱状', '柱状图'),
    ]

    # 检查节点名称中是否包含图表关键词（按优先级匹配）
    chart_type = None
    for keyword, chart_name in chart_keywords_priority:
        if keyword in name:
            chart_type = chart_name
            break

    # 如果是图表类型节点或尺寸较大可能是图表容器
    width = layout.get('width', 0)
    height = layout.get('height', 0)

    if chart_type or (width > 200 and height > 100 and node_type in ['FRAME', 'GROUP']):
        charts.append({
            'node_id': node.get('id', ''),
            'node_name': node.get('name', ''),
            'node_type': node_type,
            'chart_type': chart_type or '未知图表',
            'x': layout.get('x', 0),
            'y': layout.get('y', 0),
            'width': width,
            'height': height,
        })

    if node.get('depth', 0) < max_depth:
        for child in node.get('children', []):
            find_chart_nodes(child, charts, max_depth)


def find_common_components(node: dict, components: dict, max_depth: int = 6, depth: int = 0):
    """
    搜索常见组件：Tab 切换、图例、分页等
    这是为了防止遗漏嵌套在深层节点中的组件

    参数:
        node: 当前节点
        components: 组件收集字典 {'tabs': [], 'legends': [], 'pagination': [], 'filters': []}
        max_depth: 最大遍历深度
        depth: 当前深度
    """
    if depth > max_depth:
        return

    name = node.get('name', '').lower()
    name_original = node.get('name', '')
    node_type = node.get('type', '')
    layout = node.get('layoutStyle', {})

    # Tab 切换检测
    tab_keywords = ['tab', '页签', '标签页', '切换']
    for kw in tab_keywords:
        if kw in name or kw in name_original:
            # 尝试提取 Tab 文字
            tab_texts = []
            if 'children' in node:
                for child in node.get('children', []):
                    if child.get('type') == 'TEXT':
                        text_arr = child.get('text', [])
                        if text_arr and isinstance(text_arr, list) and len(text_arr) > 0:
                            tab_texts.append(text_arr[0].get('text', ''))

            components['tabs'].append({
                'node_id': node.get('id', ''),
                'node_name': node.get('name', ''),
                'node_type': node_type,
                'x': layout.get('relativeX', 0),
                'y': layout.get('relativeY', 0),
                'tab_texts': tab_texts,
            })
            break

    # 图例检测
    legend_keywords = ['图例', 'legend', '图例项']
    for kw in legend_keywords:
        if kw in name or kw in name_original:
            # 尝试提取图例项
            legend_items = []
            if 'children' in node:
                for child in node.get('children', []):
                    if child.get('type') == 'TEXT':
                        text_arr = child.get('text', [])
                        if text_arr and isinstance(text_arr, list) and len(text_arr) > 0:
                            legend_items.append(text_arr[0].get('text', ''))
                    elif child.get('type') == 'FRAME':
                        # 可能是图例项容器
                        for item in child.get('children', []):
                            if item.get('type') == 'TEXT':
                                text_arr = item.get('text', [])
                                if text_arr and isinstance(text_arr, list) and len(text_arr) > 0:
                                    legend_items.append(text_arr[0].get('text', ''))

            components['legends'].append({
                'node_id': node.get('id', ''),
                'node_name': node.get('name', ''),
                'node_type': node_type,
                'x': layout.get('relativeX', 0),
                'y': layout.get('relativeY', 0),
                'legend_items': legend_items,
            })
            break

    # 分页检测
    pagination_keywords = ['分页', 'pagination', '上一页', '下一页', '条/页']
    for kw in pagination_keywords:
        if kw in name or kw in name_original:
            components['pagination'].append({
                'node_id': node.get('id', ''),
                'node_name': node.get('name', ''),
                'node_type': node_type,
                'x': layout.get('relativeX', 0),
                'y': layout.get('relativeY', 0),
            })
            break

    # 筛选条件检测
    filter_keywords = ['筛选', 'filter', '搜索', 'search', '选择器', 'selector']
    for kw in filter_keywords:
        if kw in name or kw in name_original:
            components['filters'].append({
                'node_id': node.get('id', ''),
                'node_name': node.get('name', ''),
                'node_type': node_type,
                'x': layout.get('relativeX', 0),
                'y': layout.get('relativeY', 0),
            })
            break

    # 递归遍历子节点
    for child in node.get('children', []):
        find_common_components(child, components, max_depth, depth + 1)


def analyze_region(region_node: dict, styles: dict) -> dict:
    """分析单个区域的详细信息"""
    result = {
        'id': region_node.get('id', ''),
        'name': region_node.get('name', ''),
        'type': region_node.get('type', ''),
        'layout': region_node.get('layout', {}),
        'texts': [],
        'charts': [],
        'children_summary': [],
        'common_components': {
            'tabs': [],
            'legends': [],
            'pagination': [],
            'filters': [],
        },
    }

    # 收集文字节点
    find_all_texts(region_node, result['texts'], max_depth=6)

    # 收集图表节点
    find_chart_nodes(region_node, result['charts'], max_depth=6)

    # 收集常见组件（Tab、图例、分页、筛选条件）
    find_common_components(region_node, result['common_components'], max_depth=6)

    # 收集直接子节点摘要
    for child in region_node.get('children', []):
        child_layout = child.get('layout', {})
        result['children_summary'].append({
            'id': child.get('id', ''),
            'name': child.get('name', ''),
            'type': child.get('type', ''),
            'x': child_layout.get('relativeX', 0),
            'y': child_layout.get('relativeY', 0),
            'width': child_layout.get('width', 0),
            'height': child_layout.get('height', 0),
        })

    return result


def main():
    if len(sys.argv) < 2:
        print("用法: python detailed_region_analysis.py <dsl_json_file> [region_index]")
        sys.exit(1)

    dsl_file = sys.argv[1]
    region_index = int(sys.argv[2]) if len(sys.argv) > 2 else None

    dsl_data = load_dsl_data(dsl_file)
    styles = extract_styles(dsl_data)
    root_node = extract_root_node(dsl_data)
    root = parse_node_full(root_node, styles)

    # 获取主要区域
    main_regions = []
    for child in root.get('children', []):
        layout = child.get('layout', {})
        node_type = child.get('type', '')
        width = layout.get('width', 0) or 0
        height = layout.get('height', 0) or 0

        if node_type in ['FRAME', 'GROUP', 'INSTANCE'] and width >= 100 and height >= 50:
            main_regions.append(child)

    # 按 y,x 排序
    main_regions.sort(key=lambda r: (r['layout'].get('y', 0), r['layout'].get('x', 0)))

    output = {
        'page_size': {
            'width': root['layout'].get('width', 1920),
            'height': root['layout'].get('height', 1080),
        },
        'regions': []
    }

    for i, region in enumerate(main_regions):
        if region_index is not None and i != region_index:
            continue

        analysis = analyze_region(region, styles)
        output['regions'].append(analysis)

    # 输出到文件
    output_file = 'openspec/output/region_details.json'
    import os
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"详细分析已保存到: {output_file}")

    # 打印摘要
    for region in output['regions']:
        print(f"\n{'='*60}")
        print(f"区域: {region['name']}")
        print(f"ID: {region['id']}")
        print(f"布局: x={region['layout'].get('x', 0)}, y={region['layout'].get('y', 0)}, w={region['layout'].get('width', 0)}, h={region['layout'].get('height', 0)}")
        print(f"文字数量: {len(region['texts'])}")
        print(f"图表数量: {len(region['charts'])}")
        if region['charts']:
            for chart in region['charts']:
                print(f"  - 图表: {chart['node_name']} ({chart['chart_type']})")
        print(f"直接子节点数量: {len(region['children_summary'])}")

        # 打印常见组件
        cc = region.get('common_components', {})
        if cc.get('tabs'):
            print(f"Tab 切换: {len(cc['tabs'])} 个")
            for tab in cc['tabs']:
                print(f"  - {tab['node_name']}: {tab.get('tab_texts', [])}")
        if cc.get('legends'):
            print(f"图例: {len(cc['legends'])} 个")
            for legend in cc['legends']:
                print(f"  - {legend['node_name']}: {legend.get('legend_items', [])}")
        if cc.get('pagination'):
            print(f"分页: {len(cc['pagination'])} 个")
        if cc.get('filters'):
            print(f"筛选条件: {len(cc['filters'])} 个")


if __name__ == '__main__':
    main()
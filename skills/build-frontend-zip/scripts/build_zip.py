#!/usr/bin/env python3
"""
前端项目打包脚本
- 运行 pnpm build 构建
- 将 dist 目录打包为 zip 格式
- 输出 git 分支、耗时等信息
"""

import subprocess
import sys
import os
import zipfile
import time
from datetime import datetime
from pathlib import Path


def get_git_branch(project_path: str) -> str:
    """获取当前 git 分支"""
    result = subprocess.run(
        ["git", "branch", "--show-current"],
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='replace',
        cwd=project_path
    )
    if result.returncode == 0:
        return result.stdout.strip() or "unknown"
    return "unknown"


def get_git_commit_info(project_path: str) -> str:
    """获取当前 commit 的第一行信息"""
    result = subprocess.run(
        ["git", "log", "-1", "--pretty=format:%s"],
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='replace',
        cwd=project_path
    )
    if result.returncode == 0:
        return result.stdout.strip() or "unknown"
    return "unknown"


def run_build(project_path: str) -> tuple[bool, float]:
    """运行 pnpm build 命令，返回 (是否成功, 耗时秒数)"""
    print(f"正在构建项目: {project_path}")

    start_time = time.time()

    # 使用 subprocess 的 cwd 参数，不改变当前工作目录
    result = subprocess.run(
        ["pnpm", "build"],
        shell=True,
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='replace',
        cwd=project_path
    )

    elapsed_time = time.time() - start_time

    if result.returncode != 0:
        print(f"构建失败:\n{result.stderr}")
        return False, elapsed_time

    print(f"构建成功 (耗时 {elapsed_time:.1f}s)")
    return True, elapsed_time


def create_zip(project_path: str, output_dir: str = None) -> tuple[str, int, float]:
    """将 dist 目录打包为 zip，返回 (zip路径, 文件数量, 耗时秒数)"""
    dist_path = Path(project_path) / "dist"

    if not dist_path.exists():
        print(f"dist 目录不存在: {dist_path}")
        return None, 0, 0

    # 生成 zip 文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    project_name = Path(project_path).name
    zip_name = f"{project_name}_dist_{timestamp}.zip"

    # 输出目录
    if output_dir:
        output_path = Path(output_dir)
    else:
        output_path = Path(project_path)

    output_path.mkdir(parents=True, exist_ok=True)
    zip_path = output_path / zip_name

    print(f"正在打包: {zip_path}")

    start_time = time.time()
    file_count = 0

    # 创建 zip 文件
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for file_path in dist_path.rglob('*'):
            if file_path.is_file():
                # 保持相对路径结构
                arc_name = file_path.relative_to(dist_path)
                zf.write(file_path, arc_name)
                file_count += 1

    elapsed_time = time.time() - start_time

    # 获取 zip 文件大小
    zip_size = zip_path.stat().st_size
    size_mb = zip_size / (1024 * 1024)

    print(f"打包完成: {zip_path} (耗时 {elapsed_time:.1f}s)")

    return str(zip_path), file_count, elapsed_time


def format_time(seconds: float) -> str:
    """格式化时间为 HH:MM:SS 或 MM:SS"""
    if seconds < 60:
        return f"{seconds:.1f}s"
    minutes = int(seconds // 60)
    secs = seconds % 60
    if minutes < 60:
        return f"{minutes}m {secs:.1f}s"
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours}h {mins}m {secs:.1f}s"


def main():
    """主函数"""
    total_start_time = time.time()

    # 默认项目路径为当前目录或 frontend 子目录
    project_path = sys.argv[1] if len(sys.argv) > 1 else None

    # 获取原始工作目录
    original_cwd = os.getcwd()

    if not project_path:
        # 自动检测 frontend 目录
        frontend_path = os.path.join(original_cwd, "frontend")
        if os.path.exists(frontend_path):
            project_path = frontend_path
        else:
            project_path = original_cwd

    # 转为绝对路径
    project_path = os.path.abspath(project_path)

    # 输出目录参数
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    if output_dir:
        output_dir = os.path.abspath(output_dir)

    # 获取 git 信息
    git_branch = get_git_branch(project_path)
    git_commit = get_git_commit_info(project_path)

    # 1. 运行构建
    build_success, build_time = run_build(project_path)
    if not build_success:
        sys.exit(1)

    # 2. 打包 dist
    zip_path, file_count, pack_time = create_zip(project_path, output_dir)

    total_time = time.time() - total_start_time

    if zip_path:
        # 获取 zip 文件大小
        zip_size = Path(zip_path).stat().st_size
        size_mb = zip_size / (1024 * 1024)

        # 输出汇总信息
        print("\n" + "=" * 50)
        print("打包完成")
        print("=" * 50)
        print(f"项目路径: {project_path}")
        print(f"Git 分支: {git_branch}")
        print(f"Git Commit: {git_commit}")
        print(f"构建耗时: {format_time(build_time)}")
        print(f"打包耗时: {format_time(pack_time)}")
        print(f"总耗时:   {format_time(total_time)}")
        print(f"文件数量: {file_count}")
        print(f"文件大小: {size_mb:.2f} MB")
        print(f"输出文件: {zip_path}")
        print("=" * 50)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
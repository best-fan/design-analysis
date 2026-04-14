---
name: build-frontend-zip
description: 此技能用于前端项目打包。根据 package.json 的构建命令运行构建，然后将 dist 目录打包为 zip 格式。当用户请求打包、构建并压缩、或需要分发构建产物时触发。
---

# 前端项目打包

运行构建命令并将产物打包为 zip 格式，便于分发。

## 执行步骤

1. 检测项目路径（自动识别 frontend 目录）
2. 读取 `package.json` 的 `scripts.build` 命令确定构建方式
3. 运行构建命令（根据项目使用 pnpm/npm/yarn）
4. 将 `dist` 目录打包为 zip 文件
5. 输出 zip 文件路径和大小

## 构建命令检测

构建命令动态从 `package.json` 中读取：

```bash
# 先读取 package.json 确定构建命令
# 示例：若 package.json 中 scripts.build = "vue-tsc --noEmit && vite build"
# 则运行: pnpm build 或 npm run build 或 yarn build

# 根据项目锁文件判断包管理器：
# - pnpm-lock.yaml → pnpm
# - package-lock.json → npm
# - yarn.lock → yarn
```

## 执行脚本

```bash
python scripts/build_zip.py [项目路径] [输出目录]
```

参数：
- 项目路径：可选，默认自动检测 frontend 目录
- 输出目录：可选，默认输出到项目目录

示例：
```bash
python scripts/build_zip.py frontend
python scripts/build_zip.py . ./releases
```

## 输出文件命名

zip 文件命名格式：`{项目名}_dist_{时间戳}.zip`

示例：`frontend_dist_20260413_153000.zip`

## 注意事项

项目依赖需预先安装。构建失败时不生成 zip 文件。zip 文件保持 dist 目录结构。输出目录名可从 package.json 的 name 字段读取。
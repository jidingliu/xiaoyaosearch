#!/bin/bash

echo "构建小遥搜索应用..."

# 1. 构建前端
echo "构建前端..."
cd frontend
npm run build

# 2. 构建Electron应用
echo "构建Electron桌面应用..."
npm run electron:build

echo "构建完成！"
echo "应用程序输出目录: frontend/release/"
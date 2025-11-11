#!/bin/bash

# 小遥搜索项目 pre-commit 钩子脚本

echo "🔧 Running pre-commit checks..."

# 前端检查
echo "📱 Checking frontend..."
cd frontend

# 安装依赖（如果需要）
if [ ! -d "node_modules" ]; then
    npm install
fi

# 代码格式检查
echo "  📝 Checking frontend code format..."
npm run lint:fix

# 运行测试
echo "  🧪 Running frontend tests..."
npm run test

cd ..

# 后端检查
echo "🐍 Checking backend..."
cd backend

# 安装依赖（如果需要）
if [ ! -d "venv" ]; then
    python -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 代码格式检查
echo "  📝 Checking backend code format..."
black --check .
if [ $? -ne 0 ]; then
    echo "  ❌ Backend code formatting issues found. Please run 'black .' to fix."
    exit 1
fi

# 类型检查
echo "  🔍 Running type checking..."
mypy . --ignore-missing-imports

# 运行测试
echo "  🧪 Running backend tests..."
pytest

cd ..

echo "✅ All pre-commit checks passed!"
#!/bin/bash

echo "启动小遥搜索开发服务..."

# 启动后端服务
echo "启动FastAPI后端服务..."
cd backend

# Windows系统使用不同的激活命令
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

python main.py &
BACKEND_PID=$!
echo "后端服务PID: $BACKEND_PID"

# 等待后端启动
sleep 3

# 启动前端应用
echo "启动Electron前端应用..."
cd ../frontend
npm run electron:dev &
FRONTEND_PID=$!
echo "前端应用PID: $FRONTEND_PID"

# 显示进程信息
echo ""
echo "服务启动完成"
echo "前端地址: http://localhost:5173"
echo "后端API: http://localhost:8000"
echo "API文档: http://localhost:8000/docs"
echo ""
echo "按 Ctrl+C 停止服务"

# 监听退出信号
trap 'echo "正在停止服务..."; kill $BACKEND_PID $FRONTEND_PID; exit' INT

wait
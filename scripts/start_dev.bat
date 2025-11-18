@echo off
echo 启动小遥搜索开发服务...

:: 启动后端服务
echo 启动FastAPI后端服务...
cd backend
call venv\Scripts\activate.bat
start "小遥搜索后端" cmd /k "python main.py"

:: 等待后端启动
timeout /t 3 /nobreak > nul

:: 启动前端应用
echo 启动Electron前端应用...
cd ..\frontend
start "小遥搜索前端" cmd /k "npm run electron:dev"

echo.
echo 服务启动完成
echo 前端地址: http://localhost:5173
echo 后端API: http://localhost:8000
echo API文档: http://localhost:8000/docs
echo.
echo 按任意键关闭此窗口...
pause > nul
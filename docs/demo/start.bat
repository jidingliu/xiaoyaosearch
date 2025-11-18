@echo off
echo 小遥搜索高保真原型启动中...
echo.

REM 检查是否安装了Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误：未检测到 Node.js，请先安装 Node.js (https://nodejs.org/)
    pause
    exit /b 1
)

REM 检查是否安装了依赖
if not exist node_modules (
    echo 正在安装依赖包...
    npm install
    if %errorlevel% neq 0 (
        echo 错误：依赖包安装失败
        pause
        exit /b 1
    )
    echo 依赖包安装完成！
    echo.
)

REM 启动开发服务器
echo 正在启动开发服务器...
echo.
echo 项目启动后，请访问以下地址：
echo - 🎯 导航中心：http://localhost:3000/navigation.html (推荐)
echo - 🔍 搜索页面：http://localhost:3000/search.html
echo - ⚙️ 设置页面：http://localhost:3000/settings.html
echo - 📁 索引管理：http://localhost:3000/index-manage.html
echo - ❓ 帮助页面：http://localhost:3000/help.html
echo - 🎯 统一展示：http://localhost:3000/index.html
echo.
echo 按 Ctrl+C 停止服务器
echo.

npm run dev

pause
@echo off
echo 初始化小遥搜索开发环境（Windows）...

:: 1. 检查Python版本
python --version
if %errorlevel% neq 0 (
    echo 错误: 未找到Python，请先安装Python 3.10+
    pause
    exit /b 1
)

:: 2. 检查Node.js版本
node --version
if %errorlevel% neq 0 (
    echo 错误: 未找到Node.js，请先安装Node.js
    pause
    exit /b 1
)

:: 3. 创建Python虚拟环境
echo 创建Python虚拟环境...
cd backend
python -m venv venv

:: 4. 激活虚拟环境并安装依赖
call venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt

:: 5. 安装前端依赖
echo 安装前端依赖...
cd ..\frontend
npm install

:: 6. 创建数据目录
echo 创建数据目录结构...
mkdir ..\data\database
mkdir ..\data\indexes\faiss
mkdir ..\data\indexes\whoosh
mkdir ..\data\configs
mkdir ..\models\bge-m3
mkdir ..\models\faster-whisper
mkdir ..\models\cn-clip

:: 7. 创建环境配置文件
echo 创建环境配置文件...
cd ..\backend
(
echo # 小遥搜索后端环境配置
echo APP_NAME=小遥搜索
echo APP_VERSION=1.0.0
echo DEBUG=true
echo LOG_LEVEL=INFO
echo.
echo # 数据库配置
echo DATABASE_URL=sqlite:///../data/database/xiaoyaosearch.db
echo.
echo # AI模型配置
echo BGE_M3_MODEL_PATH=../models/bge-m3
echo FASTER_WHISPER_MODEL_SIZE=base
echo CN_CLIP_MODEL_PATH=../models/cn-clip
echo.
echo # 索引配置
echo FAISS_INDEX_PATH=../data/indexes/faiss
echo WHOOSH_INDEX_PATH=../data/indexes/whoosh
echo.
echo # 云端API配置（可选）
echo ALIBABA_CLOUD_ACCESS_KEY_ID=
echo ALIBABA_CLOUD_ACCESS_KEY_SECRET=
echo ALIBABA_CLOUD_REGION=cn-hangzhou
) > .env

cd ..\frontend
(
echo # 小遥搜索前端环境配置
echo VITE_APP_TITLE=小遥搜索
echo VITE_API_BASE_URL=http://localhost:8000
echo VITE_AI_MODEL_ENDPOINT=http://localhost:8000/api
) > .env

echo 环境初始化完成
echo.
echo 启动开发服务:
echo 1. 启动后端: cd backend ^&^& venv\Scripts\activate ^&^& python main.py
echo 2. 启动前端: cd frontend ^&^& npm run electron:dev
echo.
echo 或者使用启动脚本: start_dev.bat
pause
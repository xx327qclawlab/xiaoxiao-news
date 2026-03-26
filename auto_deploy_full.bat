@echo off
REM 小小新闻简报 - 完整自动化部署脚本
REM 自动完成：Git初始化、代码上传、Heroku部署

setlocal enabledelayedexpansion

echo.
echo ========================================
echo 小小新闻简报 - 完整自动化部署
echo ========================================
echo.

REM 设置变量
set WORKSPACE=C:\Users\成都工业学院\.qclaw\workspace
set APP_NAME=xiaoxiao-news-work
set REPO_NAME=xiaoxiao-news
set GITHUB_USER=your-github-username
set EMAIL=13569848@qq.com
set USERNAME=QClaw Lab

REM 第一步：检查 Git
echo [Step 1/6] Checking Git...
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git not found
    pause
    exit /b 1
)
echo OK: Git is installed

REM 第二步：进入工作目录
echo [Step 2/6] Entering workspace...
cd /d %WORKSPACE%
if errorlevel 1 (
    echo ERROR: Cannot enter workspace
    pause
    exit /b 1
)
echo OK: Workspace ready

REM 第三步：初始化 Git
echo [Step 3/6] Initializing Git repository...
git init
git config user.email "%EMAIL%"
git config user.name "%USERNAME%"
git add .
git commit -m "Initial commit - xiaoxiao news app"
if errorlevel 1 (
    echo WARNING: Git commit may have failed, continuing...
)
echo OK: Git initialized

REM 第四步：添加远程仓库
echo [Step 4/6] Adding remote repository...
echo.
echo IMPORTANT: You need to create a GitHub repository first!
echo 1. Go to https://github.com/new
echo 2. Create repository named: %REPO_NAME%
echo 3. Copy the HTTPS URL
echo.
set /p GITHUB_URL="Enter your GitHub repository URL (HTTPS): "

git remote add origin %GITHUB_URL%
git branch -M main
git push -u origin main
if errorlevel 1 (
    echo ERROR: Failed to push to GitHub
    echo Make sure your GitHub URL is correct
    pause
    exit /b 1
)
echo OK: Code pushed to GitHub

REM 第五步：登录 Heroku
echo [Step 5/6] Logging in to Heroku...
echo.
echo A browser window will open for Heroku login
echo Please enter your Heroku credentials
echo.
heroku login
if errorlevel 1 (
    echo ERROR: Heroku login failed
    pause
    exit /b 1
)
echo OK: Heroku login successful

REM 第六步：创建并部署应用
echo [Step 6/6] Creating and deploying Heroku app...
heroku create %APP_NAME%
if errorlevel 1 (
    echo WARNING: App may already exist, continuing...
)

git push heroku main
if errorlevel 1 (
    echo ERROR: Deployment failed
    pause
    exit /b 1
)
echo OK: Deployment successful

REM 显示结果
echo.
echo ========================================
echo DEPLOYMENT COMPLETE!
echo ========================================
echo.
echo Server URL: https://%APP_NAME%.herokuapp.com
echo API URL: https://%APP_NAME%.herokuapp.com/api/news
echo Callback URL: https://%APP_NAME%.herokuapp.com/wechat/callback
echo.
echo Next steps:
echo 1. Configure WeChat Work callback address
echo 2. Test the API
echo 3. Add members to the app
echo.
heroku apps:info %APP_NAME%
echo.
pause

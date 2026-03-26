@echo off
REM 小小新闻简报 - 直接 Heroku 部署（无需 GitHub）
REM 使用 Heroku Git 直接部署

setlocal enabledelayedexpansion

echo.
echo ========================================
echo Xiaoxiao News - Direct Heroku Deploy
echo ========================================
echo.

set WORKSPACE=C:\Users\成都工业学院\.qclaw\workspace
set APP_NAME=xiaoxiao-news-work

REM Step 1: Check Git
echo [1/5] Checking Git...
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git not found
    pause
    exit /b 1
)
echo OK

REM Step 2: Enter workspace
echo [2/5] Entering workspace...
cd /d %WORKSPACE%
echo OK

REM Step 3: Initialize Git
echo [3/5] Initializing Git...
if not exist .git (
    git init
    git config user.email "13569848@qq.com"
    git config user.name "QClaw Lab"
    git add .
    git commit -m "Initial commit"
)
echo OK

REM Step 4: Login to Heroku
echo [4/5] Logging in to Heroku...
echo Browser will open for login...
heroku login
if errorlevel 1 (
    echo ERROR: Heroku login failed
    pause
    exit /b 1
)
echo OK

REM Step 5: Deploy to Heroku
echo [5/5] Deploying to Heroku...
heroku create %APP_NAME% 2>nul
heroku git:remote -a %APP_NAME%
git push heroku main
if errorlevel 1 (
    echo ERROR: Deployment failed
    pause
    exit /b 1
)
echo OK

REM Show results
echo.
echo ========================================
echo DEPLOYMENT COMPLETE!
echo ========================================
echo.
echo Server: https://%APP_NAME%.herokuapp.com
echo Callback: https://%APP_NAME%.herokuapp.com/wechat/callback
echo.
heroku apps:info %APP_NAME%
echo.
pause

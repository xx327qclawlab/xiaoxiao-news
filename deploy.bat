@echo off
REM 小小新闻简报 - Heroku 自动部署脚本
REM 这个脚本会自动完成所有部署步骤

setlocal enabledelayedexpansion

echo.
echo ========================================
echo 小小新闻简报 - Heroku 自动部署
echo ========================================
echo.

REM 检查 Git 是否已安装
echo [1/5] 检查 Git...
git --version >nul 2>&1
if errorlevel 1 (
    echo Git 未安装，正在安装...
    winget install --id Git.Git -e --silent
    if errorlevel 1 (
        echo Git 安装失败，请手动安装：https://git-scm.com/download/win
        pause
        exit /b 1
    )
)
echo Git 已安装 ✓

REM 检查 Heroku CLI 是否已安装
echo [2/5] 检查 Heroku CLI...
heroku --version >nul 2>&1
if errorlevel 1 (
    echo Heroku CLI 未安装，正在安装...
    winget install --id Heroku.HerokuCLI -e --silent
    if errorlevel 1 (
        echo Heroku CLI 安装失败，请手动安装：https://devcenter.heroku.com/articles/heroku-cli
        pause
        exit /b 1
    )
)
echo Heroku CLI 已安装 ✓

REM 初始化 Git 仓库
echo [3/5] 初始化 Git 仓库...
cd /d C:\Users\成都工业学院\.qclaw\workspace
git init
git add .
git commit -m "Initial commit - xiaoxiao news app"
echo Git 仓库初始化完成 ✓

REM 登录 Heroku
echo [4/5] 登录 Heroku...
heroku login
if errorlevel 1 (
    echo Heroku 登录失败
    pause
    exit /b 1
)
echo Heroku 登录成功 ✓

REM 创建并部署到 Heroku
echo [5/5] 部署到 Heroku...
heroku create xiaoxiao-news-work
git push heroku main

echo.
echo ========================================
echo 部署完成！
echo ========================================
echo.
echo 获取服务器地址：
heroku apps:info xiaoxiao-news-work
echo.
echo 下一步：配置企业微信回调地址
echo 服务器地址：https://xiaoxiao-news-work.herokuapp.com/wechat/callback
echo.
pause

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小小新闻简报 - 直接 Heroku 部署脚本
"""

import os
import subprocess
import sys

def run_cmd(cmd, description=""):
    """执行命令"""
    if description:
        print(f"\n[*] {description}")
    print(f"    Command: {cmd}")
    
    result = subprocess.run(cmd, shell=True, cwd=r'C:\Users\成都工业学院\.qclaw\workspace')
    return result.returncode == 0

def main():
    workspace = r'C:\Users\成都工业学院\.qclaw\workspace'
    app_name = 'xiaoxiao-news-work'
    
    print("="*60)
    print("Xiaoxiao News - Heroku Direct Deploy")
    print("="*60)
    
    os.chdir(workspace)
    
    # Step 1: Init Git
    print("\n[Step 1] Initializing Git...")
    run_cmd('git init', 'Initialize Git repository')
    run_cmd('git config user.email "13569848@qq.com"', 'Set email')
    run_cmd('git config user.name "QClaw Lab"', 'Set username')
    run_cmd('git add .', 'Add all files')
    run_cmd('git commit -m "Initial commit"', 'Commit changes')
    
    # Step 2: Login Heroku
    print("\n[Step 2] Logging in to Heroku...")
    print("Browser will open for login...")
    if not run_cmd('heroku login', 'Login to Heroku'):
        print("[ERROR] Heroku login failed")
        return False
    
    # Step 3: Create app
    print("\n[Step 3] Creating Heroku app...")
    run_cmd(f'heroku create {app_name}', f'Create app {app_name}')
    
    # Step 4: Deploy
    print("\n[Step 4] Deploying to Heroku...")
    if not run_cmd('git push heroku main', 'Deploy code'):
        print("[ERROR] Deployment failed")
        return False
    
    # Step 5: Get info
    print("\n[Step 5] Getting app info...")
    run_cmd(f'heroku apps:info {app_name}', 'Get app information')
    
    # Summary
    print("\n" + "="*60)
    print("DEPLOYMENT COMPLETE!")
    print("="*60)
    print(f"\nServer URL: https://{app_name}.herokuapp.com")
    print(f"API URL: https://{app_name}.herokuapp.com/api/news")
    print(f"Callback URL: https://{app_name}.herokuapp.com/wechat/callback")
    print("\nNext: Configure WeChat Work callback address")
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import subprocess
import sys

def run_cmd(cmd):
    """Run command and return success status"""
    print(f"[RUN] {cmd}")
    result = subprocess.run(cmd, shell=True)
    return result.returncode == 0

def main():
    workspace = r'C:\Users\成都工业学院\.qclaw\workspace'
    app_name = 'xiaoxiao-news-work'
    
    print("="*60)
    print("Xiaoxiao News - Auto Deploy")
    print("="*60)
    
    # Step 1: Check tools
    print("\n[Step 1] Checking tools...")
    if not run_cmd('git --version'):
        print("[ERROR] Git not found")
        return False
    if not run_cmd('heroku --version'):
        print("[ERROR] Heroku CLI not found")
        return False
    print("[OK] All tools ready")
    
    # Step 2: Init Git
    print("\n[Step 2] Initializing Git...")
    os.chdir(workspace)
    run_cmd('git init')
    run_cmd('git config user.email "13569848@qq.com"')
    run_cmd('git config user.name "QClaw Lab"')
    run_cmd('git add .')
    run_cmd('git commit -m "Initial commit"')
    print("[OK] Git initialized")
    
    # Step 3: Login Heroku
    print("\n[Step 3] Login to Heroku...")
    print("[INFO] Browser will open for login")
    if not run_cmd('heroku login'):
        print("[ERROR] Heroku login failed")
        return False
    print("[OK] Heroku login success")
    
    # Step 4: Create app
    print("\n[Step 4] Creating Heroku app...")
    run_cmd(f'heroku create {app_name}')
    print("[OK] App created")
    
    # Step 5: Deploy
    print("\n[Step 5] Deploying code...")
    if not run_cmd('git push heroku main'):
        print("[ERROR] Deploy failed")
        return False
    print("[OK] Deploy success")
    
    # Step 6: Get info
    print("\n[Step 6] Getting app info...")
    run_cmd(f'heroku apps:info {app_name}')
    
    # Summary
    print("\n" + "="*60)
    print("Deploy Complete!")
    print("="*60)
    print(f"\nServer URL: https://{app_name}.herokuapp.com")
    print(f"API URL: https://{app_name}.herokuapp.com/api/news")
    print(f"Callback URL: https://{app_name}.herokuapp.com/wechat/callback")
    print("\nNext: Configure WeChat Work callback address")
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

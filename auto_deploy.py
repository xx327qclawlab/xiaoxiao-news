# -*- coding: utf-8 -*-
"""
小小新闻简报 - 自动化部署脚本
自动完成：Git初始化、Heroku登录、代码部署
"""

import os
import subprocess
import sys
import json
from pathlib import Path

class AutoDeployer:
    def __init__(self):
        self.workspace = r'C:\Users\成都工业学院\.qclaw\workspace'
        self.app_name = 'xiaoxiao-news-work'
        self.heroku_url = f'https://{self.app_name}.herokuapp.com'
        
    def run_command(self, cmd, description=""):
        """运行命令"""
        if description:
            print(f"\n[*] {description}")
        print(f"    执行: {cmd}")
        
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)
            if result.returncode == 0:
                print(f"    ✓ 成功")
                if result.stdout:
                    print(f"    输出: {result.stdout[:200]}")
                return True
            else:
                print(f"    ✗ 失败 (代码: {result.returncode})")
                if result.stderr:
                    print(f"    错误: {result.stderr[:200]}")
                return False
        except subprocess.TimeoutExpired:
            print(f"    ✗ 超时")
            return False
        except Exception as e:
            print(f"    ✗ 异常: {e}")
            return False
    
    def check_tools(self):
        """检查必要工具"""
        print("\n" + "="*60)
        print("[Step 1] Check Required Tools")
        print("="*60)
        
        tools = {
            'git': 'git --version',
            'heroku': 'heroku --version',
            'python': 'python --version'
        }
        
        for tool, cmd in tools.items():
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"[OK] {tool}: {result.stdout.strip()}")
            else:
                print(f"[FAIL] {tool}: Not installed")
                return False
        
        return True
    
    def init_git(self):
        """初始化 Git 仓库"""
        print("\n" + "="*60)
        print("【第二步】初始化 Git 仓库")
        print("="*60)
        
        os.chdir(self.workspace)
        
        # 检查是否已初始化
        if os.path.exists(os.path.join(self.workspace, '.git')):
            print("✓ Git 仓库已存在")
            return True
        
        commands = [
            ('git init', '初始化 Git'),
            ('git config user.email "13569848@qq.com"', '配置邮箱'),
            ('git config user.name "QClaw Lab"', '配置用户名'),
            ('git add .', '添加所有文件'),
            ('git commit -m "Initial commit - xiaoxiao news app"', '提交代码'),
        ]
        
        for cmd, desc in commands:
            if not self.run_command(cmd, desc):
                return False
        
        return True
    
    def login_heroku(self):
        """登录 Heroku"""
        print("\n" + "="*60)
        print("【第三步】登录 Heroku")
        print("="*60)
        
        print("\n⚠️  需要在浏览器中登录 Heroku")
        print("请在弹出的浏览器窗口中输入你的 Heroku 账号和密码")
        
        if not self.run_command('heroku login', '登录 Heroku'):
            print("✗ Heroku 登录失败")
            return False
        
        print("✓ Heroku 登录成功")
        return True
    
    def create_app(self):
        """创建 Heroku 应用"""
        print("\n" + "="*60)
        print("【第四步】创建 Heroku 应用")
        print("="*60)
        
        # 检查应用是否已存在
        result = subprocess.run(f'heroku apps:info {self.app_name}', 
                              shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✓ 应用 {self.app_name} 已存在")
            return True
        
        if not self.run_command(f'heroku create {self.app_name}', f'创建应用 {self.app_name}'):
            print(f"✗ 创建应用失败")
            return False
        
        print(f"✓ 应用创建成功")
        return True
    
    def deploy(self):
        """部署代码"""
        print("\n" + "="*60)
        print("【第五步】部署代码到 Heroku")
        print("="*60)
        
        if not self.run_command('git push heroku main', '推送代码到 Heroku'):
            print("✗ 部署失败")
            return False
        
        print("✓ 部署成功")
        return True
    
    def get_app_info(self):
        """获取应用信息"""
        print("\n" + "="*60)
        print("【第六步】获取应用信息")
        print("="*60)
        
        result = subprocess.run(f'heroku apps:info {self.app_name}', 
                              shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(result.stdout)
            return True
        
        return False
    
    def test_api(self):
        """测试 API"""
        print("\n" + "="*60)
        print("【第七步】测试 API")
        print("="*60)
        
        import time
        time.sleep(5)  # 等待应用启动
        
        test_url = f'{self.heroku_url}/api/health'
        print(f"\n测试地址: {test_url}")
        
        try:
            import urllib.request
            response = urllib.request.urlopen(test_url, timeout=10)
            data = json.loads(response.read().decode('utf-8'))
            print(f"✓ API 响应: {json.dumps(data, ensure_ascii=False, indent=2)}")
            return True
        except Exception as e:
            print(f"✗ API 测试失败: {e}")
            return False
    
    def show_summary(self):
        """显示总结"""
        print("\n" + "="*60)
        print("【部署完成】")
        print("="*60)
        
        print(f"""
✓ 部署成功！

📋 应用信息：
- 应用名称: {self.app_name}
- 服务器地址: {self.heroku_url}
- API 地址: {self.heroku_url}/api/news

🔧 下一步配置企业微信回调：
1. 登录企业微信后台: https://work.weixin.qq.com/
2. 进入「应用管理」→「小小新闻简报」
3. 点击「编辑」
4. 找到「接收消息的服务器配置」
5. 填写以下信息：
   - 服务器地址: {self.heroku_url}/wechat/callback
   - Token: xiaoxiao_news_token
   - 消息加密密钥: 自动生成
6. 点击「保存」

📱 测试功能：
- 访问: {self.heroku_url}/api/news
- 查看新闻列表

🎉 恭喜！小小新闻简报已成功部署！
""")
    
    def run(self):
        """执行完整部署流程"""
        print("\n" + "="*60)
        print("小小新闻简报 - 自动化部署")
        print("="*60)
        
        steps = [
            ('检查工具', self.check_tools),
            ('初始化 Git', self.init_git),
            ('登录 Heroku', self.login_heroku),
            ('创建应用', self.create_app),
            ('部署代码', self.deploy),
            ('获取应用信息', self.get_app_info),
            ('测试 API', self.test_api),
        ]
        
        for step_name, step_func in steps:
            try:
                if not step_func():
                    print(f"\n✗ {step_name} 失败，停止部署")
                    return False
            except Exception as e:
                print(f"\n✗ {step_name} 异常: {e}")
                return False
        
        self.show_summary()
        return True

if __name__ == '__main__':
    deployer = AutoDeployer()
    success = deployer.run()
    sys.exit(0 if success else 1)

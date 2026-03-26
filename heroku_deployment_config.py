"""
Heroku 部署配置文件
"""

# requirements.txt - Python 依赖
requirements_txt = """Flask==2.3.0
requests==2.31.0
Werkzeug==2.3.0
"""

# Procfile - Heroku 启动配置
procfile = """web: python wechat_work_backend.py
"""

# runtime.txt - Python 版本
runtime_txt = """python-3.11.0
"""

# .gitignore
gitignore = """__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
.env
.vscode/
.idea/
"""

# 部署说明
deployment_guide = """
# Heroku 一键部署指南

## 前置条件
1. 安装 Git：https://git-scm.com/
2. 安装 Heroku CLI：https://devcenter.heroku.com/articles/heroku-cli
3. 有 GitHub 账号

## 部署步骤

### 1. 创建 GitHub 仓库
```bash
# 初始化 Git 仓库
git init
git add .
git commit -m "Initial commit"

# 创建 GitHub 仓库并推送
git remote add origin https://github.com/your-username/xiaoxiao-news.git
git branch -M main
git push -u origin main
```

### 2. 登录 Heroku
```bash
heroku login
```

### 3. 创建 Heroku 应用
```bash
heroku create xiaoxiao-news-work
```

### 4. 部署代码
```bash
git push heroku main
```

### 5. 查看日志
```bash
heroku logs --tail
```

### 6. 获取服务器地址
```bash
heroku apps:info xiaoxiao-news-work
```

你会看到类似这样的地址：
```
https://xiaoxiao-news-work.herokuapp.com
```

## 配置企业微信回调

1. 登录企业微信后台
2. 进入「应用管理」→「小小新闻简报」
3. 找到「接收消息的服务器配置」
4. 点击「设置」
5. 填写：
   - 服务器地址：https://xiaoxiao-news-work.herokuapp.com/wechat/callback
   - Token：xiaoxiao_news_token
   - 消息加密密钥：自动生成
6. 点击「保存」

## 测试 API

```bash
# 获取新闻列表
curl https://xiaoxiao-news-work.herokuapp.com/api/news

# 按分类获取
curl https://xiaoxiao-news-work.herokuapp.com/api/news/category/时政

# 健康检查
curl https://xiaoxiao-news-work.herokuapp.com/api/health
```

## 常见问题

**Q: 部署失败？**
A: 检查 requirements.txt 和 Procfile 是否正确

**Q: 应用崩溃？**
A: 运行 `heroku logs --tail` 查看错误日志

**Q: 如何更新代码？**
A: 修改代码后，运行 `git push heroku main` 重新部署

## 下一步

部署完成后，你需要：
1. 配置企业微信回调地址
2. 配置菜单
3. 添加成员到应用
4. 测试功能
"""

print("Heroku 部署配置已生成")
print()
print("需要创建的文件：")
print("1. requirements.txt")
print("2. Procfile")
print("3. runtime.txt")
print("4. .gitignore")
print()
print("部署步骤：")
print("1. 创建 GitHub 仓库")
print("2. 登录 Heroku")
print("3. 创建 Heroku 应用")
print("4. 部署代码")
print("5. 配置企业微信回调")

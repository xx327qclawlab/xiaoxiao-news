# 小小新闻简报 - Heroku 部署完整指南

## 📋 你的部署信息

```
应用名称：xiaoxiao-news-work
服务器地址：https://xiaoxiao-news-work.herokuapp.com
企业ID：ww7b2a7bf9120e2dd4
AgentID：1000002
```

---

## 🚀 Heroku 部署步骤（5分钟快速版）

### 第一步：安装必要工具（2分钟）

#### 1. 安装 Git
- 下载：https://git-scm.com/download/win
- 安装完成后重启电脑

#### 2. 安装 Heroku CLI
- 下载：https://devcenter.heroku.com/articles/heroku-cli
- 选择 Windows 版本
- 安装完成后重启电脑

#### 3. 验证安装
打开 PowerShell，运行：
```powershell
git --version
heroku --version
```

如果都显示版本号，说明安装成功！

---

### 第二步：创建 GitHub 仓库（2分钟）

#### 1. 创建 GitHub 账号
- 访问：https://github.com/
- 点击「Sign up」
- 填写邮箱、密码、用户名
- 验证邮箱

#### 2. 创建新仓库
- 登录 GitHub
- 点击「+」→「New repository」
- 仓库名：`xiaoxiao-news`
- 选择「Public」
- 点击「Create repository」

#### 3. 获取仓库地址
- 点击「Code」
- 复制 HTTPS 地址（样子像：https://github.com/your-username/xiaoxiao-news.git）

---

### 第三步：上传代码到 GitHub（1分钟）

打开 PowerShell，进入你的工作目录：

```powershell
# 进入工作目录
cd C:\Users\成都工业学院\.qclaw\workspace

# 初始化 Git 仓库
git init

# 添加所有文件
git add .

# 提交代码
git commit -m "Initial commit - xiaoxiao news app"

# 添加远程仓库（替换为你的仓库地址）
git remote add origin https://github.com/your-username/xiaoxiao-news.git

# 推送到 GitHub
git branch -M main
git push -u origin main
```

---

### 第四步：部署到 Heroku（1分钟）

```powershell
# 登录 Heroku
heroku login

# 创建 Heroku 应用
heroku create xiaoxiao-news-work

# 部署代码
git push heroku main

# 查看日志
heroku logs --tail
```

---

### 第五步：获取服务器地址

```powershell
# 查看应用信息
heroku apps:info xiaoxiao-news-work
```

你会看到类似这样的输出：
```
=== xiaoxiao-news-work
Dynos:                web: 1
Git URL:              https://git.heroku.com/xiaoxiao-news-work.git
Web URL:              https://xiaoxiao-news-work.herokuapp.com
```

**复制 Web URL！** 这就是你的服务器地址。

---

## 🔧 配置企业微信回调

部署完成后，需要配置企业微信回调地址：

1. 登录企业微信后台：https://work.weixin.qq.com/
2. 进入「**应用管理**」
3. 找到「**小小新闻简报**」应用
4. 点击「**编辑**」
5. 找到「**接收消息的服务器配置**」
6. 点击「**设置**」

填写以下信息：
```
服务器地址(URL)：https://xiaoxiao-news-work.herokuapp.com/wechat/callback
Token：xiaoxiao_news_token
消息加密密钥(EncodingAESKey)：自动生成
消息加密方式：明文模式
```

7. 点击「**保存**」

---

## ✅ 测试功能

### 1. 测试 API

打开浏览器，访问：
```
https://xiaoxiao-news-work.herokuapp.com/api/health
```

如果看到 JSON 响应，说明服务器正常运行！

### 2. 测试新闻接口

```
https://xiaoxiao-news-work.herokuapp.com/api/news
```

### 3. 在企业微信中测试

- 打开企业微信
- 找到「**小小新闻简报**」应用
- 点击菜单测试功能

---

## 🆘 常见问题

**Q: 部署失败，显示 "No such file or directory"？**
A: 检查 requirements.txt 和 Procfile 是否在仓库根目录

**Q: 应用崩溃，显示 "Application error"？**
A: 运行 `heroku logs --tail` 查看错误日志

**Q: 如何更新代码？**
A: 修改代码后，运行：
```powershell
git add .
git commit -m "Update"
git push heroku main
```

**Q: 如何查看实时日志？**
A: 运行 `heroku logs --tail`

**Q: 如何删除应用？**
A: 运行 `heroku apps:destroy xiaoxiao-news-work`

---

## 📝 部署清单

- [ ] 安装 Git
- [ ] 安装 Heroku CLI
- [ ] 创建 GitHub 账号
- [ ] 创建 GitHub 仓库
- [ ] 上传代码到 GitHub
- [ ] 部署到 Heroku
- [ ] 获取服务器地址
- [ ] 配置企业微信回调
- [ ] 测试 API
- [ ] 在企业微信中测试

---

## 🎯 下一步

部署完成后，你需要：

1. ✅ 配置企业微信回调地址
2. ✅ 配置菜单
3. ✅ 添加成员到应用
4. ✅ 测试功能
5. ✅ 邀请用户使用

---

**最后更新：2026-03-26**

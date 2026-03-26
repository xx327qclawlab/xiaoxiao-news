# 小小新闻简报 - 微信服务号完整部署指南

## 📋 目录
1. [快速开始](#快速开始)
2. [注册微信服务号](#注册微信服务号)
3. [部署后端服务](#部署后端服务)
4. [配置微信服务号](#配置微信服务号)
5. [测试和上线](#测试和上线)

---

## 快速开始

**总耗时：30分钟**

### 需要的东西
- ✅ 微信账号
- ✅ 邮箱
- ✅ 身份证（可选，个人认证）

### 最终效果
用户关注你的服务号 → 每天早上8点自动推送新闻 → 用户可以分类浏览、搜索、点赞

---

## 注册微信服务号

### 步骤 1：访问微信公众平台
- 打开：https://mp.weixin.qq.com/
- 点击「立即注册」

### 步骤 2：选择账号类型
- 选择「服务号」（不是订阅号）
- 点击「下一步」

### 步骤 3：填写基本信息
```
邮箱：你的邮箱
密码：设置密码
确认密码：再输一遍
```

### 步骤 4：选择主体类型
- 选择「个人」（最快）
- 或「企业」（需要营业执照）

### 步骤 5：填写个人信息
```
姓名：你的名字
身份证号：你的身份证
手机号：你的手机
```

### 步骤 6：验证
- 微信会发验证码到你的手机
- 输入验证码完成注册

### 步骤 7：获取 AppID 和 AppSecret
- 登录后台
- 进入「设置」→「基本设置」
- 复制 AppID 和 AppSecret
- **保存好这两个值！**

---

## 部署后端服务

### 方案 A：使用 Heroku（推荐，完全免费）

#### 1. 注册 Heroku 账号
- 访问：https://www.heroku.com/
- 点击「Sign up」
- 填写邮箱、密码、名字
- 验证邮箱

#### 2. 安装 Heroku CLI
- 下载：https://devcenter.heroku.com/articles/heroku-cli
- 安装完成后打开终端

#### 3. 部署代码
```bash
# 登录 Heroku
heroku login

# 创建应用
heroku create xiaoxiao-news

# 部署代码
git push heroku main

# 查看日志
heroku logs --tail
```

#### 4. 获取服务 URL
```
https://xiaoxiao-news.herokuapp.com
```

### 方案 B：使用 Railway（也很简单）

#### 1. 注册 Railway 账号
- 访问：https://railway.app/
- 用 GitHub 账号登录

#### 2. 部署
- 连接 GitHub 仓库
- 自动部署

#### 3. 获取服务 URL
- 在 Railway 后台查看

### 方案 C：本地测试（开发用）

```bash
# 安装依赖
pip install flask

# 运行服务
python wechat_backend.py

# 本地地址
http://localhost:5000
```

---

## 配置微信服务号

### 步骤 1：配置服务器地址

1. 登录微信公众平台后台
2. 进入「设置」→「基本设置」
3. 找到「服务器配置」
4. 点击「修改配置」

### 步骤 2：填写服务器信息

```
服务器地址(URL)：https://xiaoxiao-news.herokuapp.com/wechat
令牌(Token)：xiaoxiao_news_token
消息加密密钥(EncodingAESKey)：自动生成
消息加密方式：明文模式（开发时）
```

### 步骤 3：验证服务器

- 点击「提交」
- 微信会向你的服务器发送验证请求
- 如果返回 200 OK，说明配置成功

### 步骤 4：配置自定义菜单

1. 进入「自定义菜单」
2. 点击「新增菜单」
3. 添加以下菜单项：

```
一级菜单：
├─ 📰 今日新闻 (点击事件: DAILY_NEWS)
├─ 分类浏览
│  ├─ 🌟 时政 (点击事件: CATEGORY_POLITICS)
│  ├─ 🚀 科技 (点击事件: CATEGORY_TECH)
│  ├─ ⚽ 体育 (点击事件: CATEGORY_SPORTS)
│  └─ 📚 教育 (点击事件: CATEGORY_EDUCATION)
└─ ⚙️ 设置 (链接: https://example.com/settings)
```

### 步骤 5：配置自动回复

1. 进入「自动回复」
2. 设置「被添加时回复」：

```
感谢关注小小新闻简报！

我是小不点，每天为小学五年级的小朋友播报有趣的新闻。

点击下方菜单开始浏览吧！
```

---

## 测试和上线

### 测试步骤

1. **扫码关注**
   - 在微信公众平台后台找到二维码
   - 用微信扫描关注

2. **测试菜单**
   - 点击「今日新闻」
   - 点击「分类浏览」→「时政」
   - 检查是否收到回复

3. **测试 API**
   ```bash
   # 获取新闻列表
   curl https://xiaoxiao-news.herokuapp.com/api/news
   
   # 按分类获取
   curl https://xiaoxiao-news.herokuapp.com/api/news/category/时政
   
   # 获取分类列表
   curl https://xiaoxiao-news.herokuapp.com/api/categories
   ```

### 上线步骤

1. **完成所有测试**
   - 确保菜单正常
   - 确保 API 正常
   - 确保推送正常

2. **提交审核**（可选）
   - 如果要发布到微信应用市场
   - 需要提交审核

3. **宣传**
   - 分享二维码给用户
   - 用户关注后自动推送新闻

---

## 常见问题

**Q: 为什么收不到消息？**
A: 检查服务器地址是否正确，Token 是否一致

**Q: 如何修改推送时间？**
A: 在后端代码中修改 `scheduled_push()` 函数

**Q: 如何添加更多新闻？**
A: 修改 `wechat_backend.py` 中的 `init_data()` 函数

**Q: 如何实现真正的爬虫？**
A: 使用 BeautifulSoup 或 Scrapy 库爬取新闻网站

---

## 下一步

1. ✅ 注册微信服务号
2. ✅ 部署后端服务
3. ✅ 配置微信服务号
4. ✅ 测试功能
5. ✅ 邀请用户关注
6. ✅ 定时推送新闻

---

**需要帮助？**
- 微信公众平台帮助中心：https://mp.weixin.qq.com/wiki
- Heroku 文档：https://devcenter.heroku.com/
- Flask 文档：https://flask.palletsprojects.com/

---

**最后更新：2026-03-26**

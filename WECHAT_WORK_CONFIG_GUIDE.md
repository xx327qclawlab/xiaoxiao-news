# 小小新闻简报 - 企业微信配置完整指南

## 📋 你的应用信息

```
企业名称：祥祥的qcloud实验室
应用名称：小小新闻简报
AgentID：1000002
Secret：pa-ak4gfNBxuX8z8ZO6AOkgit-OoW1asllaMHV2HK10
```

---

## 🚀 快速配置步骤

### 第一步：获取企业ID

1. 登录企业微信后台：https://work.weixin.qq.com/
2. 点击左侧「**我的企业**」
3. 向下滑动，找到「**企业ID**」
4. 复制企业ID（样子像：ww1234567890abcdef）

**保存这个值！** 我们后面需要用到。

---

### 第二步：配置应用回调地址

1. 进入「**应用管理**」
2. 找到「**小小新闻简报**」应用
3. 点击「**编辑**」
4. 找到「**接收消息的服务器配置**」
5. 点击「**设置**」

填写以下信息：
```
服务器地址(URL)：https://your-server.com/wechat/callback
Token：xiaoxiao_news_token
消息加密密钥(EncodingAESKey)：自动生成或自定义
消息加密方式：明文模式（开发时）或加密模式（生产）
```

**重要：** 需要一个公网服务器地址！

---

### 第三步：部署后端服务

#### 方案A：使用 Heroku（推荐）

```bash
# 1. 安装 Heroku CLI
# 下载：https://devcenter.heroku.com/articles/heroku-cli

# 2. 登录 Heroku
heroku login

# 3. 创建应用
heroku create xiaoxiao-news-work

# 4. 部署代码
git push heroku main

# 5. 查看日志
heroku logs --tail
```

**获取服务器地址：**
```
https://xiaoxiao-news-work.herokuapp.com
```

#### 方案B：使用 Railway

1. 访问：https://railway.app/
2. 用 GitHub 账号登录
3. 连接你的代码仓库
4. 自动部署

#### 方案C：本地测试

```bash
# 安装依赖
pip install flask requests

# 运行服务
python wechat_work_backend.py

# 本地地址
http://localhost:5000
```

**注意：** 本地无法接收企业微信回调，只能用于测试 API

---

### 第四步：配置菜单

1. 进入「**应用管理**」→「**小小新闻简报**」
2. 找到「**菜单配置**」
3. 点击「**设置**」
4. 添加菜单项：

```json
{
  "button": [
    {
      "type": "click",
      "name": "📰 今日新闻",
      "key": "DAILY_NEWS"
    },
    {
      "name": "分类浏览",
      "sub_button": [
        {
          "type": "click",
          "name": "🌟 时政",
          "key": "CATEGORY_POLITICS"
        },
        {
          "type": "click",
          "name": "🚀 科技",
          "key": "CATEGORY_TECH"
        },
        {
          "type": "click",
          "name": "⚽ 体育",
          "key": "CATEGORY_SPORTS"
        },
        {
          "type": "click",
          "name": "📚 教育",
          "key": "CATEGORY_EDUCATION"
        }
      ]
    },
    {
      "type": "view",
      "name": "⚙️ 设置",
      "url": "https://example.com/settings"
    }
  ]
}
```

---

### 第五步：测试功能

1. **添加成员到应用**
   - 进入「**应用管理**」→「**小小新闻简报**」
   - 点击「**成员**」
   - 添加你自己或其他成员

2. **在企业微信中测试**
   - 打开企业微信
   - 找到「**小小新闻简报**」应用
   - 点击菜单测试功能

3. **测试 API**
   ```bash
   # 获取新闻列表
   curl https://your-server.com/api/news
   
   # 按分类获取
   curl https://your-server.com/api/news/category/时政
   
   # 健康检查
   curl https://your-server.com/api/health
   ```

---

## 📝 配置清单

- [ ] 获取企业ID
- [ ] 配置应用回调地址
- [ ] 部署后端服务到公网
- [ ] 配置菜单
- [ ] 添加成员到应用
- [ ] 测试功能
- [ ] 配置定时推送

---

## 🔑 关键信息总结

| 项目 | 值 |
|------|-----|
| 企业名称 | 祥祥的qcloud实验室 |
| 应用名称 | 小小新闻简报 |
| AgentID | 1000002 |
| Secret | pa-ak4gfNBxuX8z8ZO6AOkgit-OoW1asllaMHV2HK10 |
| Token | xiaoxiao_news_token |
| 回调地址 | https://your-server.com/wechat/callback |

---

## 🆘 常见问题

**Q: 为什么收不到消息？**
A: 检查回调地址是否正确，Token 是否一致

**Q: 如何修改推送时间？**
A: 在后端代码中修改 `scheduled_push()` 函数

**Q: 如何添加更多新闻？**
A: 修改 `wechat_work_backend.py` 中的 `init_data()` 函数

**Q: 如何实现真正的爬虫？**
A: 使用 BeautifulSoup 或 Scrapy 库爬取新闻网站

---

## 📞 需要帮助？

- 企业微信文档：https://work.weixin.qq.com/api/doc
- Heroku 文档：https://devcenter.heroku.com/
- Flask 文档：https://flask.palletsprojects.com/

---

**最后更新：2026-03-26**

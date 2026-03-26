# 小小新闻简报 - 微信小程序开发指南

## 项目概述

**小小新闻简报**是一款为小学五年级孩子定制的新闻阅读微信小程序。

### 核心功能
- ✅ 实时新闻更新（8大分类）
- ✅ 个性化推荐
- ✅ 新闻搜索
- ✅ 点赞、收藏、分享
- ✅ 定时推送通知
- ✅ 离线阅读

### 支持分类
1. **时政** - 国内外政治新闻
2. **科技** - 科技创新、互联网、AI
3. **体育** - 足球、篮球、奥运等
4. **教育** - 学习、考试、教育政策
5. **军事** - 国防、军事新闻
6. **娱乐** - 电影、明星、音乐
7. **健康** - 医学、养生、健康知识
8. **环保** - 气候、生态、环境

---

## 开发环境搭建

### 1. 安装微信开发者工具
- 下载地址：https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html
- 选择 Windows 版本
- 安装完成后打开

### 2. 注册微信小程序账号
- 访问：https://mp.weixin.qq.com/
- 点击「立即注册」
- 选择「小程序」
- 填写信息并认证（需要企业营业执照）

### 3. 获取 AppID
- 登录小程序后台
- 进入「设置」→「基本设置」
- 复制 AppID

---

## 项目结构

```
xiaoxiao-news/
├── app.js                 # 主程序
├── app.json              # 全局配置
├── app.wxss              # 全局样式
├── pages/
│   ├── index/            # 首页
│   │   ├── index.js
│   │   ├── index.wxml
│   │   └── index.wxss
│   ├── detail/           # 详情页
│   │   ├── detail.js
│   │   ├── detail.wxml
│   │   └── detail.wxss
│   ├── category/         # 分类页
│   │   ├── category.js
│   │   ├── category.wxml
│   │   └── category.wxss
│   ├── search/           # 搜索页
│   │   ├── search.js
│   │   ├── search.wxml
│   │   └── search.wxss
│   └── my/               # 我的页面
│       ├── my.js
│       ├── my.wxml
│       └── my.wxss
├── utils/
│   ├── api.js            # API 调用
│   ├── util.js           # 工具函数
│   └── config.js         # 配置文件
└── images/               # 图片资源
```

---

## 后端 API 接口

### 基础 URL
```
https://api.xiaoxiao-news.com
```

### 接口列表

#### 1. 获取所有新闻
```
GET /api/news?page=1&limit=10
```

**响应示例：**
```json
{
  "code": 0,
  "message": "success",
  "data": [
    {
      "id": 1,
      "title": "中国人造太阳破纪录",
      "category": "时政",
      "source": "央视新闻",
      "snippet": "...",
      "image_url": "...",
      "timestamp": "2026-03-26T06:14:00",
      "views": 1234,
      "likes": 567
    }
  ]
}
```

#### 2. 按分类获取新闻
```
GET /api/news/category/:category?page=1&limit=10
```

#### 3. 搜索新闻
```
GET /api/news/search?keyword=人造太阳&page=1&limit=10
```

#### 4. 获取新闻详情
```
GET /api/news/:id
```

#### 5. 点赞新闻
```
POST /api/news/:id/like
```

#### 6. 收藏新闻
```
POST /api/news/:id/collect
```

#### 7. 获取分类列表
```
GET /api/categories
```

---

## 快速开始

### 步骤 1：创建项目
1. 打开微信开发者工具
2. 点击「+」新建项目
3. 填写项目名称：`xiaoxiao-news`
4. 选择项目目录
5. 填入 AppID
6. 点击「新建」

### 步骤 2：复制代码文件
将以下文件复制到项目目录：
- `app.js`
- `app.json`
- `app.wxss`
- `pages/index/index.js`
- `pages/index/index.wxml`
- `pages/index/index.wxss`

### 步骤 3：配置 app.json
```json
{
  "pages": [
    "pages/index/index",
    "pages/detail/detail",
    "pages/category/category",
    "pages/search/search",
    "pages/my/my"
  ],
  "window": {
    "backgroundTextStyle": "light",
    "navigationBarBackgroundColor": "#1a5fb4",
    "navigationBarTitleText": "小小新闻简报",
    "navigationBarTextStyle": "white"
  },
  "tabBar": {
    "color": "#999",
    "selectedColor": "#1a5fb4",
    "backgroundColor": "#fff",
    "borderStyle": "black",
    "list": [
      {
        "pagePath": "pages/index/index",
        "text": "首页",
        "iconPath": "images/home.png",
        "selectedIconPath": "images/home-active.png"
      },
      {
        "pagePath": "pages/my/my",
        "text": "我的",
        "iconPath": "images/my.png",
        "selectedIconPath": "images/my-active.png"
      }
    ]
  }
}
```

### 步骤 4：测试
1. 点击「预览」
2. 用微信扫描二维码
3. 在手机上测试功能

---

## 功能实现清单

- [ ] 首页新闻列表展示
- [ ] 分类筛选功能
- [ ] 新闻详情页
- [ ] 搜索功能
- [ ] 点赞功能
- [ ] 收藏功能
- [ ] 分享功能
- [ ] 用户偏好设置
- [ ] 定时推送通知
- [ ] 离线缓存
- [ ] 用户登录
- [ ] 个性化推荐

---

## 部署上线

### 1. 提交审核
- 完成所有功能开发
- 在开发者工具中点击「上传」
- 填写版本号和描述
- 提交审核

### 2. 等待审核
- 通常 1-3 个工作日
- 审核通过后可发布

### 3. 发布上线
- 在小程序后台点击「发布」
- 选择版本
- 确认发布

---

## 常见问题

**Q: 如何获取新闻数据？**
A: 通过后端 API 接口获取，或使用爬虫定时更新。

**Q: 如何实现定时推送？**
A: 使用微信小程序的订阅消息功能。

**Q: 如何保证内容安全？**
A: 所有新闻内容需要通过内容审核，确保符合微信小程序规范。

---

## 联系方式

- 开发者：小不点
- 邮箱：xiaobudian@example.com
- 微信：xiaobudian_official

---

**最后更新：2026-03-26**

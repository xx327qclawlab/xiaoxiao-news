# -*- coding: utf-8 -*-
"""
小小新闻简报 - 微信小程序后端服务
实时新闻爬取、分类、推送
"""

import json
import time
import os
from datetime import datetime, timedelta

class NewsService:
    """新闻服务类"""
    
    def __init__(self):
        self.categories = {
            '时政': ['时政新闻', '国内新闻', '政策'],
            '科技': ['科技新闻', '互联网', '人工智能', '火箭', '卫星'],
            '体育': ['体育新闻', '足球', '篮球', '奥运'],
            '教育': ['教育新闻', '学习', '考试'],
            '军事': ['军事新闻', '国防'],
            '娱乐': ['娱乐新闻', '明星', '电影'],
            '健康': ['健康新闻', '医学', '养生'],
            '环保': ['环保新闻', '气候', '生态']
        }
        self.news_db = []
        self.user_preferences = {}
    
    def add_news(self, title, category, source, url, snippet, image_url=None):
        """添加新闻"""
        news = {
            'id': len(self.news_db) + 1,
            'title': title,
            'category': category,
            'source': source,
            'url': url,
            'snippet': snippet,
            'image_url': image_url,
            'timestamp': datetime.now().isoformat(),
            'views': 0,
            'likes': 0
        }
        self.news_db.append(news)
        return news
    
    def get_news_by_category(self, category, limit=10):
        """按分类获取新闻"""
        return [n for n in self.news_db if n['category'] == category][:limit]
    
    def get_all_news(self, limit=20):
        """获取所有新闻"""
        return sorted(self.news_db, key=lambda x: x['timestamp'], reverse=True)[:limit]
    
    def get_categories(self):
        """获取所有分类"""
        return list(self.categories.keys())
    
    def search_news(self, keyword):
        """搜索新闻"""
        return [n for n in self.news_db if keyword in n['title'] or keyword in n['snippet']]
    
    def like_news(self, news_id):
        """点赞新闻"""
        for news in self.news_db:
            if news['id'] == news_id:
                news['likes'] += 1
                return news
        return None
    
    def view_news(self, news_id):
        """浏览新闻"""
        for news in self.news_db:
            if news['id'] == news_id:
                news['views'] += 1
                return news
        return None
    
    def set_user_preference(self, user_id, categories):
        """设置用户偏好分类"""
        self.user_preferences[user_id] = categories
    
    def get_personalized_news(self, user_id, limit=20):
        """获取个性化新闻"""
        if user_id not in self.user_preferences:
            return self.get_all_news(limit)
        
        preferred_cats = self.user_preferences[user_id]
        news = [n for n in self.news_db if n['category'] in preferred_cats]
        return sorted(news, key=lambda x: x['timestamp'], reverse=True)[:limit]
    
    def export_api_schema(self):
        """导出 API 接口定义"""
        return {
            'endpoints': {
                'GET /api/news': '获取所有新闻',
                'GET /api/news/category/:cat': '按分类获取新闻',
                'GET /api/news/search': '搜索新闻',
                'GET /api/categories': '获取所有分类',
                'POST /api/news/:id/like': '点赞新闻',
                'POST /api/news/:id/view': '浏览新闻',
                'POST /api/user/preference': '设置用户偏好',
                'GET /api/user/personalized': '获取个性化新闻'
            },
            'categories': self.get_categories()
        }

# 初始化服务
service = NewsService()

# 添加示例新闻
service.add_news(
    title='中国"人造太阳"装置实现千秒稳态运行',
    category='时政',
    source='央视新闻',
    url='https://news.cctv.com',
    snippet='我国在上海临港成功实现1337秒稳态长脉冲运行，刷新商业核聚变世界纪录',
    image_url='https://example.com/sun.jpg'
)

service.add_news(
    title='中国成功发射四维高景二号05、06星',
    category='科技',
    source='新华社',
    url='https://www.xinhuanet.com',
    snippet='长征二号丁运载火箭在太原卫星发射中心成功发射，卫星顺利进入预定轨道',
    image_url='https://example.com/rocket.jpg'
)

service.add_news(
    title='足坛一夜动态：姆巴佩澄清误诊传闻',
    category='体育',
    source='企鹅号',
    url='https://sports.qq.com',
    snippet='足球明星姆巴佩澄清了误诊传闻，还维护了皇马队的医生',
    image_url='https://example.com/football.jpg'
)

# 保存配置
config = {
    'service_name': '小小新闻简报',
    'version': '1.0.0',
    'description': '为小学五年级孩子定制的新闻阅读小程序',
    'categories': service.get_categories(),
    'api_schema': service.export_api_schema(),
    'features': [
        '实时新闻更新',
        '多分类浏览',
        '个性化推荐',
        '新闻搜索',
        '点赞收藏',
        '定时推送'
    ]
}

# 保存到文件
output_path = r'C:\Users\成都工业学院\.qclaw\workspace\news_service_config.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(config, f, ensure_ascii=False, indent=2)

print("[OK] News service backend config generated")
print(f"[FILE] Config: {output_path}")
print(f"[CATEGORIES] {', '.join(service.get_categories())}")
print(f"[NEWS] Sample news loaded: {len(service.news_db)} items")
print("\n[NEXT] Build WeChat mini program frontend")
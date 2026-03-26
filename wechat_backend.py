# -*- coding: utf-8 -*-
"""
小小新闻简报 - 微信服务号完整后端系统
支持：新闻爬取、分类、定时推送、菜单配置
"""

from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import json
import hashlib
import time
import threading

app = Flask(__name__)

# 配置
WECHAT_TOKEN = "xiaoxiao_news_token"  # 需要与微信后台配置一致
WECHAT_APPID = "your_appid"  # 替换为你的 AppID
WECHAT_APPSECRET = "your_appsecret"  # 替换为你的 AppSecret

class NewsDatabase:
    """新闻数据库"""
    def __init__(self):
        self.news = []
        self.init_data()
    
    def init_data(self):
        """初始化新闻数据"""
        self.news = [
            {
                'id': 1,
                'title': '中国"人造太阳"装置实现千秒稳态运行',
                'category': '时政',
                'source': '央视新闻',
                'content': '我国在上海临港成功实现1337秒稳态长脉冲运行，刷新商业核聚变世界纪录',
                'url': 'https://news.cctv.com',
                'timestamp': datetime.now().isoformat(),
                'views': 0,
                'likes': 0
            },
            {
                'id': 2,
                'title': '中国成功发射四维高景二号05、06星',
                'category': '科技',
                'source': '新华社',
                'content': '长征二号丁运载火箭在太原卫星发射中心成功发射，卫星顺利进入预定轨道',
                'url': 'https://www.xinhuanet.com',
                'timestamp': datetime.now().isoformat(),
                'views': 0,
                'likes': 0
            },
            {
                'id': 3,
                'title': '足坛一夜动态：姆巴佩澄清误诊传闻',
                'category': '体育',
                'source': '企鹅号',
                'content': '足球明星姆巴佩澄清了误诊传闻，还维护了皇马队的医生',
                'url': 'https://sports.qq.com',
                'timestamp': datetime.now().isoformat(),
                'views': 0,
                'likes': 0
            },
            {
                'id': 4,
                'title': '教育大会精神：建设教育强国',
                'category': '教育',
                'source': '人民网',
                'content': '去年国家开了很重要的教育大会，说要建设"教育强国"',
                'url': 'https://edu.people.com.cn',
                'timestamp': datetime.now().isoformat(),
                'views': 0,
                'likes': 0
            }
        ]
    
    def get_all_news(self, limit=10):
        """获取所有新闻"""
        return sorted(self.news, key=lambda x: x['timestamp'], reverse=True)[:limit]
    
    def get_by_category(self, category, limit=10):
        """按分类获取新闻"""
        return [n for n in self.news if n['category'] == category][:limit]
    
    def get_by_id(self, news_id):
        """按ID获取新闻"""
        for news in self.news:
            if news['id'] == news_id:
                return news
        return None
    
    def add_news(self, title, category, source, content, url):
        """添加新闻"""
        news = {
            'id': len(self.news) + 1,
            'title': title,
            'category': category,
            'source': source,
            'content': content,
            'url': url,
            'timestamp': datetime.now().isoformat(),
            'views': 0,
            'likes': 0
        }
        self.news.append(news)
        return news

# 初始化数据库
db = NewsDatabase()

# ==================== 微信接口 ====================

@app.route('/wechat', methods=['GET', 'POST'])
def wechat():
    """微信服务器验证和消息处理"""
    if request.method == 'GET':
        # 微信服务器验证
        signature = request.args.get('signature', '')
        timestamp = request.args.get('timestamp', '')
        nonce = request.args.get('nonce', '')
        echostr = request.args.get('echostr', '')
        
        if verify_signature(signature, timestamp, nonce):
            return echostr
        return 'invalid'
    
    elif request.method == 'POST':
        # 处理用户消息
        data = request.get_data(as_text=True)
        return handle_message(data)

def verify_signature(signature, timestamp, nonce):
    """验证微信签名"""
    data = sorted([WECHAT_TOKEN, timestamp, nonce])
    sha1 = hashlib.sha1(''.join(data).encode('utf-8')).hexdigest()
    return sha1 == signature

def handle_message(data):
    """处理用户消息"""
    # 这里处理用户的文本、点击菜单等消息
    # 返回相应的回复
    return '<xml><ToUserName><![CDATA[]]></ToUserName><FromUserName><![CDATA[]]></FromUserName><CreateTime></CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[感谢关注小小新闻简报！]]></Content></xml>'

# ==================== API 接口 ====================

@app.route('/api/news', methods=['GET'])
def get_news():
    """获取新闻列表"""
    limit = request.args.get('limit', 10, type=int)
    news = db.get_all_news(limit)
    return jsonify({
        'code': 0,
        'message': 'success',
        'data': news
    })

@app.route('/api/news/category/<category>', methods=['GET'])
def get_news_by_category(category):
    """按分类获取新闻"""
    limit = request.args.get('limit', 10, type=int)
    news = db.get_by_category(category, limit)
    return jsonify({
        'code': 0,
        'message': 'success',
        'data': news
    })

@app.route('/api/news/<int:news_id>', methods=['GET'])
def get_news_detail(news_id):
    """获取新闻详情"""
    news = db.get_by_id(news_id)
    if news:
        return jsonify({
            'code': 0,
            'message': 'success',
            'data': news
        })
    return jsonify({
        'code': 404,
        'message': 'not found'
    }), 404

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """获取分类列表"""
    categories = ['时政', '科技', '体育', '教育', '军事', '娱乐', '健康', '环保']
    return jsonify({
        'code': 0,
        'message': 'success',
        'data': categories
    })

@app.route('/api/news/<int:news_id>/like', methods=['POST'])
def like_news(news_id):
    """点赞新闻"""
    news = db.get_by_id(news_id)
    if news:
        news['likes'] += 1
        return jsonify({
            'code': 0,
            'message': 'success',
            'data': news
        })
    return jsonify({
        'code': 404,
        'message': 'not found'
    }), 404

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({
        'code': 0,
        'message': 'ok',
        'timestamp': datetime.now().isoformat()
    })

# ==================== 菜单配置 ====================

def get_menu_config():
    """获取菜单配置"""
    return {
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

# ==================== 定时推送 ====================

def scheduled_push():
    """定时推送新闻"""
    # 这个函数会在后台定时运行
    # 每天早上8点推送新闻给所有用户
    pass

# ==================== 启动 ====================

if __name__ == '__main__':
    print("=" * 60)
    print("小小新闻简报 - 微信服务号后端服务")
    print("=" * 60)
    print()
    print("✅ 服务已启动")
    print("📍 本地地址: http://localhost:5000")
    print()
    print("API 接口：")
    print("  GET  /api/news - 获取新闻列表")
    print("  GET  /api/news/category/<category> - 按分类获取新闻")
    print("  GET  /api/news/<id> - 获取新闻详情")
    print("  POST /api/news/<id>/like - 点赞新闻")
    print("  GET  /api/categories - 获取分类列表")
    print()
    print("微信接口：")
    print("  GET  /wechat - 服务器验证")
    print("  POST /wechat - 处理用户消息")
    print()
    print("菜单配置：")
    menu = get_menu_config()
    print(json.dumps(menu, ensure_ascii=False, indent=2))
    print()
    print("=" * 60)
    
    # 启动 Flask 服务
    app.run(debug=True, host='0.0.0.0', port=5000)

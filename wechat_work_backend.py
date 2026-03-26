# -*- coding: utf-8 -*-
"""
小小新闻简报 - 企业微信后端服务
支持：新闻推送、分类浏览、定时推送、菜单配置
"""

from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import json
import hashlib
import hmac
import base64
import requests
import time
import threading

app = Flask(__name__)

# 企业微信配置
CORP_ID = "ww7b2a7bf9120e2dd4"  # 祥祥的qcloud实验室
AGENT_ID = 1000002
AGENT_SECRET = "pa-ak4gfNBxuX8z8ZO6AOkgit-OoW1asllaMHV2HK10"
TOKEN = "xiaoxiao_news_token"
ENCODING_AES_KEY = "1234567890123456789012345678901234567890123"  # 43字符

# 全局变量
access_token = None
token_expire_time = 0

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

# 初始化数据库
db = NewsDatabase()

# ==================== 企业微信 API ====================

def get_access_token():
    """获取企业微信 access_token"""
    global access_token, token_expire_time
    
    if access_token and time.time() < token_expire_time:
        return access_token
    
    url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken"
    params = {
        'corpid': CORP_ID,
        'corpsecret': AGENT_SECRET
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if data.get('errcode') == 0:
            access_token = data.get('access_token')
            token_expire_time = time.time() + 7200  # 2小时
            return access_token
    except Exception as e:
        print(f"Error getting access token: {e}")
    
    return None

def send_message(user_id, message_type, content):
    """发送企业微信消息"""
    token = get_access_token()
    if not token:
        return False
    
    url = "https://qyapi.weixin.qq.com/cgi-bin/message/send"
    
    payload = {
        "touser": user_id,
        "msgtype": message_type,
        "agentid": AGENT_ID,
        message_type: content
    }
    
    try:
        response = requests.post(
            url,
            params={'access_token': token},
            json=payload,
            timeout=10
        )
        return response.json().get('errcode') == 0
    except Exception as e:
        print(f"Error sending message: {e}")
        return False

def send_text_message(user_id, text):
    """发送文本消息"""
    return send_message(user_id, "text", {"content": text})

def send_news_message(user_id, news_list):
    """发送新闻卡片消息"""
    articles = []
    for news in news_list[:10]:  # 最多10条
        articles.append({
            "title": news['title'],
            "description": news['content'][:100],
            "url": news['url'],
            "picurl": ""
        })
    
    return send_message(user_id, "news", {"articles": articles})

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

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """获取分类列表"""
    categories = ['时政', '科技', '体育', '教育', '军事', '娱乐', '健康', '环保']
    return jsonify({
        'code': 0,
        'message': 'success',
        'data': categories
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({
        'code': 0,
        'message': 'ok',
        'timestamp': datetime.now().isoformat()
    })

# ==================== 企业微信回调 ====================

@app.route('/wechat/callback', methods=['GET', 'POST'])
def wechat_callback():
    """企业微信回调接口"""
    if request.method == 'GET':
        # 验证服务器 - 企业微信会发送 GET 请求来验证
        signature = request.args.get('signature', '')
        msg_signature = request.args.get('msg_signature', '')
        timestamp = request.args.get('timestamp', '')
        nonce = request.args.get('nonce', '')
        echostr = request.args.get('echostr', '')
        
        # 验证签名: sort([token, timestamp, nonce]) -> sha1
        data = sorted([TOKEN, timestamp, nonce])
        sha1 = hashlib.sha1(''.join(data).encode('utf-8')).hexdigest()
        
        # 企业微信用 signature 字段验证
        if sha1 == signature or sha1 == msg_signature:
            return echostr
        return 'signature mismatch: {} vs {}'.format(sha1, signature)
    
    elif request.method == 'POST':
        # 处理消息
        return handle_message(request)

def handle_message(request):
    """处理企业微信消息"""
    # 这里处理用户的消息和菜单点击事件
    return '<xml><ToUserName><![CDATA[]]></ToUserName><FromUserName><![CDATA[]]></FromUserName><CreateTime></CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[感谢关注小小新闻简报！]]></Content></xml>'

# ==================== 定时推送 ====================

def scheduled_push():
    """定时推送新闻"""
    # 这个函数会在后台定时运行
    # 每天早上8点推送新闻给所有用户
    pass

# ==================== 启动 ====================

if __name__ == '__main__':
    print("=" * 60)
    print("小小新闻简报 - 企业微信后端服务")
    print("=" * 60)
    print()
    print("配置信息：")
    print(f"  Agent ID: {AGENT_ID}")
    print(f"  Agent Secret: {AGENT_SECRET[:20]}...")
    print()
    print("API 接口：")
    print("  GET  /api/news - 获取新闻列表")
    print("  GET  /api/news/category/<category> - 按分类获取新闻")
    print("  GET  /api/categories - 获取分类列表")
    print("  GET  /api/health - 健康检查")
    print()
    print("企业微信接口：")
    print("  GET  /wechat/callback - 服务器验证")
    print("  POST /wechat/callback - 处理消息")
    print()
    print("=" * 60)
    
    # 启动 Flask 服务
    app.run(debug=True, host='0.0.0.0', port=5000)

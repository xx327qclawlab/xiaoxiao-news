# -*- coding: utf-8 -*-
"""
小小新闻简报 - 微信服务号后端演示
"""

from datetime import datetime
import json

class WechatNewsService:
    """微信服务号新闻服务"""
    
    def __init__(self):
        self.news_db = []
        self.init_sample_news()
    
    def init_sample_news(self):
        """初始化示例新闻"""
        sample_news = [
            {
                'id': 1,
                'title': '中国"人造太阳"装置实现千秒稳态运行',
                'category': '时政',
                'source': '央视新闻',
                'content': '''
【时政大事件】中国"人造太阳"破世界纪录！

我国的"洪荒70"装置在上海成功运行了1337秒（约22分钟），创造了商业核聚变的世界纪录！

👉 给孩子的话：
这个装置叫"人造太阳"，因为它能像太阳一样产生巨大能量。未来可能是人类最重要的清洁能源！

想象一下，如果我们能在地球上造一个像太阳一样发光发热的东西，那该多厉害！

📰 来源：央视新闻
🔗 点击查看详情
                ''',
                'image': '☀️',
                'timestamp': '2026-03-26 06:14'
            },
            {
                'id': 2,
                'title': '中国成功发射两颗遥感卫星',
                'category': '科技',
                'source': '新华社',
                'content': '''
【科技新发现】中国成功发射两颗遥感卫星！

今天早上6:51，长征二号火箭在太原卫星发射中心成功发射四维高景二号05、06星！

👉 给孩子的话：
这两颗卫星就像"太空眼睛"，不管白天黑夜、刮风下雨，都能看清地球表面。可以监测农作物、帮助救灾哦！

这是长征火箭的第634次飞行，也是今年我国商业遥感卫星领域的又一次重要突破。

📰 来源：新华社
🔗 点击查看详情
                ''',
                'image': '🚀',
                'timestamp': '2026-03-26 07:50'
            },
            {
                'id': 3,
                'title': '足坛一夜动态：姆巴佩澄清误诊传闻',
                'category': '体育',
                'source': '企鹅号',
                'content': '''
【体育速递】足球明星那些事儿

- 姆巴佩（法国足球明星）最近受伤了，但他澄清说不是医生误诊，还很维护皇马队的医生呢！
- CBA篮球赛今晚有焦点战：辽宁队冲击7连胜！

👉 小思考：
运动员受伤后，团队怎么互相支持很重要，这不光在体育比赛里，学习和生活中也是一样！

📰 来源：企鹅号
🔗 点击查看详情
                ''',
                'image': '⚽',
                'timestamp': '2026-03-26 06:42'
            },
            {
                'id': 4,
                'title': '教育大会精神：建设教育强国',
                'category': '教育',
                'source': '人民网',
                'content': '''
【学习园地】教育大会精神

去年国家开了很重要的教育大会，说要建设"教育强国"。意思就是让每个小朋友都能接受更好的教育，学到更多本领！

👉 给孩子的话：
这意味着：
- 学校会有更好的设施
- 老师会有更好的培训
- 你能学到更多有趣的东西
- 每个孩子都有机会成为最好的自己

📰 来源：人民网
🔗 点击查看详情
                ''',
                'image': '📚',
                'timestamp': '2026-03-26 08:30'
            }
        ]
        self.news_db = sample_news
    
    def get_news_list(self):
        """获取新闻列表"""
        return self.news_db
    
    def get_news_by_category(self, category):
        """按分类获取新闻"""
        return [n for n in self.news_db if n['category'] == category]
    
    def get_news_detail(self, news_id):
        """获取新闻详情"""
        for news in self.news_db:
            if news['id'] == news_id:
                return news
        return None
    
    def generate_wechat_message(self, news):
        """生成微信消息格式"""
        return f"""
{news['image']} {news['title']}

{news['content']}

---
小小新闻简报 | 每天为你播报有趣的世界
        """
    
    def generate_menu_json(self):
        """生成微信菜单 JSON"""
        return {
            "button": [
                {
                    "type": "view",
                    "name": "📰 今日新闻",
                    "url": "https://example.com/news"
                },
                {
                    "name": "分类浏览",
                    "sub_button": [
                        {
                            "type": "view",
                            "name": "🌟 时政",
                            "url": "https://example.com/category/时政"
                        },
                        {
                            "type": "view",
                            "name": "🚀 科技",
                            "url": "https://example.com/category/科技"
                        },
                        {
                            "type": "view",
                            "name": "⚽ 体育",
                            "url": "https://example.com/category/体育"
                        },
                        {
                            "type": "view",
                            "name": "📚 教育",
                            "url": "https://example.com/category/教育"
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

# 初始化服务
service = WechatNewsService()

# 生成演示消息
print("=" * 60)
print("小小新闻简报 - 微信服务号演示")
print("=" * 60)
print()

for news in service.get_news_list():
    print(service.generate_wechat_message(news))
    print()
    print("-" * 60)
    print()

# 保存菜单配置
menu_config = service.generate_menu_json()
with open(r'C:\Users\成都工业学院\.qclaw\workspace\wechat_menu.json', 'w', encoding='utf-8') as f:
    json.dump(menu_config, f, ensure_ascii=False, indent=2)

print("\n✅ 演示完成！")
print("📁 菜单配置已保存到 wechat_menu.json")
print("\n接下来的步骤：")
print("1. 注册微信服务号")
print("2. 配置后端服务")
print("3. 设置自定义菜单")
print("4. 用户关注后自动推送新闻")
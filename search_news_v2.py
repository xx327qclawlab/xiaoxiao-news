import urllib.request
import urllib.parse
import json
import time
import os
import sys
import ssl

# Force UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

# Get port
PORT = os.environ.get('AUTH_GATEWAY_PORT', '19000')
FROM_TIME = int(time.time()) - 86400  # Last 24 hours

def search(keyword):
    url = f"http://localhost:{PORT}/proxy/prosearch/search"
    data = json.dumps({"keyword": keyword, "from_time": FROM_TIME}).encode('utf-8')
    headers = {'Content-Type': 'application/json'}
    req = urllib.request.Request(url, data=data, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        return {"success": False, "message": str(e)}

def clean_text(text):
    # Remove emojis for GBK compatibility
    return text.replace('⭐', '*').replace('📰', '').replace('🌍', '').replace('💼', '').replace('💻', '')

def get_image_url(keyword):
    """Search for an image related to the keyword"""
    try:
        # Use Unsplash API for free images
        url = f"https://source.unsplash.com/400x200/?{urllib.parse.quote(keyword)}"
        return url
    except:
        return None

# Search for news
print("=== 搜索新闻中 ===\n")

# 时政新闻
result1 = search("今日时政新闻 国内 人造太阳")
news_data = []

if result1.get('success') and result1.get('data', {}).get('docs'):
    docs = result1['data']['docs'][:2]
    for doc in docs:
        news_data.append({
            'type': '时政',
            'title': doc.get('title', ''),
            'url': doc.get('url', ''),
            'site': doc.get('site', ''),
            'snippet': doc.get('passage', '')[:150]
        })

# 科技新闻
result2 = search("今日科技新闻 火箭 卫星")
if result2.get('success') and result2.get('data', {}).get('docs'):
    docs = result2['data']['docs'][:2]
    for doc in docs:
        news_data.append({
            'type': '科技',
            'title': doc.get('title', ''),
            'url': doc.get('url', ''),
            'site': doc.get('site', ''),
            'snippet': doc.get('passage', '')[:150]
        })

# 体育新闻
result3 = search("今日体育新闻")
if result3.get('success') and result3.get('data', {}).get('docs'):
    docs = result3['data']['docs'][:2]
    for doc in docs:
        news_data.append({
            'type': '体育',
            'title': doc.get('title', ''),
            'url': doc.get('url', ''),
            'site': doc.get('site', ''),
            'snippet': doc.get('passage', '')[:150]
        })

# Output results
for news in news_data:
    print(f"【{news['type']}】{news['title']}")
    print(f"来源: {news['site']}")
    print(f"链接: {news['url']}")
    print(f"摘要: {news['snippet']}")
    print()

# Save to file for further processing
with open(r'C:\Users\成都工业学院\.qclaw\workspace\news_data.json', 'w', encoding='utf-8') as f:
    json.dump(news_data, f, ensure_ascii=False, indent=2)

print(f"\n共获取 {len(news_data)} 条新闻，已保存到 news_data.json")
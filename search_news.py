import urllib.request
import urllib.parse
import json
import time
import os
import sys

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

# Search for news
print("=== 时政新闻 ===")
result1 = search("今日时政新闻 国内")
if result1.get('success'):
    print(clean_text(result1.get('message', '')[:800]))
else:
    print(result1.get('message'))

print("\n=== 体育新闻 ===")
result2 = search("今日体育新闻")
if result2.get('success'):
    print(clean_text(result2.get('message', '')[:800]))
else:
    print(result2.get('message'))

print("\n=== 教育新闻 ===")
result3 = search("教育新闻 学习")
if result3.get('success'):
    print(clean_text(result3.get('message', '')[:800]))
else:
    print(result3.get('message'))

print("\n=== 科技新闻 ===")
result4 = search("今日科技新闻")
if result4.get('success'):
    print(clean_text(result4.get('message', '')[:800]))
else:
    print(result4.get('message'))
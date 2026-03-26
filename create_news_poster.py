from PIL import Image, ImageDraw, ImageFont
import json
import os

# Read news data
with open(r'C:\Users\成都工业学院\.qclaw\workspace\news_data.json', 'r', encoding='utf-8') as f:
    news_data = json.load(f)

# Create poster
width, height = 800, 1200
img = Image.new('RGB', (width, height), '#1a1a2e')
draw = ImageDraw.Draw(img)

# Load fonts
try:
    font_title = ImageFont.truetype("msyh.ttc", 36)
    font_sub = ImageFont.truetype("msyh.ttc", 24)
    font_body = ImageFont.truetype("msyh.ttc", 18)
    font_small = ImageFont.truetype("msyh.ttc", 14)
except:
    font_title = font_sub = font_body = font_small = ImageFont.load_default()

# Header
draw.rectangle([0, 0, width, 100], fill='#e94560')
draw.text((width//2, 50), "📰 小小新闻简报", fill='white', anchor='mm', font=font_title)

# Date
draw.text((width//2, 120), "2026年3月26日 星期四", fill='#aaaaaa', anchor='mm', font=font_small)

# News content
y = 160
colors = {'时政': '#4ecdc4', '科技': '#45b7d1', '体育': '#f9ca24', '教育': '#6c5ce7'}

for news in news_data[:4]:  # Limit to 4 news items
    # Category label
    cat_color = colors.get(news['type'], '#ffffff')
    draw.rectangle([20, y, 80, y+25], fill=cat_color)
    draw.text((50, y+12), news['type'], fill='white', anchor='mm', font=font_small)
    
    # Title
    title = news['title'][:30] + '...' if len(news['title']) > 30 else news['title']
    draw.text((90, y+5), title, fill='white', font=font_sub)
    
    # Source
    draw.text((90, y+35), f"📍 来源: {news['site']}", fill='#888888', font=font_small)
    
    # Snippet
    snippet = news['snippet'][:80].replace('<p>', '').replace('</p>', '').replace('<strong>', '').replace('</strong>', '')
    snippet = snippet[:77] + '...' if len(snippet) > 77 else snippet
    draw.text((90, y+60), snippet, fill='#cccccc', font=font_small)
    
    y += 120

# Footer
draw.rectangle([0, height-80, width, height], fill='#16213e')
draw.text((width//2, height-50), "🐾 小不点出品 | 每天带你看世界", fill='white', anchor='mm', font=font_sub)
draw.text((width//2, height-25), "适合小学五年级小朋友阅读", fill='#888888', anchor='mm', font=font_small)

# Save
output_path = r'C:\Users\成都工业学院\.qclaw\workspace\news_poster.png'
img.save(output_path, 'PNG')
print(f"海报已生成: {output_path}")
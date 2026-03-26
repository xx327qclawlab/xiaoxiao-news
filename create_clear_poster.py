from PIL import Image, ImageDraw, ImageFont
import json

# Read news data
with open(r'C:\Users\成都工业学院\.qclaw\workspace\news_data.json', 'r', encoding='utf-8') as f:
    news_data = json.load(f)

# Create a larger, clearer poster
width, height = 1200, 2000
img = Image.new('RGB', (width, height), '#ffffff')
draw = ImageDraw.Draw(img)

# Load fonts - bigger sizes
try:
    font_title = ImageFont.truetype("msyh.ttc", 60)
    font_sub = ImageFont.truetype("msyh.ttc", 36)
    font_body = ImageFont.truetype("msyh.ttc", 28)
    font_small = ImageFont.truetype("msyh.ttc", 22)
except:
    font_title = font_sub = font_body = font_small = ImageFont.load_default()

# Header
draw.rectangle([0, 0, width, 150], fill='#1a5fb4')
draw.text((width//2, 75), "小小新闻简报", fill='#ffffff', anchor='mm', font=font_title)
draw.text((width//2, 130), "2026年3月26日 星期四 | 小学五年级版", fill='#ffffff', anchor='mm', font=font_sub)

# News sections with clear layout
y = 180
colors = {'时政': '#e8f4fd', '科技': '#e8f5e9', '体育': '#fff3e0', '教育': '#fce4ec'}
type_labels = {'时政': '时政大事件', '科技': '科技新发现', '体育': '体育速递', '教育': '学习园地'}
icons = {'时政': '🌟', '科技': '🚀', '体育': '⚽', '教育': '📚'}

for news in news_data[:4]:
    news_type = news['type']
    bg_color = colors.get(news_type, '#ffffff')
    
    # Section box
    draw.rectangle([40, y, width-40, y+380], fill=bg_color, outline='#cccccc', width=2)
    
    # Type header
    draw.rectangle([40, y, width-40, y+60], fill='#1a5fb4')
    icon = icons.get(news_type, '')
    draw.text((width//2, y+30), f"{icon} {type_labels.get(news_type, news_type)}", fill='#ffffff', anchor='mm', font=font_sub)
    
    # Title
    title = news['title']
    if len(title) > 35:
        title = title[:32] + '...'
    draw.text((60, y+80), title, fill='#333333', font=font_body)
    
    # Snippet
    snippet = news['snippet'].replace('<p>', '').replace('</p>', '').replace('<strong>', '').replace('</strong>', '').replace('&#x2019;', "'")
    snippet = snippet.replace('&#x201C;', '"').replace('&#x201D;', '"')
    if len(snippet) > 100:
        snippet = snippet[:97] + '...'
    
    # Word wrap for snippet
    words = snippet
    for i in range(0, len(words), 45):
        line = words[i:i+45]
        draw.text((60, y+130+i//45*35), line, fill='#555555', font=font_small)
    
    # Source
    draw.text((60, y+280), f"📰 来源: {news['site']}", fill='#ff6b35', font=font_small)
    draw.text((60, y+320), "🔗 点击链接查看详情", fill='#4285f4', font=font_small)
    
    y += 400

# Footer
draw.rectangle([0, height-120, width, height], fill='#1a5fb4')
draw.text((width//2, height-75), "🐾 小不点出品", fill='#ffffff', anchor='mm', font=font_sub)
draw.text((width//2, height-35), "每天带你认识这个有趣的世界", fill='#ffffff', anchor='mm', font=font_small)

# Save
output_path = r'C:\Users\成都工业学院\.qclaw\workspace\news_poster_clear.png'
img.save(output_path, 'PNG', quality=95)
print(f"清晰版海报已生成: {output_path}")
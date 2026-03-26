# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
import random

# 创建一个高质量的乒乓球比赛海报
width, height = 1200, 1600
img = Image.new('RGB', (width, height), '#1a1a2e')
draw = ImageDraw.Draw(img)

# 背景装饰 - 抽象的运动线条
colors = ['#e94560', '#0f3460', '#16213e', '#533483']

# 动态背景圆圈
for i in range(15):
    x = random.randint(0, width)
    y = random.randint(0, height)
    r = random.randint(50, 300)
    color = random.choice(colors)
    draw.ellipse([x-r, y-r, x+r, y+r], fill=color, outline=None)

# 添加噪点纹理效果（模拟）
for _ in range(3000):
    x = random.randint(0, width)
    y = random.randint(0, height)
    draw.point((x, y), fill=(255, 255, 255, 30))

# 主标题
title = "乒乓球比赛"
subtitle = "TABLE TENNIS CHAMPIONSHIP"

# 使用系统字体
try:
    font_large = ImageFont.truetype("msyh.ttc", 180)
    font_sub = ImageFont.truetype("msyh.ttc", 60)
    font_info = ImageFont.truetype("msyh.ttc", 40)
except:
    font_large = ImageFont.load_default()
    font_sub = ImageFont.load_default()
    font_info = ImageFont.load_default()

# 绘制标题
draw.text((width//2, 300), title, fill='#ffffff', anchor='mm', font=font_large)
draw.text((width//2, 500), subtitle, fill='#e94560', anchor='mm', font=font_sub)

# 比赛信息框
info_box_y = 700
draw.rectangle([200, info_box_y, width-200, info_box_y+500], fill='#16213e', outline='#e94560', width=3)

# 比赛详情
details = [
    "📅 比赛日期：2026年4月15日",
    "📍 比赛地点：体育馆一楼",
    "👥 参赛对象：全体师生",
    "🏆 奖项设置：冠军、亚军、季军",
    "⏰ 报名截止：2026年4月10日"
]

for i, detail in enumerate(details):
    draw.text((250, info_box_y + 80 + i*80), detail, fill='#ffffff', font=font_info)

# 底部装饰
draw.rectangle([0, height-150, width, height], fill='#e94560')
draw.text((width//2, height-75), "欢迎围观 · 友谊第一 · 比赛第二", fill='#ffffff', anchor='mm', font=font_info)

# 添加乒乓球拍和球的装饰
# 球拍1
draw.ellipse([100, 200, 250, 350], fill='#c9a227', outline='#8b7355', width=3)
draw.ellipse([120, 220, 230, 330], fill='#8b4513')

# 球拍2  
draw.ellipse([width-250, 800, width-100, 950], fill='#c9a227', outline='#8b7355', width=3)
draw.ellipse([width-230, 820, width-120, 930], fill='#8b4513')

# 乒乓球
draw.ellipse([width//2-20, 600, width//2+20, 640], fill='#ffffff')

# 保存
output_path = r'C:\Users\成都工业学院\.qclaw\workspace\乒乓球比赛海报.png'
img.save(output_path, 'PNG', quality=95)
print(f"海报已生成: {output_path}")

from PIL import Image, ImageDraw, ImageFont
import io

# 创建 750x750 的图片
width, height = 750, 750
img = Image.new('RGB', (width, height), '#f0f4f8')
draw = ImageDraw.Draw(img)

# 背景渐变效果（用矩形模拟）
for i in range(height):
    color_value = int(240 + (20 * i / height))
    draw.line([(0, i), (width, i)], fill=(240, 244, 248))

# 绘制实验室背景
# 实验台
draw.rectangle([50, 400, 700, 650], fill='#8B7355', outline='#654321', width=3)

# 实验器材 - 烧杯
draw.polygon([(150, 350), (180, 500), (200, 500), (220, 350)], fill='#87CEEB', outline='#4682B4', width=2)
draw.line([(150, 350), (220, 350)], fill='#4682B4', width=2)

# 实验器材 - 试管
draw.rectangle([280, 300, 310, 480], fill='#E6F3FF', outline='#4682B4', width=2)
draw.ellipse([275, 295, 315, 315], fill='#E6F3FF', outline='#4682B4', width=2)

# 实验器材 - 烧瓶
draw.ellipse([380, 320, 450, 420], fill='#FFE4B5', outline='#FF8C00', width=2)
draw.rectangle([400, 300, 430, 320], fill='#FFE4B5', outline='#FF8C00', width=2)

# 绘制小男孩
# 头部
draw.ellipse([320, 80, 420, 180], fill='#FDBCB4', outline='#8B4513', width=2)

# 眼睛
draw.ellipse([340, 110, 355, 125], fill='#000000')
draw.ellipse([385, 110, 400, 125], fill='#000000')
draw.ellipse([345, 115, 350, 120], fill='#FFFFFF')
draw.ellipse([390, 115, 395, 120], fill='#FFFFFF')

# 嘴巴
draw.arc([(345, 130), (395, 160)], 0, 180, fill='#8B4513', width=2)

# 身体
draw.rectangle([330, 180, 410, 280], fill='#FF6B6B', outline='#8B0000', width=2)

# 手臂
draw.rectangle([310, 190, 330, 260], fill='#FDBCB4', outline='#8B4513', width=2)
draw.rectangle([410, 190, 430, 260], fill='#FDBCB4', outline='#8B4513', width=2)

# 腿
draw.rectangle([340, 280, 360, 380], fill='#4169E1', outline='#000080', width=2)
draw.rectangle([380, 280, 400, 380], fill='#4169E1', outline='#000080', width=2)

# 鞋子
draw.rectangle([335, 380, 365, 400], fill='#000000')
draw.rectangle([375, 380, 405, 400], fill='#000000')

# 绘制 QClaw 标志
# 背景圆形
draw.ellipse([600, 50, 720, 170], fill='#1a5fb4', outline='#ffffff', width=3)

# Q 字母
draw.ellipse([615, 65, 655, 105], fill='#ffffff', outline='#1a5fb4', width=2)
draw.line([(650, 100), (665, 115)], fill='#ffffff', width=3)

# C 字母
draw.arc([(660, 65), (700, 105)], 90, 270, fill='#ffffff', width=3)

# 装饰线
draw.line([(610, 160), (710, 160)], fill='#1a5fb4', width=2)

# 添加文字 "QClaw Lab"
try:
    font_large = ImageFont.truetype("msyh.ttc", 48)
    font_small = ImageFont.truetype("msyh.ttc", 24)
except:
    font_large = ImageFont.load_default()
    font_small = ImageFont.load_default()

# 底部文字
draw.text((375, 680), "QClaw Lab", fill='#1a5fb4', anchor='mm', font=font_large)
draw.text((375, 720), "Experiment Center", fill='#666666', anchor='mm', font=font_small)

# 保存为 JPG
output_path = r'C:\Users\成都工业学院\.qclaw\workspace\qclaw_lab_logo.jpg'
img.save(output_path, 'JPEG', quality=95, optimize=True)

# 检查文件大小
import os
file_size = os.path.getsize(output_path) / (1024 * 1024)  # 转换为 MB
print(f"Logo 已生成: {output_path}")
print(f"尺寸: 750x750")
print(f"文件大小: {file_size:.2f} MB")
print(f"格式: JPG")

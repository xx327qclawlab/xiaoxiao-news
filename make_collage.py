from PIL import Image, ImageDraw, ImageFont
import os

# 获取所有证书图片
cert_dir = r'C:\qclaw_temp\certificates'
images = [os.path.join(cert_dir, f) for f in os.listdir(cert_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
print(f'找到 {len(images)} 张证书')

# 创建画布 - 宽幅展示
canvas = Image.new('RGB', (1800, 1200), (245, 245, 250))
draw = ImageDraw.Draw(canvas)

# 定义不同尺寸的证书框（模拟不同证书）
frames = [
    # 底层 - 大证书（背景层）
    {'x': 100, 'y': 150, 'w': 500, 'h': 350, 'angle': -8},
    {'x': 700, 'y': 180, 'w': 520, 'h': 360, 'angle': 5},
    {'x': 1300, 'y': 160, 'w': 480, 'h': 340, 'angle': -3},
    # 中层
    {'x': 200, 'y': 400, 'w': 450, 'h': 320, 'angle': 10},
    {'x': 550, 'y': 450, 'w': 480, 'h': 330, 'angle': -5},
    {'x': 1050, 'y': 420, 'w': 460, 'h': 325, 'angle': 7},
    {'x': 1400, 'y': 480, 'w': 380, 'h': 280, 'angle': -10},
    # 前层 - 小证书（重要展示）
    {'x': 50, 'y': 650, 'w': 400, 'h': 280, 'angle': 12},
    {'x': 350, 'y': 720, 'w': 420, 'h': 300, 'angle': -6},
    {'x': 750, 'y': 700, 'w': 380, 'h': 270, 'angle': 8},
    {'x': 1100, 'y': 750, 'w': 350, 'h': 250, 'angle': -4},
    {'x': 1450, 'y': 680, 'w': 320, 'h': 230, 'angle': 15},
]

# 加载并应用所有证书
for i, frame in enumerate(frames):
    if i < len(images):
        img = Image.open(images[i])
    else:
        # 循环使用已有证书
        img = Image.open(images[i % len(images)])
    
    # 调整尺寸
    img = img.resize((frame['w'], frame['h']), Image.Resampling.LANCZOS)
    
    # 旋转
    if frame['angle'] != 0:
        img = img.rotate(frame['angle'], expand=True, fillcolor=(255,255,255))
    
    # 添加投影效果
    shadow_layer = Image.new('RGBA', (img.width + 25, img.height + 25), (0,0,0,0))
    for offset in range(20, 0, -4):
        alpha = int(40 * (20 - offset) / 20)
        shadow_layer.paste((0,0,0,alpha), (offset, offset))
    
    # 转换为RGBA
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    # 合成投影
    canvas.paste(shadow_layer, (frame['x']-12, frame['y']-12), shadow_layer)
    # 合成证书
    canvas.paste(img, (frame['x'], frame['y']), img)

# 添加装饰元素
# 标题背景
title_bg = Image.new('RGBA', (1800, 120), (255,255,255,230))
canvas.paste(title_bg, (0, 0), title_bg)

# 学院名称
try:
    font_large = ImageFont.truetype('msyh.ttc', 72)
    font_small = ImageFont.truetype('msyh.ttc', 36)
except:
    font_large = ImageFont.load_default()
    font_small = ImageFont.load_default()

draw = ImageDraw.Draw(canvas)
draw.text((900, 50), '成都工业学院', fill=(40, 60, 100), font=font_large, anchor='mm')
draw.text((900, 95), '国际化课程与专业建设成果展', fill=(80, 100, 140), font=font_small, anchor='mm')

# 添加装饰线条
draw.line([(100, 130), (1700, 130)], fill=(200, 180, 100), width=3)

# 添加飘带装饰
ribbon_color = (180, 60, 60)
draw.polygon([(0, 0), (80, 0), (100, 40), (80, 80), (0, 80)], fill=ribbon_color)
draw.polygon([(1800, 0), (1720, 0), (1700, 40), (1720, 80), (1800, 80)], fill=ribbon_color)

# 添加底部装饰
draw.rectangle([0, 1100, 1800, 1200], fill=(40, 60, 100))

output_path = r'C:\qclaw_temp\certificates_collage_designed.png'
canvas.save(output_path, 'PNG', quality=95)
print(f'已保存: {output_path}')

from PIL import Image, ImageDraw, ImageFont
import math

# 创建高分辨率图片（750x750）
width, height = 750, 750
img = Image.new('RGB', (width, height), '#f8f9fa')
draw = ImageDraw.Draw(img, 'RGBA')

# 专业色彩系统
DARK_BLUE = (13, 71, 161)      # #0D47A1
LIGHT_BLUE = (30, 136, 229)    # #1E88E5
CYAN = (0, 188, 212)           # #00BCD4
LIGHT_CYAN = (179, 229, 252)   # #B3E5FC
WHITE = (255, 255, 255)
GRAY = (55, 71, 79)            # #37474F

# 绘制渐变背景
for y in range(height):
    ratio = y / height
    r = int(248 - ratio * 8)
    g = int(249 - ratio * 9)
    b = int(250 - ratio * 8)
    draw.line([(0, y), (width, y)], fill=(r, g, b))

# 绘制科技网格
grid_color = (208, 232, 242, 76)
for x in range(0, width + 1, 75):
    draw.line([(x, 0), (x, height)], fill=grid_color, width=1)
for y in range(0, height + 1, 75):
    draw.line([(0, y), (width, y)], fill=grid_color, width=1)

# 中心点
cx, cy = width // 2, height // 2

# 绘制主圆形背景（带阴影）
shadow_radius = 285
for i in range(shadow_radius, 275, -1):
    alpha = int(30 * (1 - (shadow_radius - i) / 10))
    draw.ellipse(
        [cx - i, cy - i, cx + i, cy + i],
        fill=(0, 0, 0, alpha)
    )

# 主圆形（渐变效果）
main_radius = 280
for r in range(main_radius, 0, -2):
    ratio = (main_radius - r) / main_radius
    # 从浅蓝到深蓝的渐变
    color_r = int(30 + (30 - 30) * ratio)
    color_g = int(136 - 50 * ratio)
    color_b = int(229 - 68 * ratio)
    draw.ellipse(
        [cx - r, cy - r, cx + r, cy + r],
        fill=(color_r, color_g, color_b)
    )

# 内圆装饰线
draw.ellipse([cx - 270, cy - 270, cx + 270, cy + 270], 
             outline=CYAN, width=2)
draw.ellipse([cx - 260, cy - 260, cx + 260, cy + 260], 
             outline=CYAN, width=1)

# ===== 绘制小男孩 =====
head_y = cy - 100
head_r = 42

# 头部（带阴影）
for i in range(head_r, 0, -1):
    alpha = int(50 * (1 - i / head_r))
    draw.ellipse(
        [cx - i - 2, head_y - i - 2, cx + i - 2, head_y + i - 2],
        fill=(0, 0, 0, alpha)
    )

draw.ellipse([cx - head_r, head_y - head_r, cx + head_r, head_y + head_r],
             fill=LIGHT_CYAN, outline=(0, 151, 167), width=2)

# 眼睛
eye_y = head_y - 12
draw.ellipse([cx - 18, eye_y - 8, cx - 8, eye_y + 2], fill=DARK_BLUE)
draw.ellipse([cx + 8, eye_y - 8, cx + 18, eye_y + 2], fill=DARK_BLUE)
draw.ellipse([cx - 16, eye_y - 6, cx - 12, eye_y - 2], fill=WHITE)
draw.ellipse([cx + 10, eye_y - 6, cx + 14, eye_y - 2], fill=WHITE)

# 嘴巴（微笑）
mouth_y = head_y + 18
draw.arc([cx - 18, mouth_y - 8, cx + 18, mouth_y + 12],
         0, 180, fill=CYAN, width=2)

# 身体
body_top = head_y + head_r + 8
body_h = 75
body_w = 50

# 身体阴影
for i in range(5, 0, -1):
    alpha = int(40 * (1 - i / 5))
    draw.rectangle(
        [cx - body_w // 2 - i, body_top - i,
         cx + body_w // 2 + i, body_top + body_h + i],
        fill=(0, 0, 0, alpha)
    )

draw.rectangle([cx - body_w // 2, body_top, cx + body_w // 2, body_top + body_h],
               fill=CYAN, outline=(0, 151, 167), width=2)

# 手臂
arm_y = body_top + 20
arm_len = 55
draw.line([cx - body_w // 2, arm_y, cx - body_w // 2 - arm_len, arm_y],
          fill=LIGHT_CYAN, width=7)
draw.line([cx + body_w // 2, arm_y, cx + body_w // 2 + arm_len, arm_y],
          fill=LIGHT_CYAN, width=7)

# 腿
leg_top = body_top + body_h
leg_h = 50
draw.rectangle([cx - 16, leg_top, cx - 6, leg_top + leg_h], fill=CYAN)
draw.rectangle([cx + 6, leg_top, cx + 16, leg_top + leg_h], fill=CYAN)

# 鞋子
draw.ellipse([cx - 18, leg_top + leg_h, cx - 4, leg_top + leg_h + 8], fill=DARK_BLUE)
draw.ellipse([cx + 4, leg_top + leg_h, cx + 18, leg_top + leg_h + 8], fill=DARK_BLUE)

# ===== 绘制实验器材 =====

# 左侧烧杯
beaker_x = cx - 130
beaker_y = cy + 50

# 烧杯阴影
for i in range(3, 0, -1):
    alpha = int(30 * (1 - i / 3))
    draw.polygon(
        [(beaker_x - 18 - i, beaker_y - 35 - i),
         (beaker_x + 18 - i, beaker_y - 35 - i),
         (beaker_x + 12 + i, beaker_y + 35 + i),
         (beaker_x - 12 + i, beaker_y + 35 + i)],
        fill=(0, 0, 0, alpha)
    )

draw.polygon([(beaker_x - 18, beaker_y - 35),
              (beaker_x + 18, beaker_y - 35),
              (beaker_x + 12, beaker_y + 35),
              (beaker_x - 12, beaker_y + 35)],
             fill=LIGHT_CYAN, outline=CYAN, width=2)

# 烧杯液体
draw.polygon([(beaker_x - 10, beaker_y + 5),
              (beaker_x + 10, beaker_y + 5),
              (beaker_x + 6, beaker_y + 28),
              (beaker_x - 6, beaker_y + 28)],
             fill=CYAN)

# 烧杯口
draw.line([beaker_x - 18, beaker_y - 35, beaker_x - 22, beaker_y - 42],
          fill=CYAN, width=2)

# 右侧试管
tube_x = cx + 130
tube_y = cy + 50

# 试管阴影
for i in range(3, 0, -1):
    alpha = int(30 * (1 - i / 3))
    draw.rectangle(
        [tube_x - 12 - i, tube_y - 45 - i,
         tube_x + 12 + i, tube_y + 35 + i],
        fill=(0, 0, 0, alpha)
    )

draw.rectangle([tube_x - 12, tube_y - 45, tube_x + 12, tube_y + 35],
               fill=LIGHT_CYAN, outline=CYAN, width=2)

# 试管口
draw.ellipse([tube_x - 14, tube_y - 50, tube_x + 14, tube_y - 40],
             fill=LIGHT_CYAN, outline=CYAN, width=2)

# 试管液体
draw.rectangle([tube_x - 10, tube_y - 15, tube_x + 10, tube_y + 20],
               fill=CYAN)

# ===== 动态轨迹线 =====
for angle in [0, 72, 144, 216, 288]:
    rad = math.radians(angle)
    start_x = cx + 200 * math.cos(rad)
    start_y = cy + 200 * math.sin(rad)
    end_x = cx + 245 * math.cos(rad)
    end_y = cy + 245 * math.sin(rad)
    draw.line([start_x, start_y, end_x, end_y], fill=CYAN, width=2)
    draw.ellipse([end_x - 4, end_y - 4, end_x + 4, end_y + 4], fill=CYAN)

# ===== 文字 =====
try:
    font_title = ImageFont.truetype("msyh.ttc", 72)
    font_sub = ImageFont.truetype("msyh.ttc", 26)
except:
    font_title = ImageFont.load_default()
    font_sub = ImageFont.load_default()

# 主标题
draw.text((cx, height - 110), "QClaw Lab",
          fill=DARK_BLUE, anchor='mm', font=font_title)

# 副标题
draw.text((cx, height - 50), "Experiment Center",
          fill=GRAY, anchor='mm', font=font_sub)

# 底部装饰线
draw.line([cx - 150, height - 30, cx + 150, height - 30],
          fill=CYAN, width=2)

# 保存为高质量 JPG
output_path = r'C:\Users\成都工业学院\.qclaw\workspace\qclaw_lab_logo_hd.jpg'
img.save(output_path, 'JPEG', quality=98, optimize=True)

import os
file_size = os.path.getsize(output_path) / (1024 * 1024)
print(f"[SUCCESS] HD Logo Generated")
print(f"[SIZE] 750x750 pixels")
print(f"[FILE] {file_size:.2f} MB")
print(f"[PATH] {output_path}")

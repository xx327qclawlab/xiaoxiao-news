from PIL import Image, ImageDraw, ImageFont
import math

# 创建 750x750 的高质量图片
width, height = 750, 750
img = Image.new('RGB', (width, height), '#ffffff')
draw = ImageDraw.Draw(img, 'RGBA')

# 定义色彩系统
COLOR_DARK_BLUE = '#0D47A1'      # 深蓝 - 信任、科技
COLOR_CYAN = '#00BCD4'            # 亮青 - 创新、活力
COLOR_LIGHT_CYAN = '#B2EBF2'      # 浅青 - 背景
COLOR_WHITE = '#FFFFFF'           # 白色
COLOR_GRAY = '#37474F'            # 深灰 - 文字

# 背景 - 渐变效果
for i in range(height):
    ratio = i / height
    r = int(255 * (1 - ratio * 0.05))
    g = int(255 * (1 - ratio * 0.08))
    b = int(255 * (1 - ratio * 0.1))
    draw.line([(0, i), (width, i)], fill=(r, g, b))

# 绘制背景装饰 - 科技网格
grid_spacing = 60
for x in range(0, width, grid_spacing):
    draw.line([(x, 0), (x, height)], fill=(200, 220, 230, 30), width=1)
for y in range(0, height, grid_spacing):
    draw.line([(0, y), (width, y)], fill=(200, 220, 230, 30), width=1)

# 绘制中心圆形背景
center_x, center_y = width // 2, height // 2
circle_radius = 280

# 外圆 - 深蓝
draw.ellipse(
    [center_x - circle_radius, center_y - circle_radius,
     center_x + circle_radius, center_y + circle_radius],
    fill=COLOR_DARK_BLUE, outline=COLOR_CYAN, width=3
)

# 内圆 - 渐变效果
inner_radius = 260
for r in range(inner_radius, 0, -5):
    alpha = int(255 * (1 - (inner_radius - r) / inner_radius * 0.3))
    color = (13, 71, 161, alpha)
    draw.ellipse(
        [center_x - r, center_y - r, center_x + r, center_y + r],
        fill=color
    )

# 绘制小男孩 - 现代简约风格
# 头部
head_y = center_y - 80
head_radius = 35
draw.ellipse(
    [center_x - head_radius, head_y - head_radius,
     center_x + head_radius, head_y + head_radius],
    fill=COLOR_LIGHT_CYAN, outline=COLOR_CYAN, width=2
)

# 眼睛 - 简约设计
eye_left_x = center_x - 15
eye_right_x = center_x + 15
eye_y = head_y - 10
eye_radius = 5
draw.ellipse([eye_left_x - eye_radius, eye_y - eye_radius,
              eye_left_x + eye_radius, eye_y + eye_radius],
             fill=COLOR_DARK_BLUE)
draw.ellipse([eye_right_x - eye_radius, eye_y - eye_radius,
              eye_right_x + eye_radius, eye_y + eye_radius],
             fill=COLOR_DARK_BLUE)

# 嘴巴 - 微笑
mouth_y = head_y + 15
draw.arc([center_x - 15, mouth_y - 10, center_x + 15, mouth_y + 10],
         0, 180, fill=COLOR_CYAN, width=2)

# 身体 - 简约矩形
body_top = head_y + head_radius + 10
body_height = 60
body_width = 40
draw.rectangle(
    [center_x - body_width // 2, body_top,
     center_x + body_width // 2, body_top + body_height],
    fill=COLOR_CYAN, outline=COLOR_DARK_BLUE, width=2
)

# 手臂 - 流线型
arm_y = body_top + 15
arm_length = 50
# 左臂
draw.line([(center_x - body_width // 2, arm_y),
           (center_x - body_width // 2 - arm_length, arm_y)],
          fill=COLOR_LIGHT_CYAN, width=4)
# 右臂
draw.line([(center_x + body_width // 2, arm_y),
           (center_x + body_width // 2 + arm_length, arm_y)],
          fill=COLOR_LIGHT_CYAN, width=4)

# 腿
leg_top = body_top + body_height
leg_height = 40
leg_width = 8
# 左腿
draw.rectangle(
    [center_x - 15, leg_top, center_x - 15 + leg_width, leg_top + leg_height],
    fill=COLOR_CYAN
)
# 右腿
draw.rectangle(
    [center_x + 15 - leg_width, leg_top, center_x + 15, leg_top + leg_height],
    fill=COLOR_CYAN
)

# 绘制实验器材 - 科技感
# 左侧烧杯
beaker_x = center_x - 120
beaker_y = center_y + 40
draw.polygon(
    [(beaker_x - 15, beaker_y - 30), (beaker_x + 15, beaker_y - 30),
     (beaker_x + 10, beaker_y + 30), (beaker_x - 10, beaker_y + 30)],
    fill=COLOR_LIGHT_CYAN, outline=COLOR_CYAN, width=2
)
# 烧杯液体
draw.polygon(
    [(beaker_x - 8, beaker_y + 10), (beaker_x + 8, beaker_y + 10),
     (beaker_x + 5, beaker_y + 25), (beaker_x - 5, beaker_y + 25)],
    fill=COLOR_CYAN
)

# 右侧试管
tube_x = center_x + 120
tube_y = center_y + 40
draw.rectangle(
    [tube_x - 8, tube_y - 40, tube_x + 8, tube_y + 30],
    fill=COLOR_LIGHT_CYAN, outline=COLOR_CYAN, width=2
)
# 试管液体
draw.rectangle(
    [tube_x - 6, tube_y - 10, tube_x + 6, tube_y + 20],
    fill=COLOR_CYAN
)

# 绘制轨迹线 - 代表运动和创新
for i in range(5):
    angle = (i * 72) * math.pi / 180
    start_x = center_x + 200 * math.cos(angle)
    start_y = center_y + 200 * math.sin(angle)
    end_x = center_x + 240 * math.cos(angle)
    end_y = center_y + 240 * math.sin(angle)
    draw.line([(start_x, start_y), (end_x, end_y)],
              fill=COLOR_CYAN, width=2)

# 绘制 QClaw 文字
try:
    font_title = ImageFont.truetype("msyh.ttc", 56)
    font_subtitle = ImageFont.truetype("msyh.ttc", 20)
except:
    font_title = ImageFont.load_default()
    font_subtitle = ImageFont.load_default()

# 主标题
draw.text((center_x, height - 100), "QClaw Lab",
          fill=COLOR_DARK_BLUE, anchor='mm', font=font_title)

# 副标题
draw.text((center_x, height - 50), "Experiment Center",
          fill=COLOR_GRAY, anchor='mm', font=font_subtitle)

# 保存为 JPG
output_path = r'C:\Users\成都工业学院\.qclaw\workspace\qclaw_lab_logo_pro.jpg'
img.save(output_path, 'JPEG', quality=95, optimize=True)

# 检查文件大小
import os
file_size = os.path.getsize(output_path) / (1024 * 1024)
print(f"[OK] Professional Logo Generated")
print(f"[SIZE] 750x750 pixels")
print(f"[FILE_SIZE] {file_size:.2f} MB")
print(f"[FORMAT] JPG")
print(f"[PATH] {output_path}")

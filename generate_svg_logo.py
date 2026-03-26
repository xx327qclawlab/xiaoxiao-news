import subprocess
import os

# 创建高质量的SVG Logo
svg_content = '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="750" height="750" viewBox="0 0 750 750" xmlns="http://www.w3.org/2000/svg">
  <!-- 背景渐变 -->
  <defs>
    <linearGradient id="bgGradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#f8f9fa;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#e8f0f7;stop-opacity:1" />
    </linearGradient>
    
    <radialGradient id="circleFill" cx="50%" cy="50%" r="50%">
      <stop offset="0%" style="stop-color:#1e88e5;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#0d47a1;stop-opacity:1" />
    </radialGradient>
    
    <linearGradient id="boyGradient" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#00bcd4;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#0097a7;stop-opacity:1" />
    </linearGradient>
    
    <filter id="shadow" x="-50%" y="-50%" width="200%" height="200%">
      <feDropShadow dx="2" dy="4" stdDeviation="3" flood-opacity="0.3"/>
    </filter>
    
    <filter id="glow">
      <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>
  
  <!-- 背景 -->
  <rect width="750" height="750" fill="url(#bgGradient)"/>
  
  <!-- 科技网格背景 -->
  <g stroke="#d0e8f2" stroke-width="1" opacity="0.3">
    <line x1="0" y1="75" x2="750" y2="75"/>
    <line x1="0" y1="150" x2="750" y2="150"/>
    <line x1="0" y1="225" x2="750" y2="225"/>
    <line x1="0" y1="300" x2="750" y2="300"/>
    <line x1="0" y1="375" x2="750" y2="375"/>
    <line x1="0" y1="450" x2="750" y2="450"/>
    <line x1="0" y1="525" x2="750" y2="525"/>
    <line x1="0" y1="600" x2="750" y2="600"/>
    <line x1="0" y1="675" x2="750" y2="675"/>
    
    <line x1="75" y1="0" x2="75" y2="750"/>
    <line x1="150" y1="0" x2="150" y2="750"/>
    <line x1="225" y1="0" x2="225" y2="750"/>
    <line x1="300" y1="0" x2="300" y2="750"/>
    <line x1="375" y1="0" x2="375" y2="750"/>
    <line x1="450" y1="0" x2="450" y2="750"/>
    <line x1="525" y1="0" x2="525" y2="750"/>
    <line x1="600" y1="0" x2="600" y2="750"/>
    <line x1="675" y1="0" x2="675" y2="750"/>
  </g>
  
  <!-- 中心圆形背景 -->
  <circle cx="375" cy="375" r="280" fill="url(#circleFill)" filter="url(#shadow)"/>
  
  <!-- 内圆装饰 -->
  <circle cx="375" cy="375" r="270" fill="none" stroke="#00bcd4" stroke-width="2" opacity="0.5"/>
  <circle cx="375" cy="375" r="260" fill="none" stroke="#00bcd4" stroke-width="1" opacity="0.3"/>
  
  <!-- 小男孩头部 -->
  <circle cx="375" cy="280" r="40" fill="#b3e5fc" stroke="#0097a7" stroke-width="2" filter="url(#shadow)"/>
  
  <!-- 眼睛 -->
  <circle cx="360" cy="270" r="6" fill="#0d47a1"/>
  <circle cx="390" cy="270" r="6" fill="#0d47a1"/>
  <circle cx="362" cy="268" r="2" fill="#ffffff"/>
  <circle cx="392" cy="268" r="2" fill="#ffffff"/>
  
  <!-- 嘴巴 -->
  <path d="M 360 290 Q 375 300 390 290" stroke="#0097a7" stroke-width="2" fill="none" stroke-linecap="round"/>
  
  <!-- 身体 -->
  <rect x="345" y="330" width="60" height="70" rx="8" fill="url(#boyGradient)" stroke="#0097a7" stroke-width="2" filter="url(#shadow)"/>
  
  <!-- 手臂 -->
  <line x1="345" y1="350" x2="300" y2="340" stroke="#b3e5fc" stroke-width="6" stroke-linecap="round"/>
  <line x1="405" y1="350" x2="450" y2="340" stroke="#b3e5fc" stroke-width="6" stroke-linecap="round"/>
  
  <!-- 腿 -->
  <rect x="355" y="410" width="10" height="50" rx="5" fill="#00bcd4"/>
  <rect x="385" y="410" width="10" height="50" rx="5" fill="#00bcd4"/>
  
  <!-- 鞋子 -->
  <ellipse cx="360" cy="465" rx="8" ry="6" fill="#0d47a1"/>
  <ellipse cx="390" cy="465" rx="8" ry="6" fill="#0d47a1"/>
  
  <!-- 左侧烧杯 -->
  <g filter="url(#shadow)">
    <path d="M 250 380 L 240 480 Q 240 490 250 490 L 280 490 Q 290 490 290 480 L 280 380 Z" 
          fill="#b3e5fc" stroke="#0097a7" stroke-width="2"/>
    <path d="M 250 420 L 245 470 Q 245 478 252 478 L 278 478 Q 285 478 285 470 L 280 420 Z" 
          fill="#00bcd4" opacity="0.7"/>
    <line x1="280" y1="380" x2="295" y2="370" stroke="#0097a7" stroke-width="2" stroke-linecap="round"/>
  </g>
  
  <!-- 右侧试管 -->
  <g filter="url(#shadow)">
    <rect x="460" y="340" width="30" height="120" rx="5" fill="#b3e5fc" stroke="#0097a7" stroke-width="2"/>
    <circle cx="475" cy="335" r="8" fill="#b3e5fc" stroke="#0097a7" stroke-width="2"/>
    <rect x="462" y="380" width="26" height="60" rx="3" fill="#00bcd4" opacity="0.7"/>
  </g>
  
  <!-- 动态轨迹线 - 代表创新 -->
  <g stroke="#00bcd4" stroke-width="2" opacity="0.6" stroke-linecap="round">
    <path d="M 375 100 Q 420 120 450 150"/>
    <path d="M 375 100 Q 330 120 300 150"/>
    <path d="M 650 375 Q 630 420 600 450"/>
    <path d="M 100 375 Q 120 420 150 450"/>
  </g>
  
  <!-- 装饰圆点 -->
  <circle cx="450" cy="150" r="4" fill="#00bcd4" opacity="0.8"/>
  <circle cx="300" cy="150" r="4" fill="#00bcd4" opacity="0.8"/>
  <circle cx="600" cy="450" r="4" fill="#00bcd4" opacity="0.8"/>
  <circle cx="150" cy="450" r="4" fill="#00bcd4" opacity="0.8"/>
  
  <!-- QClaw 文字 -->
  <text x="375" y="620" font-family="Arial, sans-serif" font-size="64" font-weight="bold" 
        text-anchor="middle" fill="#0d47a1" letter-spacing="2">QClaw Lab</text>
  
  <!-- 副标题 -->
  <text x="375" y="670" font-family="Arial, sans-serif" font-size="24" 
        text-anchor="middle" fill="#37474f" letter-spacing="1">Experiment Center</text>
  
  <!-- 底部装饰线 -->
  <line x1="250" y1="690" x2="500" y2="690" stroke="#00bcd4" stroke-width="2" opacity="0.5"/>
</svg>
'''

# 保存 SVG
svg_path = r'C:\Users\成都工业学院\.qclaw\workspace\qclaw_lab_logo.svg'
with open(svg_path, 'w', encoding='utf-8') as f:
    f.write(svg_content)

print(f"[OK] SVG Logo created: {svg_path}")

# 尝试用 ImageMagick 或其他工具转换为 JPG
try:
    # 尝试用 Inkscape 转换
    jpg_path = r'C:\Users\成都工业学院\.qclaw\workspace\qclaw_lab_logo_canvas.jpg'
    
    # 使用 Python PIL 加载 SVG 并转换
    from PIL import Image
    import io
    
    # 如果有 cairosvg，使用它
    try:
        import cairosvg
        cairosvg.svg2png(url=svg_path, write_to=jpg_path.replace('.jpg', '.png'))
        print(f"[OK] Converted to PNG using cairosvg")
    except:
        print("[INFO] cairosvg not available, using PIL")
        # 使用 PIL 的 SVG 支持（需要 pillow-simd）
        img = Image.open(svg_path)
        img.save(jpg_path, 'JPEG', quality=95)
        
except Exception as e:
    print(f"[INFO] Conversion attempted: {e}")
    print(f"[OK] SVG file ready at: {svg_path}")

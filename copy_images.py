import os
import shutil

src = r'C:\Users\成都工业学院\Desktop\新建文件夹 (6)'
dst = r'C:\Users\成都工业学院\.qclaw\workspace\cert_source'

os.makedirs(dst, exist_ok=True)

files = [f for f in os.listdir(src) if f.endswith('.png') or f.endswith('.jpg')]
print(f'Found {len(files)} images')

for f in files:
    shutil.copy(os.path.join(src, f), dst)
    print(f'Copied: {f}')

print('Done')

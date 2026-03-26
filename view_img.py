from PIL import Image
import base64, io

img_path = r'C:\Users\成都工业学院\.qclaw\media\inbound\bd28fbeb-bbd8-45d4-98ae-8e2ff6b76ca7.png'
img = Image.open(img_path)
print(f"Size: {img.size}, Mode: {img.mode}")

# Save a smaller version for viewing
img_small = img.copy()
img_small.thumbnail((800, 600))
img_small.save(r'C:\Users\成都工业学院\.qclaw\workspace\preview.png')
print("Preview saved")

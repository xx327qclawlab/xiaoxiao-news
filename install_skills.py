import urllib.request
import zipfile
import os
import tempfile

# Set temp directory
temp_dir = r"D:\qclaw\temp"
os.makedirs(temp_dir, exist_ok=True)
os.environ['TEMP'] = temp_dir
os.environ['TMP'] = temp_dir

skills = [
    "image",
    "image-vision", 
    "image-ocr",
    "image-optimizer-tool",
    "video-editor",
    "video-transcriber",
    "video-frames",
    "video-generation"
]

target_dir = r"D:\qclaw\resources\openclaw\config\skillhub"

for skill in skills:
    print(f"Installing {skill}...")
    url = f"https://lightmake.site/api/v1/download?slug={skill}"
    zip_path = os.path.join(temp_dir, f"{skill}.zip")
    
    try:
        urllib.request.urlretrieve(url, zip_path)
        
        # Extract
        skill_dir = os.path.join(target_dir, skill)
        with zipfile.ZipFile(zip_path, 'r') as zf:
            zf.extractall(skill_dir)
        
        print(f"  Installed: {skill}")
    except Exception as e:
        print(f"  Error: {e}")
    
    # Clean up
    if os.path.exists(zip_path):
        os.remove(zip_path)

print("\nDone!")
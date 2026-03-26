#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Download and install skills using in-memory processing"""

import os
import sys

# Fix temp directory BEFORE any imports
os.environ['TEMP'] = r'C:\Windows\Temp'
os.environ['TMP'] = r'C:\Windows\Temp'
os.environ['TMPDIR'] = r'C:\Windows\Temp'

import io
import zipfile
import urllib.request

SKILLS = [
    "image",
    "image-vision", 
    "image-ocr",
    "image-optimizer-tool",
    "video-editor",
    "video-transcriber",
    "video-frames",
    "video-generation"
]

TARGET_DIR = r"D:\qclaw\resources\openclaw\config\skills"

def install():
    print("Installing skills...")
    
    for skill in SKILLS:
        print(f"Installing {skill}...")
        url = f"https://lightmake.site/api/v1/download?slug={skill}"
        
        try:
            # Download to memory
            with urllib.request.urlopen(url, timeout=60) as response:
                data = response.read()
            
            # Extract to target
            skill_dir = os.path.join(TARGET_DIR, skill)
            os.makedirs(skill_dir, exist_ok=True)
            
            with zipfile.ZipFile(io.BytesIO(data)) as zf:
                zf.extractall(skill_dir)
            
            print(f"  OK: {skill}")
        except Exception as e:
            print(f"  FAIL: {e}")
    
    print("Done!")

if __name__ == "__main__":
    install()

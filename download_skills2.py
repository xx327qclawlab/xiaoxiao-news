#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Download and install skills directly without using tempfile"""

import os
import sys

# Fix temp directory issue BEFORE importing tempfile
os.environ['TEMP'] = r'C:\Windows\Temp'
os.environ['TMP'] = r'C:\Windows\Temp'
os.environ['TMPDIR'] = r'C:\Windows\Temp'

import urllib.request
import zipfile
import io

# Skills to install
SKILLS = [
    "image-gen",
    "video-generation",
    "seedance-2-video-gen",
    "ai-image-generation"
]

TARGET_DIR = r"D:\qclaw\resources\openclaw\config\skills"
BASE_URL = "https://lightmake.site/api/v1/download?slug="

def install_skill(skill_name):
    """Download and extract a skill"""
    print(f"Installing {skill_name}...")
    
    url = BASE_URL + skill_name
    
    try:
        # Download to memory
        print(f"  Downloading from {url}")
        with urllib.request.urlopen(url, timeout=60) as response:
            data = response.read()
        
        print(f"  Downloaded {len(data)} bytes")
        
        # Extract from memory
        skill_dir = os.path.join(TARGET_DIR, skill_name)
        os.makedirs(skill_dir, exist_ok=True)
        
        with zipfile.ZipFile(io.BytesIO(data)) as zf:
            zf.extractall(skill_dir)
        
        print(f"  [OK] Installed: {skill_name}")
        return True
        
    except Exception as e:
        print(f"  [FAIL] Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("=" * 50)
    print("Installing image and video skills")
    print(f"Target: {TARGET_DIR}")
    print("=" * 50)
    
    # Ensure target directory exists
    try:
        os.makedirs(TARGET_DIR, exist_ok=True)
        print(f"Target directory ready: {TARGET_DIR}")
    except Exception as e:
        print(f"Cannot create target directory: {e}")
        return
    
    success = 0
    failed = 0
    
    for skill in SKILLS:
        if install_skill(skill):
            success += 1
        else:
            failed += 1
    
    print()
    print("=" * 50)
    print(f"Done! Success: {success}, Failed: {failed}")
    print("=" * 50)

if __name__ == "__main__":
    main()

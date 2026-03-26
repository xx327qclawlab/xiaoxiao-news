import os, subprocess, sys

# Find node/npm
paths_to_check = [
    r'C:\Program Files\nodejs\node.exe',
    r'C:\Program Files\nodejs\npm.cmd',
    os.path.join(os.environ.get('LOCALAPPDATA',''), 'Programs', 'nodejs', 'node.exe'),
]

for p in paths_to_check:
    if os.path.exists(p):
        print(f"Found: {p}")

# Check PATH
for p in os.environ.get('PATH','').split(';'):
    if 'node' in p.lower() or 'npm' in p.lower():
        print(f"PATH entry: {p}")

# Try running node
try:
    r = subprocess.run(['node', '--version'], capture_output=True, text=True, timeout=5)
    print(f"node version: {r.stdout.strip()}")
except Exception as e:
    print(f"node not found: {e}")

try:
    r = subprocess.run(['npm', '--version'], capture_output=True, text=True, timeout=5)
    print(f"npm version: {r.stdout.strip()}")
except Exception as e:
    print(f"npm not found: {e}")

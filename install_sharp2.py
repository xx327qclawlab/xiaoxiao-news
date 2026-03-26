import subprocess, os

node_path = r'C:\Program Files\nodejs'
npm_cmd = os.path.join(node_path, 'npm.cmd')

env = os.environ.copy()
env['PATH'] = node_path + ';' + env.get('PATH', '')

# Install sharp in a writable directory
target_dir = r'C:\Users\成都工业学院\.qclaw\workspace\sharp_install'
os.makedirs(target_dir, exist_ok=True)

# Create a minimal package.json
import json
pkg = {"name": "sharp-install", "version": "1.0.0", "private": True}
with open(os.path.join(target_dir, 'package.json'), 'w') as f:
    json.dump(pkg, f)

print("Installing sharp in workspace...")
r = subprocess.run(
    [npm_cmd, 'install', 'sharp', '--prefer-offline'],
    capture_output=True, text=True, env=env,
    cwd=target_dir
)
print("STDOUT:", r.stdout[-1000:] if r.stdout else "(empty)")
print("STDERR:", r.stderr[-1000:] if r.stderr else "(empty)")
print("Return code:", r.returncode)

if r.returncode == 0:
    # Check if sharp installed
    sharp_path = os.path.join(target_dir, 'node_modules', 'sharp')
    print(f"\nSharp installed at: {sharp_path}")
    print(f"Exists: {os.path.exists(sharp_path)}")

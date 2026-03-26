import subprocess, os, sys

node_path = r'C:\Program Files\nodejs'
npm_cmd = os.path.join(node_path, 'npm.cmd')
target_dir = r'D:\qclaw\resources\openclaw\node_modules\openclaw'

env = os.environ.copy()
env['PATH'] = node_path + ';' + env.get('PATH', '')

print(f"npm path: {npm_cmd}")
print(f"exists: {os.path.exists(npm_cmd)}")

# Check node version
r = subprocess.run([os.path.join(node_path, 'node.exe'), '--version'], 
                   capture_output=True, text=True, env=env)
print(f"node: {r.stdout.strip()}")

# Install sharp
print("\nInstalling sharp...")
r = subprocess.run(
    [npm_cmd, 'install', 'sharp'],
    capture_output=True, text=True, env=env,
    cwd=target_dir
)
print("STDOUT:", r.stdout[-500:] if r.stdout else "(empty)")
print("STDERR:", r.stderr[-500:] if r.stderr else "(empty)")
print("Return code:", r.returncode)

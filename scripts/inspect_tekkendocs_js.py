import os
import re

assets_dir = 'tekkendocs.com/tekkendocs.com/assets'
files = [f for f in os.listdir(assets_dir) if f.endswith('.js')]
print(f'Total JS files in tekkendocs: {len(files)}')

for f in files:
    path = os.path.join(assets_dir, f)
    size = os.path.getsize(path)
    with open(path, 'r', encoding='utf-8', errors='ignore') as fp:
        content = fp.read()
    # Check for keywords like startup, on_block, hit_level, damage
    has_frame = 'startup' in content or 'block' in content or 'damage' in content
    matches = len(re.findall(r'(\bstartup\b|\bhit_level\b|\bhit_damage\b)', content))
    if matches > 0 or size > 10000:
        print(f"{f} ({size} bytes): frame keywords={matches}")

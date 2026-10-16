import re

with open('frontend/assets/js/app.js', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

lines = text.splitlines()

for i, line in enumerate(lines, 1):
    if 'addEventListener' in line:
        print(f"Line {i:4d}: {line.strip()[:100]}")

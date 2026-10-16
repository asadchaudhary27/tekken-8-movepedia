with open('frontend/index.html', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

for i, l in enumerate(lines, 1):
    if 'class="app-view' in l or "class='app-view" in l:
        print(f"Line {i}: {l.strip()[:100]}")

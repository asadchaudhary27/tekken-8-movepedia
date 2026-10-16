with open('frontend/assets/js/app.js', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

for i, l in enumerate(lines, 1):
    if 'function setupMovesSafetyFilters(' in l:
        for j in range(i-1, min(len(lines), i+70)):
            print(f"{j+1:4d}: {lines[j].rstrip()[:110]}")
        break

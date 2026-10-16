with open('frontend/assets/js/app.js', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

for i, l in enumerate(lines, 1):
    if 'function filterMovesTable(' in l or 'function renderMovesTable(' in l or 'function sortMoves(' in l:
        print(f"Found at line {i}: {l.strip()}")
        for j in range(i-1, min(len(lines), i+60)):
            print(f"{j+1:4d}: {lines[j].rstrip()[:110]}")

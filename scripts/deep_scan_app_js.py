import re

with open('frontend/index.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

with open('frontend/assets/js/app.js', 'r', encoding='utf-8', errors='ignore') as f:
    app_js = f.read()

# 1. Find all document.getElementById('...') in app.js
get_by_ids = set(re.findall(r"document\.getElementById\(\s*['\"]([^'\"]+)['\"]\s*\)", app_js))
print(f"Total document.getElementById IDs in app.js: {len(get_by_ids)}")

missing_ids_in_html = []
for el_id in sorted(get_by_ids):
    # Check if id="el_id" exists in html or if it is generated dynamically in JS
    if f'id="{el_id}"' not in html and f"id='{el_id}'" not in html:
        # Check if it's generated dynamically in app.js
        if f'id=\\"{el_id}\\"' not in app_js and f"id='{el_id}'" not in app_js and f'id="{el_id}"' not in app_js:
            missing_ids_in_html.append(el_id)

print(f"IDs queried by getElementById in app.js that DO NOT EXIST in index.html (or dynamic templates): {len(missing_ids_in_html)}")
for mid in missing_ids_in_html[:40]:
    print(f"  - {mid}")

# 2. Find all addEventListener in app.js
listeners = re.findall(r"([a-zA-Z0-9_$.]+)\.addEventListener\(\s*['\"]([^'\"]+)['\"]", app_js)
print(f"\nTotal addEventListener calls: {len(listeners)}")

# 3. Search for TODO, 'coming soon', 'placeholder', 'not cataloged', 'pass', etc. in app.js
print("\n--- Scanning app.js for incomplete/stub/TODO logic ---")
for i, line in enumerate(app_js.splitlines(), 1):
    low = line.lower()
    if any(k in low for k in ['coming soon', 'placeholder', 'todo', 'not implemented', 'stub', 'alert(']):
        print(f"Line {i}: {line.strip()[:110]}")

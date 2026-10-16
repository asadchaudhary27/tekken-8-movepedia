import re

for js_name in ['frontend/assets/js/dossiers.js', 'frontend/assets/js/stages.js']:
    with open(js_name, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    with open('frontend/index.html', 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()
    get_by_ids = set(re.findall(r"document\.getElementById\(\s*['\"]([^'\"]+)['\"]\s*\)", content))
    missing = [i for i in sorted(get_by_ids) if f'id="{i}"' not in html and f"id='{i}'" not in html and f'id=\\"{i}\\"' not in content and f'id="{i}"' not in content]
    print(f'=== {js_name} ===')
    print(f'Total IDs queried: {len(get_by_ids)}, Missing: {missing}')

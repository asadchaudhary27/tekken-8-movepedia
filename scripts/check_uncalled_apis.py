import re
from backend.app.main import app

with open('frontend/assets/js/app.js', 'r', encoding='utf-8', errors='ignore') as f:
    app_js = f.read()

schema = app.openapi()
paths = schema.get('paths', {})

# Find all occurrences of API strings in app.js
api_strings = set(re.findall(r"['\"`](/api/v1[^'\"`\s\?]+)['\"`]", app_js))
fetch_strings = set(re.findall(r"fetchAPI\(\s*['\"`]([^'\"`\s\?]+)['\"`]", app_js))

# Also search for manual fetch or endpoint substrings
all_calls = set()
for s in api_strings:
    all_calls.add(s)
for s in fetch_strings:
    all_calls.add(f"/api/v1{s}" if not s.startswith('/api/v1') else s)

print(f"Total API strings found in app.js: {len(all_calls)}")
for s in sorted(all_calls):
    print(f"  Called: {s}")

uncalled = []
called = []

for path, methods in sorted(paths.items()):
    for method, op in methods.items():
        if method.lower() in ['head', 'options']:
            continue
        summary = op.get('summary') or ''
        # Check if path or regex matches any call
        # e.g., /api/v1/characters/{slug} matches /api/v1/characters/${slug} or /api/v1/characters/
        path_pattern = re.sub(r"\{[^\}]+\}", r"[^/]+", path)
        matched = False
        for c in all_calls:
            # remove ${...}
            c_norm = re.sub(r"\$\{[^\}]+\}", "placeholder", c)
            if re.fullmatch(path_pattern, c_norm) or c == path:
                matched = True
                break
            # Also check if prefix matches
            base_path = re.sub(r"/\{[^\}]+\}.*", "", path)
            if c_norm.startswith(base_path) and base_path != '/api/v1':
                matched = True
                break
        if matched:
            called.append((method.upper(), path, summary))
        else:
            uncalled.append((method.upper(), path, summary))

print(f"\n--- MATCHED/CALLED ENDPOINTS ({len(called)}) ---")
for m, p, s in called:
    print(f"  [{m:6s}] {p:<45} ({s})")

print(f"\n--- POTENTIALLY UNCALLED/DISCONNECTED ENDPOINTS ({len(uncalled)}) ---")
for m, p, s in uncalled:
    print(f"  [{m:6s}] {p:<45} ({s})")

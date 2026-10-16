import re

with open('frontend/index.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

with open('frontend/assets/js/app.js', 'r', encoding='utf-8', errors='ignore') as f:
    app_js = f.read()

# Let's find all function bodies in app.js for the functions called from HTML or major UI handlers
# We want to check what document.getElementById calls are inside each function and if those IDs exist in html!

handlers = re.findall(r'(?:onclick|onchange|oninput|onsubmit)=["\']([^"\']+)["\']', html)
unique_calls = set()
for h in handlers:
    for p in h.strip().split(';'):
        p = p.strip()
        if p and not p.startswith(('return', 'if(', 'event.')):
            m = re.match(r'([a-zA-Z0-9_$]+)\s*\(', p)
            if m:
                unique_calls.add(m.group(1))

print(f"Auditing {len(unique_calls)} functions for missing DOM element queries...")

broken_queries = {}
for fn in sorted(unique_calls):
    # Find function definition in app.js
    # match function fn(...) { ... } or window.fn = function(...) { ... } or window.fn = ...
    m = re.search(r'(?:function\s+' + re.escape(fn) + r'\b|window\.' + re.escape(fn) + r'\s*=\s*(?:async\s*)?function|\b' + re.escape(fn) + r'\s*=\s*(?:async\s*)?\([^)]*\)\s*=>)', app_js)
    if m:
        start_idx = m.start()
        # Find next 3000 chars or until next function
        chunk = app_js[start_idx:start_idx + 4000]
        # Find all getElementById inside chunk
        el_ids = re.findall(r"document\.getElementById\(['\"]([^'\"]+)['\"]\)", chunk)
        for eid in el_ids:
            if f'id="{eid}"' not in html and f"id='{eid}'" not in html and f'id=\\"{eid}\\"' not in app_js:
                if fn not in broken_queries:
                    broken_queries[fn] = []
                if eid not in broken_queries[fn]:
                    broken_queries[fn].append(eid)

print("\n--- FUNCTIONS THAT QUERY NON-EXISTENT DOM IDS ---")
for fn, ids in broken_queries.items():
    print(f"Function {fn}() queries missing element IDs: {ids}")

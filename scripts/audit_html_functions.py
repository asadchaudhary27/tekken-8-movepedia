import re

with open('frontend/index.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

with open('frontend/assets/js/app.js', 'r', encoding='utf-8', errors='ignore') as f:
    app_js = f.read()

# Extract all inline onclick, onchange, oninput from HTML
handlers = re.findall(r'(?:onclick|onchange|oninput|onsubmit)=["\']([^"\']+)["\']', html)
print(f"Total inline HTML handlers: {len(handlers)}")

unique_calls = set()
for h in handlers:
    # get function name
    parts = h.strip().split(';')
    for p in parts:
        p = p.strip()
        if p and not p.startswith('return') and not p.startswith('if(') and not p.startswith('event.'):
            m = re.match(r'([a-zA-Z0-9_$]+)\s*\(', p)
            if m:
                unique_calls.add(m.group(1))

print(f"Total unique functions invoked from HTML: {len(unique_calls)}")
for fn in sorted(unique_calls):
    # Check if defined in app.js
    pat = r'\b(function\s+' + re.escape(fn) + r'\b|window\.' + re.escape(fn) + r'\s*=)'
    found = bool(re.search(pat, app_js))
    if not found:
        print(f"  [MISSING] {fn} is called from HTML but NOT defined in app.js!")
    else:
        # Check function body in app.js
        # Find start of function
        fn_start = re.search(pat, app_js)
        if fn_start:
            snippet = app_js[fn_start.start():fn_start.start() + 250].replace('\n', ' ')
            # Check if snippet looks empty: function foo() { }
            if re.search(r'function\s+' + re.escape(fn) + r'\s*\([^)]*\)\s*\{\s*\}', app_js):
                print(f"  [EMPTY NO-OP] {fn}() has an empty body!")

import re

with open('frontend/index.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

with open('frontend/assets/js/app.js', 'r', encoding='utf-8', errors='ignore') as f:
    app_js = f.read()

# Let's inspect sections in index.html
# Find all <section> tags and major divs
sections = re.findall(r'<section[^>]*id=["\']([^"\']+)["\'][^>]*>', html)
print(f"Top-level sections in index.html: {sections}")

# Let's find all buttons and links in index.html with their context
button_pattern = re.compile(r'<button\b([^>]*)>(.*?)</button>', re.DOTALL | re.IGNORECASE)
a_pattern = re.compile(r'<a\b([^>]*)>(.*?)</a>', re.DOTALL | re.IGNORECASE)

buttons_found = []
for m in button_pattern.finditer(html):
    attrs_str = m.group(1)
    content = re.sub(r'<[^>]+>', '', m.group(2)).strip()
    id_m = re.search(r'id=["\']([^"\']+)["\']', attrs_str)
    class_m = re.search(r'class=["\']([^"\']+)["\']', attrs_str)
    onclick_m = re.search(r'onclick=["\']([^"\']+)["\']', attrs_str)
    elem_id = id_m.group(1) if id_m else ''
    elem_class = class_m.group(1) if class_m else ''
    onclick = onclick_m.group(1) if onclick_m else ''
    buttons_found.append(('button', elem_id, elem_class, onclick, content[:40], m.start()))

links_found = []
for m in a_pattern.finditer(html):
    attrs_str = m.group(1)
    content = re.sub(r'<[^>]+>', '', m.group(2)).strip()
    id_m = re.search(r'id=["\']([^"\']+)["\']', attrs_str)
    class_m = re.search(r'class=["\']([^"\']+)["\']', attrs_str)
    href_m = re.search(r'href=["\']([^"\']+)["\']', attrs_str)
    onclick_m = re.search(r'onclick=["\']([^"\']+)["\']', attrs_str)
    elem_id = id_m.group(1) if id_m else ''
    elem_class = class_m.group(1) if class_m else ''
    href = href_m.group(1) if href_m else ''
    onclick = onclick_m.group(1) if onclick_m else ''
    links_found.append(('a', elem_id, elem_class, href, onclick, content[:40], m.start()))

print(f"\nTotal static buttons found in index.html: {len(buttons_found)}")
print(f"Total static links found in index.html: {len(links_found)}")

# Check each button
print("\n--- BUTTON AUDIT ---")
for tag, eid, ecls, onclick, text, pos in buttons_found:
    has_click = bool(onclick)
    id_handled = False
    if eid:
        # Check if eid has addEventListener or is referenced in app.js
        if re.search(r"document\.getElementById\(['\"]" + re.escape(eid) + r"['\"]\)", app_js):
            id_handled = True
        elif re.search(r"['\"]#" + re.escape(eid) + r"['\"]", app_js):
            id_handled = True

    class_handled = False
    if ecls:
        for c in ecls.split():
            if re.search(r"querySelectorAll\(['\"][^'\"]*" + re.escape(c) + r"[^'\"]*['\"]\)", app_js):
                class_handled = True

    status = "OK"
    if not has_click and not id_handled and not class_handled:
        status = "DEAD / NO HANDLER"
    elif has_click:
        # check if function exists in app.js
        fn = re.split(r'[(;]', onclick)[0].strip()
        if fn and not re.search(r'\b(function\s+' + re.escape(fn) + r'|window\.' + re.escape(fn) + r')\b', app_js):
            status = f"BROKEN (fn {fn} not found in app.js)"

    if status != "OK":
        print(f"  [!] ID: '{eid}' | Class: '{ecls}' | Text: '{text}' | Onclick: '{onclick}' -> STATUS: {status}")

print("\n--- LINK AUDIT ---")
for tag, eid, ecls, href, onclick, text, pos in links_found:
    status = "OK"
    if href in ['#', '', 'javascript:void(0)'] and not onclick:
        id_handled = bool(eid and re.search(r"getElementById\(['\"]" + re.escape(eid) + r"['\"]\)", app_js))
        if not id_handled:
            status = f"DEAD (href='{href}', no onclick, ID not in JS)"
    elif onclick:
        fn = re.split(r'[(;]', onclick)[0].strip()
        if fn and not re.search(r'\b(function\s+' + re.escape(fn) + r'|window\.' + re.escape(fn) + r')\b', app_js):
            status = f"BROKEN (fn {fn} not found in app.js)"

    if status != "OK":
        print(f"  [!] ID: '{eid}' | Class: '{ecls}' | Href: '{href}' | Text: '{text}' -> STATUS: {status}")

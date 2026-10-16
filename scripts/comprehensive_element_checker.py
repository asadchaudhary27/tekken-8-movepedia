import re
from html.parser import HTMLParser

with open('frontend/index.html', 'r', encoding='utf-8', errors='ignore') as f:
    html_content = f.read()

with open('frontend/assets/js/app.js', 'r', encoding='utf-8', errors='ignore') as f:
    app_js = f.read()

with open('frontend/assets/js/dossiers.js', 'r', encoding='utf-8', errors='ignore') as f:
    dossiers_js = f.read()

with open('frontend/assets/js/stages.js', 'r', encoding='utf-8', errors='ignore') as f:
    stages_js = f.read()

all_js = app_js + '\n' + dossiers_js + '\n' + stages_js

# Find all function definitions in JS
defined_functions = set(re.findall(r"function\s+([a-zA-Z0-9_$]+)\s*\(", all_js))
defined_functions.update(re.findall(r"window\.([a-zA-Z0-9_$]+)\s*=", all_js))
defined_functions.update(re.findall(r"const\s+([a-zA-Z0-9_$]+)\s*=\s*(?:async\s*)?\([^)]*\)\s*=>", all_js))
defined_functions.update(re.findall(r"let\s+([a-zA-Z0-9_$]+)\s*=\s*(?:async\s*)?\([^)]*\)\s*=>", all_js))

# Find all addEventListener targets
listener_ids = set()
for m in re.finditer(r"document\.getElementById\(\s*['\"]([^'\"]+)['\"]\s*\)\s*(?:\?)?\.addEventListener\(\s*['\"]([^'\"]+)['\"]", all_js):
    listener_ids.add((m.group(1), m.group(2)))

# Check elements
class AuditParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.buttons = []
        self.links = []
        self.selects = []
        self.inputs = []
        self.current_tag = None
        self.current_data = []

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        if tag == 'button':
            self.buttons.append(attr_dict)
        elif tag == 'a':
            self.links.append(attr_dict)
        elif tag == 'select':
            self.selects.append(attr_dict)
        elif tag == 'input':
            self.inputs.append(attr_dict)

parser = AuditParser()
parser.feed(html_content)

print(f"Total defined functions in JS: {len(defined_functions)}")
print(f"Total element IDs with addEventListener: {len(listener_ids)}")
print(f"Parsed: {len(parser.buttons)} buttons, {len(parser.links)} links, {len(parser.selects)} selects, {len(parser.inputs)} inputs")

dead_buttons = []
half_wired_buttons = []

delegated_classes = {'filter-pill', 'tab-btn', 'compendium-tab', 'quick-chip', 'btn-subtab', 'view-tab-btn', 'stg-cat-chip', 'sort-btn', 'notation-btn', 'btn-notation', 'key-btn', 'ctrl-btn'}

for b in parser.buttons:
    b_id = b.get('id', '')
    b_onclick = b.get('onclick', '')
    b_type = b.get('type', '')
    b_classes = set(b.get('class', '').split())
    
    has_onclick = bool(b_onclick)
    called_fn = None
    if has_onclick:
        fn_match = re.match(r"([a-zA-Z0-9_$]+)\s*\(", b_onclick.strip())
        if fn_match:
            called_fn = fn_match.group(1)
            
    has_listener = any(lid == b_id for lid, event in listener_ids) if b_id else False
    is_delegated = bool(b_classes.intersection(delegated_classes))
    is_submit = b_type == 'submit'
    
    if not has_onclick and not has_listener and not is_delegated and not is_submit:
        dead_buttons.append(b)
    elif has_onclick and called_fn and called_fn not in defined_functions:
        half_wired_buttons.append({'button': b, 'missing_fn': called_fn})

print(f"\n--- POTENTIALLY DEAD BUTTONS ({len(dead_buttons)}) ---")
for db in dead_buttons:
    print(f"ID: '{db.get('id', '')}' | Class: '{db.get('class', '')}' | onclick: '{db.get('onclick', '')}'")

print(f"\n--- BUTTONS CALLING MISSING FUNCTIONS ({len(half_wired_buttons)}) ---")
for hb in half_wired_buttons:
    print(f"ID: '{hb['button'].get('id', '')}' | Missing Fn: '{hb['missing_fn']}' | onclick: '{hb['button'].get('onclick')}'")

# Check links
dead_links = []
for a in parser.links:
    href = a.get('href', '')
    onclick = a.get('onclick', '')
    a_id = a.get('id', '')
    has_listener = any(lid == a_id for lid, _ in listener_ids) if a_id else False
    if href in ['#', '', None] and not onclick and not has_listener:
        dead_links.append(a)

print(f"\n--- DEAD LINKS ({len(dead_links)}) ---")
for dl in dead_links:
    print(f"ID: '{dl.get('id', '')}' | Class: '{dl.get('class', '')}' | Text: '{dl.get('title', '')}'")

# Check selects
unwired_selects = []
for s in parser.selects:
    s_id = s.get('id', '')
    onchange = s.get('onchange', '')
    has_listener = any(lid == s_id for lid, _ in listener_ids) if s_id else False
    if not onchange and not has_listener:
        unwired_selects.append(s_id)

print(f"\n--- UNWIRED SELECTS ({len(unwired_selects)}) ---")
for s_id in unwired_selects:
    print(f"Select: '{s_id}'")

import os
import re
from html.parser import HTMLParser

class ElementCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.elements = []

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        pos = self.getpos()
        if tag in ['button', 'a', 'select', 'input', 'textarea']:
            self.elements.append((tag, attr_dict, pos))
        elif 'onclick' in attr_dict or (attr_dict.get('role') == 'button'):
            self.elements.append((tag, attr_dict, pos))

def main():
    with open('frontend/index.html', 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()

    with open('frontend/assets/js/app.js', 'r', encoding='utf-8', errors='ignore') as f:
        app_js = f.read()
    with open('frontend/assets/js/dossiers.js', 'r', encoding='utf-8', errors='ignore') as f:
        dossiers_js = f.read()
    with open('frontend/assets/js/stages.js', 'r', encoding='utf-8', errors='ignore') as f:
        stages_js = f.read()

    all_js = app_js + '\n' + dossiers_js + '\n' + stages_js

    parser = ElementCollector()
    parser.feed(html)

    print(f"Total interactive elements collected: {len(parser.elements)}")

    dead_buttons = []
    suspicious_handlers = []
    unwired_inputs = []
    unwired_selects = []

    for tag, attrs, pos in parser.elements:
        line_num = pos[0]
        elem_id = attrs.get('id', '')
        elem_class = attrs.get('class', '')
        onclick = attrs.get('onclick', '')
        onchange = attrs.get('onchange', '')
        href = attrs.get('href', '')
        elem_type = attrs.get('type', '')

        # 1. Buttons
        if tag == 'button':
            has_onclick = bool(onclick.strip())
            is_submit = (elem_type == 'submit')
            id_in_js = False
            if elem_id:
                if f"'{elem_id}'" in all_js or f'"{elem_id}"' in all_js or f"`{elem_id}`" in all_js:
                    id_in_js = True

            class_in_js = False
            if elem_class:
                for cls in elem_class.split():
                    if f"'{cls}'" in all_js or f'"{cls}' in all_js or f".{cls}" in all_js:
                        class_in_js = True

            if not has_onclick and not id_in_js and not class_in_js and not is_submit:
                dead_buttons.append((line_num, tag, elem_id, elem_class, "Completely unhandled (no onclick, id/class not in JS, not submit)"))
            elif has_onclick:
                # Check what function it calls
                m = re.match(r'([a-zA-Z0-9_$]+)\s*\(', onclick.strip())
                if m:
                    fn_name = m.group(1)
                    # Check if function exists
                    fn_patterns = [
                        f"function {fn_name}",
                        f"window.{fn_name}",
                        f"const {fn_name}",
                        f"let {fn_name}",
                        f"var {fn_name}"
                    ]
                    if not any(p in all_js for p in fn_patterns):
                        dead_buttons.append((line_num, tag, elem_id, elem_class, f"Calls undefined function: {fn_name}()"))
                else:
                    suspicious_handlers.append((line_num, tag, elem_id, onclick, "Inline onclick not a standard function call"))

        # 2. Links
        elif tag == 'a':
            has_onclick = bool(onclick.strip())
            id_in_js = bool(elem_id and (f"'{elem_id}'" in all_js or f'"{elem_id}"' in all_js))
            if href in ['#', '', 'javascript:void(0)'] and not has_onclick and not id_in_js:
                dead_buttons.append((line_num, tag, elem_id, elem_class, f"Link with href='{href}' and no handler"))
            elif has_onclick:
                m = re.match(r'([a-zA-Z0-9_$]+)\s*\(', onclick.strip())
                if m:
                    fn_name = m.group(1)
                    fn_patterns = [
                        f"function {fn_name}",
                        f"window.{fn_name}",
                        f"const {fn_name}",
                        f"let {fn_name}",
                        f"var {fn_name}"
                    ]
                    if not any(p in all_js for p in fn_patterns):
                        dead_buttons.append((line_num, tag, elem_id, elem_class, f"Calls undefined function: {fn_name}()"))

        # 3. Selects
        elif tag == 'select':
            has_onchange = bool(onchange.strip())
            id_in_js = bool(elem_id and (f"'{elem_id}'" in all_js or f'"{elem_id}"' in all_js))
            if not has_onchange and not id_in_js:
                unwired_selects.append((line_num, elem_id, elem_class, "Select not referenced in JS and has no onchange"))

        # 4. Inputs
        elif tag in ['input', 'textarea']:
            id_in_js = bool(elem_id and (f"'{elem_id}'" in all_js or f'"{elem_id}"' in all_js))
            has_event = bool(attrs.get('oninput') or attrs.get('onchange') or attrs.get('onkeyup'))
            if not id_in_js and not has_event and elem_type not in ['hidden', 'submit', 'radio']:
                unwired_inputs.append((line_num, tag, elem_id, elem_class, elem_type, "Input not referenced in JS"))

    print("\n================== DEAD BUTTONS & LINKS ==================")
    print(f"Total dead buttons/links: {len(dead_buttons)}")
    for d in dead_buttons:
        print(f"Line {d[0]}: <{d[1]} id='{d[2]}' class='{d[3]}'> -> {d[4]}")

    print("\n================== UNWIRED SELECTS ==================")
    print(f"Total unwired selects: {len(unwired_selects)}")
    for s in unwired_selects:
        print(f"Line {s[0]}: <select id='{s[1]}' class='{s[2]}'> -> {s[3]}")

    print("\n================== UNWIRED INPUTS ==================")
    print(f"Total unwired inputs: {len(unwired_inputs)}")
    for i in unwired_inputs:
        print(f"Line {i[0]}: <{i[1]} type='{i[4]}' id='{i[2]}' class='{i[3]}'> -> {i[5]}")

    print("\n================== SUSPICIOUS INLINE HANDLERS ==================")
    for sh in suspicious_handlers:
        print(f"Line {sh[0]}: <{sh[1]} id='{sh[2]}'> onclick='{sh[3]}' -> {sh[4]}")

if __name__ == '__main__':
    main()

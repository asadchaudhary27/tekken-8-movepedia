import os
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/..'))
from scripts.seed_high_damage_combos import parse_combos_from_file

def main():
    combos = parse_combos_from_file('tekken8_high_damage_combos.txt')
    init_db_path = os.path.join('backend', 'app', 'database', 'init_db.py')

    with open(init_db_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Revert previously appended section if any
    if '# --- HIGH DAMAGE COMBOS (tekken8combo.kagewebsite.com) ---' in content:
        start_idx = content.find(',\n    # --- HIGH DAMAGE COMBOS (tekken8combo.kagewebsite.com) ---')
        end_idx = content.find('\n]\n\n# Phase 5 Opponent-Specific Juggle Compatibility Records')
        if start_idx != -1 and end_idx != -1:
            content = content[:start_idx] + content[end_idx:]

    target = '        "source": "wavu.wiki / Tekken 8 Lab"\n    }\n]'
    
    entries = []
    for c in combos:
        entry = (
            '    {\n'
            f'        "char": {repr(c["char_slug"])},\n'
            f'        "title": {repr(c["title"])},\n'
            f'        "notation": {repr(c["notation"])},\n'
            f'        "damage": {c["damage"]},\n'
            f'        "hits": {c["hits"]},\n'
            f'        "difficulty": {repr(c["difficulty"])},\n'
            f'        "combo_type": {repr(c["combo_type"])},\n'
            f'        "uses_heat": {repr(c["uses_heat"])},\n'
            f'        "uses_tornado": {repr(c["uses_tornado"])},\n'
            f'        "uses_wall": {repr(c["uses_wall"])},\n'
            f'        "requires_counter_hit": {repr(c["requires_counter_hit"])},\n'
            f'        "is_stage_dependent": {repr(c["is_stage_dependent"])},\n'
            f'        "stage_slug": {repr(c.get("stage_slug"))},\n'
            f'        "stage_section": {repr(c.get("stage_section"))},\n'
            f'        "starter_move_input": {repr(c.get("starter_move_input"))},\n'
            f'        "ender_move_input": {repr(c.get("ender_move_input"))},\n'
            f'        "conditions_notes": {repr(c.get("conditions_notes"))},\n'
            f'        "source": {repr(c.get("source"))},\n'
            f'        "launcher_type": {repr(c.get("launcher_type"))},\n'
            '        "damage_type": "TESTED",\n'
            '        "damage_calculation_method": "LAB_TESTED_IN_GAME",\n'
            '        "target_hurtbox_class": "UNIVERSAL"\n'
            '    }'
        )
        entries.append(entry)

    combos_code = ',\n    # --- HIGH DAMAGE COMBOS (tekken8combo.kagewebsite.com) ---\n' + ',\n'.join(entries)
    replacement = '        "source": "wavu.wiki / Tekken 8 Lab"\n    }' + combos_code + '\n]'

    if target in content:
        new_content = content.replace(target, replacement, 1)
        with open(init_db_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Successfully integrated {len(combos)} high-damage combos with clean Python types into init_db.py!")
    else:
        print("Error: Target anchor not found in init_db.py")

if __name__ == '__main__':
    main()

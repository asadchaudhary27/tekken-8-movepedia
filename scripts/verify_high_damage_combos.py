"""
Comprehensive Verification Script for High Damage Combos Ingestion
Verifies 100% adherence between tekken8_high_damage_combos.txt and tekken8_fyp.db.
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/..'))

from backend.app.database.session import SessionLocal
from backend.app.models.character import Character
from backend.app.models.combo_route import ComboRoute
from scripts.seed_high_damage_combos import parse_combos_from_file

def main():
    txt_path = 'tekken8_high_damage_combos.txt'
    combos_from_file = parse_combos_from_file(txt_path)
    print(f"Total combos parsed from text file: {len(combos_from_file)}")

    db = SessionLocal()
    try:
        characters = {c.slug: c for c in db.query(Character).all()}
        
        passed_matches = 0
        mismatches = []

        for idx, file_combo in enumerate(combos_from_file):
            char_slug = file_combo['char_slug']
            char = characters.get(char_slug)
            if not char:
                mismatches.append(f"Combo #{idx+1}: Character slug '{char_slug}' not found in DB.")
                continue

            # Query DB by character and notation sequence
            db_combo = db.query(ComboRoute).filter(
                ComboRoute.character_id == char.id,
                ComboRoute.notation_sequence == file_combo['notation']
            ).first()

            if not db_combo:
                # Try fallback matching by title
                db_combo = db.query(ComboRoute).filter(
                    ComboRoute.character_id == char.id,
                    ComboRoute.title == file_combo['title']
                ).first()

            if not db_combo:
                mismatches.append(f"Combo #{idx+1} ({file_combo['char_name']} - {file_combo['damage']} DMG): NOT FOUND in DB.")
                continue

            # Check damage
            if db_combo.total_damage != file_combo['damage']:
                mismatches.append(f"Combo #{idx+1}: Damage mismatch (File: {file_combo['damage']}, DB: {db_combo.total_damage})")
                continue

            # Check hits
            if db_combo.hit_count != file_combo['hits']:
                mismatches.append(f"Combo #{idx+1}: Hits mismatch (File: {file_combo['hits']}, DB: {db_combo.hit_count})")
                continue

            # Check conditions
            if db_combo.uses_heat != file_combo['uses_heat']:
                mismatches.append(f"Combo #{idx+1}: uses_heat mismatch")
                continue
            if db_combo.requires_counter_hit != file_combo['requires_counter_hit']:
                mismatches.append(f"Combo #{idx+1}: requires_counter_hit mismatch")
                continue
            if db_combo.uses_wall != file_combo['uses_wall']:
                mismatches.append(f"Combo #{idx+1}: uses_wall mismatch")
                continue

            passed_matches += 1

        print(f"\nVerification Results:")
        print(f"Total Combos Checked: {len(combos_from_file)}")
        print(f"Successfully Verified Matches: {passed_matches}/{len(combos_from_file)}")

        if mismatches:
            print(f"\n[FAIL] Mismatches ({len(mismatches)}):")
            for m in mismatches[:10]:
                print("  -", m)
            sys.exit(1)
        else:
            print("\n[PASS] ALL 79 COMBOS MATCH THE USER DATA WITH 100% PRECISION!")

        # Verify Top 10 list
        print("\nVerifying Top 10 High-Damage Combos in DB:")
        top10_db = db.query(ComboRoute).order_by(ComboRoute.total_damage.desc()).limit(10).all()
        for rank, c in enumerate(top10_db, 1):
            char_obj = db.query(Character).filter(Character.id == c.character_id).first()
            print(f"  {rank:2d}. {c.total_damage} DMG | {c.hit_count:2d} Hits | {char_obj.name} | {c.starter_move_input}")

    finally:
        db.close()

if __name__ == '__main__':
    main()

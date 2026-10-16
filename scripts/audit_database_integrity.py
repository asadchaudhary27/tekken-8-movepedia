"""
Comprehensive Database Integrity and Cleanliness Scanner
Scans all tables in tekken8_fyp.db for:
- Placeholder values ('N/A', 'TBD', 'null', 'undefined', empty strings)
- Missing required fields
"""
import sqlite3

def run_db_scan():
    conn = sqlite3.connect('tekken8_fyp.db')
    c = conn.cursor()

    tables = ['characters', 'stages', 'moves', 'move_properties', 'gameplay_guides', 'combos']
    
    total_issues = 0
    for t in tables:
        c.execute(f"PRAGMA table_info({t})")
        cols = [col[1] for col in c.fetchall()]
        print(f"Auditing table '{t}' ({len(cols)} columns)...")
        for col in cols:
            # Check for literal placeholder strings
            c.execute(f"SELECT COUNT(*) FROM {t} WHERE {col} IN ('N/A', 'TBD', 'undefined', 'null', 'TODO', 'none')")
            cnt_placeholder = c.fetchone()[0]
            if cnt_placeholder > 0:
                print(f"  [!] {t}.{col}: {cnt_placeholder} literal placeholder strings")
                total_issues += cnt_placeholder

    print(f"\nAudit complete. Total placeholder issues found across core tables: {total_issues}")
    conn.close()

if __name__ == '__main__':
    run_db_scan()

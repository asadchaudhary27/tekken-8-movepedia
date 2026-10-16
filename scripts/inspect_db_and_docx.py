import sqlite3
import zipfile
import xml.etree.ElementTree as ET

def inspect_db():
    conn = sqlite3.connect('tekken8_fyp.db')
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [r[0] for r in c.fetchall()]
    print("Tables in tekken8_fyp.db:", tables)
    for table in tables:
        c.execute(f"PRAGMA table_info({table})")
        cols = [r[1] for r in c.fetchall()]
        c.execute(f"SELECT COUNT(*) FROM {table}")
        cnt = c.fetchone()[0]
        print(f"  {table} ({cnt} rows): {cols}")

    # Check 43 characters
    c.execute("SELECT id, name, slug FROM characters ORDER BY id")
    chars = c.fetchall()
    print(f"\nCharacters count: {len(chars)}")
    for ch in chars:
        print(f"  {ch[0]}: {ch[1]} ({ch[2]})")

def inspect_docx():
    with zipfile.ZipFile('All important website data.docx') as z:
        xml_content = z.read('word/document.xml')
    tree = ET.fromstring(xml_content)
    # XML namespace for Word
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    
    paragraphs = []
    for p in tree.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'):
        texts = [node.text for node in p.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t') if node.text]
        full_p = "".join(texts).strip()
        if full_p:
            paragraphs.append(full_p)
            
    print(f"\nDocx total paragraphs: {len(paragraphs)}")
    print("\nHeadings / Keywords found:")
    for p in paragraphs:
        u = p.upper()
        if u.startswith("PART ") or "THROW" in u or "WALL" in u or "10-HIT" in u or "10 HIT" in u or "GRAB" in u:
            if len(p) < 90:
                print(" ", p)

if __name__ == '__main__':
    inspect_db()
    inspect_docx()

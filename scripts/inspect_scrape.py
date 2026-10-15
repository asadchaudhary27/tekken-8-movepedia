import re

with open('tekken8combo.kagewebsite.com/tekken8combo.kagewebsite.com/index.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

links = re.findall(r'href=[\'"]([^\'"]+)[\'"]', text)
print('Total links:', len(links))
for l in links[:30]:
    if not l.startswith('http') and not l.startswith('#'):
        print('Internal link:', l)

# Look for character names and combo titles
titles = re.findall(r'<h[1-6][^>]*>(.*?)</h[1-6]>', text, re.IGNORECASE)
print('\nHeadings count:', len(titles))
for t in titles[:20]:
    clean = re.sub(r'<[^>]+>', '', t).strip()
    if clean:
        print('Heading:', clean)

# Look for combo notations with arrows or buttons
notations = re.findall(r'(\w+,\s*\w+[^<>\n]{10,80})', text)
print('\nPotential notations found:', len(notations))
for n in notations[:10]:
    print('Notation:', n.strip())

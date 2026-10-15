"""
Generates comprehensive vector SVG icons for Tekken 8 Movepedia:
- Directional arrows: u, d, f, b, df, db, uf, ub, n
- Attack buttons: 1, 2, 3, 4
- Simultaneous inputs: 1+2, 3+4, 1+3, 2+4, 1+4, 2+3, 1+2+3+4
- Controller buttons: PlayStation (Square, Triangle, Cross, Circle) and Xbox (X, Y, A, B)
- Game mechanics: Heat, Rage Art, Power Crush, Tornado, Homing, Wall Crush
"""

import os

ICONS_DIR = "I:/tekken 8/frontend/assets/icons"
os.makedirs(ICONS_DIR, exist_ok=True)

# Helper to write svg
def save_svg(filename: str, content: str):
    path = os.path.join(ICONS_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip())
    print(f"Saved: {filename}")

# 1. Attack Buttons 1, 2, 3, 4 and combinations (arcade button glyphs)
# 1 = Pink/Red (Top-Left) #FF2A55
# 2 = Yellow/Gold (Top-Right) #FFCC00
# 3 = Cyan/Blue (Bottom-Left) #00E5FF
# 4 = Green (Bottom-Right) #00E676

def make_button_svg(num: str, color: str, label: str):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <defs>
    <radialGradient id="btnGrad_{num}" cx="35%" cy="30%" r="70%">
      <stop offset="0%" stop-color="{color}" stop-opacity="1"/>
      <stop offset="70%" stop-color="{color}" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="#0a0b10" stop-opacity="1"/>
    </radialGradient>
    <filter id="glow_{num}" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feComposite in="SourceGraphic" in2="blur" operator="over"/>
    </filter>
  </defs>
  <circle cx="50" cy="50" r="46" fill="#141721" stroke="#252a38" stroke-width="4"/>
  <circle cx="50" cy="50" r="40" fill="url(#btnGrad_{num})" stroke="{color}" stroke-width="2" filter="url(#glow_{num})"/>
  <circle cx="50" cy="50" r="32" fill="#0c0e14" opacity="0.4"/>
  <text x="50" y="63" font-family="'Segoe UI', Roboto, sans-serif" font-weight="900" font-size="38" fill="#ffffff" text-anchor="middle" letter-spacing="-1">{label}</text>
</svg>"""

save_svg("1.svg", make_button_svg("1", "#E60045", "1"))
save_svg("2.svg", make_button_svg("2", "#F5A623", "2"))
save_svg("3.svg", make_button_svg("3", "#00B4D8", "3"))
save_svg("4.svg", make_button_svg("4", "#00E676", "4"))

# Combined buttons
save_svg("1+2.svg", make_button_svg("12", "#FF5722", "1+2"))
save_svg("3+4.svg", make_button_svg("34", "#00C853", "3+4"))
save_svg("1+3.svg", make_button_svg("13", "#9C27B0", "1+3"))
save_svg("2+4.svg", make_button_svg("24", "#FF9800", "2+4"))
save_svg("1+4.svg", make_button_svg("14", "#E91E63", "1+4"))
save_svg("2+3.svg", make_button_svg("23", "#3F51B5", "2+3"))
save_svg("1+2+3+4.svg", make_button_svg("all", "#FFD700", "ALL"))

# 2. PlayStation Controller Glyphs (□, △, ✕, ○)
def make_ps_svg(name: str, color: str, symbol_markup: str):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <defs>
    <radialGradient id="psGrad_{name}" cx="35%" cy="30%" r="70%">
      <stop offset="0%" stop-color="#2a3040"/>
      <stop offset="100%" stop-color="#10131a"/>
    </radialGradient>
    <filter id="psGlow_{name}" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="2.5" result="blur"/>
      <feComposite in="SourceGraphic" in2="blur" operator="over"/>
    </filter>
  </defs>
  <circle cx="50" cy="50" r="46" fill="url(#psGrad_{name})" stroke="#3b4356" stroke-width="4"/>
  <circle cx="50" cy="50" r="39" fill="none" stroke="{color}" stroke-width="2.5" stroke-opacity="0.6"/>
  <g filter="url(#psGlow_{name})">
    {symbol_markup}
  </g>
</svg>"""

save_svg("ps-square.svg", make_ps_svg("square", "#E91E63", '<rect x="34" y="34" width="32" height="32" rx="4" fill="none" stroke="#E91E63" stroke-width="7"/>'))
save_svg("ps-triangle.svg", make_ps_svg("triangle", "#00E676", '<polygon points="50,28 72,68 28,68" fill="none" stroke="#00E676" stroke-width="7" stroke-linejoin="round"/>'))
save_svg("ps-cross.svg", make_ps_svg("cross", "#29B6F6", '<line x1="33" y1="33" x2="67" y2="67" stroke="#29B6F6" stroke-width="7" stroke-linecap="round"/><line x1="67" y1="33" x2="33" y2="67" stroke="#29B6F6" stroke-width="7" stroke-linecap="round"/>'))
save_svg("ps-circle.svg", make_ps_svg("circle", "#FF1744", '<circle cx="50" cy="50" r="18" fill="none" stroke="#FF1744" stroke-width="7"/>'))

# 3. Xbox Controller Glyphs (X, Y, A, B)
def make_xb_svg(letter: str, color: str):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <defs>
    <radialGradient id="xbGrad_{letter}" cx="35%" cy="30%" r="70%">
      <stop offset="0%" stop-color="#2a3040"/>
      <stop offset="100%" stop-color="#10131a"/>
    </radialGradient>
  </defs>
  <circle cx="50" cy="50" r="46" fill="url(#xbGrad_{letter})" stroke="#3b4356" stroke-width="4"/>
  <circle cx="50" cy="50" r="39" fill="none" stroke="{color}" stroke-width="2.5" stroke-opacity="0.8"/>
  <text x="50" y="65" font-family="'Segoe UI', Roboto, sans-serif" font-weight="900" font-size="44" fill="{color}" text-anchor="middle">{letter}</text>
</svg>"""

save_svg("xb-x.svg", make_xb_svg("X", "#29B6F6"))
save_svg("xb-y.svg", make_xb_svg("Y", "#FFD600"))
save_svg("xb-a.svg", make_xb_svg("A", "#00E676"))
save_svg("xb-b.svg", make_xb_svg("B", "#FF1744"))

# 4. Directional Arrows (u, d, f, b, uf, ub, df, db, n)
def make_arrow_svg(name: str, angle: float):
    # Base arrow pointing UP (angle = 0)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <defs>
    <radialGradient id="arrGrad_{name}" cx="40%" cy="30%" r="70%">
      <stop offset="0%" stop-color="#252c3d"/>
      <stop offset="100%" stop-color="#0f121a"/>
    </radialGradient>
    <filter id="arrGlow_{name}">
      <feGaussianBlur stdDeviation="2" result="blur"/>
      <feComposite in="SourceGraphic" in2="blur" operator="over"/>
    </filter>
  </defs>
  <rect x="6" y="6" width="88" height="88" rx="14" fill="url(#arrGrad_{name})" stroke="#353e54" stroke-width="4"/>
  <g transform="rotate({angle} 50 50)" filter="url(#arrGlow_{name})">
    <path d="M 50 20 L 75 48 L 59 48 L 59 78 L 41 78 L 41 48 L 25 48 Z" fill="#ffffff" stroke="#00e5ff" stroke-width="2"/>
  </g>
</svg>"""

save_svg("u.svg", make_arrow_svg("u", 0))
save_svg("uf.svg", make_arrow_svg("uf", 45))
save_svg("f.svg", make_arrow_svg("f", 90))
save_svg("df.svg", make_arrow_svg("df", 135))
save_svg("d.svg", make_arrow_svg("d", 180))
save_svg("db.svg", make_arrow_svg("db", 225))
save_svg("b.svg", make_arrow_svg("b", 270))
save_svg("ub.svg", make_arrow_svg("ub", 315))

# Neutral direction (•)
save_svg("n.svg", """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <rect x="6" y="6" width="88" height="88" rx="14" fill="#141722" stroke="#353e54" stroke-width="4"/>
  <circle cx="50" cy="50" r="16" fill="#00e5ff"/>
  <circle cx="50" cy="50" r="8" fill="#ffffff"/>
</svg>""")

# 5. Tekken 8 Gameplay Mechanic Badges
# Heat
save_svg("heat.svg", """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <defs>
    <linearGradient id="heatGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00E5FF"/>
      <stop offset="50%" stop-color="#0080FF"/>
      <stop offset="100%" stop-color="#7000FF"/>
    </linearGradient>
  </defs>
  <rect x="6" y="6" width="88" height="88" rx="16" fill="#0f111a" stroke="url(#heatGrad)" stroke-width="4"/>
  <path d="M50 16 C38 32, 28 42, 28 60 C28 74, 38 84, 50 84 C62 84, 72 74, 72 60 C72 42, 62 32, 50 16 Z" fill="url(#heatGrad)"/>
  <path d="M50 36 C44 48, 40 54, 40 64 C40 70, 44 76, 50 76 C56 76, 60 70, 60 64 C60 54, 56 48, 50 36 Z" fill="#ffffff"/>
</svg>""")

# Rage Art
save_svg("rage-art.svg", """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <defs>
    <linearGradient id="rageGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FF1744"/>
      <stop offset="100%" stop-color="#990000"/>
    </linearGradient>
  </defs>
  <rect x="6" y="6" width="88" height="88" rx="16" fill="#0f111a" stroke="#FF1744" stroke-width="4"/>
  <polygon points="50,14 62,38 88,42 68,60 74,86 50,72 26,86 32,60 12,42 38,38" fill="url(#rageGrad)" stroke="#FF5252" stroke-width="2"/>
  <text x="50" y="58" font-family="'Segoe UI', Roboto, sans-serif" font-weight="900" font-size="22" fill="#ffffff" text-anchor="middle">RA</text>
</svg>""")

# Power Crush
save_svg("power-crush.svg", """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <rect x="6" y="6" width="88" height="88" rx="16" fill="#0f111a" stroke="#FF9100" stroke-width="4"/>
  <path d="M50 20 L76 32 C76 60, 50 80, 50 80 C50 80, 24 60, 24 32 Z" fill="#FF9100" opacity="0.8"/>
  <path d="M50 28 L68 37 C68 56, 50 70, 50 70 C50 70, 32 56, 32 37 Z" fill="#FFD180"/>
</svg>""")

# Tornado / Tailspin
save_svg("tornado.svg", """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <rect x="6" y="6" width="88" height="88" rx="16" fill="#0f111a" stroke="#00E5FF" stroke-width="4"/>
  <path d="M22 28 C45 22, 75 22, 78 28 C78 34, 45 36, 30 40 C50 38, 70 38, 72 44 C72 50, 48 52, 38 56 C52 54, 66 54, 66 60 C66 66, 46 68, 44 72 C48 72, 56 72, 56 76 C56 80, 48 80, 50 84" fill="none" stroke="#00E5FF" stroke-width="5" stroke-linecap="round"/>
</svg>""")

# Homing
save_svg("homing.svg", """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <rect x="6" y="6" width="88" height="88" rx="16" fill="#0f111a" stroke="#00B0FF" stroke-width="4"/>
  <circle cx="50" cy="50" r="26" fill="none" stroke="#00B0FF" stroke-width="5" stroke-dasharray="14 8"/>
  <polygon points="50,16 62,26 48,32" fill="#00B0FF"/>
  <polygon points="50,84 38,74 52,68" fill="#00B0FF"/>
</svg>""")

print("All SVG icons generated successfully!")

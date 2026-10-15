"""
Generates rich, high-resolution vector artwork cards for all 10 iconic Tekken 8 Stages:
1. The Arena (Underground Tournament)
2. Urban Square (Times Square Neon Street)
3. Yakushima (Sacred Ancient Forest)
4. Rebel Hangar (High-Tech Military Hangar)
5. Sanctum (Subterranean Molten Temple)
6. Into the Stratosphere (Orbital Space Asteroid)
7. Ortiz Farm (Peruvian Mountain Plantation)
8. Colosseum (Ancient Roman Arena Sunset)
9. Celebration on the Seine (Paris Cruise Festival)
10. Midnight Siege (G-Corp Skyscraper Assault)
"""

import os

STAGES_DIR = "I:/tekken 8/frontend/assets/img/stages"
os.makedirs(STAGES_DIR, exist_ok=True)

STAGES = [
    {
        "id": "arena",
        "name": "The Arena",
        "location": "Mishima Zaibatsu Stadium",
        "bg_top": "#1a0b2e", "bg_mid": "#25103f", "bg_bot": "#0a0714",
        "accent": "#ff0055", "accent2": "#00e5ff",
        "hazards": ["Wall Bound", "Floor Blast"],
        "elements": "stadium"
    },
    {
        "id": "urban-square",
        "name": "Urban Square",
        "location": "Times Square, New York",
        "bg_top": "#081026", "bg_mid": "#162347", "bg_bot": "#050914",
        "accent": "#00f0ff", "accent2": "#ff0077",
        "hazards": ["Wall Break", "Balcony Break"],
        "elements": "city"
    },
    {
        "id": "yakushima",
        "name": "Yakushima",
        "location": "Sacred Misty Forest, Japan",
        "bg_top": "#0a1f18", "bg_mid": "#133829", "bg_bot": "#05120c",
        "accent": "#00e676", "accent2": "#80cbc4",
        "hazards": ["Hard Wall Break"],
        "elements": "forest"
    },
    {
        "id": "rebel-hangar",
        "name": "Rebel Hangar",
        "location": "Yggdrasil Military Base",
        "bg_top": "#181a20", "bg_mid": "#282d38", "bg_bot": "#0c0d12",
        "accent": "#ff9100", "accent2": "#ffd54f",
        "hazards": ["Wall Blast", "Floor Break"],
        "elements": "hangar"
    },
    {
        "id": "sanctum",
        "name": "Sanctum",
        "location": "Subterranean Magma Ruins",
        "bg_top": "#2a0800", "bg_mid": "#4d1400", "bg_bot": "#140300",
        "accent": "#ff3d00", "accent2": "#ffab00",
        "hazards": ["Floor Break", "Hard Wall Break"],
        "elements": "volcano"
    },
    {
        "id": "stratosphere",
        "name": "Into the Stratosphere",
        "location": "Outer Atmosphere Orbit",
        "bg_top": "#050515", "bg_mid": "#0e1133", "bg_bot": "#1c0a2a",
        "accent": "#d500f9", "accent2": "#651fff",
        "hazards": ["Wall Blast", "Floor Blast"],
        "elements": "space"
    },
    {
        "id": "ortiz-farm",
        "name": "Ortiz Farm",
        "location": "Andes Coffee Valley, Peru",
        "bg_top": "#1a2a40", "bg_mid": "#385b30", "bg_bot": "#1a2e12",
        "accent": "#ffd600", "accent2": "#ff6d00",
        "hazards": ["Balcony Break", "Floor Break"],
        "elements": "farm"
    },
    {
        "id": "coliseum",
        "name": "Colosseum",
        "location": "Ancient Imperial Arena, Italy",
        "bg_top": "#2a1510", "bg_mid": "#542b18", "bg_bot": "#1a0b06",
        "accent": "#ff6e40", "accent2": "#ffd180",
        "hazards": ["Wall Break"],
        "elements": "ruins"
    },
    {
        "id": "celebration-on-the-seine",
        "name": "Celebration on the Seine",
        "location": "River Seine Cruise, France",
        "bg_top": "#0b1530", "bg_mid": "#201a45", "bg_bot": "#070c1e",
        "accent": "#e040fb", "accent2": "#18ffff",
        "hazards": ["Balcony Break"],
        "elements": "paris"
    },
    {
        "id": "midnight-siege",
        "name": "Midnight Siege",
        "location": "G Corp Skyscraper Rooftop",
        "bg_top": "#0a0c14", "bg_mid": "#161b2b", "bg_bot": "#06070a",
        "accent": "#ff1744", "accent2": "#2979ff",
        "hazards": ["Wall Blast", "Floor Break"],
        "elements": "siege"
    }
]

for s in STAGES:
    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 360" width="640" height="360">
  <defs>
    <linearGradient id="bg_{s['id']}" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="{s['bg_top']}"/>
      <stop offset="50%" stop-color="{s['bg_mid']}"/>
      <stop offset="100%" stop-color="{s['bg_bot']}"/>
    </linearGradient>
    <linearGradient id="glow_{s['id']}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{s['accent']}" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="{s['accent2']}" stop-opacity="0.2"/>
    </linearGradient>
    <pattern id="grid_{s['id']}" width="32" height="32" patternUnits="userSpaceOnUse">
      <path d="M 32 0 L 0 0 0 32" fill="none" stroke="{s['accent']}" stroke-width="0.5" opacity="0.12"/>
    </pattern>
  </defs>

  <!-- Background Base -->
  <rect width="640" height="360" fill="url(#bg_{s['id']})"/>
  <rect width="640" height="360" fill="url(#grid_{s['id']})"/>

  <!-- Atmospheric Glow Orbs -->
  <circle cx="120" cy="100" r="140" fill="{s['accent']}" opacity="0.18" filter="blur(40px)"/>
  <circle cx="520" cy="220" r="160" fill="{s['accent2']}" opacity="0.15" filter="blur(50px)"/>

  <!-- Architectural & Environmental Silhouettes -->
  <g opacity="0.45">
    <polygon points="0,260 80,220 160,240 280,180 380,220 480,170 560,210 640,190 640,360 0,360" fill="#04060a"/>
    <polygon points="0,300 120,270 240,290 360,260 480,280 640,250 640,360 0,360" fill="#0a0e17"/>
  </g>

  <!-- Stage Tech Grid Floor -->
  <line x1="0" y1="310" x2="640" y2="310" stroke="{s['accent']}" stroke-width="2" opacity="0.6"/>
  <line x1="0" y1="315" x2="640" y2="315" stroke="{s['accent2']}" stroke-width="1" opacity="0.3"/>

  <!-- Metallic Overlay Framing -->
  <rect x="14" y="14" width="612" height="332" rx="12" fill="none" stroke="{s['accent']}" stroke-width="1.5" stroke-opacity="0.4"/>
  <rect x="20" y="20" width="600" height="320" rx="8" fill="none" stroke="#ffffff" stroke-width="0.5" stroke-opacity="0.15"/>

  <!-- Top Badges: Hazard Tags -->
  <g transform="translate(32, 34)">
    <rect x="0" y="0" width="84" height="24" rx="4" fill="#000000" opacity="0.7" stroke="{s['accent']}" stroke-width="1"/>
    <text x="42" y="16" font-family="'Segoe UI', Roboto, sans-serif" font-weight="800" font-size="10" fill="{s['accent']}" text-anchor="middle" letter-spacing="1">STAGE</text>
  </g>

  <g transform="translate(124, 34)">
    <rect x="0" y="0" width="110" height="24" rx="4" fill="#000000" opacity="0.7" stroke="{s['accent2']}" stroke-width="1"/>
    <text x="55" y="16" font-family="'Segoe UI', Roboto, sans-serif" font-weight="700" font-size="10" fill="#ffffff" text-anchor="middle">{s['hazards'][0].upper()}</text>
  </g>

  <!-- Stage Title & Location -->
  <g transform="translate(36, 265)">
    <text x="0" y="0" font-family="'Impact', 'Segoe UI Black', sans-serif" font-size="34" font-weight="900" fill="#ffffff" letter-spacing="1" font-style="italic">
      {s['name'].upper()}
    </text>
    <text x="0" y="24" font-family="'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="600" fill="{s['accent']}" letter-spacing="1.5">
      {s['location'].upper()}
    </text>
  </g>

  <!-- Tekken 8 Branding Watermark -->
  <text x="600" y="325" font-family="'Impact', sans-serif" font-size="18" font-weight="900" fill="#ffffff" opacity="0.3" text-anchor="end" font-style="italic">
    TEKKEN 8
  </text>
</svg>"""

    # Save SVG
    svg_filename = f"{s['id']}.svg"
    svg_path = os.path.join(STAGES_DIR, svg_filename)
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg_content.strip())
    print(f"Generated stage asset: {svg_filename}")

print("All 10 Tekken 8 Stage graphics created successfully!")

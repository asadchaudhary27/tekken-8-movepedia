import os

svg_template = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 360" width="640" height="360">
  <defs>
    <linearGradient id="bg_{id}" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="{c1}"/>
      <stop offset="50%" stop-color="{c2}"/>
      <stop offset="100%" stop-color="#080a0f"/>
    </linearGradient>
    <pattern id="grid_{id}" width="32" height="32" patternUnits="userSpaceOnUse">
      <path d="M 32 0 L 0 0 0 32" fill="none" stroke="{accent}" stroke-width="0.5" opacity="0.15"/>
    </pattern>
  </defs>

  <rect width="640" height="360" fill="url(#bg_{id})"/>
  <rect width="640" height="360" fill="url(#grid_{id})"/>

  <circle cx="140" cy="110" r="130" fill="{accent}" opacity="0.18" filter="blur(40px)"/>
  <circle cx="500" cy="210" r="150" fill="{c2}" opacity="0.2" filter="blur(50px)"/>

  <!-- Silhouettes -->
  <g opacity="0.4">
    <polygon points="0,250 90,210 180,235 300,175 410,215 510,165 580,205 640,185 640,360 0,360" fill="#030508"/>
    <polygon points="0,295 130,265 260,285 380,255 500,275 640,245 640,360 0,360" fill="#0a0e16"/>
  </g>

  <!-- Ground Line -->
  <line x1="0" y1="310" x2="640" y2="310" stroke="{accent}" stroke-width="2" opacity="0.6"/>
  <line x1="0" y1="315" x2="640" y2="315" stroke="#ffffff" stroke-width="0.5" opacity="0.2"/>

  <!-- Frame -->
  <rect x="14" y="14" width="612" height="332" rx="10" fill="none" stroke="{accent}" stroke-width="1.5" stroke-opacity="0.45"/>
  <rect x="20" y="20" width="600" height="320" rx="8" fill="none" stroke="#ffffff" stroke-width="0.5" stroke-opacity="0.12"/>

  <!-- Title & Hazard Badges -->
  <text x="34" y="58" fill="#ffffff" font-family="Impact, sans-serif" font-size="24" font-weight="900" letter-spacing="2" text-transform="uppercase">{name}</text>
  <text x="34" y="78" fill="#94a3b8" font-family="sans-serif" font-size="11" font-weight="700" letter-spacing="1">{location}</text>

  <g transform="translate(34, 94)">
    <rect width="{badge_w}" height="20" rx="4" fill="{accent}" opacity="0.85"/>
    <text x="10" y="14" fill="#ffffff" font-family="sans-serif" font-size="10" font-weight="900" letter-spacing="0.5">{hazards}</text>
  </g>
</svg>"""

new_stages = [
    {
        "file": "urban-square-evening.svg",
        "id": "use",
        "name": "URBAN SQUARE (EVENING)",
        "location": "TIMES SQUARE, NEW YORK, USA",
        "c1": "#311432",
        "c2": "#581c3f",
        "accent": "#f43f5e",
        "hazards": "WALL BREAK • BALCONY BREAK",
        "badge_w": 180
    },
    {
        "file": "arena-underground.svg",
        "id": "aug",
        "name": "THE ARENA (UNDERGROUND)",
        "location": "CLANDESTINE TOURNAMENT FACILITY",
        "c1": "#1e1b4b",
        "c2": "#312e81",
        "accent": "#38bdf8",
        "hazards": "WALL BLAST • ENCLOSED CAGE",
        "badge_w": 185
    },
    {
        "file": "elegant-palace.svg",
        "id": "ep",
        "name": "ELEGANT PALACE",
        "location": "CHÂTEAU DE VERSAILLES, FRANCE",
        "c1": "#2e1065",
        "c2": "#4c1d95",
        "accent": "#fbbf24",
        "hazards": "BALCONY BREAK • WALL BREAK",
        "badge_w": 180
    },
    {
        "file": "descent-into-subconscious.svg",
        "id": "dis",
        "name": "DESCENT INTO SUBCONSCIOUS",
        "location": "MISHIMA PSYCHOLOGICAL DREAMSCAPE",
        "c1": "#172554",
        "c2": "#1e3a8a",
        "accent": "#a855f7",
        "hazards": "FLOOR BLAST • WALL BLAST",
        "badge_w": 175
    },
    {
        "file": "secluded-training-ground.svg",
        "id": "stg",
        "name": "SECLUDED TRAINING GROUND",
        "location": "ANCIENT SHINTO DOJO, JAPAN",
        "c1": "#14532d",
        "c2": "#166534",
        "accent": "#22c55e",
        "hazards": "WALL BOUND • TRADITIONAL DOJO",
        "badge_w": 195
    },
    {
        "file": "genmaji-temple.svg",
        "id": "gt",
        "name": "GENMAJI TEMPLE",
        "location": "MOUNTAIN SANCTUARY, JAPAN",
        "c1": "#451a03",
        "c2": "#78350f",
        "accent": "#f97316",
        "hazards": "WALL BREAK • AUTUMN LEAVES",
        "badge_w": 180
    }
]

out_dir = "frontend/assets/img/stages"
os.makedirs(out_dir, exist_ok=True)
for s in new_stages:
    path = os.path.join(out_dir, s["file"])
    content = svg_template.format(**s)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Generated:", path)

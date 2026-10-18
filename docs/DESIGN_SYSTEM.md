# Design System & UI Specifications

> **Theme:** High-Octane Dark Metallic, Neon Crimson & Electric Cyan  
> **Source:** `frontend/assets/css/style.css` (Zero third-party CSS frameworks)  
> **Aesthetic Philosophy:** Restrained cyberpunk esports console interface. Dark surfaces with sharp neon accents.

---

## 1. Design Tokens Reference

All design tokens are defined on `:root` in `frontend/assets/css/style.css`:

### A. Surfaces & Backgrounds
```css
--surface-0: #0a0c10;          /* Base canvas */
--surface-1: #11141c;          /* Primary card background */
--surface-2: #161a24;          /* Elevated surface / headers */
--surface-3: #1e2330;          /* Interactive hover surface */
--bg-card:   #141722;          /* Standard card panel */
--bg-card-hover: #1c2130;      /* Card hover state */
```

### B. Accent Palette
```css
--accent-red-primary: #e61c33; /* Controlled fighting-game primary red */
--accent-red-hover:   #ff2a44; /* Interactive red hover */
--accent-crimson:     #d80027; /* Dark crimson badge fill */
--accent-cyan:        #00e5ff; /* Electric cyan secondary accent */
--accent-cyan-glow:   rgba(0, 229, 255, 0.40);
--accent-blue-secondary: #00d4ff;
--accent-gold:        #ffbe0b; /* Frame advantage & warning highlights */
--accent-purple:      #9d4edd; /* Stance / special property highlights */
```

### C. Text Hierarchy
```css
--text-main:  #f0f2f5;         /* High-contrast primary reading text */
--text-muted: #8b92a5;         /* Secondary descriptions & table labels */
--text-dim:   #64748b;         /* Tertiary notes, disclaimers, timestamps */
```

### D. Borders & Shadows
```css
--border-subtle:   rgba(255, 255, 255, 0.08);
--border-metallic: rgba(255, 255, 255, 0.16);
--border-bright:   rgba(255, 255, 255, 0.28);
--shadow-subtle:   0 2px 8px rgba(0, 0, 0, 0.4);
--shadow-elevation:0 8px 24px rgba(0, 0, 0, 0.6);
--focus-ring:      0 0 0 2px #0a0c10, 0 0 0 4px #e61c33;
```

---

## 2. Button Component System

All buttons across the platform inherit standard tokens to ensure consistent height, padding, and hover states:

| Class / Role | Height Token | Value | Radius | Font Size | Example Elements |
|---|---|---|---|---|---|
| **Hero Primary** | `--btn-h-hero` | `44px` | `8px` (`--btn-radius-base`) | `0.85rem` | `.btn-hero-primary` (Browse Roster) |
| **Hero Secondary**| `--btn-h-hero` | `44px` | `8px` (`--btn-radius-base`) | `0.85rem` | `.btn-hero-secondary` (Matchup Lab) |
| **Base / Actions**| `--btn-h-base` | `36px` | `6px` (`--btn-radius-sm`) | `0.78rem` | Primary action dialog buttons |
| **Navbar Controls**| `--btn-h-nav` | `32px` | `6px` (`--btn-radius-sm`) | `0.75rem` | Search, Notation, Tactics, Favs |
| **Filter Chips**  | `--btn-h-compact`| `30px`| `4px` (`--btn-radius-xs`) | `0.73rem` | `.filter-btn` (Mishima, Allies, etc.) |
| **Card Micro**   | `--btn-h-micro`| `26px` | `4px` (`--btn-radius-xs`) | `0.66rem` | `.btn-roster-action` (Dossier, Match) |

---

## 3. Fighter Roster Card Specification

The roster grid displays all 43 fighters with dense, proportional layout rules:

```
┌─────────────────────────────────┐
│ [DLC Badge]         [★ Favorite]│  <- Absolute top corners (6px offset)
│                                 │
│       Fighter Portrait          │  <- Height: 125px (object-fit: cover, top center)
│                                 │
├─────────────────────────────────┤
│ Character Name (e.g. Kazuya)    │  <- Font: 0.85rem bold, uppercase
│ Archetype (e.g. Mishima)        │  <- Font: 0.68rem, color: --text-muted
│ [Hurtbox: Male Standard]        │  <- Chip: 0.62rem, low-contrast badge
├─────────────────────────────────┤
│ [👤 Dossier] [⚔️ Match] [🥊 Combos]│  <- 3-column subgrid, height: 26px
└─────────────────────────────────┘
```

- **Desktop Grid:** `repeat(auto-fill, minmax(150px, 1fr))`, `gap: 10px` (yields 8–10 cards per row on 1080p).
- **Tablet Grid:** `repeat(auto-fill, minmax(140px, 1fr))`, `gap: 8px`.
- **Mobile Grid:** `repeat(2, 1fr)`, `gap: 8px`.

---

## 4. Tables & Data Presentation

### Moves Table (`.moves-table`)
- **Cell Padding:** Compact `0.42rem 0.65rem` (eliminates excessive scroll).
- **Sticky Header:** Top `0px`, `z-index: 20`, background `--surface-2` with `backdrop-filter: blur(8px)`.
- **Numeric Alignment:** Frame columns (`Startup`, `Block`, `Hit`, `CH`) are centered and monospace-formatted.
- **Frame Colors:**
  - Plus frames (`+1` to `+10`): `--accent-cyan` or soft green.
  - Launch punishable (`-15` or worse): Bright red pill badge (`background: rgba(230,28,51,0.2)`).
  - Safe on block (`-1` to `-9`): Subdued gray/neutral text.

---

## 5. Accessibility Conventions

1. **Focus Ring:** All interactive buttons and inputs implement `:focus-visible { outline: none; box-shadow: var(--focus-ring); }`.
2. **Contrast Standards:** All text (`#f0f2f5`) meets WCAG AAA standards (>7:1) against dark background (`#0a0c10`).
3. **Screen Readers:** SVG icons include `aria-hidden="true"`, and icon-only buttons include `aria-label` descriptors.

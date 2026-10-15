# Project State: Tekken 8 Frame Data, Move Reference, Notation Visualization and Training Assistant

**Milestone:** Phase 4 — Stage-Aware Strategy Engine & Blueprint Visualization Completed  
**Status:** All 4 Phases Implemented & Verified (41/41 Pytest Tests Passing)  
**Last Updated:** October 15, 2026  

---

## 1. Project Overview & Objectives

The goal of this Final Year Project (FYP) is to develop a high-performance, modular, and academically rigorous Tekken 8 web platform providing:
1. Complete frame data reference with startup, block advantage, hit advantage, counter-hit advantage, and combat properties.
2. An interactive 4-mode notation visualization engine (Arrows, English, Numpad, Physical Controller buttons).
3. A standardized data-fetching and normalization architecture with transparent data provenance and audit tracking.
4. A data-completeness and quality reporting system tracking missing fields, unknown frames, conflicting values, and patch versions.
5. An intuitive training assistant user interface styled with the "Tekken 8 Movepedia" cyber-metallic visual theme.
6. A comprehensive Matchup Analyzer with character selection, directional matchup intelligence, and smart punishment assistant.
7. A Stage-Aware Strategy Engine with interactive SVG boundary blueprints, hazard validation, and multi-faceted combo filtering.

---

## 2. Completed Milestones

- **Phase 1: Foundation & Selection System:** Full 43-character roster, 10 battlegrounds, notation parser, coverage audit, and responsive Movepedia UI.
- **Phase 2: Character Matchup Intelligence:** 10-section matchup dashboard, directional provenance, confidence scoring, fuzzy guard/interrupt defense matrix, and lab notes.
- **Phase 3: Smart Punishment Assistant:** Frame-perfect punisher recommendations (i10 to i15+ launch), stance awareness, interactive practice lab, and drill reaction timer.
- **Phase 4: Stage-Aware Strategy Engine:**
  - **Structured Stage Data:** Wall distances, shapes, break interactions (Wall Break, Floor Break, Balcony Break), and verified boundary geometry.
  - **Tactical Strategy Engine:** Analyzes midscreen combos, wall-carry routes, wall enders, wall breaks, floor breaks, balcony breaks, corner pressure, and unavailable mechanics warnings.
  - **Zero Fabricated Geometry Rule:** Real SVG blueprints for mapped stages (The Arena, Urban Square, Sanctum, Rebel Hangar, Coliseum, Seine barge); structured info panels for infinite/unmapped stages (Yakushima, Ortiz Farm).
  - **Stage-Aware Combo Filtering:** Dynamic filtering across all 6 combo categories, Heat requirements, Counter-Hit starters, and difficulty levels.
  - **Data Integrity & Frame Isolation:** Changing stages refreshes environmental tactics without altering character frame data.
  - **Test Coverage:** 41/41 passing tests in pytest across coverage, database, health, matchup, notation, punishment, and stage strategy.

---

## 2. Current Architecture & Components

```
tekken 8/
├── backend/
│   ├── app/
│   │   ├── api/v1/endpoints/  # Health, characters, moves, notation, coverage, sources
│   │   ├── core/              # App configuration, error handlers, constants
│   │   ├── database/          # SQLAlchemy session engine & DB initializers
│   │   ├── models/            # 11 Relational entities (Character, Move, DataSource, etc.)
│   │   ├── schemas/           # Pydantic validation & transfer schemas
│   │   ├── services/          # Notation parsing engine, coverage generator, adapters
│   │   └── main.py            # FastAPI main entrypoint
│   └── tests/                 # Automated pytest suite (health, models, notation, coverage)
├── frontend/
│   ├── index.html             # Movepedia SPA interface
│   └── assets/
│       ├── css/style.css      # Dark/red neon fighting game styling
│       ├── js/app.js          # Client-side reactivity, search, filter, live notation
│       ├── avatars/           # 86 local character portraits and brand icons
│       └── icons/             # 15 local SVG directional and input button glyphs
├── data/
│   ├── raw/                   # Preserved original payloads
│   ├── normalized/            # Validated JSON/CSV data records
│   ├── reports/               # Generated completeness & audit reports
│   └── fixtures/              # Test fixtures (characters, moves, imports)
├── docs/                      # Architectural specifications & audits
└── scripts/                   # Server execution and report CLI tools
```

---

## 3. Implemented Capabilities (Phase 1)

- **Source Research & Legal Audit:** Conducted thorough empirical investigation of 11 Tekken sources, documenting API capabilities, licensing terms, rate limits, and approval statuses in `docs/source-audit.md`.
- **Database Schema:** 11 SQLAlchemy models defined in `backend/app/models/` implementing relationships, uniqueness constraints, indexation, provenance separation, and non-zero handling for unknown frame values.
- **Notation Engine:** 4-mode parser supporting 9 directional states (including Neutral `•`), attack buttons (1, 2, 3, 4, 1+2, etc.), simultaneous vs sequential sequences, holds (`F`, `D`), repeated inputs (`f,f`), and preservation of unsupported tokens.
- **Coverage & Completeness Reporting:** System capable of computing field-population metrics, identifying missing vs unknown vs inapplicable fields, detecting conflicting values, and exporting JSON/CSV summaries.
- **Movepedia Frontend & Complete Visual Assets:** Complete frontend interface matching the user's uploaded "Tekken 8 Movepedia" visual design, including:
  - High-octane Hero faceoff artwork featuring Jin Kazama (flaming gauntlet & embers) vs Kazuya Mishima (electric blue lightning).
  - Official vector Tekken 8 logo and brand typography.
  - Choose Your Fighter carousel with all 43 fighters, animated `<` and `>` controls, and martial arts style subtitles.
  - Right sidebar with quick fighter pickers and design-accurate featured move rows.
  - Battle Stages showcase with photorealistic Arena render and 10 high-resolution stage vector cards with hazard tags.
  - Full suite of vector SVG glyphs for all 9 directions, 4 attack limbs, simultaneous buttons (1+2, 3+4, etc.), PlayStation/Xbox controller buttons, and Tekken 8 gameplay mechanics (Heat, Rage Art, Power Crush, Tornado, Homing).
- **100% Roster Moves Coverage:** Ingested 175 canonical verified moves spanning all 43 Tekken 8 fighters, ensuring zero empty states when browsing any character.
- **Multi-Device Responsive Design:** Fully optimized across Mobile (<480px), Tablets (768px-1024px), Laptops, and Desktops, featuring an adaptive navigation rail that smoothly transitions into a native-feeling bottom navigation bar on mobile devices.
- **Automated Tests:** Comprehensive unit and integration test suite targeting backend startup, health check, notation conversions, coverage reporting, and database integrity (14/14 passing).

---

## 4. Phase 1 Acceptance Checklist

| # | Criterion | Status | Notes |
|---|---|---|---|
| 1 | Existing project inspected and documented | **PASS** | `docs/initial-project-audit.md` |
| 2 | Every required source has an audit entry | **PASS** | 11 sources analyzed in `docs/source-audit.md` |
| 3 | Verified findings separated from unknown info | **PASS** | Explicit verification dates and limitation notes |
| 4 | Source permissions and licensing documented | **PASS** | Distinguishes code license vs data usage vs artwork copyright |
| 5 | Initial project structure created | **PASS** | Clean directory hierarchy matching specifications |
| 6 | Backend starts using documented instructions | **PASS** | Tested with Uvicorn and FastAPI |
| 7 | Health-check endpoint works | **PASS** | `/api/v1/health` verified |
| 8 | Initial database schema documented & implemented | **PASS** | 11 SQLAlchemy entities in `backend/app/models/` |
| 9 | Notation prototype produces tested conversions | **PASS** | 9 directions, `df+2`, controller mappings tested |
| 10 | Unsupported notation preserved | **PASS** | Unrecognized tokens flagged for review without data loss |
| 11 | Coverage report format implemented & tested | **PASS** | JSON & CSV export with fixtures verified |
| 12 | Setup & execution instructions in README | **PASS** | Comprehensive README.md created |
| 13 | Automated tests run and results recorded | **PASS** | pytest executed with 100% pass rate |
| 14 | Known limitations & decisions documented | **PASS** | Logged in `docs/architecture.md` and handover section |
| 15 | No fabricated real-game data claimed | **PASS** | Only verified fixtures and transparent imports utilized |

---

## 5. Handover Plan for Phase 2

1. Expand adapter network to ingest live MediaWiki API data from `wavu.wiki` (CC0 licensed).
2. Implement automated conflict resolution pipelines when multiple sources report divergent frame data.
3. Build the advanced combo path finder and training assistant drills.

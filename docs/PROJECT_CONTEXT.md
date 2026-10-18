# Project Context & Capabilities

> **System:** Tekken 8 Movepedia & Tournament Intelligence Platform  
> **Milestone:** Academic Computer Science Final Year Project (FYP) — Phase 1 through 9 Verified  
> **Patch Target:** Bandai Namco TEKKEN 8 Patch `v3.00.02` (Season 2 Standard)  
> **Live Deployment:** Vercel Serverless (`https://tekken-8-movepedia.vercel.app`)

---

## 1. System Purpose & Core Value Proposition

Tekken 8 Movepedia is a high-performance, frame-accurate competitive combat reference and tournament laboratory for Tekken 8. It replaces bulky spreadsheet databases and ad-heavy wikis with a zero-framework, low-latency, cyber-metallic fighting game interface backed by a verified relational database.

### Key Capabilities
1. **Verified Move Explorer:** 1,203 moves across all 43 fighters with startup frames, block/hit/counter-hit advantages, damage, hit levels, and combat properties (`PC`, `T!`, `Heat Engager`, `Homing`, `Tornado`).
2. **Complete Throw Arsenal:** 397 throws categorized into generic (`1+3`, `2+4`, `u/f+1+2`), command grabs, and side/back throws with visual hand cues (`1`, `2`, `1+2`) and break windows.
3. **Stage-Aware Strategy Engine:** 18 official stages with precision dimensions in meters and centimeters, round-start wall distances, backdash counts, combo carry requirements, and destructible hazards (Wall, Floor, Balcony breaks).
4. **Authentic Combo Scaling Lab:** 89 verified combo routes modeling Tekken 8's authentic damage degradation ($100\% \to 70\% \to 50\% \to 40\% \dots$), Heat Burst/Dash multipliers, and wall carry splats.
5. **Dual-Perspective Matchup Lab:** P1 vs P2 engine calculating optimal sidestep directions (`SSL`/`SSR`), whiff punishes, string duck/interrupt counters, and frame-perfect punisher recommendations (i10 to i15+ launch).
6. **Bilingual Tactics Compendium:** 10-tab tournament knowledge base supporting real-time language toggling between **English** and **Roman Urdu** for Pakistani/South Asian competitive esports communities.
7. **Character Profile Dossiers:** Comprehensive dossier modal for all 43 fighters detailing archetype, tournament tier, key neutral tools, panic moves, and optimal gameplans.
8. **Interactive 10-Slide Defense Deck:** Standalone slide deck at `/presentation` featuring dynamic Chart.js radar charts and system architecture walkthrough for academic defense.

---

## 2. Technology Stack

| Layer | Technology | Version | Purpose |
|---|---|---|---|
| **Backend Runtime** | Python | `3.12+` | Async execution, data parsing, API services |
| **Web Framework** | FastAPI | `>=0.115.0` | High-speed ASGI REST API, automatic OpenAPI/Swagger docs |
| **Database ORM** | SQLAlchemy | `>=2.0.35` | Relational 2.0 mapping, typed queries, foreign keys |
| **Data Validation** | Pydantic v2 | `>=2.9.0` | Schema validation, type enforcement, settings management |
| **Storage Engine** | SQLite 3 | `3.x` | Embedded relational persistence (`tekken8_fyp.db`) |
| **Frontend Core** | HTML5 / CSS3 / ES6 | Native | Zero-framework single-page application (SPA) |
| **Security & Auth** | bcrypt, PyJWT, pyotp | `bcrypt 5.0`, `PyJWT 2.15`, `pyotp 2.10` | Salted passwords, HMAC-SHA256 JWT, RFC 6238 TOTP 2FA |
| **Test Suite** | pytest | `>=9.1.1` | 148 automated unit, integration, and security tests |
| **Deployment Target**| Vercel Serverless | v2 builds | Static Edge CDN + ASGI Python serverless runtime |

---

## 3. Application Pages & Active Views

The application operates as a Single-Page Application (SPA) driven by `frontend/index.html` with tabbed views switched via `switchAppView(viewId)`:

| View ID / Route | Title | Content & Functionality |
|---|---|---|
| `view-fighters` (`#fighters`) | **Fighters & Moves** | 43-character roster grid (filters: Mishima, Allies, Rebels, Newcomers, Grappler, DLC), character dossier modal, verified move explorer table, combo lab cards, hurtbox class chips, and 4-mode notation toggle. |
| `view-matchup` (`#matchup`) | **Matchup Lab** | Dual fighter selectors (P1 vs P2), relative sidestep advice (`SSL`/`SSR`), fuzzy guard matrix, punish practice assistant, and reaction drill timer. |
| `view-stages` (`#stages`) | **Stage Blueprints** | 18 stages selector, vector blueprint renderers, centimeter spatial telemetry, wall carry calculators, and hazard transition matrices. |
| `view-tactics` (`#tactics`) | **Tactics Compendium** | 10-tab competitive encyclopedia with English / Roman Urdu language toggle covering Sidestep Matrix, Throw Breaks, Anti-Cheese, Installs, Wall Enders, 10-Hit Strings, Heat Smashes, Movement Bible, Hardware Lag Optimization, and Blender Protocol. |
| `/presentation` (`presentation.html`) | **FYP Defense Presentation** | 10-slide interactive slide deck with keyboard/swipe controls, Chart.js radar charts, architecture diagrams, and testing metrics. |
| **Admin Portal** (Modal) | **System Administration** | Cryptographic JWT login, TOTP 2FA QR code provisioning, audit trail log, batch JSON import/export, patch release manager, and database integrity checks. |
| **Global Search** (Modal `Ctrl+K`)| **Search Engine** | Real-time search across moves, inputs, notations, and fighter mechanics. |
| **Notation Guide** (Modal) | **Notation Visualizer** | Interactive converter rendering Tekken inputs into Directional Arrows, English, Numpad, and PS/Xbox/Arcade controller layouts. |

---

## 4. Current Scale & Verified Quantities

- **Total Fighters:** 43 (32 base roster + Season 1/2 DLC: Eddy Gordo, Lidia Sobieska, Heihachi Mishima, Clive, etc.)
- **Total Verified Moves:** 1,203
- **Total Character Throws:** 397
- **Total Wall Combo Enders:** 129
- **Total 10-Hit Strings:** 43
- **Total Heat Smashes:** 43
- **Total Battlegrounds:** 18
- **Total Verified Combos:** 89
- **Total Automated Pytest Tests:** 148 (100% passing)

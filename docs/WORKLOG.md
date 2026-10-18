# Project Worklog & Operational Activity

> **Current Status:** Phase 1 through Phase 9 Complete & Fully Verified  
> **Repository:** `https://github.com/asadchaudhary27/tekken-8-movepedia`  
> **Branch:** `main` | **Target Patch:** `v3.00.02`

---

## 1. Recent Milestone & Git Activity

| Commit | Date | Summary of Changes & Verifications |
|---|---|---|
| `c066bc1` | Oct 16, 2026 | **fix(vercel):** Add catch-all frontend handler and standard Vercel v2 build routes. Resolved 404 and MIME type issues on Vercel Edge CDN. |
| `e8fcb75` | Oct 16, 2026 | **fix(vercel):** Map static `/assets`, `/presentation` and root HTML directly to Vercel edge CDN. |
| `476fe4b` | Oct 16, 2026 | **fix(routing):** Add `VercelPathMiddleware` and explicit Vercel index route aliases to resolve 404 Not Found. |
| `8afef0a` | Oct 16, 2026 | **fix(vercel):** Configure Vercel serverless entrypoint `api/index.py`, writable `/tmp` database replication in `session.py`, `vercel.json`, and complete `requirements.txt` dependencies (`bcrypt`, `PyJWT`, `pyotp`, `qrcode`, `pillow`, `email-validator`). |
| `514d8e8` | Oct 16, 2026 | **fix(entrypoint):** Add root `main.py` and `app.py` FastAPI entrypoints, `Procfile`, and `pytest.ini` for cloud buildpack auto-detection. |
| `ac7586a` | Oct 16, 2026 | **feat(ui-data-expansion):** Website-wide button redesign, responsive compact fighter cards, bilingual compendium (English/Roman Urdu), complete throw arsenals (397), wall enders (129), 10-hit counters (43), and centimeter-accurate stage telemetry (18 stages). |
| `4c73048` | Oct 16, 2026 | **feat:** Complete interactive character profile and fighter dossier command center for all 43 fighters. |
| `9a909c3` | Oct 18, 2026 | **feat(ui-ux-modernization):** Implemented `world_famous_ui_tekken_8_design_system.md` blueprint. Removed `#userModeSwitcher` and `#btnNavSearch` to declutter navbar. Unified web app into single unhidden view with all technical frame data and matchup telemetry permanently visible. Added Linear/Vercel spotlight card glows, slanted cyber CTA buttons, high-contrast frame badges, distinct section demarcation headers, and optimized 2-column mobile responsiveness with horizontal scroll indicators (148/148 tests passing). |
| `433abb4` | Oct 18, 2026 | **feat(ui-buttons-cards):** Overhauled fighter roster cards with non-overlapping strict CSS grid layouts, solid dark carbon glass surfaces, and isolated hover states. Implemented 100% solid, non-transparent Tekken 8 cyber gaming styling on all buttons across the entire platform. 148/148 tests passing. |
| `ac9957d` | Oct 18, 2026 | **feat(ui-kinetic-blob):** Integrated user-requested kinetic roll flip buttons (`border-radius: 2rem`, `#3653f8` royal blue, staggered cascading `.span-mother` / `.span-mother2` letter roll) across hero CTAs and fighter action buttons. Implemented animated plasma blob bounce card architecture (`@keyframes blob-bounce 5s infinite ease`, `border-radius: 14px`, backdrop-filtered `.bg` plate with moving crimson/blue aura perimeter) across all 43 fighter roster cards. Set move cards to full width (1 per line). Removed Guide & right-side buttons from navbar. Zero-scroll 2-column stage selector. 148/148 tests passing. |
| `a49bf32` | Oct 18, 2026 | **feat(ui-notation-icons-ribbon):** Integrated authentic fighting game SVG icons (`1.svg`, `2.svg`, `3.svg`, `4.svg`, combinations `1+2`, `1+3`, `1+4`, `2+3`, `2+4`, `3+4`, `1+2+3+4`, directions `f`, `d`, `b`, `u`, diagonals `df`, `db`, `uf`, `ub`, `n` neutral star, `tornado`, `heat`, `power-crush`, `rage-art`, `follow.svg` step chevrons, and PS/Xbox controller icons) into notation engine and Combo Input Guide HUD. Zero mapping error constraint strictly verified. Enlarged Quick Ribbon cards (`.carousel-fighter-card` min-width 110px, avatar 82px x 82px, smooth hover transitions, clear archetype style subtitles, full responsive visibility). 148/148 tests passing. |
| `20b47fd` | Oct 18, 2026 | **refactor(ui):** Comprehensive platform button audit. Retained all 198 functional interactive buttons (roster, moves explorer, combo lab, matchup combat lab, reaction trainer, character dossiers, blueprints, compendium). Pruned 17 unattached dead buttons across 4 orphaned modals (`#favoritesModal`, `#settingsModal`, `#notationGuideModal`, `#practiceNotesModal`) whose navbar triggers were removed previously. 148/148 tests passing. |
| `b7069c8` | Oct 19, 2026 | **feat(story-stages-typography):** Ingested all 43 fighter stories, alliances, combat strengths (taqat), and weaknesses (kamzoriyan) from `story.docx` into character profiles and dossiers. Re-architected Battle Stages: eliminated sidebar column, introduced glowing cyber dropdown selection at section top, expanded arena imagery to full responsive scale with cinematic toggle, and removed internal scrolling constraints for 100% visible stage intelligence. Replaced entire site typography with Google Fonts `Plus Jakarta Sans`, `Chakra Petch`, and `JetBrains Mono` for maximum readability. 148/148 tests passing. |
| `c628e91` | Oct 19, 2026 | **feat(ui-ux-modernization):** 1. Combo Lab 1-per-row full-width cards with natural content height. 2. Expanded character roster cards (`minmax(215px, 1fr)`) with zero text collision and solid Tekken 8 themed buttons (Cyan Dossier, Gold Matchup, Crimson Combos). 3. 2026 Next-Gen Cyber Dropdowns with obsidian glass and custom SVG chevrons. 4. Enlarged Hero Section with clamp display typography and prominent stats. 5. Large Tables Architecture: Replaced dense spreadsheets with interactive 10-Hit Sequential Stepper Flow (10-node timeline with low parry alerts) and Blender Protocol Tactical Decision Cards (two-tone survival split: fatal mistake vs verified escape, with 1-click drill copy) + dual-mode table toggle. 148/148 tests passing. |
| `1cb48c1` | Oct 19, 2026 | **feat(combos-nav-cleanup):** 1. Removed Notation Engine section and modal test button. 2. Repaired mobile navigation drawer with fixed top-anchored layout, frosted glass backdrop, and responsive toggle. 3. Ingested all 79 high-damage optimal combo routes from `tekken8_high_damage_combos.txt` into `tekken8_fyp.db` and `init_db.py`. 4. Verified 79/79 combos match user data with 100% precision. 148/148 tests passing. |

---

## 2. Current Session Task

- **Task Name:** Tekken 8 Roster & Anti-Character Strategy Hub Integration (44 Characters + Universal Mechanics).
- **Objective:**
  1. Parse 100% of raw data from `Tekken 8 Master Guide.docx` (all 44 characters + universal combat mechanics).
  2. Create modular Data Layer `frontend/assets/js/tekken8MasterData.js` storing `UNIVERSAL_MECHANICS` and `ROSTER_DATA` (44 characters).
  3. Create modular Component Controller `frontend/assets/js/strategyHub.js` powering:
     - Component 1: Filterable Character Cards Grid with Search, Faction pills, Season pills, and Weak Side (`SSL` / `SSR`) badges.
     - Component 2: 3-Tab Interactive Character Profile Modal (Tab 1: Profile & Lore, Tab 2: Offense & Traps "Jaal", Tab 3: Anti-Character Guide "Chakma Dena & Kamzoriyan" with SSL/SSR, punishable moves, duck & interrupt strings, and parry vulnerabilities).
     - Component 3: Universal Mechanics Sub-Tabs (Controls & Notation, Frame Data Science, Master Low Parry Matrix, and Wall Traps & Escape Bible).
  4. Scoped CSS styling in `frontend/assets/css/style.css` matching dark cyberpunk HUD theme with zero style collisions.
  5. SPA integration in `frontend/index.html`, `index.html`, and `frontend/assets/js/app.js` (`switchAppView('strategy-hub')`).
- **Deliverables:**
  1. `frontend/assets/js/tekken8MasterData.js` (Complete 44-character database + universal combat mechanics)
  2. `frontend/assets/js/strategyHub.js` (Interactive UI controller with tab switching, search/filter, and modal)
  3. `frontend/assets/css/style.css` (Scoped `.strat-hub-*` and `.sh-modal-*` styles with responsive design down to 320px)
  4. `frontend/index.html` & `index.html` (100% byte-for-byte synchronized with `#strategy-hub` nav link, `#view-strategy-hub` view, and `#strategyDossierModal`)
  5. `frontend/assets/js/app.js` (Updated `switchAppView`, `hashchange`, and `DOMContentLoaded` router)
  6. `scripts/generate_master_data.py` & `scripts/build_strategy_data.py` (Deterministic ingestion pipelines)
  7. Verification: 148/148 backend pytest tests passing; zero JS syntax errors.

---

## 3. Known Issues & Operational Notes

- **Upstream Scraping Status:** Live web scraping against WavuWiki / TekkenDocs is disabled by default to eliminate upstream rate limiting and maintain deterministic offline execution. All data is verified and seeded from local fixtures.
- **Vercel Read-Only Filesystem:** On Vercel, the SQLite database is automatically copied to `/tmp/tekken8_fyp.db` on cold start. Any mutations in the serverless environment are temporary per instance. Production persistence should be migrated to PostgreSQL / Supabase if user-generated content needs persistent multi-instance storage.

---

## 4. Pending / Optional Future Work

- **Future DLC Ingestion:** Ingest Season 3+ DLC fighters when released by Bandai Namco.
- **Audio Sound FX:** Optional audio cues for controller button clicks in the notation guide.
- **Cloud PostgreSQL Migration:** Provision a Supabase or Neon PostgreSQL instance if multi-user writable data (custom notes, user accounts) is moved beyond demo stage.


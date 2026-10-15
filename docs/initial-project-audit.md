# Initial Project Audit & Baseline Inventory

**Project Title:** Tekken 8 Frame Data, Move Reference, Notation Visualization and Training Assistant Website  
**Audit Date:** October 15, 2026  
**Auditor:** Senior Software Architect & Lead Engineer  
**Workspace Root:** `I:\tekken 8`

---

## 1. Executive Summary

Prior to initiating Phase 1, a comprehensive filesystem and architectural inspection was conducted across the root directory `I:\tekken 8`. 

The initial workspace contained two pre-existing web asset mirrors:
1. `tekken8combo.kagewebsite.com`: A mirror of the community combo repository containing HTML templates, combo submission UI, character cards, input SVG vectors (`1.svg`, `2.svg`, `df.svg`, etc.), and character portraits.
2. `tekkendocs.com`: A mirror of the TekkenDocs static React/Tailwind frontend containing compiled client bundles, high-resolution 256px character brand avatars, and static data configuration mappings (`t8AvatarBrandMap256`, `staticDataService`).

No backend architecture (FastAPI), database (SQLite/PostgreSQL), ORM models, test suite, or automated data pipeline previously existed.

---

## 2. Inventory of Existing Project Files & Directories

| Path | Type | Size / Items | Description & Purpose | Preservation Decision |
|---|---|---|---|---|
| `tekken8combo.kagewebsite.com/` | Directory | ~4.5 MB | Full mirror of `tekken8combo.kagewebsite.com`. Includes combo pages, community poll markup, input icons (`tpl/img/input/`), and character portrait images (`tpl/img/char/`). | **Preserved intact.** Extracted 42 character portraits and 15 input SVGs into the application asset pipeline. |
| `tekkendocs.com/` | Directory | ~6.8 MB | Static mirror of `tekkendocs.com`. Contains compiled React client bundles, 256px character webp avatars (`assets/*brand-256*.webp`), and static mappings. | **Preserved intact.** Extracted 44 high-resolution brand avatars into `frontend/assets/avatars/`. |
| `.git/` | Directory | N/A | Previously non-existent. | Initialized Git version control repository. |
| `backend/` | Directory | N/A | Previously non-existent. | Initialized modular FastAPI backend architecture. |
| `frontend/` | Directory | N/A | Previously non-existent. | Initialized clean vanilla HTML5/CSS3/JS user interface matching "Tekken 8 Movepedia" UI design. |
| `data/` | Directory | N/A | Previously non-existent. | Initialized data directory (`raw/`, `normalized/`, `reports/`, `fixtures/`). |
| `docs/` | Directory | N/A | Previously non-existent. | Initialized project documentation suite. |

---

## 3. Existing Functionality & Preservation Strategy

### Preserved Components:
1. **Character Roster Assets:**
   - 44 character portraits and brand avatars from `tekkendocs.com` and `tekken8combo.kagewebsite.com` (e.g. Jin, Kazuya, Reina, King, Jun, Paul, Hwoarang, Clive, Eddy, Lidia, Heihachi, etc.).
   - Input glyphs for directions and attacks (`1.svg`, `2.svg`, `3.svg`, `df.svg`, `dh.svg`, `holdmax.svg`, etc.).
2. **Upstream Combo Structure:**
   - Notation sequences, hit counts, and damage values identified in the HTML archives (e.g., Kuma combo #2556, Panda combo #2555) serve as validated real-world combo fixtures.
3. **Third-Party Noise Isolation:**
   - Scraped ad scripts (`googlesyndication.com`, `posthog`, `cloudflareinsights`) are isolated and excluded from version control via `.gitignore` to prevent telemetry bloat and dependency vulnerabilities.

---

## 4. Deficiencies, Errors & Incomplete Features Identified

1. **No Backend or Service Layer:** No RESTful API, ASGI web server, or routing system existed.
2. **No Data Storage or Schema:** No database engine, tables, foreign keys, or integrity constraints were present.
3. **No Notation Normalization Engine:** Input notations existed only as fragmented HTML spans or unstructured strings with varying syntax conventions (`d/f` vs `df`, `1+2` vs `12.svg`).
4. **No Test Coverage:** pytest and automated QA infrastructure were completely absent.
5. **No Data Completeness & Quality Reporting:** No mechanism existed to audit move attributes, distinguish missing versus unknown frame data, or detect duplicate entries.

---

## 5. Baseline Conclusion

The baseline audit establishes that the project was essentially in an uninitialized greenfield state regarding backend, database, and business logic, but possessed valuable visual assets and raw HTML samples from community websites. Phase 1 establishes the complete foundation upon which later training features and live data fetchers will build.

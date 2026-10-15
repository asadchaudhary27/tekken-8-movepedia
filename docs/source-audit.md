# Data Source Research & Audit

**Audit Date:** October 15, 2026  
**Auditor:** Senior Software Architect & Data Extraction Engineer  
**Scope:** Evaluation of 11 potential data sources for Tekken 8 frame data, move lists, notation glyphs, and character guides.

---

## 1. Compliance, Legal & Licensing Guidelines

1. **Separation of Code, Data, and Artwork:**
   - A repository's open source license (such as MIT, BSD, or Apache) applies strictly to code logic, not to game art assets, logos, character renders, or third-party proprietary data.
   - Game artwork, trademarks, character designs, and logos are the intellectual property of **Bandai Namco Entertainment Inc.** and cannot be redistributed for commercial purposes without explicit licensing.
   - Factual frame data (frame numbers, startup frames, damage numbers, block advantages) represents mathematical measurements of game rules and mechanics. While factual game data is generally eligible for compilation and fair reference use, mass scraping of community-curated databases requires compliance with source terms of service and appropriate attribution.
2. **Acceptable Status Taxonomy:**
   - **Approved:** Legally permissible API/export with clear terms permitting academic or community ingestion.
   - **Approved with restrictions:** Allowed for non-commercial or academic research under specific attribution or rate limit constraints.
   - **Research only:** Useful for reference, cross-validation, and UI conceptualization; automated mass scraping not authorized.
   - **Blocked pending permission:** Access or redistribution explicitly prohibited or ambiguous; requires formal written consent.
   - **Unverified:** Source unreachable, endpoint non-existent, or documentation unavailable during the audit.

---

## 2. Comprehensive Source Audit Matrix

| Source | URL | Accessible | Tekken 8 data available | API/export | Available fields | Character coverage | Patch information | Code license | Data-use permission | Attribution | Restrictions | Upstream source | Limitations | Recommended use | Final status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **TekkenDocs** | `https://tekkendocs.com/` | Yes (Verified 2026-10-15) | Yes | Web API (`/api/t8/...`) & JSON endpoints | Move input, name, startup, block, hit, counter-hit, damage, level, properties, video URLs | All T8 characters (38+ base & DLC) | Patch versions tracked in guides & updates | Proprietary (No code distribution without permission) | Community data use permitted | Mandatory credit to `tekkendocs.com` & `rbnorway.org` | Non-commercial use, polite rate limiting | `wavu.wiki`, RBNorway, Community testing | No bulk ZIP dump; code closed-source | Secondary validation and reference adapter | **Approved with restrictions** |
| **TekkenDocs Features** | `https://tekkendocs.com/features` | Yes (Verified 2026-10-15) | Yes (Feature catalog) | None (Informational web page) | Documentation of frame quiz, daily challenge, video player, sidestep chart | N/A (Meta-features) | Version mentions | Proprietary | Documentation viewable | Standard attribution if cited | None | TekkenDocs team | Web page only, no raw data | Architectural reference for feature design | **Research only** |
| **TekkenDocs Credits** | `https://tekkendocs.com/credits` | Yes (Verified 2026-10-15) | Yes (Provenance audit) | Static JSON in page context | Contributor identities, data upstream origins, tool credits | N/A (Attribution list) | References T8 Season updates | Proprietary | Public credit notice | Acknowledge original contributors | None | `wavu.wiki`, RBNorway, tekkenwarehouse | Documentation only | Provenance tracing and citation verification | **Research only** |
| **Tekken8.org Frame Data** | `https://tekken8.org/frame-data/feng/` | Yes (Verified 2026-10-15) | Yes | Server-rendered HTML tables | Hit level, input, move name, startup, block, hit, CH, damage, properties (heat, crush, tornado) | Full T8 roster (Feng, Jin, etc.) | Explicit patch tagging (`Patch 3.00.02`) | Proprietary website | Informational use; no public bulk API | Credit `tekken8.org` | Automated scraping without consent discouraged | VizStudio Art / Community | No documented JSON API; HTML parsing required if scraped | Cross-reference validation & test fixture generation | **Research only** |
| **Tekken8-API** | `https://github.com/dammar01/Tekken8-API` | No (404 / Missing repo) | Unverified | Unknown | None | 0 | None | Unknown | Unknown | Unknown | Unknown | `dammar01` profile checked | Repository does not exist publicly under this URL (author hosts `Tekken8-Punisher`) | None until verified | **Unverified** |
| **T8 Notation Maker** | `https://github.com/LinSDK/t8-notation-maker` | Yes (Verified 2026-10-15) | Yes (Notation glyphs & combos) | Client-side JS generator (`index.html`, `render.html`) | Button glyphs, directions, bracket notations, OBS overlay settings | Universal T8 notation rules | Independent of game patches | MIT License (Code) | Code reusable under MIT; game art assets subject to Bandai Namco IP | MIT copyright notice | Do not claim ownership of Namco button icons | LinSDK | Notation tool only, does not store frame numbers | Notation engine design & glyph mapping | **Approved with restrictions** |
| **Tekken-Query** | `https://github.com/rekoriku/Tekken-Query` | No (404 / Missing repo) | Unverified | Unknown | None | 0 | None | Unknown | Unknown | Unknown | Unknown | User/repo query yielded no public hit | Repository inaccessible or private | None until verified | **Unverified** |
| **WavuWiki** | `https://wavu.wiki/` | Yes (Verified 2026-10-15) | Yes | MediaWiki REST/Action API & Cargo JSON export (`/w/api.php`) | Full move attributes, frame advantage, stances, transitions, hitboxes, recovery, notes | Complete T8 character roster | Explicit patch version tracking per revision | MediaWiki content under **Creative Commons Zero (CC0 1.0)** / Public Domain dedication | **Freely permissible under CC0** | Voluntary attribution appreciated | Polite querying, compress requests (`Accept-Encoding: gzip`) | Wavu community & laboratory testing | Wiki template variations between character pages | Primary authoritative data source for automated ingestion | **Approved** |
| **Tekken Space Archive** | `https://github.com/rherwig/tekken-space-archive` | Yes (Verified 2026-10-15) | Yes | Web app repo & parser tooling (`tekken-parser`) | Move properties, frame data tables, combo strings | Select T8 characters | Patch metadata tracked in git commits | Public Git repository | Open source companion tool | Standard git attribution | No official public API guarantee | `tekken.space` | Repository focused on frontend app; data embedded in code/parsers | Reference for parser structure and schema models | **Research only** |
| **Official Tekken Website** | `https://tekken.com/` | Yes (Verified 2026-10-15) | Yes (Official profiles, story, basic moves) | None (Commercial promotional website) | Character bios, official art, teaser videos, game modes | All official launched characters | Latest official updates & announcements | Proprietary © Bandai Namco | Commercial rights strictly reserved; no programmatic extraction rights | © Bandai Namco Entertainment Inc. | Scraping prohibited by Terms of Service; copyrighted artwork | Bandai Namco development studio | Basic move lists only; no detailed numerical frame data | Canonical character naming and visual inspiration | **Blocked pending permission** |
| **Bandai Namco Official** | `https://www.bandainamcoent.com/` | Yes (Verified 2026-10-15) | Yes (Corporate & release news) | None | Publisher news, official patch notes releases, EULA | Overall franchise coverage | Official publisher patch note PDFs/articles | Proprietary © Bandai Namco | Commercial reproduction strictly forbidden without license | Bandai Namco Entertainment | Strict copyright & anti-scraping policies | Bandai Namco | No structured frame database | Ground truth for official game patch releases and version numbers | **Research only** |

---

## 3. Summary of Approvals & Ingestion Strategy

1. **Primary Ingestion Source:** **WavuWiki (`wavu.wiki`)** is designated as the primary approved automated data source. Its MediaWiki Action API (`/w/api.php`) and CC0 (Creative Commons Zero) dedication offer the cleanest legal and technical foundation for automated, repeatable frame data ingestion.
2. **Secondary Cross-Validation Source:** **TekkenDocs (`tekkendocs.com`)** is approved with restrictions (academic/non-commercial citation with attribution to `tekkendocs.com` and `rbnorway.org`).
3. **Notation Standard Reference:** **T8 Notation Maker (`LinSDK/t8-notation-maker`)** provides verified notation syntax conventions under MIT.
4. **Offline Fixtures:** For initial development and offline testing, curated JSON fixtures based on verified community datasets are preserved in `data/fixtures/` to guarantee test reproducibility without live network dependence.

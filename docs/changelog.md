# Changelog - Tekken 8 FYP

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - Movepedia UI Precision & Visual Asset Engine - 2026-10-15

### Added
- **AI-Generated Hero Artwork:** Generated high-resolution 16:9 cinematic hero banner depicting Jin Kazama (with fiery demonic gauntlets and embers) clashing against Kazuya Mishima (with electric blue lightning) matching the user reference screenshot.
- **Stage Visuals & Renders:** Generated AAA photorealistic arena image for "The Arena" and 10 high-resolution vector artwork cards for all Tekken 8 battle stages with hazard badges (Wall Bound, Floor Blast, Balcony Break).
- **Official Vector Logos & Notation Icons:** Added official vector Tekken 8 logo SVG, full directional arrow SVG icons (9 directions), arcade button glyphs (1, 2, 3, 4, 1+2, 3+4, etc.), console controller buttons (PlayStation □, △, ✕, ○; Xbox X, Y, A, B), and gameplay mechanics (Heat, Rage Art, Power Crush, Tornado, Homing).
- **Roster & Carousel Perfection:** Complete 43-fighter roster with official high-resolution avatars and martial art style subtitles (e.g. Jin Kazama: Mishima-Style Karate).
- **Design-Matched Interactive Layout:** Implemented slim left navigation rail, interactive fighter carousel with `<` and `>` controls, quick fighter selector, and featured moves & combos panel.

## [0.1.0] - Phase 1 Foundation - 2026-10-15

### Added
- **Project Inspection & Baseline:** Completed comprehensive audit of existing mirrored website assets in `docs/initial-project-audit.md` and baseline project status in `docs/project-state.md`.
- **Legal & Technical Source Audit:** Audited 11 candidate Tekken sources with real endpoint verification, licensing parameters, and approval statuses in `docs/source-audit.md`.
- **Database Architecture:** Created 11 SQLAlchemy models with strict foreign keys, indexation, non-zero frame handling, and provenance tracking (`Character`, `Move`, `MoveInput`, `DataSource`, `ImportBatch`, `GamePatch`, `VerificationRecord`, `DataConflict`, `MissingDataIssue`, `MoveProperty`, `ComboRoute`, `UserPreference`).
- **Data Dictionary:** Formulated complete database specifications in `docs/data-dictionary.md`.
- **Data Completeness & Quality Reporter:** Developed quality audit framework tracking missing, unknown, conflicting, unverified, and inapplicable attributes with JSON/CSV export in `docs/coverage-report-design.md`.
- **Notation Engine Prototype:** Built modular tokenizer supporting 9 directional states (`↑`, `↖`, `↗`, `←`, `•`, `→`, `↙`, `↓`, `↘`), attack buttons (1, 2, 3, 4), holds, simultaneous/sequential inputs, and 4 display projections (Arrows, English, Numpad, Controller).
- **FastAPI Backend Skeleton:** Implemented type-safe ASGI application with health check (`/api/v1/health`), OpenAPI docs (`/docs`), database initialization, and error handling.
- **Movepedia User Interface:** Designed dark/red cyber-metallic fighting game UI matching the user's uploaded "Tekken 8 Movepedia" visual brief, featuring 42+ fighter cards, category filters, interactive notation translator, and data source status indicators.
- **Automated Test Suite:** Engineered comprehensive pytest suite validating backend startup, health check, database constraints, 9-direction notation conversions, and coverage reports.

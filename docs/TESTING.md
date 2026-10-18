# Testing & Quality Verification Guide

> **Test Runner:** pytest `>=9.1.1` via `pytest.ini` (`pythonpath = .`)  
> **Test Suite Scale:** 18 test files | **148 automated tests** | **100% Green Pass Rate**  
> **Mandatory Rule:** Never claim tests passed unless they were actually executed in the terminal.

---

## 1. Quick Test Execution Commands

Run all commands from the repository root (`I:\tekken 8`):

### A. Run Complete Backend Test Suite (148 Tests)
```powershell
.\.venv\Scripts\pytest backend/tests -v
```

### B. Fast Smoke Test (Health & Database Connectivity)
```powershell
.\.venv\Scripts\pytest backend/tests/test_health.py backend/tests/test_database.py -v
```

### C. Authentication & Security Test Suite
```powershell
.\.venv\Scripts\pytest backend/tests/test_admin_auth.py backend/tests/test_admin_data_management.py -v
```

### D. Combat Engines (Matchup, Punishment & Notation)
```powershell
.\.venv\Scripts\pytest backend/tests/test_matchup.py backend/tests/test_punishment.py backend/tests/test_notation.py -v
```

### E. Stage Strategy, Combos & Hurtbox Compatibility
```powershell
.\.venv\Scripts\pytest backend/tests/test_stage_strategy.py backend/tests/test_stage_combos.py backend/tests/test_combo_compatibility.py -v
```

### F. Quality Audit & Non-Destructive Ingestion
```powershell
.\.venv\Scripts\pytest backend/tests/test_audit_phase9.py backend/tests/test_source_audit.py backend/tests/test_coverage.py -v
```

---

## 2. Frontend & Static Asset Validation

Because the frontend is native ES6 JavaScript without a Webpack/Vite build pipeline, use Node.js syntax inspection:

### A. Validate JavaScript Syntax
```powershell
node -c frontend/assets/js/app.js
node -c frontend/assets/js/dossiers.js
node -c frontend/assets/js/stages.js
```

### B. Validate UI Elements & IDs
Executes DOM sanity check ensuring zero missing element IDs or broken class hooks:
```powershell
.\.venv\Scripts\python.exe scripts/verify_ui_refinement.py
```

### C. Validate Database Integrity
Scans core database tables for nulls, placeholders, or orphaned foreign keys:
```powershell
.\.venv\Scripts\python.exe scripts/audit_database_integrity.py
```

---

## 3. Test Files Directory Mapping

All tests reside in `backend/tests/`:

| Test File | Tests | Validated Subsystem |
|---|---|---|
| `test_health.py` | 2 | API status endpoint and database connectivity ping. |
| `test_database.py` | 3 | SQLite table creation, foreign key constraints, and seed idempotency. |
| `test_notation.py` | 14 | 4-mode notation conversions (arrows, numpad, english, buttons). |
| `test_matchup.py` | 8 | P1 vs P2 dual-perspective sidestep calculations and weak side logic. |
| `test_punishment.py` | 10 | Standing and while-standing frame-perfect punishers (i10 to i15+). |
| `test_stage_strategy.py` | 12 | Stage geometry, boundary shapes, and break hazard properties. |
| `test_stage_combos.py` | 8 | Stage carry distances and combo wall splat interactions. |
| `test_combo_compatibility.py` | 9 | Hurtbox class Quirks (Bears, Gigas/Jack, Female hurtboxes). |
| `test_admin_auth.py` | 11 | Salted bcrypt hashing, JWT expiry, brute-force rate limiter, TOTP 2FA. |
| `test_admin_data_management.py` | 10 | Batch import/export JSON, audit log recording, non-destructive rollbacks. |
| `test_move_explorer.py` | 12 | Multi-criteria move search, frame filtering, and property queries. |
| `test_gameplay_guides.py` | 7 | Tactical anti-cheese strings, duck points, and install mechanics. |
| `test_qol_features.py` | 11 | Favorites, user preferences, and export formatting. |
| `test_source_audit.py` | 6 | Provenance attribution and rate-limit delay verification. |
| `test_coverage.py` | 8 | Data completeness metric calculations and health score reporting. |
| `test_data_architecture.py` | 6 | Relational join integrity and session lifecycle management. |
| `test_integration_phase8.py` | 6 | End-to-end API client workflows across all 4 views. |
| `test_audit_phase9.py` | 5 | Final system-wide validation and zero-placeholder guarantees. |
| **Total** | **148** | **All 148 passing (100% green).** |

---

## 4. Pre-Commit Smoke Checklist

Before committing any code or pushing to remote, verify:
- [ ] `pytest backend/tests` passes 148/148 tests.
- [ ] `node -c frontend/assets/js/app.js` returns clean with exit code 0.
- [ ] `git status` reports only files related to the requested task.
- [ ] No hardcoded passwords, personal access tokens, or secrets in git diff.

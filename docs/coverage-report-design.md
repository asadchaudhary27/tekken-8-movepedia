# Data Completeness & Coverage Report Specification

**Document Version:** 1.0 (Phase 1 Specification)  
**Standard:** Tekken 8 Academic Research Quality Assurance  
**Formats Supported:** JSON & CSV  

---

## 1. Quality & Completeness Taxonomy

To avoid false representations of completeness, the system defines eight explicit states for every data point:

1. **Missing Field:** A required property (e.g. startup, hit level, input notation) that is expected for the move category but is absent from the dataset.
2. **Not Provided by Source:** A property that the upstream data source does not capture or publish (e.g. recovery frames on whiff, active hitbox duration).
3. **Inapplicable Field:** A property that has no physical meaning for the move type (e.g. block advantage on a hit-throw or an unblockable attack; startup frames on a passive stance).
4. **Unknown Value:** A property that exists in game mechanics but is currently undetermined or variable (represented as `NULL` in the database, never `0`).
5. **Conflicting Value:** A property where two distinct approved sources report contradictory numerical measurements (e.g. Source A reports `-13`, Source B reports `-14`).
6. **Unverified Value:** A raw imported measurement that has not yet been corroborated by multi-source consensus or manual frame analysis.
7. **Verified Value:** A measurement confirmed by game memory inspection, developer patch notes, or unanimous community consensus.
8. **Confirmed Absence:** An attribute explicitly confirmed to not exist for this move (e.g. confirmed lack of counter-hit property or absence of chip damage).

---

## 2. Mathematical Definition of Field Coverage

Field-population percentages **MUST NOT** be presented as proof of complete roster or move list coverage. Instead, they represent the attribute completeness of known records:

$$\text{Field Coverage \%} = \left( \frac{\text{Populated Applicable Fields}}{\text{Total Required Applicable Fields}} \right) \times 100$$

Where:
- Inapplicable fields (`is_applicable == False`) are strictly excluded from the denominator.
- Fields marked `NOT_PROVIDED` are tracked separately in the provenance audit and not counted as missing if documented.
- Unknown fields (`NULL`) count against the field coverage percentage.

---

## 3. JSON Schema Specification

The coverage report is exported according to the following JSON structure:

```json
{
  "report_id": "cov-20261015-001",
  "generated_at": "2026-10-15T10:45:00Z",
  "game_patch": "3.00.02",
  "roster_summary": {
    "expected_roster_count": 42,
    "ingested_character_count": 42,
    "roster_coverage_percentage": 100.0,
    "missing_characters": []
  },
  "move_summary": {
    "total_moves_ingested": 1850,
    "average_moves_per_character": 44.05,
    "duplicate_records_detected": 0,
    "unverified_records": 120,
    "conflicting_records": 4
  },
  "field_coverage": {
    "required_fields": {
      "input_notation": 100.0,
      "hit_level": 99.2,
      "damage": 98.5,
      "startup_frames": 96.8,
      "block_advantage": 95.4
    },
    "optional_fields": {
      "hit_advantage": 92.1,
      "counter_hit_advantage": 84.7,
      "move_name": 78.3,
      "stance_context": 62.0
    },
    "overall_field_coverage_percentage": 94.6
  },
  "deficiency_breakdown": {
    "missing_required_count": 42,
    "not_provided_count": 88,
    "inapplicable_count": 115,
    "unknown_value_count": 31,
    "unsupported_notation_tokens": [
      { "token": "~F", "count": 12, "example_move": "f,F+3~F" },
      { "token": "DVK", "count": 4, "example_move": "1,1,2,DVK.D" }
    ]
  },
  "data_sources_audited": [
    {
      "source_name": "wavu_wiki",
      "status": "APPROVED",
      "records_provided": 1400,
      "conflicts_count": 2
    },
    {
      "source_name": "tekkendocs",
      "status": "APPROVED_WITH_RESTRICTIONS",
      "records_provided": 450,
      "conflicts_count": 2
    }
  ]
}
```

---

## 4. CSV Schema Specification

For tabular analysis and archival review, the report generator exports a per-character summary CSV (`data/reports/coverage_summary.csv`):

```csv
character_slug,character_name,total_moves,startup_coverage_pct,block_coverage_pct,hit_coverage_pct,ch_coverage_pct,damage_coverage_pct,unverified_count,conflict_count
jin,Jin Kazama,85,97.6,96.4,94.1,88.2,100.0,3,0
kazuya,Kazuya Mishima,78,98.7,97.4,92.3,87.1,98.7,2,1
reina,Reina,82,95.1,93.9,91.4,82.9,97.5,5,1
king,King,110,94.5,92.7,89.0,80.0,96.3,8,2
```

---

## 5. Report Generation Workflow

1. Ingestion of data from adapter or test fixtures.
2. Normalization and integrity validation via Pydantic schemas.
3. Execution of the `CoverageReportingService`:
   - Calculates field-by-field completeness per character.
   - Audits unrecognized notation syntax tokens.
   - Detects duplicates by composite key `(character_id, normalized_notation)`.
   - Flags discrepancies in conflicting sources.
4. Export to `data/reports/coverage_<timestamp>.json` and `.csv`.

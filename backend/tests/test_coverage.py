import os
import pytest
from backend.app.services.coverage import CoverageReportingService


def test_empty_coverage_report_generation(empty_db):
    """Verifies that an empty database generates a valid report with 0% coverage and no division by zero."""
    report = CoverageReportingService.generate_report(empty_db)
    assert report is not None
    assert report.roster_summary.ingested_character_count == 0
    assert report.roster_summary.roster_coverage_percentage == 0.0
    assert report.move_summary.total_moves_ingested == 0
    assert report.move_summary.average_moves_per_character == 0.0
    assert report.field_coverage.overall_field_coverage_percentage == 0.0


def test_populated_coverage_report_and_export(test_db):
    """Verifies coverage report generation on populated database and checks JSON/CSV output."""
    report = CoverageReportingService.generate_report(test_db)
    assert report.roster_summary.ingested_character_count == 43
    assert report.roster_summary.roster_coverage_percentage == 100.0
    assert report.move_summary.total_moves_ingested > 0
    assert report.field_coverage.overall_field_coverage_percentage > 0.0

    # Test file export
    json_path, csv_path = CoverageReportingService.export_report_files(report, reports_dir="data/reports")
    assert os.path.exists(json_path)
    assert os.path.exists(csv_path)

    with open(csv_path, "r", encoding="utf-8") as f:
        header = f.readline()
        assert "character_slug" in header
        assert "startup_coverage_pct" in header

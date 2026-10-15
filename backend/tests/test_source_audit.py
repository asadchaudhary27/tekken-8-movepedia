import pytest
from backend.app.models.source import DataSource
from backend.app.services.adapters.fixture_adapter import LocalFixtureAdapter


def test_data_sources_approval_status(test_db):
    """Ensures audited sources are correctly cataloged with their verified status."""
    wavu = test_db.query(DataSource).filter(DataSource.name == "wavu_wiki").first()
    assert wavu is not None
    assert wavu.approval_status == "APPROVED"
    assert wavu.license_type == "CC0 1.0"

    tekkendocs = test_db.query(DataSource).filter(DataSource.name == "tekkendocs").first()
    assert tekkendocs is not None
    assert tekkendocs.approval_status == "APPROVED_WITH_RESTRICTIONS"

    namco = test_db.query(DataSource).filter(DataSource.name == "official_tekken").first()
    assert namco is not None
    assert namco.approval_status == "BLOCKED_PENDING_PERMISSION"


def test_fixture_adapter_import_and_error_handling():
    """Validates adapter execution, record normalization, and graceful error reporting."""
    adapter = LocalFixtureAdapter(raw_storage_dir="data/raw")

    # Valid import
    report = adapter.run_import("feng", fixture_path="data/fixtures/sample_moves.json")
    assert report.total_records >= 2
    assert report.successful_records >= 2
    assert report.failed_records == 0
    assert len(report.errors) == 0

    # Non-existent fixture file handling
    empty_report = adapter.run_import("feng", fixture_path="data/fixtures/non_existent.json")
    assert empty_report.total_records == 0
    assert empty_report.successful_records == 0

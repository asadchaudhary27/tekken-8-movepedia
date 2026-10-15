"""
CLI script to generate, compute, and export real-time Data Completeness and Coverage Reports.
"""

import sys
import os

# Add root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.app.database.session import SessionLocal
from backend.app.services.coverage import CoverageReportingService


def main():
    print("Generating Tekken 8 Coverage & Data Completeness Report...")
    db = SessionLocal()
    try:
        report = CoverageReportingService.generate_report(db)
        json_path, csv_path = CoverageReportingService.export_report_files(report)
        print(f"Report ID: {report.report_id}")
        print(f"Roster Coverage: {report.roster_summary.roster_coverage_percentage}% ({report.roster_summary.ingested_character_count}/{report.roster_summary.expected_roster_count} fighters)")
        print(f"Total Moves: {report.move_summary.total_moves_ingested}")
        print(f"Overall Field Coverage: {report.field_coverage.overall_field_coverage_percentage}%")
        print(f"JSON Report exported to: {json_path}")
        print(f"CSV Summary exported to: {csv_path}")
    except Exception as e:
        print(f"Error generating report: {e}")
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    main()

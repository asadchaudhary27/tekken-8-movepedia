from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse, PlainTextResponse
from sqlalchemy.orm import Session
from backend.app.database.session import get_db
from backend.app.schemas.coverage import CoverageReportResponse
from backend.app.services.coverage import CoverageReportingService

router = APIRouter()


@router.get("/summary", response_model=CoverageReportResponse, summary="Get real-time data coverage report")
def get_coverage_summary(db: Session = Depends(get_db)):
    report = CoverageReportingService.generate_report(db)
    # Also save to data/reports/
    CoverageReportingService.export_report_files(report)
    return report


@router.get("/export/{file_format}", summary="Export coverage report as JSON or CSV")
def export_coverage_report(file_format: str, db: Session = Depends(get_db)):
    fmt = file_format.lower()
    if fmt not in ["json", "csv"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Supported export formats are 'json' or 'csv'."
        )

    report = CoverageReportingService.generate_report(db)
    json_path, csv_path = CoverageReportingService.export_report_files(report)

    if fmt == "csv":
        return FileResponse(
            path=csv_path,
            filename=f"coverage_report_{report.report_id}.csv",
            media_type="text/csv"
        )
    return FileResponse(
        path=json_path,
        filename=f"coverage_report_{report.report_id}.json",
        media_type="application/json"
    )

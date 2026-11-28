from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import SessionLocal
from app.services.ap_workflow_service import process_invoice

router = APIRouter(tags=["Finance - AP Workflow"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/documents/{document_id}/process")
def process_uploaded_invoice(
    document_id: int,
    db: Session = Depends(get_db),
):
    try:
        return process_invoice(document_id, db)

    except ValueError as exc:
        raise HTTPException(
            status_code=404 if str(exc) == "Document not found" else 400,
            detail=str(exc),
        )
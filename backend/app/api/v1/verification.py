from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import SessionLocal
from app.database.models.document import Document
from app.services.invoice_matching_service import verify_invoice
from app.services.exception_explanation_service import (
    explain_invoice_exception,
)

router = APIRouter(tags=["Finance - Invoice Verification"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/documents/{document_id}/verify")
def verify_uploaded_invoice(
    document_id: int,
    db: Session = Depends(get_db),
):
    document = (
        db.query(Document)
        .filter(Document.id == document_id)
        .first()
    )

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found",
        )

    if not document.invoice_data:
        raise HTTPException(
            status_code=400,
            detail="Invoice has not been extracted yet",
        )

    result = verify_invoice(document.invoice_data, db)

    explanation = explain_invoice_exception(
        document.invoice_data,
        result,
    )

    return {
        "document_id": document.id,
        "filename": document.original_filename,
        **result,
        "exception_explanation": explanation,
    }
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import SessionLocal
from app.database.models.document import Document
from app.services.invoice_extraction_service import extract_invoice_fields

router = APIRouter(tags=["Finance - Invoices"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/documents/{document_id}/extract-invoice")
def extract_invoice(
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

    if not document.extracted_text:
        raise HTTPException(
            status_code=400,
            detail="Document has no extracted text",
        )

    try:
        extracted_data = extract_invoice_fields(
            document.extracted_text
        )

        document.invoice_data = extracted_data
        db.commit()
        db.refresh(document)

    except RuntimeError as exc:
        db.rollback()
        raise HTTPException(
            status_code=502,
            detail=str(exc),
        )
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Could not save extracted invoice data",
        )

    return {
        "document_id": document.id,
        "filename": document.original_filename,
        "invoice_data": extracted_data,
    }
from sqlalchemy.orm import Session

from app.database.models.document import Document
from app.services.invoice_extraction_service import extract_invoice_fields
from app.services.invoice_matching_service import verify_invoice
from app.services.exception_explanation_service import (
    explain_invoice_exception,
)


def process_invoice(document_id: int, db: Session):

    document = (
        db.query(Document)
        .filter(Document.id == document_id)
        .first()
    )

    if not document:
        raise ValueError("Document not found")

    if not document.extracted_text:
        raise ValueError("Document has no extracted text")

    # Step 1: Extract invoice fields
    invoice_data = extract_invoice_fields(document.extracted_text)

    # Step 2: Persist extracted invoice data
    document.invoice_data = invoice_data
    db.commit()
    db.refresh(document)

    # Step 3: Verify invoice against purchase order
    verification_result = verify_invoice(invoice_data, db)

    # Step 4: Generate exception explanation
    explanation = explain_invoice_exception(
        invoice_data,
        verification_result,
    )

    # Step 5: Return complete AP result
    return {
        "document_id": document.id,
        "filename": document.original_filename,
        "invoice_data": invoice_data,
        **verification_result,
        "exception_explanation": explanation,
    }
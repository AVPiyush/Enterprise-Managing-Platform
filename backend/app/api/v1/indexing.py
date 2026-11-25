
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import SessionLocal
from app.database.models.document import Document
from app.services.document_indexer import index_document


router = APIRouter(tags=["Document Indexing"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/documents/{document_id}/index")
def index_existing_document(
    document_id: int,
    db: Session = Depends(get_db),
):
    document = db.query(Document).filter(
        Document.id == document_id
    ).first()

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
        chunk_count = index_document(
            document_id=document.id,
            filename=document.original_filename,
            text=document.extracted_text,
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Document indexing failed",
        )

    return {
        "document_id": document.id,
        "filename": document.original_filename,
        "chunks_created": chunk_count,
        "status": "indexed",
    }

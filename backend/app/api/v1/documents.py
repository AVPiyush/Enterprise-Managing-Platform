
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database.session import SessionLocal
from app.database.models.document import Document
from app.services.pdf_service import extract_pdf_text


router = APIRouter(tags=["Documents"])

UPLOAD_DIR = Path(__file__).resolve().parents[3] / "uploads"
MAX_FILE_SIZE = 10 * 1024 * 1024


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/documents/upload")
def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    if not file.filename or Path(file.filename).suffix.lower() != ".pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    file_content = file.file.read(MAX_FILE_SIZE + 1)

    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="Maximum file size is 10 MB")

    if not file_content.startswith(b"%PDF-"):
        raise HTTPException(status_code=400, detail="Invalid PDF file")

    try:
        extracted_text = extract_pdf_text(file_content)
    except Exception:
        raise HTTPException(status_code=400, detail="Could not read PDF file")

    stored_filename = f"{uuid4().hex}.pdf"

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    file_path = UPLOAD_DIR / stored_filename
    file_path.write_bytes(file_content)

    document = Document(
        original_filename=file.filename,
        stored_filename=stored_filename,
        file_path=str(file_path),
        extracted_text=extracted_text,
        extraction_status=(
            "extracted" if extracted_text else "no_text_found"
        ),
    )

    try:
        db.add(document)
        db.commit()
        db.refresh(document)
    except Exception:
        db.rollback()
        file_path.unlink(missing_ok=True)
        raise HTTPException(status_code=500, detail="Could not save document")

    return {
        "id": document.id,
        "filename": document.original_filename,
        "extraction_status": document.extraction_status,
        "extracted_characters": len(extracted_text),
        "message": "Document uploaded successfully",
    }

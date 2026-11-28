
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.sql import func

from app.database.base import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    original_filename = Column(String, nullable=False)
    stored_filename = Column(String, unique=True, nullable=False)
    file_path = Column(String, nullable=False)
    content_type = Column(String, default="application/pdf")
    extracted_text = Column(Text, nullable=True)
    extraction_status = Column(String, default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    invoice_data = Column(JSON, nullable=True)

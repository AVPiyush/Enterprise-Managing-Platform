from sqlalchemy import Column, Integer, String, Numeric, DateTime
from sqlalchemy.sql import func

from app.database.base import Base


class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"

    id = Column(Integer, primary_key=True, index=True)

    po_number = Column(String, unique=True, nullable=False, index=True)

    vendor_name = Column(String, nullable=False)

    currency = Column(String(3), nullable=False)

    total_amount = Column(Numeric(12, 2), nullable=False)

    status = Column(String, default="approved", nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database.session import SessionLocal
from app.database.models.purchase_order import PurchaseOrder

router = APIRouter(tags=["Finance - Purchase Orders"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class PurchaseOrderRequest(BaseModel):
    po_number: str = Field(min_length=1, max_length=100)
    vendor_name: str = Field(min_length=1, max_length=255)
    currency: str = Field(min_length=3, max_length=3)
    total_amount: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    status: str = "approved"


@router.post("/purchase-orders")
def create_purchase_order(
    request: PurchaseOrderRequest,
    db: Session = Depends(get_db),
):
    purchase_order = PurchaseOrder(
        po_number=request.po_number,
        vendor_name=request.vendor_name,
        currency=request.currency.upper(),
        total_amount=request.total_amount,
        status=request.status.lower(),
    )

    db.add(purchase_order)

    try:
        db.commit()
        db.refresh(purchase_order)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Purchase order number already exists",
        )

    return {
        "id": purchase_order.id,
        "po_number": purchase_order.po_number,
        "vendor_name": purchase_order.vendor_name,
        "currency": purchase_order.currency,
        "total_amount": str(purchase_order.total_amount),
        "status": purchase_order.status,
    }


@router.get("/purchase-orders")
def get_purchase_orders(db: Session = Depends(get_db)):
    purchase_orders = (
        db.query(PurchaseOrder)
        .order_by(PurchaseOrder.id.desc())
        .all()
    )

    return [
        {
            "id": po.id,
            "po_number": po.po_number,
            "vendor_name": po.vendor_name,
            "currency": po.currency,
            "total_amount": str(po.total_amount),
            "status": po.status,
        }
        for po in purchase_orders
    ]
from decimal import Decimal, InvalidOperation

from app.database.models.purchase_order import PurchaseOrder


def normalize_name(value: str) -> str:
    return " ".join(value.lower().strip().split())


def verify_invoice(invoice_data: dict, db):
    discrepancies = []

    po_number = invoice_data.get("purchase_order_number")
    vendor_name = invoice_data.get("vendor_name")
    currency = invoice_data.get("currency")
    invoice_total = invoice_data.get("total_amount")

    # Required invoice fields
    if not po_number:
        discrepancies.append("Invoice is missing its purchase order number")

    if not vendor_name:
        discrepancies.append("Invoice is missing its vendor name")

    if not currency:
        discrepancies.append("Invoice is missing its currency")

    if invoice_total is None:
        discrepancies.append("Invoice is missing its total amount")

    # Find the corresponding purchase order
    purchase_order = None

    if po_number:
        purchase_order = (
            db.query(PurchaseOrder)
            .filter(PurchaseOrder.po_number == po_number)
            .first()
        )

        if not purchase_order:
            discrepancies.append(
                f"Purchase order {po_number} was not found"
            )

    if purchase_order:
        # Vendor comparison
        if vendor_name and normalize_name(vendor_name) != normalize_name(
            purchase_order.vendor_name
        ):
            discrepancies.append(
                f"Vendor mismatch: invoice says '{vendor_name}', "
                f"but PO says '{purchase_order.vendor_name}'"
            )

        # Currency comparison
        if currency and currency.upper() != purchase_order.currency.upper():
            discrepancies.append(
                f"Currency mismatch: invoice uses {currency.upper()}, "
                f"but PO uses {purchase_order.currency.upper()}"
            )

        # Amount comparison
        if invoice_total is not None:
            try:
                invoice_amount = Decimal(str(invoice_total))
                po_amount = Decimal(str(purchase_order.total_amount))

                if abs(invoice_amount - po_amount) > Decimal("0.01"):
                    discrepancies.append(
                        f"Amount mismatch: invoice total is "
                        f"{invoice_amount}, but PO total is {po_amount}"
                    )
            except InvalidOperation:
                discrepancies.append(
                    "Invoice total amount is not a valid number"
                )

        # PO status check
        if purchase_order.status.lower() != "approved":
            discrepancies.append(
                f"Purchase order status is '{purchase_order.status}', "
                "not approved"
            )

    return {
        "verification_status": (
            "matched" if not discrepancies else "exception"
        ),
        "purchase_order": (
            {
                "id": purchase_order.id,
                "po_number": purchase_order.po_number,
                "vendor_name": purchase_order.vendor_name,
                "currency": purchase_order.currency,
                "total_amount": str(purchase_order.total_amount),
                "status": purchase_order.status,
            }
            if purchase_order
            else None
        ),
        "discrepancies": discrepancies,
    }
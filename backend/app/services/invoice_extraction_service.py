import json
import httpx

from app.core.config import settings


def extract_invoice_fields(document_text: str) -> dict:
    url = f"{settings.OLLAMA_BASE_URL}/api/chat"

    prompt = f"""
Extract the invoice information from the document below.

Return ONLY valid JSON with these exact keys:

{{
    "invoice_number": null,
    "vendor_name": null,
    "invoice_date": null,
    "due_date": null,
    "purchase_order_number": null,
    "currency": null,
    "subtotal": null,
    "tax_amount": null,
    "total_amount": null
}}

Rules:
- Do not invent missing information.
- Use null when a field is not available.
- Dates must use YYYY-MM-DD format.
- Monetary values must be strings containing numbers only.
- Do not calculate missing amounts.
- Extract the values as printed on the invoice.

INVOICE DOCUMENT:
{document_text}
"""

    payload = {
        "model": settings.OLLAMA_MODEL,
        "stream": False,
        "format": "json",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are an invoice data extraction system. "
                    "Extract information accurately. Never guess."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    }

    try:
        response = httpx.post(url, json=payload, timeout=120)
        response.raise_for_status()

        result = response.json()["message"]["content"]
        extracted_data = json.loads(result)

        required_fields = [
            "invoice_number",
            "vendor_name",
            "invoice_date",
            "due_date",
            "purchase_order_number",
            "currency",
            "subtotal",
            "tax_amount",
            "total_amount",
        ]

        return {
            field: extracted_data.get(field)
            for field in required_fields
        }

    except (httpx.HTTPError, KeyError, ValueError) as exc:
        raise RuntimeError(
            f"Invoice extraction failed: {exc}"
        ) from exc
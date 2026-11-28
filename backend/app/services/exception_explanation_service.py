import json

from app.services.ollama_service import generate_answer


def explain_invoice_exception(
    invoice_data: dict,
    verification_result: dict,
) -> str:

    if verification_result["verification_status"] == "matched":
        return "No discrepancies found. Invoice matches the purchase order."

    evidence = {
        "invoice_data": invoice_data,
        "purchase_order": verification_result.get("purchase_order"),
        "discrepancies": verification_result.get("discrepancies", []),
    }

    prompt = f"""
You are an accounts payable exception analyst.

Explain the invoice verification discrepancies using only the evidence below.

Requirements:
- State the specific problem.
- Explain why it requires review.
- Recommend the next action for the accounts payable team.
- Do not invent missing information.
- Do not approve or reject payments.
- Keep the explanation concise and professional.

Evidence:
{json.dumps(evidence, indent=2)}
"""

    return generate_answer(
        question=prompt,
        context="",
    )
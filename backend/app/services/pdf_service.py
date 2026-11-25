
from io import BytesIO
from pypdf import PdfReader


def extract_pdf_text(file_content: bytes) -> str:
    reader = PdfReader(BytesIO(file_content))

    extracted_pages = []

    for page in reader.pages:
        text = page.extract_text() or ""
        extracted_pages.append(text)

    return "\n\n".join(extracted_pages).strip()

import httpx

from app.core.config import settings


def generate_answer(question: str, context: str) -> str:
    url = f"{settings.OLLAMA_BASE_URL}/api/chat"

    payload = {
        "model": settings.OLLAMA_MODEL,
        "stream": False,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are an enterprise finance assistant. "
                    "Answer using only the supplied document context. "
                    "Do not invent facts or assume missing information. "
                    "If the context does not contain the answer, say so. "
                    "Cite supporting sources using their labels, "
                    "for example [filename, chunk 2]."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"DOCUMENT CONTEXT:\n{context}\n\n"
                    f"QUESTION:\n{question}"
                ),
            },
        ],
    }

    try:
        response = httpx.post(url, json=payload, timeout=120)
        response.raise_for_status()
        return response.json()["message"]["content"]

    except httpx.HTTPError as exc:
        raise RuntimeError(f"Ollama request failed: {exc}") from exc
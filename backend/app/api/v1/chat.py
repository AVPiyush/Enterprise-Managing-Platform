from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.document_indexer import search_documents
from app.services.ollama_service import generate_answer

router = APIRouter(tags=["RAG Chat"])


class AskRequest(BaseModel):
    query: str = Field(min_length=3)
    top_k: int = Field(default=5, ge=1, le=10)
    document_id: int | None = None


@router.post("/documents/ask")
def ask_documents(request: AskRequest):
    matches = search_documents(
        query=request.query,
        top_k=request.top_k,
        document_id=request.document_id,
    )

    if not matches:
        return {
            "answer": "No relevant document content was found.",
            "sources": [],
        }

    context_parts = []
    sources = []

    for match in matches:
        metadata = match["metadata"]

        filename = metadata.get("filename", "Unknown")
        chunk_index = metadata.get("chunk_index", -1)
        document_id = metadata.get("document_id")

        source_label = f"[{filename}, chunk {chunk_index}]"

        context_parts.append(
            f"{source_label}\n{match['text']}"
        )

        sources.append({
            "document_id": document_id,
            "filename": filename,
            "chunk_index": chunk_index,
            "distance": match["distance"],
        })

    context = "\n\n".join(context_parts)

    try:
        answer = generate_answer(request.query, context)
    except RuntimeError as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc),
        )

    return {
        "question": request.query,
        "answer": answer,
        "sources": sources,
    }
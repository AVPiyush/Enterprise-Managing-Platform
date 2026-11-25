
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.document_indexer import search_documents


router = APIRouter(tags=["Document Search"])


class SearchRequest(BaseModel):
    query: str = Field(min_length=2)
    top_k: int = Field(default=5, ge=1, le=10)
    document_id: int | None = None


@router.post("/documents/search")
def search_document_chunks(request: SearchRequest):

    try:
        results = search_documents(
            query=request.query,
            top_k=request.top_k,
            document_id=request.document_id,
        )

        return {
            "query": request.query,
            "results_count": len(results),
            "results": results,
        }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Document search failed",
        )

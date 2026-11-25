
from pathlib import Path

import chromadb
from fastembed import TextEmbedding


# Persistent local vector database
VECTOR_DB_PATH = Path("/app/vector_store")

client = chromadb.PersistentClient(
    path=str(VECTOR_DB_PATH)
)

collection = client.get_or_create_collection(
    name="finance_documents",
    metadata={"hnsw:space": "cosine"},
)

# Local embedding model
embedding_model = TextEmbedding(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


def chunk_text(
    text: str,
    chunk_size: int = 200,
    overlap: int = 40,
) -> list[str]:
    words = text.split()
    chunks = []

    if not words:
        return chunks

    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])

        if chunk.strip():
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def index_document(
    document_id: int,
    filename: str,
    text: str,
) -> int:
    chunks = chunk_text(text)

    if not chunks:
        return 0

    embeddings = [
        embedding.tolist()
        for embedding in embedding_model.embed(chunks)
    ]

    ids = [
        f"document_{document_id}_chunk_{i}"
        for i in range(len(chunks))
    ]

    metadatas = [
        {
            "document_id": document_id,
            "filename": filename,
            "chunk_index": i,
        }
        for i in range(len(chunks))
    ]

    collection.upsert(
        ids=ids,
        embeddings=embeddings,
        documents=chunks,
        metadatas=metadatas,
    )

    return len(chunks)

def search_documents(
    query: str,
    top_k: int = 5,
    document_id: int | None = None,
) -> list[dict]:

    query_embedding = next(
        embedding_model.embed([query])
    ).tolist()

    search_args = {
        "query_embeddings": [query_embedding],
        "n_results": top_k,
        "include": ["documents", "metadatas", "distances"],
    }

    if document_id is not None:
        search_args["where"] = {
            "document_id": document_id
        }

    results = collection.query(**search_args)

    matches = []

    for i, chunk in enumerate(results["documents"][0]):
        matches.append({
            "text": chunk,
            "metadata": results["metadatas"][0][i],
            "distance": results["distances"][0][i],
        })

    return matches

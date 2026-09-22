from fastapi import APIRouter, Request

from app.schemas.query import QueryRequest, QueryResponse
from app.services.retrieval import retrieve_chunks
from app.services.generation import generate_answer


router = APIRouter()


@router.post("/query", response_model=QueryResponse)
def query_laptop(
    http_request: Request,
    query_request: QueryRequest
):

    # Get the resources loaded during application startup
    embedding_model = http_request.app.state.embedding_model
    collection = http_request.app.state.collection
    ollama_model = http_request.app.state.ollama_model

    # Retrieve the most relevant chunks from ChromaDB
    results = retrieve_chunks(
        query_request.question,
        embedding_model,
        collection
    )

    # Generate an answer using the retrieved chunks
    answer = generate_answer(
        query_request.question,
        results,
        ollama_model
    )

    # Extract unique source names
    sources = []

    for metadata in results["metadatas"][0]:
        source = metadata["source"]

        if source not in sources:
            sources.append(source)

    return QueryResponse(
        answer=answer,
        sources=sources
    )
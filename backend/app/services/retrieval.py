import chromadb
from sentence_transformers import SentenceTransformer

from app.core.config import settings


def load_retrieval_resources():
    """
    Load the embedding model and ChromaDB collection.
    """

    # Load the embedding model
    embedding_model = SentenceTransformer(
        settings.embedding_model
    )

    # Connect to the persisted ChromaDB vector store
    chroma_client = chromadb.PersistentClient(
        path=settings.vector_store_path
    )

    # Open the collection
    collection = chroma_client.get_collection(
        name=settings.collection_name
    )

    return embedding_model, chroma_client, collection


def retrieve_chunks(
    question: str,
    embedding_model,
    collection,
    number_of_results: int | None = None
):
    """
    Retrieve the most relevant document chunks
    for a user question.
    """

    # Use the configured top_k value if no specific number is provided
    if number_of_results is None:
        number_of_results = settings.top_k

    # Convert the user's question into an embedding
    question_embedding = embedding_model.encode(question)

    # Search ChromaDB for the most similar chunks
    results = collection.query(
        query_embeddings=[question_embedding.tolist()],
        n_results=number_of_results
    )

    return results
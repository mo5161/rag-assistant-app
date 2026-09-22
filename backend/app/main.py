from contextlib import asynccontextmanager
from app.utils.logging_config import setup_logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.query import router
from app.services.retrieval import load_retrieval_resources
from app.services.generation import load_generation_resources

setup_logging()
@asynccontextmanager
async def lifespan(app: FastAPI):

    # Startup
    print("Starting application...")

    # Load retrieval resources
    (
        app.state.embedding_model,
        app.state.chroma_client,
        app.state.collection
    ) = load_retrieval_resources()

    # Load generation resources
    app.state.ollama_model = load_generation_resources()

    print("RAG resources loaded successfully.")

    yield

    # Shutdown
    print("Shutting down application...")


app = FastAPI(
    title="Laptop Support RAG API",
    description="RAG API for laptop manual support",
    version="1.0.0",
    lifespan=lifespan
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(router)
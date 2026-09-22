from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # Ollama model used for answer generation
    ollama_model: str = "llama3.2:3b"

    # Path to the persisted ChromaDB vector store
    vector_store_path: str = "data/vector_store"

    # Name of the ChromaDB collection
    collection_name: str = "laptop_manuals"

    # Sentence Transformer embedding model
    embedding_model: str = "all-MiniLM-L6-v2"

    # Number of chunks retrieved for each question
    top_k: int = 5

    # Tell Pydantic Settings to read variables from the .env file
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
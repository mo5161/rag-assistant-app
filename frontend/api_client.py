import os

import requests
from dotenv import load_dotenv


# Load environment variables from the .env file
load_dotenv()


# Get the backend URL from the environment
API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "http://127.0.0.1:8000"
)


def send_query(question: str):
    """
    Send the user's question to the FastAPI backend.
    """

    response = requests.post(
        f"{API_BASE_URL}/query",
        json={
            "question": question
        }
    )

    response.raise_for_status()

    return response.json()
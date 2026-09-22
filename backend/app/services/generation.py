import ollama

from app.core.config import settings


# Create the Ollama generation resources
def load_generation_resources():
    """
    Prepare the Ollama model used for answer generation.
    """

    model = settings.ollama_model

    return model


def create_prompt(question: str, results):
    """
    Build the prompt using the user's question
    and the chunks retrieved from ChromaDB.
    """

    # Get the retrieved document chunks
    documents = results["documents"][0]

    # Get the source of each retrieved chunk
    metadatas = results["metadatas"][0]

    # Start with an empty context
    context = ""

    # Add every retrieved chunk to the context
    for i in range(len(documents)):

        context = context + f"""
Source: {metadatas[i]["source"]}

Document Chunk:
{documents[i]}

"""

    # Build the final prompt
    prompt = f"""
You are a laptop support assistant.

Your job is to answer the user's question using ONLY
the information provided in the document context below.

Rules:

1. Do not use outside knowledge.
2. Do not invent or assume information.
3. If the answer is not available in the provided context,
   say: "The information is not available in the provided laptop manuals."
4. Give a clear and concise answer.
5. When the context provides step-by-step instructions,
   present them as numbered steps.
6. Mention the source document used for the answer.
7. If multiple sources are relevant, mention all relevant sources.

Document Context:
{context}

User Question:
{question}

Answer:
"""

    return prompt


def generate_answer(question: str, results, model):
    """
    Generate an answer using Ollama and the retrieved chunks.
    """

    # Create the prompt using the retrieved context
    prompt = create_prompt(question, results)

    # Send the prompt to the local Ollama model
    response = ollama.chat(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]
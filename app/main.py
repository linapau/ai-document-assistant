from fastapi import FastAPI
from dotenv import load_dotenv
from openai import OpenAI
import os

from app.document_loader import load_document_pages
from app.chunking import chunk_document_pages
from app.embedding_vector_store import embed_and_store_chunks
from app.rag_pipeline import answer_question_with_rag

load_dotenv() # Load environment variables from .env file, which includes the OpenAI API key needed for authentication when making requests to OpenAI's API
app = FastAPI()

# provide a function to get the OpenAI client, which can be used in the API endpoints to ensure that the API key is properly loaded and the client is initialized correctly
def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    return OpenAI(api_key=api_key)


@app.get("/")
def healthcheck():
    return {"status": "ok"}


@app.post("/load")
def load_document():
    client = get_openai_client() # Get the OpenAI client to ensure that the API key is properly loaded and the client is initialized correctly
    pages = load_document_pages("data/sample.pdf")

    chunks = chunk_document_pages(pages)
    embed_and_store_chunks(chunks, client)

    return {"message": "Document indexed successfully"}


@app.get("/ask")
def ask(question: str):
    client = get_openai_client()
    return {"answer": answer_question_with_rag(question, client)}
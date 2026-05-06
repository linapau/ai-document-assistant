from openai import OpenAI
import chromadb
import os
from dotenv import load_dotenv

#load_dotenv() # Load environment variables from .env file, which includes the OpenAI API key needed for authentication when making requests to OpenAI's API 

#openAI_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
chroma_client = chromadb.Client()

document_index = chroma_client.get_or_create_collection(name="documents")


def embed_and_store_chunks(chunks, client: OpenAI):
    for i, chunk in enumerate(chunks):
        text = chunk["text"]
        page_number = chunk["page"]

        if not text.strip(): # Skip empty chunks of text
            continue

        embedding = client.embeddings.create(input=text, model="text-embedding-3-small") # Generate an embedding for the chunk of text using OpenAI's embedding model

        document_index.add(
            documents=[text], # Add the chunk of text to the ChromaDB collection,
            embeddings=[embedding.data[0].embedding], # Add the corresponding embedding for the chunk of text to the ChromaDB collection
            metadatas=[{"page": page_number}], # Add metadata for the chunk of text, which includes the page number it came from
            ids=[str(i)] # Add a unique ID for the chunk of text, which is generated based on its index in the list of chunks
        )


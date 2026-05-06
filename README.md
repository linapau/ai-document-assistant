
## Tech Stack

- FastAPI (backend)
- OpenAI API (LLM + embeddings)
- ChromaDB (vector database)
- Python

flow 
User requestx
   ↓
FastAPI endpoint
   ↓
Question's Embedding
   ↓
Vector DB (Chroma)
   ↓
Top chunks (context)
   ↓
OpenAI (LLM)
   ↓
Response
   ↓
User


###
You have to create document/sample.pdf in your project
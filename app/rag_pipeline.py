from openai import OpenAI
from .embedding_vector_store import document_index


def answer_question_with_rag(question: str, client: OpenAI): # Define a function that takes a user's question and an OpenAI client as input and returns an answer based on the relevant information retrieved from the indexed document using a RAG
    q_emb = client.embeddings.create(
        model="text-embedding-3-small", # Generate an embedding for the user's question using OpenAI's embedding model which will be used to retrieve relevant chunks of text from the indexed document based on their similarity to the question
        input=question
    )

    results = document_index.query( # Query the ChromaDB collection to retrieve the most relevant chunks of text based on the similarity between the question embedding and the embeddings of the indexed chunks of text
        query_embeddings=[q_emb.data[0].embedding],
        n_results=3 # returning the top 3 most relevant results
    )

    # get the retrieved documents and their corresponding metadata (with the page numbers) and format them into a context string
    docs = results.get("documents", [[]])[0]
    metas = results.get("metadatas", [[]])[0]

    if not docs:
        return "No data indexed. Please upload a document first."

    context_parts = []
    for doc, meta in zip(docs, metas):
        page = meta.get("page", "?")  # Get the page number from the metadata, if available, otherwise use "?" as a placeholder
        context_parts.append(f"[PAGE {page}]\n{doc}")

    context = "\n\n".join(context_parts)

    # backend is making a request to OpenAI
    response = client.chat.completions.create( # Generate a response to the user's question using OpenAIs chat completion API, providing the retrieved context as part of the prompt to ensure that the answer is based on the relevant information from the indexed document
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system", # system prompt
                "content": "Answer only based on the context and include page numbers."
            },
            {
                "role": "user", # user prompt that includes the retrieved context and the user's original question
                "content": f"Context:\n{context}\n\nQuestion: {question}"
            }
        ]
    )

    return response.choices[0].message.content


# context string ex 
# [PAGE 1]
# text from page 1  
# [PAGE 2]
# text from page 2

# chunk ex
# {
#     "text": "text from page 1",
#     "page": 1
# } 

# metadata ex
# {
#     "page": 1
# }     

# embedding ex
# {
#     "data": [
#         {
#             "embedding": [0.1, 0.2, 0.3, ...] # A list of floating-point numbers representing the embedding vector for the input text         
#         }
#     ]
# } 


# response ex
# {
#     "choices": [
#         {
#             "message": {
#                 "content": "The answer to your question based on the context.",
#                 "role": "assistant"
#             }
#         }
#     ]
# }


# The RAG pipeline works as follows:
# 1. The user submits a question to the API endpoint.
# 2. The backend generates an embedding for the user's question using OpenAI's embedding model.
# 3. The backend queries the ChromaDB collection to retrieve the most relevant chunks of text based on the similarity between the question embedding and the embeddings of the indexed chunks of text.
# 4. The backend formats the retrieved documents and their corresponding metadata (with the page numbers) into a context string.
# 5. The backend generates a response to the user's question using OpenAI's chat completion API, providing the retrieved context as part of the prompt to ensure that the answer is based on the relevant information from the indexed document.
# 6. The backend returns the generated answer to the user.      


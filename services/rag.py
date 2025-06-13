import os
import google.generativeai as genai
import chromadb
from chromadb.utils import embedding_functions
from templates.rag_prompt import format_rag_prompt


chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection("documents")

def embed_texts(texts):
    API_KEY=os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=API_KEY)
    return [genai.embed_content(
                    model="models/embedding-001", 
                    content=t, 
                    task_type="RETRIEVAL_DOCUMENT"
                )['embedding'] for t in texts]

def load_and_index_documents(filepath: str = "data/docs.txt"):
    with open(filepath, "r") as f:
        full_text = f.read()

    chunks = [line.strip() for line in full_text.split(".") if line.strip()]

    embeddings = embed_texts(chunks)
    collection.add(
        documents=chunks, 
        embeddings=embeddings, 
        ids=[f"id_{i}" for i in range(len(chunks))]
    )

def retrieve_similar(query: str, k: int = 3):
    query_embedding = embed_texts([query])[0]
    results = collection.query(query_embeddings=[query_embedding], n_results=k)
    return results["documents"][0]

def query_rag_model(question: str) -> str:
    relevant_chunks = retrieve_similar(question)
    context = "/n/n".join(chunk['content'] for chunk in relevant_chunks)

    prompt = format_rag_prompt(context=context, question=question)

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    return response.text
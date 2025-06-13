from fastapi import APIRouter
from models.rag_model import RAGQuery, RAGResponse
from services import rag
import google.generativeai as genai

router = APIRouter()

@router.post("/rag", response_model=RAGResponse)
def rag_endpoint(payload: RAGQuery):
    query = payload.query

    docs = rag.retrieve_similar(query)

    context = "\n".join(docs)
    prompt = f"Answer the question based on the context below:\n\nContext:\n{context}\n\nQuestion: {query}"

    model = genai.GenerativeModel("gemini-1.5-flash")
    chat = model.start_chat()
    response = chat.send_message(prompt)

    return RAGResponse(
        relevant_docs=docs,
        generated_answer=response.text
    )
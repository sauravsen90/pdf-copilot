from services.rag import embed_texts
from utils.chroma import query_chroma
import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_answer_with_rag(query: str, collection_name: str, top_k: int = 5) -> str:
    matches = query_chroma(query, collection_name, top_k=top_k)

    if not matches:
        return "I couldn't find anything relevant in the document."
    
    context_text = "\n\n".join(
        [
        f"[Page {m['metadata']['page']} | {m['metadata']['type']}]\n{m['content']}"
        for m in matches
        ]
    )

    prompt = (
        "You are an assistant answering questions based on a car manual.\n"
        "Only answer based on the content provided below. If unsure, say so.\n\n"
        f"### Context:\n{context_text}\n\n"
        f"### Question:\n{query}\n\n"
        "### Answer:"
    )
    
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    return response.text.strip()        
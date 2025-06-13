def format_rag_prompt(context: str, question: str) -> str:
    return f"""
You are a helpful assistant. Use the following context to answer the user's question.

Context:
{context}

Question:
{question}

Answer:
"""
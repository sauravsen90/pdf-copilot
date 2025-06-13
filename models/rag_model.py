from pydantic import BaseModel

class RAGQuery(BaseModel):
    query: str

class RAGResponse(BaseModel):
    relevant_docs: list[str]
    generated_answer: str
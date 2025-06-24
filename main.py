from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from models.chat import ChatRequest, ChatResponse
from services.chat import generate_reply
from db.history import init_db
from dotenv import load_dotenv
from services.rag import load_and_index_documents
from routers import rag_router
from pydantic import BaseModel
from utils.rag import generate_answer_with_rag

@asynccontextmanager
async def lifespan(app: FastAPI):
    load_dotenv()
    init_db()
    load_and_index_documents()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(rag_router.router)

@app.post("/chat", response_model = ChatResponse)
def chat_endpoint(req: ChatRequest):
    reply, history = generate_reply(req.session_id, req.message)
    return ChatResponse(session_id=req.session_id, response = reply, history = history)

class Query(BaseModel):
    query: str

@app.post("/generate")
def generate(query: Query):
    try:
        answer = generate_answer_with_rag(query.query, collection_name="tiago_manual", top_k=5)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
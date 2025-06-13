from db.history import add_message, get_history
from models.chat import Message
import google.generativeai as genai
from typing import List, Tuple
import os
from services.rag import query_rag_model

API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=API_KEY)

def generate_reply_pre_rag(session_id: str, user_message: str) -> Tuple[str, List[Message]]:
    history = get_history(session_id)
    
    add_message(session_id, "user", user_message)

    messages = [{"role": r, "parts": [c]} for r, c in history]
    messages.append({"role":"user", "parts": [user_message]})

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(messages)

    assistant_response = response.text.strip()
    add_message(session_id, "assistant", assistant_response)

    updated_history = get_history(session_id)
    return assistant_response, [Message(role = r, content = c) for r,c in updated_history]

def generate_reply(session_id:str, user_message:str) -> tuple[str, List[str]]:
    history = get_history(session_id)
    
    add_message(session_id, "user", user_message)

    messages = [{"role": r, "parts": [c]} for r, c in history]
    messages.append({"role":"user", "parts": [user_message]})

    response_text =query_rag_model(user_message)

    assistant_response = response_text.strip()
    add_message(session_id, "assistant", assistant_response)

    updated_history = get_history(session_id)
    return assistant_response, [Message(role = r, content = c) for r,c in updated_history]
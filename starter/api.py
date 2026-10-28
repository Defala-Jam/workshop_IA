"""Execute: python -m uvicorn starter.api:app --reload"""
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from .config import BASE_DIR, settings
from .chat_service import chat

app = FastAPI(title="Science Tutor - Alunos")

class ChatRequest(BaseModel):
    message: str = Field(min_length=1)
    thread_id: str = Field(default="student-01", min_length=1)

@app.get("/health")
def health():
    return {"status": "ok", "model": settings.text_model}

@app.get("/")
def index():
    return FileResponse(BASE_DIR / "frontend" / "index.html")

@app.post("/chat")
def chat_endpoint(payload: ChatRequest):
    try:
        return chat(payload.message, payload.thread_id)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

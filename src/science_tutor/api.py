from __future__ import annotations
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from .config import BASE_DIR, settings
from .service import chat

app = FastAPI(title="Science Tutor Workshop API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class ChatRequest(BaseModel):
    message: str = Field(min_length=1)
    thread_id: str = Field(default="workshop-student", min_length=1)

@app.get("/health")
def health():
    return {"status": "ok", "model": settings.text_model}

@app.post("/chat")
def chat_endpoint(payload: ChatRequest):
    try:
        return chat(payload.message, payload.thread_id)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

FRONTEND = "frontend/index.html"

@app.get("/")
def index():
    return FileResponse(FRONTEND)

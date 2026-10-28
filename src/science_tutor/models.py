from __future__ import annotations
from langchain_ollama import ChatOllama
from .config import settings


def get_text_model(temperature: float = 0.0) -> ChatOllama:
    return ChatOllama(base_url="http://127.0.0.1:11434", model=settings.text_model, temperature=temperature)

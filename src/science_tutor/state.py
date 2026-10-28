from __future__ import annotations
from typing import NotRequired
from langgraph.graph import MessagesState

class TutorState(MessagesState):
    """Estado da conversa: histórico de mensagens + dados do jogo."""
    current_topic: NotRequired[str | None]      # Tópico atual (ex: "fisica")
    current_question_id: NotRequired[str | None] # ID da pergunta ativa
    score: NotRequired[int]                      # Pontuação do aluno
    attempts: NotRequired[int]                   # Tentativas na pergunta atual

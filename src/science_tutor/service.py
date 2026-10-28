from __future__ import annotations
from langchain.messages import HumanMessage, AIMessage
from .config import settings
from .graph import build_graph

_graph = None


def get_graph():
    """Singleton do grafo compilado (evita recompilar a cada request)."""
    global _graph
    if _graph is None:
        _graph = build_graph()
    return _graph


def chat(message: str, thread_id: str) -> dict:
    """
    Processa uma mensagem do usuário e retorna a resposta do tutor.

    Args:
        message: Texto da mensagem do aluno
        thread_id: ID da sessão (mantém histórico e estado)

    Returns:
        dict com message, state (score, topic, question_id)
    """
    graph = get_graph()
    config = {"configurable": {"thread_id": thread_id}, "recursion_limit": settings.max_steps}

    # Invoca o grafo com a nova mensagem
    result = graph.invoke({"messages": [HumanMessage(content=message)]}, config=config)

    # Extrai a última resposta do assistente
    assistant = next(
        (m for m in reversed(result["messages"]) if isinstance(m, AIMessage) and m.content),
        None
    )

    return {
        "message": str(assistant.content) if assistant else "Sem resposta gerada.",
        "state": {
            "current_topic": result.get("current_topic"),
            "current_question_id": result.get("current_question_id"),
            "score": result.get("score", 0),
            "attempts": result.get("attempts", 0),
        },
    }

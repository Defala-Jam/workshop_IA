from __future__ import annotations
import json
from langchain.tools import tool
from .config import settings
from .repository import KnowledgeBase

# Instância única do repositório (singleton simples)
kb = KnowledgeBase(settings.data_path)


def _event(name: str, **payload) -> str:
    """Serializa evento como JSON string para o LLM consumir."""
    return json.dumps({"event": name, **payload}, ensure_ascii=False)


@tool
def list_topics() -> str:
    """Lista todos os tópicos de ciências disponíveis."""
    return _event("topics_listed", topics=kb.list_topics())


@tool
def search_questions(topic: str) -> str:
    """Busca perguntas de um tópico. Use antes de escolher um question_id."""
    matches = kb.search_questions(topic)
    return _event("questions_found", query=topic, count=len(matches), questions=matches)


@tool
def get_question(question_id: str) -> str:
    """Carrega uma pergunta (com alternativas), mas NUNCA a resposta."""
    q = kb.get_question(question_id, include_answer=False)
    return _event("question_loaded", question=q)


@tool
def check_answer(question_id: str, answer: str) -> str:
    """Verifica a resposta do aluno. Aceita 'A', 'a)', ou o texto da opção."""
    result = kb.check_answer(question_id, answer)
    return _event("answer_checked", **result)


# Lista exportada para o grafo bind_tools(TOOLS)
TOOLS = [list_topics, search_questions, get_question, check_answer]

from __future__ import annotations

import json

from langchain.messages import SystemMessage, ToolMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import START, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from .config import settings
from .models import get_text_model
from .state import TutorState
from .tools import TOOLS

SYSTEM_PROMPT = """Você é um tutor de ciências conciso e encorajador.
Ensina a partir de um banco local de múltipla escolha.

Regras:
- Responda sempre em português, mesmo que o usuário escreva em outro idioma.
- Use tools quando o usuário pedir tópicos, perguntas ou enviar respostas.
- Nunca invente question_id.
- Não revele a resposta antes da tentativa.
- Mostre a pergunta e alternativas claramente.
- Explique o resultado em até 3 parágrafos curtos.
"""


def _format_state(state: TutorState) -> str:
    """Formata o estado atual para o system prompt."""
    return "\n".join([
        "Estado atual:",
        f"- Tópico: {state.get('current_topic') or 'nenhum'}",
        f"- Pergunta: {state.get('current_question_id') or 'nenhuma'}",
        f"- Pontuação: {state.get('score', 0)}",
        f"- Tentativas: {state.get('attempts', 0)}",
    ])


def build_graph():
    """Constrói o grafo de estados do tutor."""
    model = get_text_model(temperature=0).bind_tools(TOOLS)

    def agent_node(state: TutorState):
        """Nó do agente: LLM decide qual tool chamar (ou responde)."""
        system = SystemMessage(content=SYSTEM_PROMPT + "\n\n" + _format_state(state))
        return {"messages": [model.invoke([system, *state["messages"]])]}

    def sync_state(state: TutorState):
        """Sincroniza estado da aplicação lendo resultados das tools."""
        updates: dict[str, object] = {}

        tool_msgs = []
        for msg in reversed(state["messages"]):
            if not isinstance(msg, ToolMessage):
                break
            tool_msgs.append(msg)
        tool_msgs.reverse()

        attempts = int(state.get("attempts", 0))
        score = int(state.get("score", 0))

        for msg in tool_msgs:
            try:
                payload = json.loads(str(msg.content))
            except (TypeError, json.JSONDecodeError):
                continue

            event = payload.get("event")
            if event == "questions_found" and payload.get("questions"):
                updates["current_topic"] = payload["questions"][0].get("topic_id")
            elif event == "question_loaded":
                q = payload.get("question", {})
                updates["current_question_id"] = q.get("id")
                updates["current_topic"] = q.get("topic_id")
                attempts = 0
                updates["attempts"] = attempts
            elif event == "answer_checked":
                attempts += 1
                updates["attempts"] = attempts
                if payload.get("correct"):
                    score += 1
                    updates["score"] = score

        return updates

    # --- Monta o grafo ---
    builder = StateGraph(TutorState)
    builder.add_node("agent", agent_node)
    builder.add_node("tools", ToolNode(TOOLS))
    builder.add_node("sync", sync_state)

    builder.add_edge(START, "agent")
    builder.add_conditional_edges("agent", tools_condition)  # agent → tools se tool_call
    builder.add_edge("tools", "sync")                         # tools → sync
    builder.add_edge("sync", "agent")                         # sync → agent (loop)

    return builder.compile(checkpointer=InMemorySaver())

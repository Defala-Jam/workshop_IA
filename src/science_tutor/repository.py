from __future__ import annotations
import json
from pathlib import Path
from typing import Any

class KnowledgeBase:
    """Acesso ao banco de perguntas (JSON) - padrão Repository."""

    def __init__(self, path: str | Path):
        self.path = Path(path)
        if not self.path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {self.path}")

        # Carrega JSON e cria índice plano de perguntas para busca O(1)
        self.data = json.loads(self.path.read_text(encoding="utf-8"))
        self._questions: dict[str, dict[str, Any]] = {}
        for topic in self.data.get("topics", []):
            for q in topic.get("questions", []):
                item = dict(q)
                item["topic_id"] = topic["id"]
                item["topic_name"] = topic["name"]
                item["category"] = topic["category"]
                self._questions[item["id"]] = item

    # ---------- Consultas ----------

    def list_topics(self) -> list[dict[str, str]]:
        """Retorna todos os tópicos disponíveis."""
        return [
            {"id": t["id"], "name": t["name"], "category": t["category"], "description": t["description"]}
            for t in self.data.get("topics", [])
        ]

    def search_questions(self, topic: str) -> list[dict[str, Any]]:
        """Busca perguntas por nome/descrição do tópico (busca simples)."""
        needle = topic.strip().lower()
        matches = []
        for t in self.data.get("topics", []):
            hay = f"{t['id']} {t['name']} {t['description']}".lower()
            if needle in hay or any(p in hay for p in needle.split() if len(p) > 2):
                matches.extend({
                    "id": q["id"], "question": q["question"],
                    "topic_id": t["id"], "topic_name": t["name"]
                } for q in t["questions"])
        return matches

    def get_question(self, question_id: str, include_answer: bool = False) -> dict[str, Any]:
        """Pega uma pergunta pelo ID. Por padrão, NÃO inclui a resposta."""
        q = self._questions.get(question_id)
        if q is None:
            raise KeyError(f"Pergunta não encontrada: {question_id}")
        out = dict(q)
        if not include_answer:
            out.pop("answer", None)
            out.pop("explanation", None)
        return out

    # ---------- Verificação ----------

    def check_answer(self, question_id: str, answer: str) -> dict[str, Any]:
        """Verifica se a resposta está correta. Aceita 'A', 'a)', ou o texto da opção."""
        q = self._questions.get(question_id)
        if q is None:
            raise KeyError(f"Pergunta não encontrada: {question_id}")

        # Normaliza: "A", "a)", "a." → "a"
        normalized = answer.strip().lower().replace(")", "").replace(".", "")
        label = normalized[:1]  # pega primeira letra

        # Se não for letra, tenta achar pelo texto da opção
        if normalized not in q["options"]:
            for k, v in q["options"].items():
                if normalized == str(v).strip().lower():
                    label = k
                    break

        correct = label == q["answer"].lower()
        return {
            "question_id": question_id,
            "submitted": answer,
            "correct": correct,
            "correct_answer": q["answer"],
            "correct_option": q["options"][q["answer"]],
            "explanation": q.get("explanation", ""),
        }

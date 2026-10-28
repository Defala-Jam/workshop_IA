"""Consultas e pontuacao em memoria para a aula."""
from copy import deepcopy
from threading import RLock
from .config import settings
from .repository import JsonRepository


class KnowledgeService:
    def __init__(self, path=settings.data_path):
        # O JSON e lido apenas na criacao do servico.
        self.topics = JsonRepository(path).read()["topics"]
        self.questions = {}
        for topic in self.topics:
            for question in topic["questions"]:
                self.questions[question["id"]] = question
        self.sessions = {}
        self.lock = RLock()

    def list_topics(self):
        """Lista os temas sem trazer suas perguntas."""
        topics = []
        for topic in self.topics:
            topics.append({"id": topic["id"], "name": topic["name"],
                           "description": topic["description"]})
        return topics

    def list_questions(self, topic_id):
        """Recebe o ID do tema e lista IDs e enunciados, sem gabarito."""
        for topic in self.topics:
            if topic["id"] == topic_id:
                return [{"id": q["id"], "question": q["question"]}
                        for q in topic["questions"]]
        raise KeyError(f"Topico nao encontrado: {topic_id}")

    def load_question(self, question_id):
        """Dados completos para a LLM: enunciado, alternativas e gabarito.

        A LLM deve apresentar enunciado e alternativas sem revelar a resposta.
        """
        return deepcopy(self.questions[question_id])

    def check_answer(self, thread_id, question_id, answer):
        """Registra uma tentativa e soma 1 ponto no primeiro acerto da questao.

        Aceita a letra (A, a), a.) ou o texto exato da alternativa,
        ignorando maiusculas e espacos nas extremidades.
        """
        question = self.questions[question_id]
        normalized = answer.strip().casefold()
        label = normalized.rstrip(").")
        if label not in question["options"]:
            for option, text in question["options"].items():
                if normalized == text.strip().casefold():
                    label = option
                    break
        correct = label == question["answer"].casefold()

        with self.lock:
            session = self.sessions.setdefault(thread_id, {
                "score": 0, "attempts": 0, "question_attempts": {}, "solved": set(),
            })
            session["attempts"] += 1
            attempts = session["question_attempts"]
            attempts[question_id] = attempts.get(question_id, 0) + 1
            points = 0
            if correct and question_id not in session["solved"]:
                points = 1
                session["score"] += points
                session["solved"].add(question_id)
            return {
                "question_id": question_id,
                "correct": correct,
                "points_awarded": points,
                "score": session["score"],
                "attempts": session["attempts"],
                "question_attempts": attempts[question_id],
            }

    def add_topic(self, topic_id, name, description):
        """Adiciona um topico vazio em memoria."""
        if not all(isinstance(value, str) and value.strip()
                   for value in (topic_id, name, description)):
            raise ValueError("Informe id, nome e descricao nao vazios")
        with self.lock:
            if any(topic["id"] == topic_id for topic in self.topics):
                raise ValueError("ID de topico ja existe")
            topic = {"id": topic_id, "name": name,
                     "description": description, "questions": []}
            self.topics.append(topic)
            return {"id": topic_id, "name": name, "description": description}

    def add_question(self, topic_id, question_id, question, options, answer, explanation):
        """Adiciona uma pergunta ao topico e ao indice de perguntas."""
        if not all(isinstance(value, str) and value.strip()
                   for value in (question_id, question, answer, explanation)):
            raise ValueError("Informe id, enunciado, resposta e explicacao nao vazios")
        if not isinstance(options, dict) or len(options) < 2:
            raise ValueError("Informe pelo menos duas alternativas")
        if any(not isinstance(key, str) or not key.strip() or key != key.casefold()
               or not isinstance(text, str) or not text.strip()
               for key, text in options.items()):
            raise ValueError("Alternativas precisam de chaves minusculas e textos nao vazios")
        if answer not in options:
            raise ValueError("A resposta deve ser uma chave das alternativas")
        with self.lock:
            if question_id in self.questions:
                raise ValueError("ID de pergunta ja existe")
            for topic in self.topics:
                if topic["id"] == topic_id:
                    item = {"id": question_id, "question": question,
                            "options": deepcopy(options), "answer": answer,
                            "explanation": explanation}
                    topic["questions"].append(item)
                    self.questions[question_id] = item
                    return deepcopy(item)
            raise KeyError(f"Topico nao encontrado: {topic_id}")

    def remove_question(self, question_id):
        """Remove a pergunta; pontuacoes e tentativas anteriores sao mantidas."""
        with self.lock:
            if question_id not in self.questions:
                raise KeyError(f"Pergunta nao encontrada: {question_id}")
            for topic in self.topics:
                for question in topic["questions"]:
                    if question["id"] == question_id:
                        topic["questions"].remove(question)
                        del self.questions[question_id]
                        return

    def remove_topic(self, topic_id):
        """Remove o topico e todas as suas perguntas em memoria."""
        with self.lock:
            for topic in self.topics:
                if topic["id"] == topic_id:
                    for question in topic["questions"]:
                        del self.questions[question["id"]]
                    self.topics.remove(topic)
                    return
            raise KeyError(f"Topico nao encontrado: {topic_id}")

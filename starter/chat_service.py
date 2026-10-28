"""Ponto de entrada para o chat que os alunos implementarao."""
from .knowledge_service import KnowledgeService

# Criado uma vez: dados e resultados permanecem em memoria entre chamadas.
knowledge = KnowledgeService()


def chat(message: str, thread_id: str) -> dict:
    """Recebe uma mensagem do aluno e retorna uma resposta do tutor."""
    pass

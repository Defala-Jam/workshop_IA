# Starter para os alunos

API e frontend prontos; implemente o modelo/grafo em chat_service.py.

## Executar

Na pasta que contem starter:

```bash
python -m pip install -r starter/requirements.txt
python -m uvicorn starter.api:app --reload
```

Abra http://127.0.0.1:8000. Documentacao da API em /docs.

## Camadas

- api.py: recebe message e thread_id em POST /chat e chama chat_service.chat.
- chat_service.py: instancia unica de KnowledgeService e exercicio do chat.
- config.py: configuracao pronta de modelo, Ollama e caminho do JSON.
- knowledge_service.py: cinco operacoes simples de consulta e correcao.
- repository.py: le o JSON apenas ao criar o servico.
- data/: copia independente dos dados.
- frontend/: interface pronta que recebe message e state com score e attempts.

## Cinco operacoes

```python
from starter.knowledge_service import KnowledgeService

base = KnowledgeService()
print(base.list_topics())
print(base.list_questions("plate_tectonics"))
print(base.get_question("pt_001"))
print(base.load_question("pt_001"))
print(base.check_answer("aluno-1", "pt_001", "b"))
```

1. list_topics(): IDs, nomes e descricoes dos temas.
2. list_questions(topic_id): IDs e enunciados das perguntas daquele tema.
3. get_question(question_id): somente o texto do enunciado.
4. load_question(question_id): pergunta completa, alternativas, gabarito e explicacao para a LLM. Ao apresentar ao aluno, omita o gabarito.
5. check_answer(thread_id, question_id, answer): verifica a alternativa e registra a tentativa e a pontuacao.

A correcao aceita a letra (inclusive A, a), a.) ou o texto exato da alternativa,
ignorando maiusculas e espacos nas extremidades. Nao usa LLM para julgar respostas abertas.
Retorna correct, points_awarded, score, attempts e question_attempts.
score soma um ponto por pergunta acertada; repetir um acerto nao gera outro ponto.
attempts conta todas as respostas enviadas na conversa, certas ou erradas;
question_attempts conta as tentativas daquela pergunta na conversa.
Uma resposta que nao corresponde a alternativa alguma conta como tentativa errada.
IDs inexistentes geram KeyError e nao contam como tentativa.

Tudo acontece em memoria. O JSON nao e alterado. Cada thread_id tem pontuacao
independente. Reiniciar o processo (inclusive com --reload) apaga os resultados.
Use um unico processo/worker na aula. Reutilize a instancia knowledge do
chat_service; criar um novo servico a cada mensagem reinicia a pontuacao.

O chat ainda retorna uma mensagem provisoria, sem chamar o modelo. A API
retorna JSON completo, sem streaming, e o frontend mostra score e attempts.

## Verificar

```bash
python -m unittest starter.test_starter -v
```

## Adicionar e remover em memoria

```python
base.add_topic("demo", "Tema da aula", "Descricao do tema")
base.add_question(
    "demo", "demo_001", "Quanto e 2 + 2?",
    {"a": "3", "b": "4"}, "b", "Dois mais dois e quatro."
)
base.remove_question("demo_001")
base.remove_topic("demo")
```

IDs duplicados e dados invalidos geram ValueError; IDs inexistentes geram KeyError.
As chaves das alternativas devem estar em minusculas, e answer deve ser uma delas.
Remover um topico remove suas perguntas. Pontos e tentativas ja registrados
permanecem no historico em memoria, inclusive se um ID removido for reutilizado.
Nenhuma dessas operacoes altera o JSON; reiniciar restaura os dados originais.

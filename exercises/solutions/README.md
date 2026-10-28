# Soluções dos desafios

As soluções foram separadas para que o professor possa distribuí-las somente depois da atividade.

## 1 — Temperatura

Não há uma saída textual única esperada. O aluno deve observar que aumentar a temperatura pode aumentar a diversidade da amostragem. A atividade **não** deve ser interpretada como “temperatura = criatividade” nem como ajuste de factualidade.

## 2 — System prompt

Uma solução mínima:

```python
SystemMessage(
    content=(
        "You are a concise science tutor. "
        "Do not reveal the correct multiple-choice answer before the student attempts it."
    )
)
```

O critério é comportamental: teste uma pergunta em que o usuário peça diretamente a alternativa correta.

## 3 — Primeira tool

Veja [`03_list_topics.py`](03_list_topics.py). A lista deve ser derivada do JSON, sem nomes hard-coded.

## 4 — Tool calling

Veja [`04_tool_calling.py`](04_tool_calling.py). O ciclo manual é:

`HumanMessage → AIMessage(tool_calls) → Python tool → ToolMessage → AIMessage final`.

O modelo produz a solicitação estruturada; **a aplicação executa Python**.

## 5 — Estado da aplicação

Veja [`05_state.py`](05_state.py). `messages` tem semântica de acumulação; `score`, `attempts` e `current_question_id` são canais de estado atualizados pela aplicação.

A implementação completa da atualização está em `src/science_tutor/graph.py`, no nó `sync_state`.

## 6 — Endpoint final

Veja [`06_api.py`](06_api.py) e `src/science_tutor/service.py`.

O `thread_id` é passado ao checkpointer do LangGraph por meio de:

```python
config = {
    "configurable": {"thread_id": thread_id},
    "recursion_limit": 12,
}
```

Duas requisições com o mesmo `thread_id` continuam o mesmo estado; um novo identificador cria outra linha de conversa.

# Desafios da oficina

## 1 — Temperatura
Execute a mesma pergunta científica com `temperature=0` e `temperature=1`. Registre duas diferenças observáveis. **Objetivo:** distinguir determinismo aproximado de diversidade de geração.

## 2 — System prompt
Adicione uma mensagem `system` para transformar o modelo em um tutor que não entrega a resposta antes da tentativa do aluno. **Critério:** a restrição deve aparecer no comportamento, não apenas no texto do prompt.

## 3 — Primeira tool
Implemente `list_topics()` lendo `data/knowledge_base.json`. **Critério:** nenhum nome de tema deve ficar hard-coded na função.

## 4 — Tool calling
Vincule `list_topics` e `search_questions` ao modelo com `bind_tools()`. Inspecione `AIMessage.tool_calls` antes de executar qualquer função. **Pergunta:** quem realmente executa Python — o modelo ou a aplicação?

## 5 — Estado da aplicação
Estenda `TutorState` com `score` e `attempts`. Mostre no notebook que esses campos não fazem parte do histórico de mensagens.

## 6 — Desafio final
Implemente o endpoint `POST /chat` usado pelo frontend. Ele deve:
1. receber `message` e `thread_id`;
2. invocar o grafo usando o `thread_id` como configuração;
3. devolver texto e o estado resumido;
4. manter score e histórico entre requisições da mesma thread.

### Extensão opcional
Adicione um modo `difficulty` ao estado e uma tool `set_difficulty(level)` sem quebrar as quatro tools originais do núcleo da oficina.

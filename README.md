# Tutor de Ciências — oficina de IA

Material completo para uma oficina de **3 horas**, com **20 minutos de intervalo**, voltada a alunos de graduação que já programam em Python.

## Resultado da oficina

Os alunos evoluem de uma chamada local a uma LLM até um agente com **histórico conversacional + estado de aplicação + 4 tools + LangGraph**. A interface é fornecida pronta; no desafio final, eles implementam o endpoint `/chat` que invoca o grafo.

## Stack

- Ollama
- `qwen3.5:4b` para chat e tool calling
- LangChain apenas nas abstrações essenciais (`ChatOllama`, mensagens, `@tool`)
- LangGraph para estado, nós, edges e loop agente/tools
- FastAPI para o endpoint final

## Preparação rápida

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m ipykernel install --user --name science-tutor-workshop --display-name "Python (Science Tutor Workshop)"
ollama pull qwen3.5:4b
python scripts/validate_dataset.py
python scripts/preflight.py
PYTHONPATH=src uvicorn science_tutor.api:app --reload
```

Abra `http://127.0.0.1:8000`.
Para executar os notebooks no VS Code, selecione o kernel **Python (Science Tutor Workshop)**.

## Dados

`data/knowledge_base.json` é uma base original e offline, com 6 temas e 6 questões por tema.

## Organização

- `notebooks/`: progressão didática da oficina
- `src/science_tutor/`: implementação completa de referência
- `starter/api.py`: endpoint incompleto entregue aos alunos
- `frontend/`: interface já pronta
- `data/`: base local
- `exercises/`: desafios e soluções
- `instructor/`: roteiro, timing, prompts de demonstração e troubleshooting
- `slides/`: apresentação da oficina
- `scripts/`: preparação/validação do dataset

## Testes locais que não exigem Ollama

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

## Fontes técnicas verificadas na preparação

- Ollama model library: qwen3.5
- LangChain ChatOllama integration docs
- LangGraph Graph API / ToolNode docs

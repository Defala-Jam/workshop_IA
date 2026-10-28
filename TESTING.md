# Validação do pacote

Validações executadas na geração deste material:

- `scripts/validate_dataset.py`: **OK** — 6 temas e 36 questões;
- testes unitários de `KnowledgeBase`: **4/4 OK**;
- `py_compile` em `src/`, `scripts/`, `starter/` e soluções: **OK**;
- validação estrutural dos cinco notebooks com `nbformat`: **OK**;
- renderização dos slides e teste de overflow: **OK** — 28 slides, sem objetos fora do canvas.

## Limite da validação

O ambiente usado para gerar o pacote não possui Ollama nem as dependências LangChain/LangGraph instaladas e não permite instalar pacotes da internet. Por isso, o fluxo completo contra `qwen3.5:4b` **não foi executado aqui**.

Antes da oficina, execute em uma máquina com o ambiente real:

```bash
pip install -r requirements.txt
python scripts/preflight.py
PYTHONPATH=src python -m unittest discover -s tests -v
PYTHONPATH=src uvicorn science_tutor.api:app
```

Depois faça pelo menos um teste completo no frontend com:

1. listagem de temas;
2. uma questão textual;
3. uma questão de cada tema;
4. uma tentativa correta e uma incorreta;
5. duas mensagens com o mesmo `thread_id`.

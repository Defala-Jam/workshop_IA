# Preparação do ambiente

Pré-requisitos: Python 3.11+ recomendado, 16 GB RAM e Ollama.

Depois de instalar Ollama:

```bash
ollama --version
ollama pull qwen3.5:4b
ollama list
```

Crie o ambiente Python na raiz do projeto:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m ipykernel install --user --name science-tutor-workshop --display-name "Python (Science Tutor Workshop)"
python scripts/validate_dataset.py
python scripts/preflight.py
```

Teste o Ollama:

```bash
ollama run qwen3.5:4b "Reply only with: setup ok"
```

No Linux, use o instalador oficial do Ollama e confirme que o serviço está ativo antes de abrir os notebooks.


Abra os notebooks a partir da raiz do projeto:

```bash
jupyter lab
```

No VS Code, selecione o kernel **Python (Science Tutor Workshop)** nos notebooks.

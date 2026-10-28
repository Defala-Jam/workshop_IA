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
.venv\Scripts\activate
pip install -r requirements.txt
python -m ipykernel install --user --name science-tutor-workshop --display-name "Python (Science Tutor Workshop)"
python scripts/validate_dataset.py
python scripts/preflight.py
```

Teste o Ollama:

```bash
ollama run qwen3.5:4b "Reply only with: setup ok"
```

No Windows, instale o Ollama pelo instalador oficial. PowerShell é recomendado para os comandos da oficina.


Abra os notebooks a partir da raiz do projeto:

```bash
jupyter lab
```

No VS Code, selecione o kernel **Python (Science Tutor Workshop)** nos notebooks.

## VS Code neste projeto

Abra a pasta raiz da oficina no VS Code. Execute `Python: Select Interpreter`
(Ctrl+Shift+P) e escolha `.venv\Scripts\python.exe`.
Em cada notebook, clique em **Select Kernel** > **Python Environments** e
selecione esse mesmo `.venv`, ou o kernel **Python (Science Tutor Workshop)**.
Se havia outro kernel selecionado, reinicie-o antes de usar **Run All**.
Abra um terminal novo depois de mudar o interpretador.

Para conferir o ambiente, sem depender da ativa??o do PowerShell:

```powershell
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe scripts/preflight.py
```

As chamadas locais usam `http://127.0.0.1:11434`: `0.0.0.0` ? um endere?o
para o servidor escutar conex?es, n?o o endere?o que o notebook deve usar.
O aplicativo Ollama deve estar em execu??o com `qwen3.5:4b` dispon?vel.

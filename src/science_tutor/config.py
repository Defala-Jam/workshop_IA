from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import os

# Caminhos do projeto
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"

@dataclass(frozen=True)
class Settings:
    """Configurações do tutor - todas via variáveis de ambiente com defaults."""
    text_model: str = os.getenv("TEXT_MODEL", "qwen3.5:4b")
    data_path: Path = Path(os.getenv("SCIENCE_TUTOR_DATA", DATA_DIR / "knowledge_base.json"))
    max_steps: int = int(os.getenv("MAX_AGENT_STEPS", "12"))

settings = Settings()

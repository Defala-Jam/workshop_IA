from dataclasses import dataclass
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent

@dataclass(frozen=True)
class Settings:
    text_model: str = os.getenv("TEXT_MODEL", "qwen3.5:4b")
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
    data_path: Path = Path(os.getenv("SCIENCE_TUTOR_DATA", str(BASE_DIR / "data" / "knowledge_base.json")))
    max_steps: int = int(os.getenv("MAX_AGENT_STEPS", "12"))

settings = Settings()

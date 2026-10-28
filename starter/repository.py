"""Leitura do arquivo de perguntas; nenhum dado e gravado em disco."""
import json
from pathlib import Path


class JsonRepository:
    def __init__(self, path: str | Path):
        self.path = Path(path)

    def read(self) -> dict:
        return json.loads(self.path.read_text(encoding="utf-8"))

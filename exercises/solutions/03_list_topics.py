from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "knowledge_base.json"


def list_topics() -> list[dict[str, str]]:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    return [
        {
            "id": topic["id"],
            "name": topic["name"],
            "category": topic["category"],
        }
        for topic in data["topics"]
    ]


if __name__ == "__main__":
    print(list_topics())

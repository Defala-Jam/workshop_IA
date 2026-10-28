#!/usr/bin/env python3
"""Instructor preflight: run this before the workshop starts."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_IMPORTS = {
    "langchain": "langchain",
    "langgraph": "langgraph",
    "langchain_ollama": "langchain_ollama",
    "fastapi": "fastapi",
    "uvicorn": "uvicorn",
    "pydantic": "pydantic",
}
EXPECTED_MODELS = {"qwen3.5:4b"}


def ok(label: str, detail: str = "") -> None:
    print(f"[ OK ] {label}" + (f": {detail}" if detail else ""))


def warn(label: str, detail: str = "") -> None:
    print(f"[WARN] {label}" + (f": {detail}" if detail else ""))


def fail(label: str, detail: str = "") -> None:
    print(f"[FAIL] {label}" + (f": {detail}" if detail else ""))


print("Science Tutor Workshop — preflight\n")
ok("Python", platform.python_version())
print("Platform:", platform.platform())

missing = []
for label, module in REQUIRED_IMPORTS.items():
    if importlib.util.find_spec(module):
        ok(f"import {label}")
    else:
        missing.append(label)
        fail(f"import {label}", "run pip install -r requirements.txt")

kb_path = ROOT / "data" / "knowledge_base.json"
try:
    data = json.loads(kb_path.read_text(encoding="utf-8"))
    topics = data.get("topics", [])
    questions = [q for t in topics for q in t.get("questions", [])]
    if len(topics) == 6 and len(questions) == 36:
        ok("Dataset", "6 topics / 36 questions")
    else:
        fail("Dataset counts", f"topics={len(topics)}, questions={len(questions)}")
except Exception as exc:
    fail("Dataset", str(exc))

# Check the service directly: the desktop app may run without a CLI on PATH.
try:
    from ollama import Client
    client = Client(host="http://127.0.0.1:11434")
    installed = {m.model for m in client.list().models}
    ok("Ollama server", "http://127.0.0.1:11434")
    for model in sorted(EXPECTED_MODELS):
        if model in installed:
            ok("Model", model)
        else:
            warn("Model missing", f"{model} - run: ollama pull {model}")
except Exception as exc:
    fail("Ollama server", str(exc))
    sys.exit(1)

if missing:
    print("\nPreflight finished with missing Python dependencies.")
    sys.exit(1)
print("\nPreflight finished. Review WARN lines before the class.")

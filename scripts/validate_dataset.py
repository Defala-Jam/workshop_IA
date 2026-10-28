#!/usr/bin/env python3
from pathlib import Path
import json
import sys

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "knowledge_base.json"

data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
errors: list[str] = []

topics = data.get("topics", [])
if len(topics) != 6:
    errors.append(f"Expected 6 topics, found {len(topics)}")

ids: set[str] = set()
total = 0
for topic in topics:
    questions = topic.get("questions", [])
    if len(questions) != 6:
        errors.append(f"{topic.get('id')}: expected 6 questions, found {len(questions)}")
    for question in questions:
        total += 1
        question_id = question["id"]
        if question_id in ids:
            errors.append(f"duplicate id {question_id}")
        ids.add(question_id)
        if question.get("answer") not in question.get("options", {}):
            errors.append(f"{question_id}: invalid answer")

print(f"topics={len(topics)} questions={total}")
if errors:
    print("\n".join(f"ERROR: {error}" for error in errors))
    sys.exit(1)
print("Dataset OK")

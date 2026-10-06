import json
from pathlib import Path


DATA_DIR = Path("data")


def load_documents() -> list[dict]:
    documents = []

    for path in DATA_DIR.rglob("*.json"):
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, list):
            documents.extend(data)
        else:
            documents.append(data)

    return documents
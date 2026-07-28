import json
import csv
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "tests" / "data"


def load_json(filename: str) -> list:
    path = DATA_DIR / filename
    with open(path, "r") as f:
        return json.load(f)


def load_csv(filename: str) -> list[dict]:
    path = DATA_DIR / filename
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def json_to_pytest_params(filename: str, fields: list[str]) -> list[tuple]:
    data = load_json(filename)
    return [tuple(row[f] for f in fields) for row in data]

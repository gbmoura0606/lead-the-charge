import json
from pathlib import Path
from typing import Any


class JsonStore:
    def __init__(self, path: Path, default: Any):
        self.path = path
        self.default = default
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def read(self) -> Any:
        if not self.path.exists():
            self.write(self.default)
            return self.default

        with self.path.open("r", encoding="utf-8") as file:
            return json.load(file)

    def write(self, payload: Any) -> None:
        with self.path.open("w", encoding="utf-8") as file:
            json.dump(payload, file, indent=2)

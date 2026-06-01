from __future__ import annotations

import json
from pathlib import Path


DEFAULT_CONFIG = {
    "required_docs": ["README.md", "LICENSE", "CONTRIBUTING.md", "SECURITY.md", "CODE_OF_CONDUCT.md"],
    "issue_template_path": ".github/ISSUE_TEMPLATE",
}


def load_config(path: Path) -> dict[str, object]:
    config = dict(DEFAULT_CONFIG)
    if not path.exists():
        return config

    loaded = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(loaded, dict):
        raise ValueError(f"Config file must contain a JSON object: {path}")

    for key, value in loaded.items():
        if key in DEFAULT_CONFIG:
            config[key] = value
    return config


def required_docs_from_config(config: dict[str, object]) -> list[str]:
    value = config.get("required_docs", DEFAULT_CONFIG["required_docs"])
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ValueError("required_docs must be a list of strings")
    return value


def issue_template_path_from_config(config: dict[str, object]) -> str:
    value = config.get("issue_template_path", DEFAULT_CONFIG["issue_template_path"])
    if not isinstance(value, str):
        raise ValueError("issue_template_path must be a string")
    return value


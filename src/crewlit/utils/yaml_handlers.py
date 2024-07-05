import yaml
from typing import Dict, Any

def load_yaml(file_path: str) -> Dict[str, Any]:
    try:
        with open(file_path, "r") as file:
            return yaml.safe_load(file) or {}
    except FileNotFoundError:
        return {}

def save_yaml(file_path: str, data: Dict[str, Any]):
    with open(file_path, "w") as file:
        yaml.dump(data, file)

def dump_yaml(data: Dict[str, Any]) -> str:
    return yaml.dump(data)
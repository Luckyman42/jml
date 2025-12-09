import json
import yaml
from typing import Literal
from pathlib import Path
import typer

def load_file(path: Path):
    text = path.read_text()
    if path.suffix.lower() == ".json":
        return json.loads(text)
    elif path.suffix.lower() in [".yaml", ".yml"]:
        return yaml.safe_load(text)
    else:
       raise typer.BadParameter("Unsupported input file type.")

def output_json(data, pretty: bool) -> str:
    if pretty:
        return json.dumps(data, indent=2, ensure_ascii=False)
    return json.dumps(data, separators=(",", ":"), ensure_ascii=False)

def output_yaml(data) -> str:
    return yaml.safe_dump(data, sort_keys=False, allow_unicode=True)

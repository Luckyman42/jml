import json
import yaml
from pathlib import Path
import typer


def load_file(path: Path):
    text = path.read_text()
    if path.suffix.lower() == ".json":
        return parse_json(text)
    elif path.suffix.lower() in [".yaml", ".yml"]:
        return parse_yaml(text)
    else:
        raise typer.BadParameter("Unsupported input file type.")


def parse_json(text: str):
    return json.loads(text)


def parse_yaml(text: str):
    return yaml.safe_load(text)


def try_parse_json(text):
    try:
        return parse_json(text)
    except Exception:
        return None


def try_parse_yaml(text):
    try:
        return parse_yaml(text)
    except Exception:
        return None


def try_parse(text: str):
    return try_parse_json(text) or try_parse_yaml(text)


def output_json(data, pretty: bool) -> str:
    if pretty:
        return json.dumps(data, indent=2, ensure_ascii=False)
    return json.dumps(data, separators=(",", ":"), ensure_ascii=False)


def output_yaml(data) -> str:
    return yaml.safe_dump(data, sort_keys=False, allow_unicode=True)

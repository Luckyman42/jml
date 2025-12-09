import json
import yaml
from pathlib import Path
from typing import Any
import typer


def load_file(path: Path) -> Any:
    """
    Load a JSON or YAML file from the given path.

    Args:
        path (Path): Path to the input file.

    Returns:
        Any: Parsed Python object (dict, list, etc.).

    Raises:
        typer.BadParameter: If the file extension is unsupported.
        JSONDecodeError / YAMLError: If the file content cannot be parsed.
    """
    text = path.read_text()
    if path.suffix.lower() == ".json":
        return parse_json(text)
    elif path.suffix.lower() in [".yaml", ".yml"]:
        return parse_yaml(text)
    else:
        raise typer.BadParameter("Unsupported input file type.")


def parse_json(text: str) -> Any:
    """
    Parse a JSON string into a Python object.

    Args:
        text (str): JSON string.

    Returns:
        Any: Parsed Python object.
    """
    return json.loads(text)


def parse_yaml(text: str) -> Any:
    """
    Parse a YAML string into a Python object.

    Args:
        text (str): YAML string.

    Returns:
        Any: Parsed Python object.
    """
    return yaml.safe_load(text)


def try_parse_json(text: str) -> Any | None:
    """
    Try to parse a JSON string; return None if parsing fails.

    Args:
        text (str): JSON string.

    Returns:
        Any | None: Parsed Python object or None if parsing fails.
    """
    try:
        return parse_json(text)
    except Exception:
        return None


def try_parse_yaml(text: str) -> Any | None:
    """
    Try to parse a YAML string; return None if parsing fails.

    Args:
        text (str): YAML string.

    Returns:
        Any | None: Parsed Python object or None if parsing fails.
    """
    try:
        return parse_yaml(text)
    except Exception:
        return None


def try_parse(text: str) -> Any | None:
    """
    Try to parse a string as JSON first, then YAML if JSON fails.

    Args:
        text (str): Input string.

    Returns:
        Any | None: Parsed Python object or None if both JSON and YAML parsing fail.
    """
    return try_parse_json(text) or try_parse_yaml(text)


def output_json(data: Any, pretty: bool = False) -> str:
    """
    Convert Python object to JSON string.

    Args:
        data (Any): Python object (dict, list, etc.).
        pretty (bool, optional): If True, pretty-print with indentation. Defaults to False.

    Returns:
        str: JSON string.
    """
    if pretty:
        return json.dumps(data, indent=2, ensure_ascii=False)
    return json.dumps(data, separators=(",", ":"), ensure_ascii=False)


def output_yaml(data: Any) -> str:
    """
    Convert Python object to YAML string.

    Args:
        data (Any): Python object (dict, list, etc.).

    Returns:
        str: YAML string.
    """
    return yaml.safe_dump(data, sort_keys=False, allow_unicode=True)

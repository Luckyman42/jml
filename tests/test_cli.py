import pytest
from typer.testing import CliRunner
from pathlib import Path
import sys
import io

from jml.app import app
from jml import utils

runner = CliRunner()

# ---------------------
# Unit tests for utils
# ---------------------
def test_parse_json_and_yaml():
    json_data = '{"key": "value"}'
    yaml_data = 'key: value'

    assert utils.parse_json(json_data) == {"key": "value"}
    assert utils.parse_yaml(yaml_data) == {"key": "value"}


def test_try_parse():
    assert utils.try_parse('{"key":1}') == {"key":1}
    assert utils.try_parse('key: 1') == {"key":1}
    assert utils.try_parse('invalid:\ncontent') is None


def test_output_json_and_yaml():
    data = {"a": 1, "b": 2}
    json_str = utils.output_json(data, pretty=False)
    json_pretty = utils.output_json(data, pretty=True)
    yaml_str = utils.output_yaml(data)

    assert json_str == '{"a":1,"b":2}'
    assert '  ' in json_pretty  # pretty should have indentation
    assert 'a: 1' in yaml_str and 'b: 2' in yaml_str

# ---------------------
# Integration tests CLI
# ---------------------

def test_cli_json_to_yaml(tmp_path: Path):
    input_file = tmp_path / "test.json"
    input_file.write_text('{"key":"value"}')

    output_file = tmp_path / "out.yaml"

    result = runner.invoke(app, ["-y", "-i", str(input_file), "-o", str(output_file)])
    assert result.exit_code == 0
    assert output_file.read_text().strip() == 'key: value'


def test_cli_yaml_to_json_stdout(tmp_path: Path):
    input_file = tmp_path / "test.yaml"
    input_file.write_text('key: value')

    result = runner.invoke(app, ["-j", "-i", str(input_file)])
    assert result.exit_code == 0
    assert '{"key":"value"}' in result.output


def test_cli_pretty_json(tmp_path: Path):
    input_file = tmp_path / "test.yaml"
    input_file.write_text('key: value')

    result = runner.invoke(app, ["-j", "-p", "-i", str(input_file)])
    assert result.exit_code == 0
    assert '\n' in result.output  # pretty JSON should contain newlines


def test_cli_stdin(monkeypatch: pytest.MonkeyPatch):
    stdin_data = '{"key": "value"}'
    monkeypatch.setattr(sys, 'stdin', io.StringIO(stdin_data))

    result = runner.invoke(app, ["-y"], input=stdin_data)
    assert result.exit_code == 0
    assert 'key: value' in result.output

def test_cli_input():
    stdin_data = 'key: value'

    result = runner.invoke(app, ["-j"], input=stdin_data)
    assert result.exit_code == 0
    assert '{"key":"value"}' in result.output


def test_cli_invalid_file(tmp_path: Path):
    input_file = tmp_path / "test.txt"
    input_file.write_text('invalid:\ncontent')

    result = runner.invoke(app, ["-j", "-i", str(input_file)])
    assert result.exit_code == 1

def test_cli_invalid_stdin():
    invalid_stdin_data = '---'

    result = runner.invoke(app, ["-j"], input=invalid_stdin_data)
    assert result.exit_code == 1

def test_cli_both_output_type():
    stdin_data = 'key: value'

    result = runner.invoke(app, ["-j","-y"], input=stdin_data)
    assert result.exit_code == 2

def test_cli_no_output_type():
    stdin_data = 'key: value'

    result = runner.invoke(app, ["-p"], input=stdin_data)
    assert result.exit_code == 2

def test_invalid_parse(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    input_file = tmp_path / "test.json"
    input_file.write_text('{"key":"value"}')

    output_file = tmp_path / "out.yaml"
    monkeypatch.setattr(Path, 'write_text', RuntimeError())
    
    result = runner.invoke(app, ["-y", "-i", str(input_file), "-o", str(output_file)])
    assert result.exit_code == 1



def test_validate_command_valid(tmp_path: Path):
    input_file = tmp_path / "test.json"
    input_file.write_text('{"a":1}')

    result = runner.invoke(app, ["validate", str(input_file)])
    assert result.exit_code == 0
    assert 'is valid' in result.output


def test_validate_command_invalid(tmp_path: Path):
    input_file = tmp_path / "test.json"
    input_file.write_text('invalid')

    result = runner.invoke(app, ["validate", str(input_file)])
    assert result.exit_code != 0
    assert 'Invalid file' in result.output

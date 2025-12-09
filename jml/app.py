import typer
import sys
from rich.console import Console
from pathlib import Path
from jml.utils import load_file, output_json, output_yaml, try_parse

console = Console()
"""Console instance for interactions"""
app = typer.Typer(
    invoke_without_command=True,
    no_args_is_help=True,
)
"""Typer application which is the main componenet"""


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    json_out: bool = typer.Option(False, "-j", "--json", help="Output JSON"),
    yaml_out: bool = typer.Option(False, "-y", "--yaml", help="Output YAML"),
    pretty: bool = typer.Option(
        False, "-p", "--pretty", help="Pretty output (JSON only)"
    ),
    input_file: Path = typer.Option(
        None, "-i", "--input", help="Input file (json/yaml)"
    ),
    output: Path = typer.Option(
        None, "-o", "--output", help="Write to file instead of stdout"
    ),
):
    """
    Main entrypoing for the application which wil call every times even if other subcommand the targets
    This handling the main logic which is the basic conversions

    Args:
        ctx (typer.Context): context of the running it contians if there is any other subcomand
        json_out (bool, optional): If True then the output format is in JSON. Defaults to False.
        yaml_out (bool, optional): If True then the output format is in YAML. Defaults to False.
        pretty (bool, optional): Pretty output (JSON only). Defaults to False.
        input_file (Path, optional): Input file (json/yaml). Defaults to None.
        output (Path, optional): Write to file instead of stdout. Defaults to None.

    Raises:
        typer.BadParameter: If you specify both or none of json or yaml output
        typer.Exit(1): If the parsing are failed
    """

    if ctx.invoked_subcommand:
        return

    if json_out and yaml_out:
        raise typer.BadParameter("Choose only one output format: -j OR -y")

    if not json_out and not yaml_out:
        raise typer.BadParameter("Specify output format: -j or -y")

    # Read from file or stdin-ből
    if input_file is not None:
        try:
            data = load_file(input_file)
        except Exception as e:
            console.print(f"[red]Failed to load input:[/] {e}")
            raise typer.Exit(1)
    else:
        # stdin-ről olvas
        text = sys.stdin.read()
        data = try_parse(text)
        if data is None:
            console.print("[red]Failed to parse input![/]")
            raise typer.Exit(1)

    # format output
    if json_out:
        text = output_json(data, pretty)
    else:
        text = output_yaml(data)

    # write or print
    if output:
        try:
            output.write_text(text)
            console.print(f"[green]Wrote to {output}[/]")
        except Exception as e:
            console.print(f"[red]Failed to write:[/] {e}")
            raise typer.Exit(1)
    else:
        typer.echo(text)


@app.command()
def validate(input_path: Path):
    """Validate a JSON/YAML if it is valid

    Args:
        input_path (Path): The YAML or JSON path

    Raises:
        typer.Exit(1): If it can't be parsing
    """
    try:
        load_file(input_path)
        console.print(f"[green]✓ {input_path} is valid[/]")
    except Exception as e:
        console.print(f"[red]✗ Invalid file:[/] {e}")
        raise typer.Exit(1)

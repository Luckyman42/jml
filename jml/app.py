import typer
from rich.console import Console
from pathlib import Path
from jml.utils import load_file, output_json, output_yaml

console = Console()
app = typer.Typer(
    invoke_without_command=True,
    no_args_is_help=True,
)


@app.callback()
def main(
    ctx: typer.Context,
    json_out: bool = typer.Option(False, "-j", "--json", help="JSON format output"),
    yaml_out: bool = typer.Option(False, "-y", "--yaml", help="YAML format output"),
    pretty: bool = typer.Option(False, "-p", "--pretty", help="If the output format is JSON then it makes pretty"),
    input_path: Path = typer.Option(None, "-i", "--input", help="Input file (json/yaml)"),
    output: Path = typer.Option(None, "-o", "--output", help="Output file path, if missing output goes to stdout"),
):
    """Process and convert JSON/YAML files."""
    # Ha van subcommand, akkor ne fusson ez a blokk.
    if ctx.invoked_subcommand:
        return

    if input_path is None:
        typer.echo(ctx.get_help())
        raise typer.Exit()
    
    # conflict check
    if json_out and yaml_out:
        raise typer.BadParameter("Choose only one output format: use -j OR -y, not both.")

    if not json_out and not yaml_out:
        raise typer.BadParameter("You must specify -j or -y.")

    # load file
    try:
        data = load_file(input_path)
    except Exception as e:
        console.print(f"[red]Failed to load:[/] {e}")
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
    """Check if the file is a valid JSON/YAML."""
    try:
        load_file(input_path)
        console.print(f"[green]✓ {input_path} is valid[/]")
    except Exception as e:
        console.print(f"[red]✗ Invalid file:[/] {e}")
        raise typer.Exit(1)

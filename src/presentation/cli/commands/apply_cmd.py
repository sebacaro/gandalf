import typer
import questionary
from questionary import Style
from src.application.use_cases.apply_spec import list_in_progress_features, apply_spec
from src.presentation.ui.display import (
    console, show_step, show_success, show_error, show_warning, show_info
)

app = typer.Typer()

_style = Style([
    ("qmark", "fg:yellow bold"),
    ("question", "bold"),
    ("answer", "fg:cyan bold"),
    ("pointer", "fg:yellow bold"),
    ("highlighted", "fg:yellow bold"),
    ("selected", "fg:green"),
])


@app.callback(invoke_without_command=True)
def apply(
    ctx: typer.Context,
    path: str = typer.Option(".", "--path", "-p", help="Ruta del proyecto"),
):
    """Abre los archivos de spec de una feature en Cursor para ejecutar sdd-apply."""
    if ctx.invoked_subcommand is not None:
        return

    features = list_in_progress_features(path)

    if not features:
        show_warning("No hay features en [cyan]specs/in-progress/[/cyan]")
        show_info("Usa [bold cyan]gandalf spec[/bold cyan] para crear una.")
        raise typer.Exit(0)

    choices = [
        questionary.Choice(title=slug, value=feature_path)
        for slug, feature_path in features
    ]

    selected = questionary.select(
        "¿Qué feature quieres aplicar en Cursor?",
        choices=choices,
        style=_style,
    ).ask()

    if selected is None:
        show_error("Cancelado.")
        raise typer.Exit(1)

    show_step("Abriendo en Cursor...")
    success, error = apply_spec(selected)

    if not success:
        show_error(error)
        raise typer.Exit(1)

    show_success("Cursor abierto con los 4 archivos de spec.")
    console.print(
        "\n[dim]En Cursor:[/dim] Usa [bold cyan]@01_proposal.md @02_requirements.md "
        "@03_design.md @04_tasks.md[/bold cyan] y el comando [bold]sdd-apply[/bold]."
    )

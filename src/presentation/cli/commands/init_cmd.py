import typer
import questionary
from src.presentation.forms.project_form import collect_project
from src.application.use_cases.init_project import init_project
from src.presentation.ui.display import (
    console, show_step, show_success, show_error, show_info
)

app = typer.Typer()


@app.callback(invoke_without_command=True)
def init(
    ctx: typer.Context,
    output: str = typer.Option(".", "--output", "-o", help="Directorio donde crear el proyecto"),
):
    """Inicializa un nuevo proyecto con estructura de carpetas y Cursor rules SDD."""
    if ctx.invoked_subcommand is not None:
        return

    console.print("[dim]Configura tu nuevo proyecto. Ctrl+C para cancelar.[/dim]\n")

    project = collect_project(output_path=output)
    if project is None:
        show_error("Cancelado.")
        raise typer.Exit(1)

    show_step(f"Creando proyecto [bold yellow]{project.name}[/bold yellow]...")
    success, paths, error = init_project(project)

    if not success:
        show_error(f"Error creando proyecto: {error}")
        raise typer.Exit(1)

    show_success(f"Proyecto '[bold]{project.name}[/bold]' creado en [cyan]{output}/{project.slug}/[/cyan]")
    console.print(f"\n[dim]Stack:[/dim] {project.stack} · [dim]Arquitectura:[/dim] {project.architecture}")
    console.print(f"[dim]Carpetas creadas:[/dim] {len(paths)}")
    console.print(
        "\n[dim]Cursor rules SDD creadas en[/dim] [cyan].cursor/rules/[/cyan]"
        "\n[dim]Specs folder:[/dim] [cyan]specs/in-progress/[/cyan]"
        "\n\n[dim]Siguiente paso:[/dim] [bold cyan]gandalf spec[/bold cyan] [dim]para crear tu primera feature[/dim]"
    )

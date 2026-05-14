import typer
from src.presentation.forms.feature_form import collect_feature_spec
from src.application.use_cases.create_feature_spec import create_feature_spec
from src.presentation.ui.display import (
    console, show_step, show_success, show_error, show_warning,
    show_files_created, show_spec_summary,
)
from src.infrastructure.detectors.file_stack_detector import FileStackDetector

app = typer.Typer()
_detector = FileStackDetector()


@app.callback(invoke_without_command=True)
def spec(
    ctx: typer.Context,
    path: str = typer.Option(".", "--path", "-p", help="Ruta del proyecto (default: directorio actual)"),
):
    """Genera los 4 archivos SDD para una feature y crea la rama git."""
    if ctx.invoked_subcommand is not None:
        return

    detected = _detector.detect(path)
    stack_name = _detector.stack_display_name(detected)

    show_step(f"Stack detectado: [bold yellow]{stack_name}[/bold yellow]")
    console.print("[dim]Responde las preguntas para generar los specs. Ctrl+C para cancelar.[/dim]\n")

    feature_spec = collect_feature_spec(project_path=path)
    if feature_spec is None:
        show_error("Cancelado.")
        raise typer.Exit(1)

    show_step("Generando archivos de spec...")
    success, files, error, git_result = create_feature_spec(feature_spec)

    if not success:
        show_error(f"Error generando specs: {error}")
        raise typer.Exit(1)

    show_spec_summary(
        feature_spec.name,
        _detector.stack_display_name(feature_spec.stack),
        f"specs/in-progress/{feature_spec.slug}/",
    )
    show_files_created(files)
    show_success(f"Specs generados para '[bold]{feature_spec.name}[/bold]'")

    git_ok, branch_name, git_error = git_result
    if git_ok:
        show_success(f"Rama creada: [bold cyan]{branch_name}[/bold cyan]")
    else:
        show_warning(f"No se pudo crear la rama: {git_error}")

    console.print(
        f"\n[dim]Siguiente paso:[/dim] [bold cyan]gandalf apply[/bold cyan] "
        f"[dim]para abrir en Cursor[/dim]"
    )

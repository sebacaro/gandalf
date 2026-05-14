import typer
import questionary
from questionary import Style
from src.application.use_cases.apply_spec import list_verifiable_features
from src.application.use_cases.verify_spec import (
    load_criteria_from_spec, load_tasks_from_spec, verify_spec
)
from src.presentation.ui.display import (
    console, show_step, show_error, show_warning, show_info, show_verify_results
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
def verify(
    ctx: typer.Context,
    path: str = typer.Option(".", "--path", "-p", help="Ruta del proyecto"),
):
    """Valida la implementación contra los criterios de aceptación del spec."""
    if ctx.invoked_subcommand is not None:
        return

    features = list_verifiable_features(path)
    if not features:
        show_warning("No hay features en [cyan]specs/in-progress/[/cyan] ni en [cyan]specs/done/[/cyan]")
        show_info("Usa [bold cyan]gandalf spec[/bold cyan] para crear una.")
        raise typer.Exit(0)

    choices = [
        questionary.Choice(title=f"{slug}  [dim]({status})[/dim]", value=feature_path)
        for slug, feature_path, status in features
    ]

    selected = questionary.select(
        "¿Qué feature quieres verificar?",
        choices=choices,
        style=_style,
    ).ask()

    if selected is None:
        show_error("Cancelado.")
        raise typer.Exit(1)

    criteria = load_criteria_from_spec(selected)
    pending_tasks = load_tasks_from_spec(selected)

    if not criteria:
        show_warning("No se encontraron criterios de aceptación en [cyan]02_requirements.md[/cyan]")
        raise typer.Exit(1)

    show_step(f"Verificando {len(criteria)} criterios de aceptación...")
    console.print("[dim]Para cada criterio, indica si está cumplido.[/dim]\n")

    results = []
    for criterion in criteria:
        status = questionary.select(
            f"Criterio: {criterion[:80]}{'...' if len(criterion) > 80 else ''}",
            choices=[
                questionary.Choice("✅  Cumplido", value="approved"),
                questionary.Choice("⚠️   Parcial", value="partial"),
                questionary.Choice("❌  Faltante", value="failed"),
            ],
            style=_style,
        ).ask()
        if status is None:
            show_error("Cancelado.")
            raise typer.Exit(1)
        results.append({"label": criterion, "status": status})

    if pending_tasks:
        console.print(f"\n[dim]Tasks pendientes en 04_tasks.md: {len(pending_tasks)}[/dim]")
        for t in pending_tasks[:5]:
            console.print(f"  [red]□[/red] {t}")
        if len(pending_tasks) > 5:
            console.print(f"  [dim]... y {len(pending_tasks) - 5} más[/dim]")

    summary = verify_spec(selected, results)

    console.print()
    show_verify_results(results)

    if summary["verdict"] == "APPROVED" and not pending_tasks:
        console.print(
            "\n[dim]Siguiente paso:[/dim] mueve la carpeta a [cyan]specs/done/[/cyan] "
            "y crea el PR."
        )
    else:
        console.print(
            "\n[dim]Completa los criterios faltantes y vuelve a ejecutar[/dim] "
            "[bold cyan]gandalf verify[/bold cyan]."
        )

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box

console = Console()

def show_banner():
    content = (
        "  🧙🏽‍♂️  [bold yellow]GANDALF[/bold yellow]\n"
        "  [dim]Spec Driven Development · Local CLI[/dim]"
    )
    console.print(Panel(content, border_style="yellow", padding=(1, 4)))


def show_success(message: str):
    console.print(f"[bold green]✅ {message}[/bold green]")


def show_error(message: str):
    console.print(f"[bold red]❌ {message}[/bold red]")


def show_warning(message: str):
    console.print(f"[bold yellow]⚠️  {message}[/bold yellow]")


def show_info(message: str):
    console.print(f"[dim]ℹ  {message}[/dim]")


def show_step(step: str):
    console.print(f"\n[bold cyan]→[/bold cyan] {step}")


def show_files_created(files: list[str], title: str = "Archivos generados"):
    table = Table(title=title, box=box.ROUNDED, border_style="green")
    table.add_column("Archivo", style="cyan")
    for f in files:
        table.add_row(f)
    console.print(table)


def show_spec_summary(feature_name: str, stack: str, output_dir: str):
    table = Table(box=box.ROUNDED, border_style="yellow", show_header=False)
    table.add_column("Campo", style="dim")
    table.add_column("Valor", style="bold white")
    table.add_row("Feature", feature_name)
    table.add_row("Stack", stack)
    table.add_row("Carpeta", output_dir)
    console.print(table)


def show_verify_results(results: list[dict]):
    table = Table(title="Verificación de Spec", box=box.ROUNDED, border_style="cyan")
    table.add_column("Estado", width=8)
    table.add_column("Criterio")

    approved = 0
    for r in results:
        status = r.get("status", "pending")
        label = r.get("label", "")
        if status == "approved":
            icon = "[bold green]  ✅[/bold green]"
            approved += 1
        elif status == "failed":
            icon = "[bold red]  ❌[/bold red]"
        else:
            icon = "[bold yellow]  ⚠️[/bold yellow]"
        table.add_row(icon, label)

    console.print(table)
    total = len(results)
    if approved == total:
        show_success(f"APPROVED — {approved}/{total} criterios cumplidos")
    else:
        show_warning(f"NEEDS WORK — {approved}/{total} criterios cumplidos")

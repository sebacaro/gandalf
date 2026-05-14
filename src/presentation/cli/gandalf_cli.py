import typer
from src.presentation.ui.display import show_banner
from src.presentation.cli.commands import spec_cmd, init_cmd, apply_cmd, verify_cmd

app = typer.Typer(
    name="gandalf",
    help="Gandalf — Spec Driven Development CLI",
    no_args_is_help=True,
    rich_markup_mode="rich",
    add_completion=False,
)

app.add_typer(spec_cmd.app, name="spec", help="Genera specs SDD para una feature")
app.add_typer(init_cmd.app, name="init", help="Inicializa un nuevo proyecto con estructura SDD")
app.add_typer(apply_cmd.app, name="apply", help="Abre los specs de una feature en Cursor")
app.add_typer(verify_cmd.app, name="verify", help="Valida la implementación contra el spec")


def main():
    show_banner()
    app(standalone_mode=True)


if __name__ == "__main__":
    main()

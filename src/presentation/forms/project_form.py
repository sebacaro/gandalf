import re
import questionary
from questionary import Style

from src.domain.entities.project import Project
from src.infrastructure.detectors.file_stack_detector import STACKS

_style = Style([
    ("qmark", "fg:yellow bold"),
    ("question", "bold"),
    ("answer", "fg:cyan bold"),
    ("pointer", "fg:yellow bold"),
    ("highlighted", "fg:yellow bold"),
    ("selected", "fg:green"),
    ("separator", "fg:yellow"),
    ("instruction", "fg:gray"),
])


def _slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    return text.strip("-")


def collect_project(output_path: str = ".") -> Project | None:
    print()

    name = questionary.text(
        "Nombre del proyecto:",
        style=_style,
    ).ask()
    if name is None:
        return None

    description = questionary.text(
        "Descripción breve del proyecto:",
        style=_style,
    ).ask()
    if description is None:
        return None

    stack_choices = [
        questionary.Choice(title=display, value=key)
        for key, display in STACKS.items()
    ]
    stack = questionary.select(
        "Stack principal:",
        choices=stack_choices,
        style=_style,
    ).ask()
    if stack is None:
        return None

    architecture = questionary.select(
        "Arquitectura:",
        choices=[
            questionary.Choice("Clean Architecture", "Clean Architecture"),
            questionary.Choice("MVC", "MVC"),
            questionary.Choice("Simple (sin capas estrictas)", "Simple"),
        ],
        style=_style,
    ).ask()
    if architecture is None:
        return None

    initial_features_raw = questionary.checkbox(
        "Features iniciales a incluir:",
        choices=[
            questionary.Choice("Autenticación (auth)", "auth"),
            questionary.Choice("Base de datos / ORM", "database"),
            questionary.Choice("API REST", "api"),
            questionary.Choice("Internacionalización (i18n)", "i18n"),
            questionary.Choice("CI/CD básico", "cicd"),
            questionary.Choice("Tests (setup inicial)", "tests"),
        ],
        style=_style,
    ).ask()
    if initial_features_raw is None:
        return None

    return Project(
        name=name.strip(),
        slug=_slugify(name),
        stack=stack,
        architecture=architecture,
        description=description.strip(),
        initial_features=initial_features_raw,
        output_path=output_path,
    )

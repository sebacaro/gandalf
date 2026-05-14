import re
import questionary
from questionary import Style

from src.domain.entities.feature_spec import FeatureSpec
from src.infrastructure.detectors.file_stack_detector import FileStackDetector, STACKS

_detector = FileStackDetector()

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


def collect_feature_spec(project_path: str = ".") -> FeatureSpec | None:
    detected_stack = _detector.detect(project_path)
    stack_choices = [
        questionary.Choice(title=display, value=key)
        for key, display in STACKS.items()
    ]

    # Move detected stack to top of list
    stack_choices = sorted(
        stack_choices,
        key=lambda c: (0 if c.value == detected_stack else 1, c.title),
    )

    print()
    answers = {}

    name = questionary.text(
        "Nombre de la feature:",
        style=_style,
    ).ask()
    if name is None:
        return None
    answers["name"] = name.strip()
    answers["slug"] = _slugify(name)

    description = questionary.text(
        "Descripción breve (qué problema resuelve, 1-2 frases):",
        style=_style,
    ).ask()
    if description is None:
        return None
    answers["description"] = description.strip()

    context = questionary.text(
        "Contexto adicional (pantallas, usuarios, flujo, motivación):",
        instruction="(puede ser largo — Enter para continuar)",
        style=_style,
    ).ask()
    if context is None:
        return None
    answers["context"] = context.strip()

    stack = questionary.select(
        "Stack del proyecto:",
        choices=stack_choices,
        style=_style,
    ).ask()
    if stack is None:
        return None
    answers["stack"] = stack

    ext = questionary.text(
        "Servicios externos involucrados (APIs, SDKs, libs nuevas):",
        instruction="(dejar vacío si ninguno)",
        style=_style,
    ).ask()
    if ext is None:
        return None
    answers["external_services"] = ext.strip()

    components = questionary.text(
        "Componentes / pantallas / módulos NUEVOS a crear:",
        style=_style,
    ).ask()
    if components is None:
        return None
    answers["new_components"] = components.strip()

    modified = questionary.text(
        "Archivos / módulos EXISTENTES que se modificarán:",
        style=_style,
    ).ask()
    if modified is None:
        return None
    answers["modified_files"] = modified.strip()

    out_of_scope = questionary.text(
        "¿Qué queda FUERA del scope? (opcional):",
        instruction="(dejar vacío para usar texto por defecto)",
        style=_style,
    ).ask()
    if out_of_scope is None:
        return None
    answers["out_of_scope"] = out_of_scope.strip()

    print("\nCriterios de aceptación (formato Gherkin).")
    print("  Escribe un criterio por línea. Ejemplo:")
    print("  Given usuario logueado / When toca 'Guardar' / Then aparece confirmación")
    print("  (escribe 'listo' cuando termines)\n")

    criteria = []
    i = 1
    while True:
        c = questionary.text(
            f"Criterio {i} (o 'listo' para terminar):",
            style=_style,
        ).ask()
        if c is None or c.strip().lower() in ("listo", "done", "q", ""):
            break
        criteria.append(c.strip())
        i += 1

    if not criteria:
        criteria = ["Given [condición inicial] / When [acción del usuario] / Then [resultado esperado]"]

    answers["acceptance_criteria"] = criteria

    edge_cases = questionary.text(
        "Edge cases a considerar (separados por comas o líneas):",
        instruction="(estado vacío, sin conexión, usuario sin permisos, etc.)",
        style=_style,
    ).ask()
    if edge_cases is None:
        return None
    answers["edge_cases"] = edge_cases.strip()

    return FeatureSpec(
        name=answers["name"],
        slug=answers["slug"],
        stack=answers["stack"],
        description=answers["description"],
        context=answers["context"],
        new_components=answers["new_components"],
        modified_files=answers["modified_files"],
        acceptance_criteria=answers["acceptance_criteria"],
        edge_cases=answers["edge_cases"],
        external_services=answers["external_services"],
        out_of_scope=answers["out_of_scope"],
        project_path=project_path,
    )

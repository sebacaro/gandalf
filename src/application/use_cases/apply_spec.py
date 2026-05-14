from pathlib import Path

from src.infrastructure.cursor.cursor_integration import open_in_cursor


def list_in_progress_features(project_path: str = ".") -> list[tuple[str, str]]:
    """
    Returns list of (slug, full_path) for features in specs/in-progress/.
    """
    specs_dir = Path(project_path) / "specs" / "in-progress"
    if not specs_dir.exists():
        return []

    features = []
    for entry in sorted(specs_dir.iterdir()):
        if entry.is_dir() and not entry.name.startswith("."):
            features.append((entry.name, str(entry)))
    return features


def list_verifiable_features(project_path: str = ".") -> list[tuple[str, str, str]]:
    """
    Returns list of (slug, full_path, status) for features in both
    specs/in-progress/ and specs/done/.
    """
    features = []
    for status in ("in-progress", "done"):
        specs_dir = Path(project_path) / "specs" / status
        if not specs_dir.exists():
            continue
        for entry in sorted(specs_dir.iterdir()):
            if entry.is_dir() and not entry.name.startswith("."):
                features.append((entry.name, str(entry), status))
    return features


def apply_spec(feature_path: str) -> tuple[bool, str]:
    """
    Open the feature spec folder in Cursor.
    Returns (success, error_message).
    """
    if not Path(feature_path).exists():
        return False, f"Carpeta no encontrada: {feature_path}"

    files = [
        str(Path(feature_path) / f)
        for f in ["01_proposal.md", "02_requirements.md", "03_design.md", "04_tasks.md"]
        if (Path(feature_path) / f).exists()
    ]

    if not files:
        return False, "No se encontraron archivos de spec en la carpeta."

    success = open_in_cursor(files)
    if not success:
        return False, (
            "No se pudo abrir Cursor. Verifica que esté instalado y en PATH.\n"
            f"  Abre manualmente: cursor {feature_path}"
        )
    return True, ""

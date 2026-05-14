from pathlib import Path

from src.domain.entities.project import Project
from src.infrastructure.generators.jinja_spec_generator import JinjaSpecGenerator

_generator = JinjaSpecGenerator()


def init_project(project: Project) -> tuple[bool, list[str], str]:
    """
    Create project folder structure + cursor rules + specs folder.
    Returns (success, list_of_created_paths, error_message).
    """
    try:
        created = _generator.generate_project_structure(project, project.output_path)
        return True, created, ""
    except Exception as e:
        return False, [], str(e)

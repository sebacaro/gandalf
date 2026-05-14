from pathlib import Path

from src.domain.entities.feature_spec import FeatureSpec
from src.infrastructure.generators.jinja_spec_generator import JinjaSpecGenerator
from src.infrastructure.git.git_ops import create_feature_branch

_generator = JinjaSpecGenerator()


def create_feature_spec(
    spec: FeatureSpec,
) -> tuple[bool, list[str], str, tuple[bool, str, str]]:
    """
    Generate the 4 SDD spec files and create a git branch for the feature.
    Returns (success, created_files, error_message, (git_ok, branch_name, git_error)).
    """
    specs_dir = Path(spec.project_path) / "specs" / "in-progress" / spec.slug

    try:
        created = _generator.generate_feature_specs(spec, str(specs_dir))
    except Exception as e:
        return False, [], str(e), (False, f"feature/{spec.slug}", "")

    git_result = create_feature_branch(spec.project_path, spec.slug)
    return True, created, "", git_result

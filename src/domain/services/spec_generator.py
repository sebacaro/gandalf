from abc import ABC, abstractmethod
from ..entities.feature_spec import FeatureSpec
from ..entities.project import Project


class SpecGenerator(ABC):
    @abstractmethod
    def generate_feature_specs(self, spec: FeatureSpec, output_dir: str) -> list[str]:
        """Generate the 4 SDD spec files. Returns list of created file paths."""
        ...

    @abstractmethod
    def generate_project_structure(self, project: Project, output_dir: str) -> list[str]:
        """Generate project folder structure and template specs."""
        ...

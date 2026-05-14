from dataclasses import dataclass, field
from typing import Optional


@dataclass
class FeatureSpec:
    name: str
    slug: str
    stack: str
    description: str
    context: str
    new_components: str
    modified_files: str
    acceptance_criteria: list[str]
    edge_cases: str
    external_services: str = ""
    out_of_scope: str = ""
    project_path: str = "."

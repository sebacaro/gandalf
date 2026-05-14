from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Project:
    name: str
    slug: str
    stack: str
    architecture: str
    description: str
    initial_features: list[str] = field(default_factory=list)
    output_path: str = "."

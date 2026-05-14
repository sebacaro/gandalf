from abc import ABC, abstractmethod


class StackDetector(ABC):
    @abstractmethod
    def detect(self, project_path: str) -> str:
        """Detect the stack of the project at project_path. Returns stack name."""
        ...

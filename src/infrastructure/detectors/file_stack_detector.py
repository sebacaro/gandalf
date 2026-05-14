import json
import os
from pathlib import Path
from src.domain.services.stack_detector import StackDetector

STACKS = {
    "flutter": "Flutter",
    "fastapi": "FastAPI",
    "nextjs": "Next.js",
    "node": "Node.js",
    "python": "Python",
    "rust": "Rust",
    "go": "Go",
    "generic": "Genérico",
}


class FileStackDetector(StackDetector):
    def detect(self, project_path: str) -> str:
        path = Path(project_path)

        if (path / "pubspec.yaml").exists():
            return "flutter"

        if (path / "Cargo.toml").exists():
            return "rust"

        if (path / "go.mod").exists():
            return "go"

        pkg = path / "package.json"
        if pkg.exists():
            try:
                data = json.loads(pkg.read_text())
                deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
                if "next" in deps:
                    return "nextjs"
            except Exception:
                pass
            return "node"

        for req_file in ("requirements.txt", "pyproject.toml"):
            if (path / req_file).exists():
                content = (path / req_file).read_text().lower()
                if "fastapi" in content:
                    return "fastapi"
                return "python"

        return "generic"

    def stack_display_name(self, stack_key: str) -> str:
        return STACKS.get(stack_key, "Genérico")

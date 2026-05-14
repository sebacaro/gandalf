import os
from datetime import date
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

from src.domain.entities.feature_spec import FeatureSpec
from src.domain.entities.project import Project
from src.domain.services.spec_generator import SpecGenerator
from src.infrastructure.detectors.file_stack_detector import FileStackDetector

TEMPLATES_DIR = Path(__file__).parent.parent / "templates"

TEMPLATE_FILES = [
    "01_proposal.md.j2",
    "02_requirements.md.j2",
    "03_design.md.j2",
    "04_tasks.md.j2",
]

OUTPUT_NAMES = [
    "01_proposal.md",
    "02_requirements.md",
    "03_design.md",
    "04_tasks.md",
]

_detector = FileStackDetector()


class JinjaSpecGenerator(SpecGenerator):
    def _get_env(self, stack: str) -> tuple[Environment, str]:
        stack_dir = TEMPLATES_DIR / stack
        if not stack_dir.exists():
            stack_dir = TEMPLATES_DIR / "generic"
        env = Environment(
            loader=FileSystemLoader(str(stack_dir)),
            autoescape=select_autoescape([]),
            keep_trailing_newline=True,
        )
        return env, str(stack_dir)

    def generate_feature_specs(self, spec: FeatureSpec, output_dir: str) -> list[str]:
        env, _ = self._get_env(spec.stack)
        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)

        context = {
            "spec": spec,
            "stack_display": _detector.stack_display_name(spec.stack),
            "date": date.today().isoformat(),
        }

        created = []
        for template_name, output_name in zip(TEMPLATE_FILES, OUTPUT_NAMES):
            # Fall back to generic template if stack-specific not found
            try:
                template = env.get_template(template_name)
            except Exception:
                generic_env, _ = self._get_env("generic")
                template = generic_env.get_template(template_name)

            content = template.render(**context)
            file_path = out_path / output_name
            file_path.write_text(content, encoding="utf-8")
            created.append(str(file_path))

        return created

    def generate_project_structure(self, project: Project, output_dir: str) -> list[str]:
        base = Path(output_dir) / project.slug
        base.mkdir(parents=True, exist_ok=True)

        created_dirs = []
        for d in self._get_project_dirs(project):
            (base / d).mkdir(parents=True, exist_ok=True)
            created_dirs.append(str(base / d))

        # Create specs folder structure
        specs_templates = base / "specs" / "_templates"
        specs_in_progress = base / "specs" / "in-progress"
        specs_done = base / "specs" / "done"
        for d in [specs_templates, specs_in_progress, specs_done]:
            d.mkdir(parents=True, exist_ok=True)
            created_dirs.append(str(d))

        # Create cursor rules
        cursor_rules = base / ".cursor" / "rules"
        cursor_rules.mkdir(parents=True, exist_ok=True)
        self._write_cursor_rules(cursor_rules, project)
        created_dirs.append(str(cursor_rules))

        # Create README
        readme = base / "README.md"
        readme.write_text(
            f"# {project.name}\n\n{project.description}\n\n"
            f"Stack: **{_detector.stack_display_name(project.stack)}** — "
            f"Arquitectura: **{project.architecture}**\n\n"
            f"Generado con [Gandalf](https://github.com/sebacaro/gandalf).\n"
        )
        created_dirs.append(str(readme))

        return created_dirs

    def _get_project_dirs(self, project: Project) -> list[str]:
        common = ["docs", "scripts", "tests"]

        stack_dirs = {
            "flutter": [
                "lib/core/routing",
                "lib/core/theme",
                "lib/core/widgets",
                "lib/core/utils",
                "lib/features",
                "lib/injection_container.dart".replace(".dart", ""),
                "assets/images",
                "assets/fonts",
            ],
            "fastapi": [
                "app/core",
                "app/routers",
                "app/services",
                "app/repositories",
                "app/schemas",
                "app/models",
                "app/database",
                "migrations",
            ],
            "nextjs": [
                "app/(routes)",
                "components/ui",
                "lib",
                "hooks",
                "types",
                "public",
            ],
            "python": [
                "src/core",
                "src/services",
                "src/models",
                "config",
            ],
        }

        if project.architecture in ("Clean Architecture", "clean"):
            arch_dirs = {
                "python": [
                    "src/domain/entities",
                    "src/domain/services",
                    "src/application/use_cases",
                    "src/infrastructure/repositories",
                    "src/presentation/cli",
                ],
            }
            extra = arch_dirs.get(project.stack, [])
        else:
            extra = []

        return common + stack_dirs.get(project.stack, []) + extra

    def _write_cursor_rules(self, rules_dir: Path, project: Project) -> None:
        rules = {
            "sdd-enrich-us.mdc": self._enrich_us_rule(project),
            "sdd-fast-forward.mdc": self._fast_forward_rule(project),
            "sdd-apply.mdc": self._apply_rule(project),
            "sdd-verify.mdc": self._verify_rule(project),
            "sdd-core-review.mdc": self._core_review_rule(project),
        }
        for filename, content in rules.items():
            (rules_dir / filename).write_text(content, encoding="utf-8")

    def _enrich_us_rule(self, project: Project) -> str:
        return f"""---
description: Enrich a vague user story into a complete technical specification
---

Actúa como Senior Product + Tech Lead de {project.name}.

Stack: {project.stack} · {project.architecture}

Toma la siguiente historia vaga y conviértela en especificación completa:

**Output:**
- Descripción clara (1 párrafo)
- Criterios de aceptación (formato Gherkin: Given/When/Then)
- Casos límite y edge cases
- Reglas de negocio
- Componentes/módulos afectados
- Escenarios de testing
- Preguntas abiertas (si las hay)

Historia:
[PEGAR HISTORIA AQUÍ]
"""

    def _fast_forward_rule(self, project: Project) -> str:
        return f"""---
description: Generate the 4 SDD spec files for a feature from an enriched user story
---

Actúa como Tech Lead de {project.name}. Genera los 4 archivos de especificación SDD.

Stack: {project.stack} · {project.architecture}

Crea estos archivos en specs/in-progress/[feature-slug]/:

**01_proposal.md** — Contexto, objetivo, alcance, qué NO incluye, impacto en módulos existentes
**02_requirements.md** — Criterios Gherkin, edge cases, reglas de negocio, escenarios de error
**03_design.md** — Estructura de módulos/capas, clases nuevas, decisiones técnicas, contratos
**04_tasks.md** — Checklist completo (mínimo 30 tasks), ordenado por capa/área

Formato tasks: `- [ ] [CAPA] descripción específica y atómica`

Historia enriquecida:
[PEGAR OUTPUT DE ENRICH-US]
"""

    def _apply_rule(self, project: Project) -> str:
        return f"""---
description: Implement all tasks from the SDD checklist following {project.name} conventions
---

Eres Senior Engineer de {project.name}. Implementa TODAS las tareas de specs/in-progress/[feature]/04_tasks.md.

Stack: {project.stack} · {project.architecture}

Reglas:
- No inventar lógica fuera de 03_design.md
- Marcar cada task como `- [x]` al completarla
- Escribir tests para la lógica nueva
- Al terminar: actualizar 04_tasks.md con tasks completadas

[PEGAR RUTA DEL FEATURE AQUÍ]
"""

    def _verify_rule(self, project: Project) -> str:
        return """---
description: Verify implementation against the SDD spec
---

Actúa como QA Engineer + Code Reviewer.

Verifica que la implementación cumple EXACTAMENTE:
1. Todos los criterios de 02_requirements.md
2. Diseño de 03_design.md (estructura, contratos, clases)
3. Todas las tasks de 04_tasks.md están completadas
4. Tests escritos y pasando
5. No hay código fuera del scope de 01_proposal.md

Output:
- ✅ Cumplido / ❌ Faltante / ⚠️ Parcial para cada criterio
- Lista de problemas con archivo:línea
- Veredicto: APPROVED / NEEDS WORK

[PEGAR RUTA DEL FEATURE AQUÍ]
"""

    def _core_review_rule(self, project: Project) -> str:
        return f"""---
description: Deep architectural review before PR
---

Actúa como Principal Engineer revisando {project.name} antes del merge.

Stack: {project.stack} · {project.architecture}

Revisa:
- Violaciones de arquitectura
- Problemas de performance (queries N+1, rebuilds innecesarios)
- Seguridad (validación de input, exposición de datos)
- Consistencia con patrones existentes
- Tests faltantes o insuficientes

Output: feedback específico con archivo:línea, severidad (P0/P1/P2) y fix sugerido.

[PEGAR RUTA DEL FEATURE AQUÍ]
"""

# Gandalf — CLI para Spec Driven Development

Herramienta local para generar specs SDD y estructuras de proyecto en la terminal.

## Comandos

```bash
# Activar entorno
source venv/bin/activate

# Ejecutar directamente
python main.py --help
python main.py spec
python main.py init
python main.py apply
python main.py verify

# O con gandalf global (después de install.sh)
gandalf spec
gandalf init
gandalf apply
gandalf verify
```

## Tests rápidos

```bash
# Smoke test: que el CLI arranca
python main.py --help

# Test de detección de stack
python -c "from src.infrastructure.detectors.file_stack_detector import FileStackDetector; print(FileStackDetector().detect('.'))"

# Test de generación (requiere carpeta temporal)
python -c "
from src.domain.entities.feature_spec import FeatureSpec
from src.application.use_cases.create_feature_spec import create_feature_spec
spec = FeatureSpec(name='Test', slug='test', stack='generic', description='Test feature', context='Test context', new_components='TestComponent', modified_files='main.py', acceptance_criteria=['Given user / When action / Then result'], edge_cases='Empty state', project_path='/tmp/gandalf_test')
ok, files, err = create_feature_spec(spec)
print('OK', files) if ok else print('ERROR', err)
"
```

## Instalación

```bash
bash scripts/install.sh
```

## Arquitectura

```
gandalf/
├── main.py                              # Entry point
├── src/
│   ├── domain/                          # Entidades + interfaces
│   ├── application/use_cases/           # Lógica de cada comando
│   ├── infrastructure/
│   │   ├── detectors/                   # Auto-detección de stack
│   │   ├── generators/                  # Renderizado Jinja2
│   │   ├── templates/{stack}/           # Templates por stack
│   │   └── cursor/                      # Integración con Cursor
│   └── presentation/
│       ├── cli/commands/                # Comandos typer
│       ├── forms/                       # Formularios questionary
│       └── ui/display.py                # Componentes rich
```

## Agregar un nuevo stack

1. Crear carpeta `src/infrastructure/templates/{stack}/` con los 4 templates `.j2`
2. Agregar entrada en `STACKS` dict en `file_stack_detector.py`
3. Agregar lógica de detección en `FileStackDetector.detect()`
4. Agregar dirs de proyecto en `JinjaSpecGenerator._get_project_dirs()`

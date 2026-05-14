#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

try:
    from src.presentation.cli.gandalf_cli import main

    if __name__ == "__main__":
        main()

except ImportError as e:
    print(f"❌ Error importando Gandalf: {e}")
    print("\n🛠️  Soluciones:")
    print("  1. Activa el venv:  source venv/bin/activate")
    print("  2. Instala deps:    pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error fatal: {e}")
    sys.exit(1)

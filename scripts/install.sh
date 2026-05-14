#!/usr/bin/env bash
set -e

GANDALF_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_PYTHON="$GANDALF_DIR/venv/bin/python"

# Prefer ~/.local/bin (no sudo), fall back to /usr/local/bin
if [ -w "/usr/local/bin" ]; then
  INSTALL_PATH="/usr/local/bin/gandalf"
else
  INSTALL_PATH="$HOME/.local/bin/gandalf"
  mkdir -p "$HOME/.local/bin"
fi

echo "⚡ Instalando Gandalf..."
echo "   Directorio: $GANDALF_DIR"

# Crear venv si no existe
if [ ! -f "$VENV_PYTHON" ]; then
  echo "   Creando entorno virtual..."
  python3 -m venv "$GANDALF_DIR/venv"
fi

# Instalar dependencias
echo "   Instalando dependencias..."
"$GANDALF_DIR/venv/bin/pip" install -r "$GANDALF_DIR/requirements.txt" -q

# Crear script wrapper
echo "   Creando comando 'gandalf' en $INSTALL_PATH..."
cat > "$INSTALL_PATH" << EOF
#!/usr/bin/env bash
exec "$VENV_PYTHON" "$GANDALF_DIR/main.py" "\$@"
EOF
chmod +x "$INSTALL_PATH"

echo ""
echo "✅ Gandalf instalado en $INSTALL_PATH"
echo ""

# Check if install dir is in PATH
if [[ ":$PATH:" != *":$(dirname $INSTALL_PATH):"* ]]; then
  echo "⚠️  Agrega esta línea a tu ~/.zshrc o ~/.bashrc:"
  echo "   export PATH=\"$(dirname $INSTALL_PATH):\$PATH\""
  echo ""
fi

echo "   Ejecuta: gandalf --help"
echo ""

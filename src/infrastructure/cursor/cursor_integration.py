import subprocess
import sys
from pathlib import Path


def open_in_cursor(paths: list[str]) -> bool:
    """Open one or more paths in Cursor. Returns True on success."""
    try:
        cmd = ["cursor"] + paths
        subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except FileNotFoundError:
        # Try common installation paths on macOS
        for cursor_path in [
            "/usr/local/bin/cursor",
            "/usr/bin/cursor",
            "/Applications/Cursor.app/Contents/MacOS/Cursor",
        ]:
            if Path(cursor_path).exists():
                subprocess.Popen(
                    [cursor_path] + paths,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                return True
        return False
    except Exception:
        return False


def cursor_available() -> bool:
    try:
        subprocess.run(["cursor", "--version"], capture_output=True, timeout=3)
        return True
    except Exception:
        return False

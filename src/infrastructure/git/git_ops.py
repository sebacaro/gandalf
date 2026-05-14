import subprocess


def create_feature_branch(project_path: str, slug: str) -> tuple[bool, str, str]:
    """
    Crea rama git feature/[slug] en project_path.
    Returns (success, branch_name, error_message).
    Nunca lanza excepción — git es opcional.
    """
    branch_name = f"feature/{slug}"
    try:
        result = subprocess.run(
            ["git", "checkout", "-b", branch_name],
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            return True, branch_name, ""
        return False, branch_name, result.stderr.strip()
    except FileNotFoundError:
        return False, branch_name, "git no está en PATH"
    except Exception as e:
        return False, branch_name, str(e)

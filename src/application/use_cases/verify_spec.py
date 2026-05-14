import re
from pathlib import Path


def load_criteria_from_spec(feature_path: str) -> list[str]:
    """Extract Gherkin scenario titles from 02_requirements.md."""
    req_file = Path(feature_path) / "02_requirements.md"
    if not req_file.exists():
        return []

    content = req_file.read_text(encoding="utf-8")
    # Extract text between ```gherkin blocks
    blocks = re.findall(r"```gherkin\s*(.*?)```", content, re.DOTALL)
    criteria = []
    for block in blocks:
        first_line = block.strip().split("\n")[0].strip()
        if first_line:
            criteria.append(first_line)
    return criteria


def load_tasks_from_spec(feature_path: str) -> list[str]:
    """Extract incomplete tasks from 04_tasks.md."""
    tasks_file = Path(feature_path) / "04_tasks.md"
    if not tasks_file.exists():
        return []

    content = tasks_file.read_text(encoding="utf-8")
    incomplete = re.findall(r"- \[ \] (.+)", content)
    return [t.strip() for t in incomplete]


def verify_spec(
    feature_path: str,
    criteria_results: list[dict],
) -> dict:
    """
    Given user-provided results for each criterion,
    return summary with verdict.

    criteria_results: [{"label": str, "status": "approved"|"failed"|"partial"}]
    """
    total = len(criteria_results)
    approved = sum(1 for r in criteria_results if r["status"] == "approved")
    failed = sum(1 for r in criteria_results if r["status"] == "failed")
    partial = total - approved - failed

    verdict = "APPROVED" if approved == total else "NEEDS WORK"

    return {
        "criteria_results": criteria_results,
        "total": total,
        "approved": approved,
        "failed": failed,
        "partial": partial,
        "verdict": verdict,
    }

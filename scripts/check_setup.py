"""Check that your environment is ready for the workshop.

Run from the repository root:

    uv run python scripts/check_setup.py

Every line should say OK. If one does not, the message tells you what to do.
"""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = ["pandas", "numpy", "sklearn", "matplotlib", "pydantic", "joblib", "ipykernel", "pytest"]


def check(label: str, ok: bool, fix: str) -> bool:
    print(f"[{'OK' if ok else 'FAIL'}] {label}" + ("" if ok else f"\n       -> {fix}"))
    return ok


def main() -> int:
    results = [
        check(
            f"Python {sys.version.split()[0]}",
            sys.version_info >= (3, 11),
            "Python 3.11 or newer is needed. Run `uv sync`, uv installs a suitable Python for you.",
        ),
        check(
            "Running inside the project's virtual environment",
            Path(sys.prefix).resolve() == (ROOT / ".venv").resolve(),
            "Start this script with `uv run python scripts/check_setup.py` from the repository root.",
        ),
    ]

    for name in REQUIRED:
        try:
            importlib.import_module(name)
            results.append(check(f"import {name}", True, ""))
        except ImportError:
            results.append(check(f"import {name}", False, "Run `uv sync` in the repository root."))

    try:
        import churn

        results.append(check(f"import churn (reference package {churn.__version__})", True, ""))
    except ImportError:
        results.append(
            check("import churn", False, "Run `uv sync` so the src/ packages get installed.")
        )

    data = ROOT / "data" / "raw" / "telco_churn.csv"
    results.append(
        check(
            "Dataset data/raw/telco_churn.csv",
            data.exists() and data.stat().st_size > 900_000,
            "The file is part of the repository. Run `git status` and `git pull`.",
        )
    )

    if all(results):
        print("\nAll good. Open notebooks/00_warmup_whats_wrong.ipynb and select the .venv kernel.")
        return 0
    print("\nSomething is missing. Fix the FAIL lines above or ask your buddy or the trainer.")
    return 1


if __name__ == "__main__":
    sys.exit(main())

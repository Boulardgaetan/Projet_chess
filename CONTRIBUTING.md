# Contributing to Projet Chess

This repository is a public solo project maintained by its owner and licensed under the **AGPL-3.0**. External contributions are welcome via **Pull Requests** at the maintainer's discretion, provided they respect the project's guidelines and pass all automated checks—though acceptance is not guaranteed.

## License & Dependencies

* This project is distributed under the **GNU Affero General Public License v3.0 (AGPL-3.0)**. By submitting a Pull Request, you agree to license your contribution under the terms of the **AGPL-3.0**.
* All runtime and development dependencies defined in `pyproject.toml` (such as `chess`, `chess-detect`, `pygame`, `numpy`, `pandas`, `matplotlib`, and `scipy`) must remain compatible with the **AGPL-3.0**. If you propose adding a new dependency, verify its license and any bundled components first.

## How to Contribute

1. **Fork the repository** and create a focused branch from `main` (for example, `git switch -c feat/analyser-tests` or `git switch -c fix/opening-book-alignment`).
2. **Set up the development environment** using `pyproject.toml` (Python 3.10+):
   ```bash
   python -m pip install --upgrade pip
   pip install -e ".[dev]"

3. **Make clean, scoped changes** without leaving temporary files, build artifacts, or unrelated edits.
4. **Add or update unit tests** in `tests/` (for example, covering `ChessAnalyser`, `AnalysedGame`, opening book alignment, and Elo calculation behavior).
5. **Run checks locally** before opening a Pull Request:
```bash
ruff check .
ruff format --check .
pytest

```
6. **Open a Pull Request against `main`** with a clear summary of the changes and why they are needed.

## Review & Merge Policy

* Direct pushes to `main` are blocked; all changes must go through a Pull Request.
* Pull Requests must pass the GitHub Actions CI checks (`test-and-lint`: `ruff check`, `ruff format --check`, and `pytest`).
* As the solo maintainer, I review Pull Requests before merging and may request changes or close PRs that do not align with the project's scope, architecture, or licensing rules.

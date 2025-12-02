# Repository Guidelines

## Project Structure & Module Organization
- Core library lives in `tgio/`: `main.py` (Telegram wrapper), `_files.py` (file handling), `_keyboard.py` (keyboard helpers), `__init__.py` (version/exports).
- Packaging is defined in `pyproject.toml` and `setup.py` (dynamic version from `tgio.__version__`).
- Tests in `tests/` (fixtures in `tests/data/`). Examples in `examples/`.
- Build artifacts output to `build/` and `dist/`. Local scripts and entrypoints include `main2.py`.

## Build, Test, and Development Commands
- `make setup` — create venv in `env/`, upgrade pip, install package.
- `make setup-dev` — venv + install `.[dev]` (pytest, pylint, build, twine).
- `make test` — run lint (`pylint`) and unit tests (`pytest`).
- `make release` — clean, build via `python -m build`, upload with `twine` (requires credentials).
- `pip install ".[dev]"` — install package plus dev/test extras if not using Makefile.

## Coding Style & Naming Conventions
- Python 3.9+; prefer type hints. Use standard 4-space indentation.
- Linting via `pylint` with config at `tests/.pylintrc` (invoked by Makefile).
- Inline comments should be minimal and explain non-obvious logic. Keep ASCII only unless needed.
- Module exports: add to `__all__`/`__init__.py` when exposing new public objects.

## Testing Guidelines
- Frameworks: `pytest` and `pytest-asyncio`. Linting is part of `make test`.
- Place tests in `tests/`; name files `test_*.py` and async tests with `pytest.mark.asyncio` where needed.
- Avoid hitting live Telegram APIs; use fixtures/mocks. Keep test assets under `tests/data/`.

## Commit & Pull Request Guidelines
- Commit messages: concise imperative (e.g., “Add send fallback”, “Fix keyboard URL handling”).
- PRs should describe behavior changes, list tests run (`make test`), and mention any breaking changes or new dependencies.
- Include screenshots or logs only when UI/behavioral changes need demonstration (rare for this repo).

## Security & Configuration Tips
- Do not commit real bot tokens; use placeholders in examples/tests. Environment secrets should stay local.
- Release uploads require valid PyPI creds; verify version bump in `tgio/__init__.py` before publishing.

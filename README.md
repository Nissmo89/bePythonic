# bePythonic

Backbone AI to learn Python through a terminal-first workflow.

## Current Scope (v0.1.0)

This first production baseline implements the MVP core loop:

1. Load lesson JSON
2. Show lesson metadata/content
3. Run learner code with timeout
4. Judge output
5. Save local progress

## Install (editable)

```bash
pip install -e .[dev]
```

## Run

```bash
bepythonic start
bepythonic lesson 01_variables
bepythonic progress
bepythonic tui
```

## Test and Quality

```bash
pytest
ruff check .
mypy src
```

## Packaging

```bash
python -m build
```

## Notes

- Lessons live under `src/bepythonic/lessons/`.
- Local progress is stored in `src/bepythonic/data/progress.json` by default.
- AI integration is intentionally deferred until the core learning loop is stable.
# bePythonic

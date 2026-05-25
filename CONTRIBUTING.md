# Contributing

Thanks for helping improve AI Open Lab.

## Development

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
python -m unittest
```

## Pull Request Checklist

- Keep changes focused on one feature or bug fix.
- Add or update tests for behavior changes.
- Update examples or docs when the CLI behavior changes.
- Do not commit secrets, API keys, private prompts, or production logs.

## Code Style

The project currently uses only the Python standard library. Prefer small modules, typed functions, and readable errors.

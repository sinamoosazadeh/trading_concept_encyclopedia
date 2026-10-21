# Contributing

## Before opening a change

1. Check for an existing canonical concept and likely synonyms.
2. Choose the narrowest accurate category.
3. Separate definition, interpretation, hypothesis, and empirical claim.
4. Add sources only when they directly support the cited statement.
5. Record uncertainty, conflicting definitions, and limitations.
6. Update tests when schema or validation behavior changes.

## Local validation

Use Python 3.11 or later. Create a virtual environment, install the development extras, then run:

    python -m pip install -e ".[dev]"
    python -m pytest
    python scripts/validate_registry.py
    python scripts/build_report.py

## Pull request checklist

- [ ] IDs are stable and unique.
- [ ] JSON files validate and referenced IDs resolve.
- [ ] Claims have clear type, scope, and status.
- [ ] Sources are genuine and relevant.
- [ ] Contradictory and negative evidence is not omitted.
- [ ] No claim of profitability is inferred from the concept name.
- [ ] Any changes to schema or lifecycle rules include tests and migration notes.

Do not upload confidential data, API keys, account credentials, or copyrighted source material without authorization. Summarize evidence and cite the source rather than copying large protected passages.

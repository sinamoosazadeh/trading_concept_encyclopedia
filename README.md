# Trading Concept Encyclopedia

An evidence-first, version-controlled reference for trading concepts, price-action terminology, patterns, setups, strategy hypotheses, execution methods, and risk controls.

## Project status

**Stage:** Initial repository scaffold.  
**Important:** A concept's inclusion documents terminology or a hypothesis; it does not establish predictive power or profitability. Entry status and evidence quality must be tracked separately.

## Design principles

- **Evidence before authority:** record sources, claims, disagreements, uncertainty, and context limits.
- **No profitability by naming:** a pattern or setup name is not evidence of an edge.
- **Clear conceptual boundaries:** distinguish observations, descriptive concepts, features, hypotheses, signals, setups, strategies, execution mechanisms, and risk controls.
- **Reproducibility:** stable IDs, version history, explicit schemas, validation, and traceable editorial changes.
- **Statistical integrity:** document look-ahead bias, leakage, survivorship bias, selection bias, multiple testing, transaction costs, slippage, and execution assumptions where relevant.
- **Negative evidence matters:** preserve null results, contradictory findings, failed replications, and limits of generalization.
- **No silent completion claims:** candidate labels, extracted material, reviewed entries, and empirically validated results are different states.

## Repository map

- `docs/` — scope, methodology, evidence policy, editorial standards, QA, and governance.
- `schema/` — machine-readable schemas for concepts, sources, and claims.
- `registry/` — taxonomy, controlled vocabularies, and lifecycle states.
- `entries/` — individual concept records, organized by family.
- `sources/` — source registry and source-ingestion records.
- `scripts/` — deterministic validation and report generation.
- `tests/` — automated tests for validation logic.
- `.github/workflows/` — automated validation in CI.

## Quick start

Python 3.11 or later is recommended.

```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
python -m pip install -e ".[dev]"
python -m pytest
python scripts/validate_registry.py
```

Commands and dependencies will be made authoritative in `pyproject.toml` as the scaffold is completed.

## Entry lifecycle

An entry should move through explicit states such as:

1. `candidate` — a label or idea awaiting disambiguation.
2. `draft` — a structured record exists, but review is incomplete.
3. `needs_sources` — important factual or historical claims need support.
4. `under_review` — editorial or evidence review is in progress.
5. `reviewed` — terminology, scope, sources, and limitations have been checked.
6. `empirically_tested` — a specified test exists with data, protocol, and results recorded.
7. `deprecated` or `merged` — retained history points to the replacement or canonical record.

These states are not a simple quality score. In particular, an entry can be editorially reviewed without being empirically validated.

## Contribution standard

Changes should preserve source provenance, define terms operationally where possible, distinguish fact from interpretation, add tests for validation rules, and never describe a strategy as profitable without appropriately scoped, reproducible evidence.

## Disclaimer

This repository is for research and education. It is not investment advice, and documented concepts are not trading recommendations.

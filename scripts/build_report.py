#!/usr/bin/env python3
"""Build a deterministic inventory and quality-gap report from canonical records."""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from trading_encyclopedia.validation import read_json, validate_repository  # noqa: E402


def load_records(directory: Path) -> tuple[list[tuple[Path, dict[str, Any]]], list[str]]:
    """Load object-valued JSON records and report unreadable/non-object files."""
    records: list[tuple[Path, dict[str, Any]]] = []
    errors: list[str] = []
    if not directory.is_dir():
        return records, [directory.relative_to(ROOT).as_posix()]
    for path in sorted(directory.rglob("*.json")):
        try:
            record = read_json(path)
            if isinstance(record, dict):
                records.append((path, record))
            else:
                errors.append(path.relative_to(ROOT).as_posix())
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            errors.append(path.relative_to(ROOT).as_posix())
    return records, errors


def counts(records: list[tuple[Path, dict[str, Any]]], field: str) -> dict[str, int]:
    tally = Counter(str(record.get(field, "missing")) for _, record in records)
    return dict(sorted(tally.items()))


def get_list(value: Any, key: str) -> list[Any]:
    """Return a list-valued property only; malformed values are handled by validation."""
    if not isinstance(value, dict):
        return []
    candidate = value.get(key, [])
    return candidate if isinstance(candidate, list) else []


def main() -> int:
    concepts, concept_errors = load_records(ROOT / "entries")
    studies, study_errors = load_records(ROOT / "studies")

    source_records: list[dict[str, Any]] = []
    source_registry_error = None
    try:
        registry = read_json(ROOT / "sources" / "registry.json")
        if isinstance(registry, dict) and isinstance(registry.get("sources"), list):
            source_records = [item for item in registry["sources"] if isinstance(item, dict)]
        else:
            source_registry_error = "sources/registry.json"
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        source_registry_error = "sources/registry.json"

    claim_records = [
        claim
        for _, concept in concepts
        for claim in get_list(concept, "claims")
        if isinstance(claim, dict)
    ]
    diagnostics = validate_repository(ROOT)
    diagnostic_counts = Counter(item.severity for item in diagnostics)

    concepts_without_sources = sorted(
        record.get("id", path.relative_to(ROOT).as_posix())
        for path, record in concepts
        if not get_list(record, "sources")
    )
    concepts_without_claims = sorted(
        record.get("id", path.relative_to(ROOT).as_posix())
        for path, record in concepts
        if not get_list(record, "claims")
    )
    predictive_claims_without_refs = sorted(
        f"{record.get('id', path.stem)}:{claim.get('id', 'missing-id')}"
        for path, record in concepts
        for claim in get_list(record, "claims")
        if isinstance(claim, dict)
        and claim.get("type", claim.get("claim_type")) == "predictive"
        and not (get_list(claim, "supporting_source_ids") or get_list(claim, "contrary_source_ids"))
    )
    studies_without_sources = sorted(
        record.get("id", path.relative_to(ROOT).as_posix())
        for path, record in studies
        if not (get_list(record, "source_ids") or get_list(record.get("data"), "source_ids"))
    )

    report = {
        "report_version": "1.2",
        "inventory": {
            "concept_count": len(concepts),
            "source_count": len(source_records),
            "embedded_claim_count": len(claim_records),
            "study_record_count": len(studies),
            "concept_editorial_status_counts": counts(concepts, "editorial_status"),
            "concept_evidence_status_counts": counts(concepts, "evidence_status"),
            "concept_category_counts": counts(concepts, "category"),
            "claim_status_counts": dict(sorted(Counter(str(claim.get("status", "missing")) for claim in claim_records).items())),
            "claim_type_counts": dict(sorted(Counter(str(claim.get("type", claim.get("claim_type", "missing"))) for claim in claim_records).items())),
            "study_status_counts": counts(studies, "study_status"),
            "study_type_counts": counts(studies, "study_type"),
        },
        "coverage_gaps": {
            "concepts_without_sources": concepts_without_sources,
            "concepts_without_claims": concepts_without_claims,
            "predictive_claims_without_source_refs": predictive_claims_without_refs,
            "studies_without_sources": studies_without_sources,
        },
        "integrity": {
            "validation_error_count": diagnostic_counts["error"],
            "validation_warning_count": diagnostic_counts["warning"],
            "validation_info_count": diagnostic_counts["info"],
            "validation_diagnostics": [item.as_dict() for item in diagnostics],
            "unreadable_concept_or_study_files": sorted(concept_errors + study_errors),
            "source_registry_error": source_registry_error,
        },
        "interpretation": (
            "This deterministic snapshot counts checked-in metadata and reports validation diagnostics. "
            "It does not measure domain coverage, source credibility, empirical validity, or strategy profitability."
        ),
    }
    out_path = ROOT / "reports" / "registry_report.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    print(f"Report written to {out_path.relative_to(ROOT)}")
    return 1 if concept_errors or study_errors or source_registry_error or diagnostic_counts["error"] else 0


if __name__ == "__main__":
    raise SystemExit(main())

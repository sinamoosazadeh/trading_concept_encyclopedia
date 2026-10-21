#!/usr/bin/env python3
"""Build a deterministic snapshot of entry statuses and coverage gaps."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    entries_root = ROOT / "entries"
    records = []
    parse_errors = []
    for path in sorted(entries_root.rglob("*.json")):
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(record, dict):
                records.append((path, record))
            else:
                parse_errors.append(str(path.relative_to(ROOT)))
        except (OSError, json.JSONDecodeError):
            parse_errors.append(str(path.relative_to(ROOT)))

    report = {
        "report_version": "1.0",
        "entry_count": len(records),
        "editorial_status_counts": dict(sorted(Counter(r.get("editorial_status", "missing") for _, r in records).items())),
        "evidence_status_counts": dict(sorted(Counter(r.get("evidence_status", "missing") for _, r in records).items())),
        "category_counts": dict(sorted(Counter(r.get("category", "missing") for _, r in records).items())),
        "entries_without_sources": sorted(r.get("id", str(p)) for p, r in records if not r.get("sources")),
        "entries_without_claims": sorted(r.get("id", str(p)) for p, r in records if not r.get("claims")),
        "parse_errors": sorted(parse_errors),
        "interpretation": "Counts describe repository metadata only. They do not measure concept coverage, evidence quality, or strategy profitability."
    }
    out_path = ROOT / "reports" / "registry_report.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print(f"Report written to {out_path.relative_to(ROOT)}")
    return 1 if parse_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Validate concept entries, source references, studies, schemas, and vocabulary contracts."""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from trading_encyclopedia.validation import validate_repository  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="Repository root (default: project root)")
    parser.add_argument("--json", action="store_true", help="Print diagnostics as a JSON array")
    parser.add_argument(
        "--strict-warnings",
        action="store_true",
        help="Return non-zero when warnings are present, as well as when errors are present.",
    )
    args = parser.parse_args()

    diagnostics = validate_repository(args.root.resolve())
    counts = Counter(item.severity for item in diagnostics)
    has_errors = counts["error"] > 0
    has_strict_warnings = args.strict_warnings and counts["warning"] > 0

    if args.json:
        print(
            json.dumps(
                {
                    "summary": {
                        "error_count": counts["error"],
                        "warning_count": counts["warning"],
                        "info_count": counts["info"],
                        "passed": not has_errors and not has_strict_warnings,
                        "strict_warnings": args.strict_warnings,
                    },
                    "diagnostics": [item.as_dict() for item in diagnostics],
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    elif not diagnostics:
        print("Validation passed: no structural, schema, or reference diagnostics were found.")
        print("This does not establish factual accuracy, research quality, completeness, or profitability.")
    else:
        for item in diagnostics:
            print(f"{item.severity.upper()} [{item.code}] {item.path}: {item.message}")
        print(f"Summary: {counts['error']} error(s), {counts['warning']} warning(s), {counts['info']} info item(s).")
        if has_errors:
            print("Result: FAILED because one or more errors were found.")
        elif has_strict_warnings:
            print("Result: FAILED because strict warning mode is enabled.")
        else:
            print("Result: no errors found; review warnings before promotion or release.")

    return 1 if has_errors or has_strict_warnings else 0


if __name__ == "__main__":
    raise SystemExit(main())

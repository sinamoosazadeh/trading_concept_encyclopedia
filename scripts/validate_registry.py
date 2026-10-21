#!/usr/bin/env python3
"""Validate concept entries, source references, and schemas."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from trading_encyclopedia.validation import validate_repository  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="Repository root (default: current project root)")
    parser.add_argument("--json", action="store_true", help="Print diagnostics as JSON")
    args = parser.parse_args()

    diagnostics = validate_repository(args.root.resolve())
    if args.json:
        print(json.dumps([item.as_dict() for item in diagnostics], ensure_ascii=False, indent=2))
    elif not diagnostics:
        print("Validation passed: repository structure is consistent.")
        print("Note: structural validation does not establish factual accuracy or profitability.")
    else:
        for item in diagnostics:
            print(f"{item.severity.upper()} [{item.code}] {item.path}: {item.message}")

    return 1 if any(item.severity == "error" for item in diagnostics) else 0


if __name__ == "__main__":
    raise SystemExit(main())

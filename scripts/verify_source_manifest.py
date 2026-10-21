#!/usr/bin/env python3
"""Verify the preserved source against its checked-in integrity manifest."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "legacy" / "source" / "source_manifest.json"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="Repository root (default: project root)")
    args = parser.parse_args()
    root = args.root.resolve()
    manifest_path = root / "legacy" / "source" / "source_manifest.json"

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot read manifest {manifest_path}: {exc}", file=sys.stderr)
        return 1

    relative_path = manifest.get("repository_path")
    if not isinstance(relative_path, str) or not relative_path:
        print("ERROR: manifest has no valid repository_path.", file=sys.stderr)
        return 1

    source_path = root / relative_path
    try:
        raw = source_path.read_bytes()
        text = raw.decode("utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        print(f"ERROR: cannot read source as UTF-8 ({relative_path}): {exc}", file=sys.stderr)
        return 1

    actual = {
        "sha256": hashlib.sha256(raw).hexdigest(),
        "byte_length": len(raw),
        "unicode_character_count": len(text),
        "line_count": len(text.splitlines()),
    }
    errors = []
    for field, actual_value in actual.items():
        expected_value = manifest.get(field)
        if expected_value != actual_value:
            errors.append(f"{field}: expected {expected_value!r}, actual {actual_value!r}")

    if errors:
        print("Source integrity verification FAILED:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("Source integrity verification PASSED.")
    print(json.dumps(actual, ensure_ascii=False, indent=2, sort_keys=True))
    print("Note: a matching hash proves byte identity with the recorded digest, not the factual accuracy of the source.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from trading_encyclopedia.validation import ID_PATTERN, validate_repository


def test_id_pattern_accepts_canonical_slug():
    assert ID_PATTERN.fullmatch("market-structure-break")


def test_id_pattern_rejects_uppercase_and_spaces():
    assert not ID_PATTERN.fullmatch("Market Structure Break")
    assert not ID_PATTERN.fullmatch("market_structure_break")


def test_initial_repository_is_structurally_valid():
    diagnostics = validate_repository(ROOT)
    errors = [item for item in diagnostics if item.severity == "error"]
    assert errors == [], "\n".join(f"{d.code} {d.path}: {d.message}" for d in errors)


def test_provisional_entry_does_not_claim_empirical_support():
    import json

    entry_path = ROOT / "entries" / "market-structure" / "market-structure-break.json"
    entry = json.loads(entry_path.read_text(encoding="utf-8"))
    assert entry["editorial_status"] == "candidate"
    assert entry["evidence_status"] == "unassessed"

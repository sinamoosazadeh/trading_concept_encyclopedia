from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from trading_encyclopedia.validation import ID_PATTERN, validate_repository  # noqa: E402


def copy_repository(tmp_path: Path) -> Path:
    destination = tmp_path / "repo"
    shutil.copytree(
        ROOT,
        destination,
        ignore=shutil.ignore_patterns(".git", ".venv", "__pycache__", ".pytest_cache", "*.pyc"),
    )
    return destination


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, value) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def diagnostic_codes(root: Path) -> set[str]:
    return {item.code for item in validate_repository(root)}


def diagnostics_by_code(root: Path, code: str):
    return [item for item in validate_repository(root) if item.code == code]


def test_id_pattern_accepts_canonical_slug():
    assert ID_PATTERN.fullmatch("market-structure-break")
    assert ID_PATTERN.fullmatch("rsi")


def test_id_pattern_rejects_uppercase_spaces_and_underscores():
    assert not ID_PATTERN.fullmatch("Market Structure Break")
    assert not ID_PATTERN.fullmatch("market_structure_break")
    assert not ID_PATTERN.fullmatch("market--structure")


def test_initial_repository_has_no_validation_errors():
    diagnostics = validate_repository(ROOT)
    errors = [item for item in diagnostics if item.severity == "error"]
    assert errors == [], "\n".join(f"{d.code} {d.path}: {d.message}" for d in errors)


def test_provisional_entry_does_not_claim_empirical_support():
    entry_path = ROOT / "entries" / "market-structure" / "market-structure-break.json"
    entry = load_json(entry_path)
    assert entry["editorial_status"] == "candidate"
    assert entry["evidence_status"] == "unassessed"


def test_all_schemas_are_loadable_and_schema_self_validation_is_clean():
    diagnostics = validate_repository(ROOT)
    assert "invalid_schema_definition" not in {item.code for item in diagnostics}
    assert "schema_missing" not in {item.code for item in diagnostics}


def test_missing_schema_is_reported(tmp_path):
    root = copy_repository(tmp_path)
    (root / "schema" / "claim.schema.json").unlink()
    diagnostics = validate_repository(root)
    assert any(item.code == "schema_missing" and item.path == "schema/claim.schema.json" for item in diagnostics)


def test_invalid_schema_definition_is_reported(tmp_path):
    root = copy_repository(tmp_path)
    schema_path = root / "schema" / "concept.schema.json"
    schema_path.write_text('{"type": "not-a-json-schema-type"}\n', encoding="utf-8")
    assert "invalid_schema_definition" in diagnostic_codes(root)


def test_duplicate_concept_ids_and_filename_mismatches_are_reported(tmp_path):
    root = copy_repository(tmp_path)
    original = root / "entries" / "market-structure" / "market-structure-break.json"
    duplicate = root / "entries" / "other" / "another-name.json"
    duplicate.parent.mkdir(parents=True)
    duplicate.write_text(original.read_text(encoding="utf-8"), encoding="utf-8")
    codes = diagnostic_codes(root)
    assert "duplicate_concept_id" in codes
    assert "filename_id_mismatch" in codes


def test_unknown_source_reference_is_reported(tmp_path):
    root = copy_repository(tmp_path)
    entry_path = root / "entries" / "market-structure" / "market-structure-break.json"
    entry = load_json(entry_path)
    entry["sources"] = ["source-that-does-not-exist"]
    save_json(entry_path, entry)
    assert "unknown_source_reference" in diagnostic_codes(root)


def test_duplicate_embedded_claim_ids_are_reported(tmp_path):
    root = copy_repository(tmp_path)
    entry_path = root / "entries" / "market-structure" / "market-structure-break.json"
    entry = load_json(entry_path)
    entry["claims"].append(dict(entry["claims"][0]))
    save_json(entry_path, entry)
    assert "duplicate_claim_id" in diagnostic_codes(root)


def test_vocabulary_drift_from_schema_is_reported(tmp_path):
    root = copy_repository(tmp_path)
    vocab_path = root / "registry" / "vocabularies.json"
    vocab = load_json(vocab_path)
    vocab["concept_categories"].remove("other")
    save_json(vocab_path, vocab)
    assert "vocabulary_schema_mismatch" in diagnostic_codes(root)


def test_source_registry_records_are_checked_individually(tmp_path):
    root = copy_repository(tmp_path)
    registry_path = root / "sources" / "registry.json"
    registry = load_json(registry_path)
    registry["sources"] = [{
        "schema_version": "1.0",
        "id": "example-source",
        "title": "Missing required fields",
        "source_type": "other"
    }]
    save_json(registry_path, registry)
    assert "schema_violation" in diagnostic_codes(root)


def test_study_timestamps_must_be_explicit_utc(tmp_path):
    root = copy_repository(tmp_path)
    template = load_json(root / "templates" / "research-study.template.json")
    template["id"] = "test-study"
    template["scope"]["start_date_utc"] = "2026-01-01T00:00:00+02:00"
    template["scope"]["end_date_utc"] = "2026-01-03T00:00:00Z"
    study_path = root / "studies" / "test-study.json"
    save_json(study_path, template)
    assert "study_timestamp_not_utc" in diagnostic_codes(root)


def test_study_end_must_follow_start(tmp_path):
    root = copy_repository(tmp_path)
    study = load_json(root / "templates" / "research-study.template.json")
    study["id"] = "test-study"
    study["scope"]["start_date_utc"] = "2026-01-03T00:00:00Z"
    study["scope"]["end_date_utc"] = "2026-01-01T00:00:00Z"
    save_json(root / "studies" / "test-study.json", study)
    assert "study_date_range_invalid" in diagnostic_codes(root)


def test_unknown_study_source_and_concept_references_are_reported(tmp_path):
    root = copy_repository(tmp_path)
    study = load_json(root / "templates" / "research-study.template.json")
    study["id"] = "test-study"
    study["source_ids"] = ["missing-source"]
    study["related_concept_ids"] = ["missing-concept"]
    save_json(root / "studies" / "test-study.json", study)
    codes = diagnostic_codes(root)
    assert "unknown_study_source_reference" in codes
    assert "unknown_study_concept_reference" in codes


def test_supported_claim_without_source_is_warning_not_silent_success(tmp_path):
    root = copy_repository(tmp_path)
    entry_path = root / "entries" / "market-structure" / "market-structure-break.json"
    entry = load_json(entry_path)
    entry["claims"][0]["status"] = "supported"
    save_json(entry_path, entry)
    found = diagnostics_by_code(root, "supported_claim_without_supporting_source")
    assert found
    assert all(item.severity == "warning" for item in found)


def test_diagnostics_are_deterministically_sorted(tmp_path):
    root = copy_repository(tmp_path)
    entry_path = root / "entries" / "market-structure" / "market-structure-break.json"
    entry = load_json(entry_path)
    entry["sources"] = ["z-missing", "a-missing"]
    save_json(entry_path, entry)
    first = [item.as_dict() for item in validate_repository(root)]
    second = [item.as_dict() for item in validate_repository(root)]
    assert first == second
    assert first == sorted(first, key=lambda item: (
        {"error": 0, "warning": 1, "info": 2}.get(item["severity"], 9),
        item["path"], item["code"], item["message"]
    ))



def test_preserved_source_matches_integrity_manifest():
    import hashlib

    manifest_path = ROOT / "legacy" / "source" / "source_manifest.json"
    manifest = load_json(manifest_path)
    source_path = ROOT / manifest["repository_path"]
    raw = source_path.read_bytes()
    decoded = raw.decode("utf-8")
    assert hashlib.sha256(raw).hexdigest() == manifest["sha256"]
    assert len(raw) == manifest["byte_length"]
    assert len(decoded) == manifest["unicode_character_count"]
    assert len(decoded.splitlines()) == manifest["line_count"]


def test_source_registry_container_schema_and_source_schema_are_separate():
    import json

    container_schema = load_json(ROOT / "schema" / "source-registry.schema.json")
    source_schema = load_json(ROOT / "schema" / "source.schema.json")
    assert container_schema["properties"]["sources"]["type"] == "array"
    assert source_schema["required"]
    assert "source_type" in source_schema["required"]

"""Repository validation with machine-readable diagnostics.

Validation confirms structural consistency, not truth, completeness, or profitability.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError:  # pragma: no cover - exercised in minimal installations
    Draft202012Validator = None
    FormatChecker = None

ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SCHEMA_FILES = {
    "concept": "concept.schema.json",
    "source": "source.schema.json",
    "claim": "claim.schema.json",
}


@dataclass(frozen=True)
class Diagnostic:
    severity: str
    code: str
    path: str
    message: str

    def as_dict(self) -> dict[str, str]:
        return {
            "severity": self.severity,
            "code": self.code,
            "path": self.path,
            "message": self.message,
        }


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as stream:
        return json.load(stream)


def schema_diagnostics(record: Any, schema: dict[str, Any], path: str) -> list[Diagnostic]:
    if Draft202012Validator is None:
        return [
            Diagnostic(
                "error",
                "jsonschema_missing",
                path,
                'Install development dependencies with: python -m pip install -e ".[dev]"',
            )
        ]
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    diagnostics = []
    for error in sorted(validator.iter_errors(record), key=lambda item: list(map(str, item.absolute_path))):
        location = ".".join(str(part) for part in error.absolute_path)
        diagnostics.append(
            Diagnostic(
                "error",
                "schema_violation",
                f"{path}:{location}" if location else path,
                error.message,
            )
        )
    return diagnostics


def iter_json_files(directory: Path) -> list[Path]:
    if not directory.exists():
        return []
    return sorted(path for path in directory.rglob("*.json") if path.is_file())


def validate_repository(root: Path) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    schema_root = root / "schema"
    schemas: dict[str, dict[str, Any]] = {}
    for record_type, filename in SCHEMA_FILES.items():
        schema_path = schema_root / filename
        if not schema_path.exists():
            diagnostics.append(Diagnostic("error", "schema_missing", str(schema_path.relative_to(root)), "Required schema is missing."))
            continue
        try:
            schemas[record_type] = read_json(schema_path)
        except (OSError, json.JSONDecodeError) as exc:
            diagnostics.append(Diagnostic("error", "schema_unreadable", str(schema_path.relative_to(root)), str(exc)))

    concept_paths = iter_json_files(root / "entries")
    source_registry_path = root / "sources" / "registry.json"
    source_ids: set[str] = set()
    if source_registry_path.exists():
        try:
            registry = read_json(source_registry_path)
            for index, source in enumerate(registry.get("sources", [])):
                source_id = source.get("id") if isinstance(source, dict) else None
                if not source_id:
                    diagnostics.append(Diagnostic("error", "source_id_missing", f"sources/registry.json:sources[{index}]", "Source record has no ID."))
                elif source_id in source_ids:
                    diagnostics.append(Diagnostic("error", "duplicate_source_id", "sources/registry.json", f"Duplicate source ID: {source_id}"))
                else:
                    source_ids.add(source_id)
                if isinstance(source, dict) and "source" in schemas:
                    diagnostics.extend(schema_diagnostics(source, schemas["source"], f"sources/registry.json:sources[{index}]"))
        except (OSError, json.JSONDecodeError) as exc:
            diagnostics.append(Diagnostic("error", "source_registry_unreadable", "sources/registry.json", str(exc)))
    else:
        diagnostics.append(Diagnostic("error", "source_registry_missing", "sources/registry.json", "Required source registry is missing."))

    concept_ids: set[str] = set()
    parsed_concepts: list[tuple[Path, dict[str, Any]]] = []
    for path in concept_paths:
        relative = str(path.relative_to(root))
        try:
            record = read_json(path)
        except (OSError, json.JSONDecodeError) as exc:
            diagnostics.append(Diagnostic("error", "invalid_json", relative, str(exc)))
            continue
        if not isinstance(record, dict):
            diagnostics.append(Diagnostic("error", "record_not_object", relative, "Concept record must be a JSON object."))
            continue
        concept_id = record.get("id")
        if not isinstance(concept_id, str) or not ID_PATTERN.fullmatch(concept_id):
            diagnostics.append(Diagnostic("error", "invalid_concept_id", relative, f"Invalid concept ID: {concept_id!r}"))
        elif concept_id in concept_ids:
            diagnostics.append(Diagnostic("error", "duplicate_concept_id", relative, f"Duplicate concept ID: {concept_id}"))
        else:
            concept_ids.add(concept_id)
        if path.stem != concept_id:
            diagnostics.append(Diagnostic("error", "filename_id_mismatch", relative, f"Filename stem {path.stem!r} must match record ID {concept_id!r}."))
        if "concept" in schemas:
            diagnostics.extend(schema_diagnostics(record, schemas["concept"], relative))
        parsed_concepts.append((path, record))

    for path, record in parsed_concepts:
        relative = str(path.relative_to(root))
        for source_id in record.get("sources", []):
            if source_id not in source_ids:
                diagnostics.append(Diagnostic("error", "unknown_source_reference", relative, f"Unknown source ID: {source_id}"))
        for claim in record.get("claims", []):
            if not isinstance(claim, dict):
                continue
            for source_id in claim.get("supporting_source_ids", []) + claim.get("contrary_source_ids", []):
                if source_id not in source_ids:
                    diagnostics.append(Diagnostic("error", "unknown_claim_source_reference", relative, f"Unknown claim source ID: {source_id}"))
        for relation in record.get("related_concepts", []):
            if not isinstance(relation, dict):
                continue
            related_id = relation.get("id")
            if related_id not in concept_ids:
                diagnostics.append(Diagnostic("error", "unknown_related_concept", relative, f"Unknown related concept ID: {related_id}"))
            if related_id == record.get("id"):
                diagnostics.append(Diagnostic("error", "self_relation", relative, "A concept cannot relate to itself."))

    vocab_path = root / "registry" / "vocabularies.json"
    try:
        vocab = read_json(vocab_path)
        if vocab.get("schema_version") != "1.0":
            diagnostics.append(Diagnostic("error", "vocabulary_version", "registry/vocabularies.json", "Expected vocabulary schema_version 1.0."))
    except FileNotFoundError:
        diagnostics.append(Diagnostic("error", "vocabulary_missing", "registry/vocabularies.json", "Controlled vocabularies file is missing."))
    except (OSError, json.JSONDecodeError) as exc:
        diagnostics.append(Diagnostic("error", "vocabulary_unreadable", "registry/vocabularies.json", str(exc)))

    return diagnostics

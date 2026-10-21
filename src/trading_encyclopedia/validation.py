"""Deterministic repository validation with machine-readable diagnostics.

The validator checks structure, reference integrity, and selected editorial guardrails.
A clean run does not establish factual accuracy, evidence quality, or trading profitability.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from jsonschema import Draft202012Validator, FormatChecker
    from jsonschema.exceptions import SchemaError
except ImportError:  # pragma: no cover - dependency is installed in CI
    Draft202012Validator = None
    FormatChecker = None
    SchemaError = Exception  # type: ignore[assignment,misc]

ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SCHEMA_FILES = {
    "concept": "concept.schema.json",
    "source": "source.schema.json",
    "claim": "claim.schema.json",
    "source_registry": "source-registry.schema.json",
    "study": "research-study.schema.json",
}

# Schema paths whose enum is governed by registry/vocabularies.json.
ENUM_BINDINGS: tuple[tuple[str, tuple[str, ...], str], ...] = (
    ("concept", ("properties", "category"), "concept_categories"),
    ("concept", ("properties", "editorial_status"), "editorial_statuses"),
    ("concept", ("properties", "evidence_status"), "evidence_statuses"),
    ("concept", ("properties", "claims", "items", "properties", "type"), "claim_types"),
    ("concept", ("properties", "claims", "items", "properties", "status"), "claim_statuses"),
    ("concept", ("properties", "related_concepts", "items", "properties", "relationship"), "relationship_types"),
    ("source", ("properties", "source_type"), "source_types"),
    ("source", ("properties", "source_level"), "source_levels"),
    ("claim", ("properties", "claim_type"), "claim_types"),
    ("claim", ("properties", "status"), "claim_statuses"),
    ("study", ("properties", "study_status"), "study_statuses"),
    ("study", ("properties", "study_type"), "study_types"),
    ("study", ("$defs", "biasCheck", "properties", "status"), "bias_statuses"),
)


@dataclass(frozen=True)
class Diagnostic:
    """One stable, machine-readable validation finding."""

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
    """Read one UTF-8 JSON document."""
    with path.open("r", encoding="utf-8") as stream:
        return json.load(stream)


def relative_path(path: Path, root: Path) -> str:
    """Return a stable repository-relative path when possible."""
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def get_nested(value: Any, path: tuple[str, ...]) -> Any:
    """Read a nested mapping path, returning None when any segment is absent."""
    current = value
    for part in path:
        if not isinstance(current, dict):
            return None
        current = current.get(part)
    return current


def schema_diagnostics(record: Any, schema: dict[str, Any], path: str) -> list[Diagnostic]:
    """Validate a record against one already-loaded schema."""
    if Draft202012Validator is None or FormatChecker is None:
        return [
            Diagnostic(
                "error",
                "jsonschema_missing",
                path,
                'Install development dependencies with: python -m pip install -e ".[dev]"',
            )
        ]
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    diagnostics: list[Diagnostic] = []
    errors = sorted(
        validator.iter_errors(record),
        key=lambda item: (
            tuple(map(str, item.absolute_path)),
            item.validator or "",
            item.message,
        ),
    )
    for error in errors:
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
    """Return deterministic recursive JSON file list."""
    if not directory.exists():
        return []
    return sorted(path for path in directory.rglob("*.json") if path.is_file())


def _load_schema(
    root: Path,
    record_type: str,
    filename: str,
    diagnostics: list[Diagnostic],
) -> dict[str, Any] | None:
    schema_path = root / "schema" / filename
    rel = relative_path(schema_path, root)
    if not schema_path.is_file():
        diagnostics.append(Diagnostic("error", "schema_missing", rel, "Required schema is missing."))
        return None
    try:
        schema = read_json(schema_path)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        diagnostics.append(Diagnostic("error", "schema_unreadable", rel, str(exc)))
        return None
    if not isinstance(schema, dict):
        diagnostics.append(Diagnostic("error", "schema_not_object", rel, "Schema root must be a JSON object."))
        return None
    if Draft202012Validator is None:
        diagnostics.append(
            Diagnostic(
                "error",
                "jsonschema_missing",
                rel,
                'Install development dependencies with: python -m pip install -e ".[dev]"',
            )
        )
        return None
    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError as exc:
        diagnostics.append(
            Diagnostic("error", "invalid_schema_definition", rel, f"{exc.message} (validator path: {list(exc.absolute_path)})")
        )
        return None
    return schema


def _validate_vocabulary_contracts(
    schemas: dict[str, dict[str, Any]],
    vocab: Any,
    diagnostics: list[Diagnostic],
) -> None:
    if not isinstance(vocab, dict):
        diagnostics.append(
            Diagnostic("error", "vocabulary_not_object", "registry/vocabularies.json", "Vocabulary root must be a JSON object.")
        )
        return
    if vocab.get("schema_version") != "1.0":
        diagnostics.append(
            Diagnostic("error", "vocabulary_version", "registry/vocabularies.json", "Expected vocabulary schema_version 1.0.")
        )
    for key, values in vocab.items():
        if key == "schema_version":
            continue
        if not isinstance(values, list) or any(not isinstance(item, str) or not item for item in values):
            diagnostics.append(
                Diagnostic(
                    "error",
                    "invalid_vocabulary",
                    "registry/vocabularies.json",
                    f"Vocabulary {key!r} must be a list of non-empty strings.",
                )
            )
        elif len(values) != len(set(values)):
            diagnostics.append(
                Diagnostic(
                    "error",
                    "duplicate_vocabulary_value",
                    "registry/vocabularies.json",
                    f"Vocabulary {key!r} contains duplicate values.",
                )
            )
    for schema_name, nested_path, vocabulary_key in ENUM_BINDINGS:
        schema = schemas.get(schema_name)
        if schema is None:
            continue
        schema_values = get_nested(schema, nested_path + ("enum",))
        vocabulary_values = vocab.get(vocabulary_key)
        loc = f"schema/{SCHEMA_FILES[schema_name]}:" + "/".join(nested_path)
        if not isinstance(schema_values, list):
            diagnostics.append(
                Diagnostic("error", "schema_enum_missing", loc, f"Expected enum for vocabulary {vocabulary_key!r}.")
            )
            continue
        if not isinstance(vocabulary_values, list):
            diagnostics.append(
                Diagnostic(
                    "error",
                    "vocabulary_missing",
                    "registry/vocabularies.json",
                    f"Controlled vocabulary {vocabulary_key!r} is missing or malformed.",
                )
            )
            continue
        if set(schema_values) != set(vocabulary_values):
            diagnostics.append(
                Diagnostic(
                    "error",
                    "vocabulary_schema_mismatch",
                    loc,
                    f"Schema enum and vocabulary {vocabulary_key!r} differ. "
                    f"Only in schema={sorted(set(schema_values) - set(vocabulary_values))}; "
                    f"only in vocabulary={sorted(set(vocabulary_values) - set(schema_values))}.",
                )
            )


def _utc_datetime(value: Any) -> datetime | None:
    """Parse a timezone-aware ISO datetime and return it only if its offset is UTC."""
    if not isinstance(value, str) or not value:
        return None
    candidate = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(candidate)
    except ValueError:
        return None
    if parsed.tzinfo is None or parsed.utcoffset() is None or parsed.utcoffset().total_seconds() != 0:
        return None
    return parsed


def validate_repository(root: Path) -> list[Diagnostic]:
    """Validate schemas, records, global identifiers, references, and selected quality rules."""
    root = root.resolve()
    diagnostics: list[Diagnostic] = []
    schemas: dict[str, dict[str, Any]] = {}

    for record_type, filename in SCHEMA_FILES.items():
        schema = _load_schema(root, record_type, filename, diagnostics)
        if schema is not None:
            schemas[record_type] = schema

    vocab_path = root / "registry" / "vocabularies.json"
    vocab: Any = None
    try:
        vocab = read_json(vocab_path)
    except FileNotFoundError:
        diagnostics.append(
            Diagnostic("error", "vocabulary_missing", "registry/vocabularies.json", "Controlled vocabularies file is missing.")
        )
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        diagnostics.append(Diagnostic("error", "vocabulary_unreadable", "registry/vocabularies.json", str(exc)))
    if vocab is not None:
        _validate_vocabulary_contracts(schemas, vocab, diagnostics)

    source_registry_path = root / "sources" / "registry.json"
    source_ids: set[str] = set()
    if not source_registry_path.is_file():
        diagnostics.append(
            Diagnostic("error", "source_registry_missing", "sources/registry.json", "Required source registry is missing.")
        )
    else:
        registry_rel = relative_path(source_registry_path, root)
        try:
            source_registry = read_json(source_registry_path)
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            diagnostics.append(Diagnostic("error", "source_registry_unreadable", registry_rel, str(exc)))
            source_registry = None
        if source_registry is not None:
            if "source_registry" in schemas:
                diagnostics.extend(schema_diagnostics(source_registry, schemas["source_registry"], registry_rel))
            if isinstance(source_registry, dict):
                records = source_registry.get("sources", [])
                if isinstance(records, list):
                    for index, source in enumerate(records):
                        source_path = f"{registry_rel}:sources[{index}]"
                        if not isinstance(source, dict):
                            diagnostics.append(Diagnostic("error", "source_not_object", source_path, "Source record must be a JSON object."))
                            continue
                        source_id = source.get("id")
                        if not isinstance(source_id, str) or not ID_PATTERN.fullmatch(source_id):
                            diagnostics.append(Diagnostic("error", "invalid_source_id", source_path, f"Invalid source ID: {source_id!r}"))
                        elif source_id in source_ids:
                            diagnostics.append(Diagnostic("error", "duplicate_source_id", source_path, f"Duplicate source ID: {source_id}"))
                        else:
                            source_ids.add(source_id)
                        if "source" in schemas:
                            diagnostics.extend(schema_diagnostics(source, schemas["source"], source_path))

    entries_dir = root / "entries"
    if not entries_dir.is_dir():
        diagnostics.append(Diagnostic("error", "entries_dir_missing", "entries", "Canonical entries directory is missing."))
    concept_paths = iter_json_files(entries_dir)
    concept_ids: set[str] = set()
    claim_ids: set[str] = set()
    parsed_concepts: list[tuple[Path, dict[str, Any]]] = []

    for path in concept_paths:
        rel = relative_path(path, root)
        try:
            record = read_json(path)
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            diagnostics.append(Diagnostic("error", "invalid_json", rel, str(exc)))
            continue
        if not isinstance(record, dict):
            diagnostics.append(Diagnostic("error", "record_not_object", rel, "Concept record must be a JSON object."))
            continue
        concept_id = record.get("id")
        if not isinstance(concept_id, str) or not ID_PATTERN.fullmatch(concept_id):
            diagnostics.append(Diagnostic("error", "invalid_concept_id", rel, f"Invalid concept ID: {concept_id!r}"))
        elif concept_id in concept_ids:
            diagnostics.append(Diagnostic("error", "duplicate_concept_id", rel, f"Duplicate concept ID: {concept_id}"))
        else:
            concept_ids.add(concept_id)
        if path.stem != concept_id:
            diagnostics.append(
                Diagnostic("error", "filename_id_mismatch", rel, f"Filename stem {path.stem!r} must match record ID {concept_id!r}.")
            )
        if "concept" in schemas:
            diagnostics.extend(schema_diagnostics(record, schemas["concept"], rel))
        parsed_concepts.append((path, record))

        claims = record.get("claims", [])
        if isinstance(claims, list):
            for index, claim in enumerate(claims):
                if not isinstance(claim, dict):
                    continue
                claim_id = claim.get("id")
                claim_path = f"{rel}:claims[{index}]"
                if not isinstance(claim_id, str) or not ID_PATTERN.fullmatch(claim_id):
                    diagnostics.append(Diagnostic("error", "invalid_claim_id", claim_path, f"Invalid claim ID: {claim_id!r}"))
                elif claim_id in claim_ids:
                    diagnostics.append(Diagnostic("error", "duplicate_claim_id", claim_path, f"Duplicate embedded claim ID: {claim_id}"))
                else:
                    claim_ids.add(claim_id)

    for path, record in parsed_concepts:
        rel = relative_path(path, root)
        for source_id in record.get("sources", []) if isinstance(record.get("sources", []), list) else []:
            if source_id not in source_ids:
                diagnostics.append(Diagnostic("error", "unknown_source_reference", rel, f"Unknown source ID: {source_id}"))
        claims = record.get("claims", [])
        if isinstance(claims, list):
            for index, claim in enumerate(claims):
                if not isinstance(claim, dict):
                    continue
                ref_ids: list[str] = []
                for field in ("supporting_source_ids", "contrary_source_ids"):
                    values = claim.get(field, [])
                    if isinstance(values, list):
                        ref_ids.extend(item for item in values if isinstance(item, str))
                for source_id in ref_ids:
                    if source_id not in source_ids:
                        diagnostics.append(
                            Diagnostic("error", "unknown_claim_source_reference", f"{rel}:claims[{index}]", f"Unknown source ID: {source_id}")
                        )
                if claim.get("status") == "supported" and not claim.get("supporting_source_ids"):
                    diagnostics.append(
                        Diagnostic(
                            "warning",
                            "supported_claim_without_supporting_source",
                            f"{rel}:claims[{index}]",
                            "Claim is marked supported but has no supporting source IDs.",
                        )
                    )
                if claim.get("type", claim.get("claim_type")) == "predictive" and not (
                    claim.get("supporting_source_ids") or claim.get("contrary_source_ids")
                ):
                    diagnostics.append(
                        Diagnostic(
                            "warning",
                            "predictive_claim_without_sources",
                            f"{rel}:claims[{index}]",
                            "Predictive claim has no supporting or contrary source references.",
                        )
                    )
        relations = record.get("related_concepts", [])
        if isinstance(relations, list):
            for relation in relations:
                if not isinstance(relation, dict):
                    continue
                related_id = relation.get("id")
                if related_id not in concept_ids:
                    diagnostics.append(Diagnostic("error", "unknown_related_concept", rel, f"Unknown related concept ID: {related_id}"))
                if related_id == record.get("id"):
                    diagnostics.append(Diagnostic("error", "self_relation", rel, "A concept cannot relate to itself."))
        if record.get("editorial_status") == "reviewed" and not record.get("review_notes"):
            diagnostics.append(
                Diagnostic(
                    "warning",
                    "reviewed_entry_missing_review_notes",
                    rel,
                    "Entry is marked reviewed but review_notes is empty.",
                )
            )

    studies_dir = root / "studies"
    if not studies_dir.is_dir():
        diagnostics.append(Diagnostic("error", "studies_dir_missing", "studies", "Studies directory is missing."))
    study_ids: set[str] = set()
    for path in iter_json_files(studies_dir):
        rel = relative_path(path, root)
        try:
            study = read_json(path)
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            diagnostics.append(Diagnostic("error", "invalid_json", rel, str(exc)))
            continue
        if not isinstance(study, dict):
            diagnostics.append(Diagnostic("error", "study_not_object", rel, "Study record must be a JSON object."))
            continue
        study_id = study.get("id")
        if not isinstance(study_id, str) or not ID_PATTERN.fullmatch(study_id):
            diagnostics.append(Diagnostic("error", "invalid_study_id", rel, f"Invalid study ID: {study_id!r}"))
        elif study_id in study_ids:
            diagnostics.append(Diagnostic("error", "duplicate_study_id", rel, f"Duplicate study ID: {study_id}"))
        else:
            study_ids.add(study_id)
        if path.stem != study_id:
            diagnostics.append(Diagnostic("error", "filename_id_mismatch", rel, f"Filename stem {path.stem!r} must match study ID {study_id!r}."))
        if "study" in schemas:
            diagnostics.extend(schema_diagnostics(study, schemas["study"], rel))
        source_ref_ids: set[str] = set()
        top_source_ids = study.get("source_ids", [])
        data = study.get("data", {})
        data_source_ids = data.get("source_ids", []) if isinstance(data, dict) else []
        for value in (top_source_ids, data_source_ids):
            if isinstance(value, list):
                source_ref_ids.update(item for item in value if isinstance(item, str))
        for source_id in sorted(source_ref_ids):
            if source_id not in source_ids:
                diagnostics.append(Diagnostic("error", "unknown_study_source_reference", rel, f"Unknown source ID: {source_id}"))
        concept_refs = study.get("related_concept_ids", [])
        if isinstance(concept_refs, list):
            for concept_id in concept_refs:
                if concept_id not in concept_ids:
                    diagnostics.append(Diagnostic("error", "unknown_study_concept_reference", rel, f"Unknown concept ID: {concept_id}"))
        scope = study.get("scope", {})
        if isinstance(scope, dict):
            start = scope.get("start_date_utc")
            end = scope.get("end_date_utc")
            for field, value in (("start_date_utc", start), ("end_date_utc", end)):
                if value is not None and _utc_datetime(value) is None:
                    diagnostics.append(
                        Diagnostic("error", "study_timestamp_not_utc", f"{rel}:scope.{field}", "Timestamp must be ISO 8601 with an explicit UTC offset (Z or +00:00).")
                    )
            if start is not None and end is not None:
                start_dt, end_dt = _utc_datetime(start), _utc_datetime(end)
                if start_dt and end_dt and end_dt <= start_dt:
                    diagnostics.append(
                        Diagnostic("error", "study_date_range_invalid", rel, "end_date_utc must be later than start_date_utc.")
                    )
        if study.get("study_status") == "completed":
            reproducibility = study.get("reproducibility", {})
            if isinstance(reproducibility, dict) and not reproducibility.get("code_revision"):
                diagnostics.append(
                    Diagnostic("warning", "completed_study_missing_code_revision", rel, "Completed study has no code revision recorded.")
                )

    diagnostics.sort(key=lambda item: ({"error": 0, "warning": 1, "info": 2}.get(item.severity, 9), item.path, item.code, item.message))
    return diagnostics

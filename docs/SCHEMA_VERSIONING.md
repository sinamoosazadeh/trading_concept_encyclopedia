# Schema versioning and migration discipline

## Goals

The schema must evolve without silently corrupting meaning, invalidating IDs, or overstating historical comparability.

## Compatibility classes

- **Patch-level change:** correction to documentation or validation wording that does not alter accepted record shape or interpretation.
- **Minor-level change:** backward-compatible addition of an optional field, enum expansion, or additive report field, with defaults and migration guidance where needed.
- **Major-level change:** removal or rename of a required field, incompatible type change, changed field semantics, or a vocabulary change that could reinterpret existing data.

This policy is a project convention; it does not override any formal versioning standard for a released software package.

## Migration requirements

Every breaking schema change must include:
1. rationale and affected fields;
2. a versioned migration script or an explicitly documented manual procedure;
3. pre-migration and post-migration validation;
4. preservation of IDs and source references when possible;
5. before/after examples;
6. tests covering valid, invalid, and edge-case records;
7. a rollback or recovery note;
8. changelog and release notes.

## Avoiding silent semantic changes

Do not change a field's meaning while keeping the same schema version merely because the JSON type remains unchanged. If an editorial status or evidence label changes semantics, document it as a migration. Historical reports should state which schema/vocabulary version they used.

## IDs and references

IDs should be stable and independent of filenames for display labels. A file path may move while preserving the record ID only if tooling supports it. A renamed or merged concept must provide a replacement or migration mapping. Never reuse a retired ID for a different meaning.

## Deprecation

A deprecated field or enum should have a documented replacement, reason, and removal target release. Where possible, a transition period should accept both old and new representations while emitting warnings. Removal should occur only after migration and validation of repository-wide references.

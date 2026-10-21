# Legacy knowledge material and migration boundaries

This directory preserves the prior Persian encyclopedia source and the imported reference material without falsely elevating historical text into evidence-reviewed canonical entries.

## Preservation rule

`source/ORIGINAL_SOURCE_FA.md` is retained byte-for-byte as UTF-8 text. Its SHA-256 digest, byte length, Unicode character count, and line count are recorded in `source/source_manifest.json`. The digest must be checked by `python scripts/verify_source_manifest.py`.

## How to interpret the source

- The preserved file is the **original source artifact**, not an assertion that every statement in it is accurate or that its concept list is exhaustive.
- A heading, label, definition, formula, practitioner explanation, or citation string in the source does not automatically become a reviewed canonical record.
- Source references such as `[S1]` in the preserved source must be resolved through an auditable citation workflow before a claim is promoted.
- Extracted blocks and candidate inventories, when imported, must retain their legacy IDs and provenance so they can be reconciled without silent data loss.
- Candidate counts describe inventory work, not the number of completed or empirically validated concepts.

## Migration policy

Migrate from the source into `entries/` only when the concept is identified, classified, deduplicated, and represented under the current schema. Preserve the original wording and line reference in migration metadata when allowed; do not overwrite the original. Every migration should state whether it is a transcription, normalization, translation, merge, split, or substantive rewrite. Unresolved claims and missing sources remain visible as open work.

## Rights and responsibility

The original source and the repository's new tooling can have different reuse conditions. See `docs/LICENSE_AND_DATA_POLICY.md`. Do not infer a license from public visibility alone.

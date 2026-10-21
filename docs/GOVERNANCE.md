# Governance

## Status dimensions

Editorial lifecycle and evidence status must be represented independently. An entry may be in draft while its claims are unreviewed, or editorially reviewed while empirical support is absent.

Suggested editorial states: candidate, draft, needs_sources, under_review, reviewed, deprecated, merged.

Suggested evidence states: unassessed, descriptive_only, mixed, empirical_support, empirical_null, contested, insufficient_evidence.

These labels are not a ranking of commercial usefulness and must not be collapsed into a single score.

## IDs and migrations

Canonical IDs are lowercase ASCII slugs. Once published, IDs should remain stable. Renames change the display name, not the ID, unless the original ID is misleading or harmful. ID changes require an explicit migration map and references updated in the same change.

## Reviews

Changes to schemas, evidence policy, lifecycle vocabularies, or automated validation need an explanation and tests. Empirical claims need an evidence review separate from code review. Where possible, the author of a strong performance claim should not be the sole reviewer of its evidence.

## Versioning

Use semantic versioning for schema and tooling releases where compatibility is meaningful. Record entry changes in version control and in entry-level change logs. A release is not a certification that a strategy is profitable.

## Incomplete records

Candidate entries may exist in an explicitly provisional state. They must not be presented in reports as reviewed or empirically supported. Completeness metrics should be calculated from machine-readable fields, not editorial intuition.

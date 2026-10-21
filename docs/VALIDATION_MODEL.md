# Validation model

## Validation layers

1. **Parse:** each input file is valid UTF-8 JSON and has the expected container type.
2. **Schema self-validation:** every schema itself is valid against the declared JSON Schema draft.
3. **Record validation:** concepts, sources, claims, studies, and registries satisfy their relevant schema.
4. **Identity integrity:** IDs are present, syntactically valid, unique in their namespaces, and consistent with file naming where required.
5. **Reference integrity:** source, claim, study, and concept references resolve to the intended namespace.
6. **Vocabulary integrity:** schema enum values and controlled vocabularies are consistent; every enum-bearing property is constrained to the canonical vocabulary.
7. **Semantic warnings:** likely quality gaps are surfaced separately from hard structural errors, such as a reviewed entry with no review notes or a predictive claim with no source references.
8. **Report reproducibility:** derived reports are generated deterministically from checked-in canonical inputs.

## Error and warning policy

- **Error:** the repository cannot safely treat the record as structurally or referentially consistent.
- **Warning:** the record is syntactically valid but contains an editorial or evidence gap requiring judgement.
- **Informational:** useful inventory or context that is not itself a quality verdict.

A warning must not be silently promoted to proof that the record is wrong. Conversely, a clean validation run must not be described as an evidence review.

## Diagnostic contract

Each diagnostic includes severity, stable code, repository-relative path, and message. Stable codes should be preferred over parsing human-readable messages in downstream tools. Where relevant, include a JSON path to the field; avoid including secrets or full record bodies in logs.

## Failure behavior

The CLI returns a non-zero status when any error is found. Warnings are printed and optionally cause a non-zero result only when an explicit strict mode is enabled. JSON diagnostics must be deterministic in ordering to support automation and diffing.

## Testing requirements

Tests should include:
- valid minimal and representative records;
- malformed JSON;
- missing schema files and invalid schema definitions;
- duplicate IDs and file/ID mismatches;
- unknown and self references;
- bad enum values and mismatch between schema and controlled vocabularies;
- malformed source registry containers;
- studies with incomplete bias reviews;
- stable diagnostic ordering and CLI exit codes;
- no false claim that validation establishes empirical support.

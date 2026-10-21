# Empirical studies

Each JSON file under this directory is a study record validated by `schema/research-study.schema.json`.

A study can be a proposal, preregistered protocol, exploratory analysis, confirmatory evaluation, replication, robustness test, or execution analysis. Do not put unsourced narrative claims in this directory as if they were executed tests.

## Rules

- Create one stable lowercase-hyphenated ID per study; the filename stem must equal the ID.
- Define a falsifiable hypothesis, a null or competing hypothesis, primary outcome, and failure criterion.
- Document UTC event-time policy, venue and instrument selection, source IDs, snapshot identity, and data rights.
- Record all key biases, including look-ahead, leakage, survivorship, selection, multiple testing, and execution realism.
- Preserve negative results and deviations from the original protocol.
- An empty or proposal-only studies directory is not evidence of validation.

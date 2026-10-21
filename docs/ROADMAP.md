# Project roadmap

This roadmap is a set of gates, not a claim that work has been completed. Each milestone should be closed only with verifiable repository artifacts and recorded results.

## Phase 0 — Repository foundation

**Goal:** establish identity, scope, repository hygiene, schemas, and basic tooling.

Exit criteria:
- [ ] scope, ontology, evidence, contribution, licensing, and security policies reviewed;
- [ ] schemas validate under the declared JSON Schema draft;
- [ ] canonical IDs and local references are checked;
- [ ] test suite and CI run are observed and their result recorded;
- [ ] project license decision is documented before encouraging reuse.

## Phase 1 — Data integrity and content lifecycle

**Goal:** enforce a reliable editorial workflow.

Exit criteria:
- [ ] validator checks all required schema files and schema self-validity;
- [ ] source registry and vocabularies are structurally validated;
- [ ] duplicate concept/source/claim IDs and broken references are detected;
- [ ] test fixtures cover valid and deliberately invalid records;
- [ ] report differentiates inventory counts from reviewed coverage;
- [ ] schema changes use migration notes and tests.

## Phase 2 — Taxonomy and terminology corpus

**Goal:** build a deduplicated, navigable concept inventory.

Exit criteria:
- [ ] taxonomy categories have definitions and inclusion/exclusion rules;
- [ ] candidate concepts are kept separate from reviewed entries;
- [ ] aliases, regional names, homonyms, and translations are traceable;
- [ ] a merge/redirect policy is implemented;
- [ ] no candidate count is presented as completed evidence-reviewed coverage.

## Phase 3 — Evidence review and source registry

**Goal:** link claims to traceable source evidence.

Exit criteria:
- [ ] source registry has a consistent source schema;
- [ ] every reviewed material claim has relevant source references;
- [ ] contradictory sources and null findings are represented;
- [ ] source quality dimensions are recorded independently;
- [ ] copyright, licenses, and data rights are respected.

## Phase 4 — Reproducible empirical studies

**Goal:** create a reusable study-record format and protocol for performance claims.

Exit criteria:
- [ ] research question and primary metrics are prespecified;
- [ ] datasets and code revisions are traceable;
- [ ] time boundaries and leakage controls are explicit;
- [ ] costs and execution assumptions are documented;
- [ ] out-of-sample, robustness, and negative results are reported;
- [ ] no claim exceeds tested scope.

## Phase 5 — Discovery and publication

**Goal:** publish useful, reviewable views without losing canonical traceability.

Exit criteria:
- [ ] deterministic exports or indexes link back to canonical entry IDs;
- [ ] coverage reports state what is not reviewed;
- [ ] releases include schema version, known gaps, and migration notes;
- [ ] publication and reuse rights are explicit;
- [ ] accessibility and Persian/English terminology quality are reviewed.

## Continuous improvement

Quality priorities are: correctness and traceability first; data integrity and reproducibility second; breadth third; presentation and convenience after the preceding gates. Complexity must earn its maintenance cost.

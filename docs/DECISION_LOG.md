# Architecture decision log

This log records material decisions and their rationale. Revisit an accepted decision when constraints change; do not rewrite history as though the original trade-off never existed.

## ADR-001 — Canonical records are version-controlled JSON

**Status:** Accepted  
**Decision:** Store canonical concept records as UTF-8 JSON and validate them with JSON Schema.  
**Context:** Records need diffable history, predictable shape, language-neutral parsing, and tooling support.  
**Trade-offs:** JSON is strict and machine-friendly but less convenient for long-form prose. Long editorial guidance remains in Markdown.  
**Review trigger:** Record size or editing friction becomes high enough to justify a new canonical format.

## ADR-002 — Editorial status and evidence status are separate

**Status:** Accepted  
**Decision:** Track editorial lifecycle separately from evidence maturity.  
**Context:** A definition may be well reviewed without empirical testing; a test may be reproducible while its conclusion remains uncertain.  
**Trade-offs:** Reporting requires multiple dimensions but avoids a misleading single quality rank.

## ADR-003 — Validation must not imply truth or profitability

**Status:** Accepted  
**Decision:** Automated checks report structural and referential integrity only.  
**Context:** Schemas cannot verify source credibility, causal identification, or generalizable trading edge.  
**Trade-offs:** Human review remains necessary and is more expensive, but avoids false assurance.

## ADR-004 — No explicit repository license is selected yet

**Status:** Open decision  
**Decision:** Do not add a license file before the owner chooses scope and terms.  
**Context:** The repository may contain original code, text, third-party sources, and derived research artifacts with different rights.  
**Consequence:** Do not advertise the current repository as freely reusable under a selected open-source or content license.  
**Review trigger:** Before accepting external contributions or making the first public release.

## ADR-005 — Keep the initial tooling dependency-light

**Status:** Accepted  
**Decision:** Use Python and JSON Schema validation before adopting databases, a search index, or a web application.  
**Context:** The primary immediate need is reliable content structure and reviewable quality gates.  
**Trade-offs:** Advanced discovery interfaces are postponed until corpus size and usage justify them.

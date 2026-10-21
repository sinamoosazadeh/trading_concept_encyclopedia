# Quality gates

## Structural checks

- all entry and source records parse as UTF-8 JSON;
- every record validates against its current JSON Schema;
- concept IDs are unique and match the ID convention;
- referenced source and related-concept IDs resolve or are explicitly marked as external/unregistered;
- controlled-vocabulary values are valid;
- required provenance and change-log fields exist;
- no accidental duplicate canonical records are introduced.

## Editorial checks

- definition is separable from performance claims;
- ambiguity and known synonyms are documented;
- claims are atomic, scoped, and supported by relevant sources;
- material disagreement and uncertainty are disclosed;
- operational rules can be reproduced, or discretionary parts are named;
- entry status does not overstate the evidence.

## Research checks for performance claims

- data provenance and date boundaries are disclosed;
- leakage, look-ahead, selection bias, and multiple testing are evaluated;
- transaction costs and executable fills are considered;
- baselines, sample sizes, uncertainty, and negative results are reported;
- out-of-sample and robustness evidence is distinguished from in-sample selection.

## Release rule

Passing automated validation establishes structural consistency, not truth, completeness, or profitability. Human evidence review remains required. Release notes should state coverage changes, known gaps, and any schema migrations.

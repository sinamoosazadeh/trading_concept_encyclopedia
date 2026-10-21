# Research methodology

## Evidence-first workflow

1. Capture a candidate label and provenance.
2. Disambiguate synonyms, homonyms, regional usage, and conflicting definitions.
3. Write a neutral definition before evaluating trading value.
4. Operationalize any claimed rule: inputs, timing, thresholds, market, timeframe, and edge cases.
5. Register each material claim separately from the term definition.
6. Attach sources and record their type, date, relevance, and limitations.
7. Search for contradictory results, null findings, and alternative explanations.
8. Review for ambiguity, look-ahead risk, and hidden discretionary choices.
9. Validate schema, references, identifiers, and repository tests.
10. Assign an editorial lifecycle status and record the rationale.

## Empirical testing requirements

An empirical claim should identify, where applicable:

- instrument universe, venue, market type, timeframe, and sample dates;
- source and quality of data, timestamp conventions, missing-data treatment, and adjustments;
- exact signal and outcome definitions, including decision timing;
- training, validation, and out-of-sample boundaries;
- fees, spread, slippage, funding, latency, partial fills, and market impact assumptions as relevant;
- benchmark, sample size, uncertainty intervals, and relevant baseline comparisons;
- parameter-search space, number of trials, selection procedure, and multiple-testing controls;
- robustness checks across periods, instruments, and plausible execution assumptions;
- code, configuration, data lineage, and seeds where reproducibility is possible.

A backtest can be useful evidence without being conclusive evidence. A single attractive result cannot establish general profitability.

## Bias controls

Review every empirical workflow for look-ahead bias, target leakage, survivorship and selection bias, data snooping, repeated parameter search, regime dependence, non-stationarity, and unrealistic fills. If a risk is not relevant, explain why rather than omitting it silently.

## Evidence vocabulary

Use the controlled vocabularies in registry/vocabularies.json. Evidence status and editorial status are separate dimensions. A carefully reviewed descriptive definition can have no empirical validation; an empirical result can remain uncertain or contested.

## Negative findings

Preserve null or adverse results with their protocol and limitations. Do not delete inconvenient results merely because a hypothesis was not supported. Corrections should append or amend history transparently.

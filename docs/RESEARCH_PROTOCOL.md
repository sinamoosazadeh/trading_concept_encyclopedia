# Empirical research protocol

## Purpose

This protocol governs any claim that a concept, feature, signal, setup, strategy, or execution method has a measurable effect. It is designed to reduce hindsight selection, data leakage, overfitting, and claims that exceed the evidence.

## Stage 0 — State the question before testing

Record the hypothesis, counter-hypothesis, intended use, target population, asset/venue/timeframe scope, decision horizon, target outcome, primary metric, baseline, material exclusions, and what result would count as failure. Separate exploration from confirmatory evaluation. Log any change made after inspecting results.

## Stage 1 — Define the object of study

Write a deterministic rule or explicitly identify discretionary inputs. Specify:
- event timestamp and information available at that moment;
- entry/exit and labeling logic;
- windows, thresholds, parameters, warm-up, and reset rules;
- handling of overlapping events and duplicate signals;
- missing observations, abnormal candles, venue outages, and symbol changes;
- whether the concept can be identified in real time without future bars.

A retrospectively visible pattern is not automatically a tradable real-time signal.

## Stage 2 — Data contract and provenance

Register the data source, market, instrument identifiers, venue, timezone, interval, collection method, extraction timestamp, coverage, known gaps, duplicate policy, schema, revision policy, and hash or immutable snapshot identifier where possible. Use explicit UTC timestamps for event chronology. Distinguish exchange event time, local collection time, and processing time.

Do not silently join instruments or venues with incompatible contracts, quote units, timestamps, or trading rules. Record symbol lifecycle, delistings, contract changes, and funding rules where relevant.

## Stage 3 — Leakage and bias review

Assess at minimum:
- **Look-ahead bias:** future observations or retrospectively confirmed features used as if available at decision time.
- **Target leakage:** target-derived information included in predictors or transformations.
- **Survivorship bias:** excluding failed, delisted, or otherwise absent instruments.
- **Selection bias:** selecting examples, assets, time periods, or contexts because they look successful.
- **Data snooping and multiple testing:** trying many hypotheses, variants, thresholds, and parameter combinations without accounting for selection.
- **Label leakage and overlapping samples:** training/test observations share information or outcome horizons.
- **Regime dependence:** observed behavior may be concentrated in a specific market state or period.
- **Execution optimism:** fills, latency, liquidity, costs, funding, spread, and market impact are unrealistically favorable.
- **Publication and reporting bias:** only attractive outcomes are retained.

Document each risk, mitigation, residual uncertainty, and why an item is not applicable when excluded.

## Stage 4 — Evaluation design

Prespecify chronological train, validation, and out-of-sample windows as appropriate. Keep final holdout data untouched during design decisions. For time-dependent systems, random shuffling is not an acceptable default substitute for chronological evaluation. Use walk-forward or rolling-origin evaluation where it matches the intended deployment process. Purge or embargo overlapping outcomes when needed.

Compare against meaningful baselines, including simple rules or no-trade baselines. Report sample counts, exposure, turnover, uncertainty, and failures, not only a headline score.

## Stage 5 — Performance and risk

Choose metrics aligned with the question. Depending on the study, report returns after realistic costs, drawdown, tail losses, volatility, risk-adjusted metrics, hit rate with denominator, average win/loss, expectancy, exposure, turnover, trade duration, concentration, and sensitivity to cost assumptions. State the return frequency, annualization assumptions, leverage convention, and handling of open positions.

Avoid treating a high hit rate, a visually clean chart, a high in-sample Sharpe ratio, or one profitable parameter set as sufficient evidence. Include uncertainty intervals or other uncertainty summaries when suitable. Do not compare metrics with incompatible definitions.

## Stage 6 — Robustness and negative findings

Test sensitivity to reasonable parameter perturbations, neighboring periods, instruments, market regimes, fee/slippage assumptions, and implementation variants. Avoid choosing robustness dimensions after observing which ones preserve the preferred outcome without disclosing the selection. Record negative and null findings in the same registry as positive findings.

## Stage 7 — Reproducibility package

Where legally and practically possible, record:
- protocol and its version;
- data snapshot identifier or cryptographic hash;
- code revision and dependency versions;
- configuration and parameter search space;
- random seed and nondeterminism notes;
- commands to reproduce;
- metrics, diagnostics, and machine-readable results;
- deviations from preregistration and reason.

If raw data cannot be redistributed, record access instructions and a reproducibility limitation rather than implying that the result is fully independently reproducible.

## Stage 8 — Claim wording

Claims must match the test population and method. Prefer “in this sample, under this protocol and cost model...” to universal language. Distinguish exploratory, replicated, out-of-sample, paper-traded, and live evidence. Each has different limitations; none guarantees future results.

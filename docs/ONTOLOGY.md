# Concept ontology

## Why an ontology is needed

Trading vocabulary often overloads a single word across descriptive observation, visual pattern, indicator, market hypothesis, trading rule, and performance claim. The ontology prevents a name from silently standing in for a precise definition or a verified edge.

## Core entity types

### Descriptive market phenomenon

A label for an observable price, volume, order-flow, or market-structure configuration. It describes what is observed; it does not prescribe action.

### Pattern

A configuration of observations over a defined interval. A visual pattern must be operationalized sufficiently to determine when it starts, when it is complete, how it is recognized, and when it is invalidated. If the definition depends on retrospective visual judgement, the discretionary component must be explicit.

### Indicator

A calculation that transforms historical or current inputs into a value or series. Record inputs, formula, parameters, initialization, warm-up behavior, missing-data policy, and whether the value is revised after new data arrives. Indicator status does not imply predictive validity.

### Feature

A model or rule input, usually represented as a numeric, categorical, or boolean value. A feature specification requires an information-availability timestamp and reproducible computation. Features are not necessarily signals.

### Hypothesis

A falsifiable statement about occurrence, behavior, conditional distribution, or outcomes. A useful hypothesis defines the population and context where it could be tested and the evidence that would count against it.

### Signal

A rule that maps information available at a decision time to an output such as direction, event, probability, or no-action. It must specify decision timing and treatment of unavailable or revised data.

### Setup

A defined market condition used to identify a possible trade opportunity. The setup may be discretionary or mechanical; the distinction must be stated. A setup need not specify full position sizing and order execution.

### Strategy

A decision policy covering the relevant entry, exit, sizing, position, and no-trade behavior. A strategy record needs enough detail to reproduce the decisions and evaluate costs and risk. A strategy label alone is not an implementation.

### Execution method

A policy for translating intent into orders and fills. Capture order types, timing, urgency, constraints, failure modes, and assumptions about spread, fees, slippage, latency, partial fills, and market impact when relevant.

### Risk or portfolio control

A rule to manage exposure, concentration, leverage, drawdown, liquidity, operational loss, or related hazards. State whether the control is pre-trade, in-trade, post-trade, portfolio-level, or system-level and whether it is a hard constraint or a configurable policy.

### Evidence record

A claim or study linked to source material, protocol, data lineage, scope, uncertainty, and findings. A source that defines a pattern does not by itself prove that the pattern predicts outcomes.

## Relationship semantics

- `synonym`: same intended meaning in a named context; language or regional variation should be noted.
- `broader_than`: the target concept is broader than the current concept. Use consistently and avoid reciprocal contradictions.
- `narrower_than`: the current concept is narrower than the target.
- `prerequisite_for`: the target is a prerequisite to understanding or applying the current concept; explain whether conceptual or operational.
- `alternative_to`: competing or substitutable methods, not necessarily equivalent.
- `often_confused_with`: similar wording or appearance but materially different meaning.
- `implemented_as`: one concept has a concrete implementation represented by the target; include version and assumptions if relevant.
- `related_to`: use only when a more specific relationship does not fit, and provide a rationale.

Directional semantics should be tested and documented. Do not assume a relation graph is symmetric.

## Boundary tests for a new record

Before adding a concept, ask:

1. Is it a genuinely distinct meaning, or just an alias?
2. Is it an observation, computation, hypothesis, decision rule, complete strategy, or execution mechanism?
3. What is the smallest unambiguous definition?
4. Which parts are objective and which require analyst discretion?
5. What data is available at the actual decision time?
6. Is a performance claim being smuggled into a descriptive definition?
7. Should the new record be a separate concept, an implementation, an alternative, or a related term?

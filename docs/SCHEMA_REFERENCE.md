# Schema reference

All schemas use JSON Schema Draft 2020-12. Schema changes must include tests and migration notes where backward compatibility is affected.

| Record | Schema | Canonical location |
|---|---|---|
| Concept | `schema/concept.schema.json` | `entries/**/*.json` |
| Source | `schema/source.schema.json` | `sources/registry.json` `sources[].` |
| Source registry container | `schema/source-registry.schema.json` | `sources/registry.json` |
| Claim (standalone contract for future use) | `schema/claim.schema.json` | Currently embedded in concept records |
| Empirical study | `schema/research-study.schema.json` | `studies/**/*.json` |

## Important distinctions

- The source-registry schema validates the container shape. Each source record is then validated independently against the source schema.
- A standalone claim schema is defined for possible future normalization; current canonical claims live inside concept entries. The validator still enforces global claim-ID uniqueness for embedded claims.
- Schema validity does not establish source authenticity, empirical correctness, or a trading edge.

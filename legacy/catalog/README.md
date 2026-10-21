# Legacy entry inventory

`legacy_entry_inventory.jsonl` contains 288 numbered level-3 entry blocks extracted from `legacy/source/ORIGINAL_SOURCE_FA.md`. The records preserve their legacy IDs, the nearest preceding level-2 section, the heading text, the 1-indexed source line, and the extracted block content.

## Reproducibility and integrity

Run:

```bash
python scripts/extract_legacy_catalog.py --check
```

The extraction logic mirrors the audited legacy extraction rule and block boundaries. It verifies the source file against the source manifest and verifies the generated JSONL against the inventory manifest. To intentionally regenerate the checked-in inventory, use `--write`; a source or output digest change should be reviewed and the manifest updated deliberately.

## Boundary rules

- A numbered level-3 heading is recognized by the Python Unicode-aware expression `^###\s+\d+\s*[.)]`.
- The current block closes before the next level-2 heading or any other level-3 heading.
- The block content is right-trimmed after extraction, matching the audited legacy transformation.
- Source line numbers refer to the preserved original source and are 1-indexed.

## Editorial status

These are legacy extracts, not current canonical entries. They are immutable migration input until reviewed. Do not promote them automatically, because one source block can contain multiple concepts, definitions may be under-specified, and references may be unresolved. The original source remains the authority for source-level preservation.

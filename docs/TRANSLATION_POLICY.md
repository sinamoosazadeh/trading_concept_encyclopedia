# Multilingual terminology and translation policy

## Principle

A translation is a representation of a concept, not proof that two terms are semantically identical. The canonical concept identity should survive spelling, language, regional usage, and translation changes.

## Canonical identity

Each concept uses a stable machine ID independent of its display name. The current schema supports language metadata and aliases; as multilingual coverage grows, localized names and definitions may be promoted into a structured field or linked translation record through a versioned schema migration. Do not improvise incompatible fields in individual entries.

## Translation review

For each translated label or definition:
- retain the source language and original term;
- distinguish direct translation, common equivalent, transliteration, and approximate counterpart;
- identify geography, market community, school, or context where usage differs;
- note when no exact equivalent is known;
- do not strengthen probabilistic or disputed source wording;
- have a bilingual reviewer check meaning, not merely grammar, when the entry is promoted to reviewed status.

## Persian and English terminology

English aliases should not automatically be treated as universal canonical terms. Persian translations should preserve technical distinctions and disclose borrowed vocabulary, transliteration alternatives, and competing local usage. If two Persian terms differ in practitioner usage, record the difference rather than flattening them into synonyms.

## Machine processing

Machine-generated translations may be used as drafts, not as independently reviewed translations. Store the original source reference and translation-review status. Search indexes and glossary exports should include aliases but must resolve to one canonical ID.

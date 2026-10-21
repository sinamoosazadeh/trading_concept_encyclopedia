# Security policy

## Scope

This policy covers repository contents, validation scripts, automation, data ingestion, dependencies, and research artifacts. The project does not currently accept private credentials or operational trading secrets as data.

## Sensitive data

Never commit:
- exchange API keys, bot tokens, passwords, or private keys;
- personal identifiers or private account material;
- non-public datasets that the contributor is not authorized to disclose;
- credential-bearing URLs or unredacted environment files.

Use placeholders in examples. Keep credentials outside version control and restrict API permissions to the minimum required by the relevant workflow.

## Dependency and automation hygiene

- Minimize dependencies and justify additions.
- Pin or constrain versions where reproducibility or security requires it.
- Review dependency changes before release.
- Keep CI permissions least-privilege; content validation normally needs read-only repository permissions.
- Do not execute downloaded scripts or source-ingestion artifacts automatically without review.
- Avoid workflows that expose secrets to untrusted pull requests.
- Review third-party GitHub Actions and update references through a controlled process.

## Reporting

For accidental disclosure, revoke or rotate affected credentials first, then remove exposure and review repository history. Deleting a file in a later commit does not invalidate a leaked credential or erase earlier history. For vulnerabilities in project code, contact the repository owner privately rather than publishing exploitable details in an issue.

## Known limitation

A public repository and CI workflow are not a security certification. The project must avoid implying that the absence of detected secrets is a proof that no sensitive data exists.

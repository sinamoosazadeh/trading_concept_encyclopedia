# Licensing and research data handling policy

## Current status

The repository has not yet selected an explicit license for its original code and documentation. Public visibility on a hosting platform must not be presented as an explicit grant to reuse, redistribute, or sublicense all repository contents. A license decision is a release gate before encouraging external contributions or reuse.

## Third-party materials

Before committing third-party text, diagrams, datasets, code, or other assets, establish the applicable license and permitted uses. Record attribution and license metadata where required. Do not copy paid course materials, entire books, proprietary reports, large copyrighted passages, or restricted market datasets into the repository without authorization.

## Market data

For each dataset or derived result, record provider, venue, instrument coverage, period, collection method, terms or restrictions, timezone, schema, gaps, revision policy, and retention/distribution limitations. Permission to access a data endpoint does not automatically permit redistribution of raw data or derived datasets.

## Sensitive information

Never commit API keys, passwords, private tokens, session cookies, personal data, account identifiers, or confidential user material. Use environment variables or a managed secrets store for credentials. Sample configs must contain placeholders only. Revoke exposed credentials promptly and document incident handling without reproducing the secret.

## Licensing checklist for releases

- [ ] A license has been selected for original code, if code reuse is intended.
- [ ] A license or rights statement covers original documentation, if reuse is intended.
- [ ] Third-party materials have compatible permissions and attribution.
- [ ] Data distribution rights have been reviewed.
- [ ] External contribution terms and ownership are clear.
- [ ] No secrets or unauthorized data are included.

Do not add a license file until its intended scope and terms have been deliberately chosen by the repository owner.

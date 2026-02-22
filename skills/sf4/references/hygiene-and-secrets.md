# SF4 Hygiene And Secrets

## Goal

Keep `simai.data` clean, reviewable, and safe for repository storage and deployment.

## Typical Hygiene Risks

1. Archive artifacts inside block folders (`*.tar.gz`, `*.zip`, etc.).
2. Embedded cache directories under block code.
3. Vendor/tool manifests inside block folders (`composer.json`, `package.json`, lock files).
4. Duplicate keys in `.site.property.php` (silent overwrite risk).
5. Secret-like values in `.site.property.php` (for example `*_secret_*`, `token`, `password`).

## What To Enforce

- Keep `grid/block` focused on template/runtime files only.
- Store secrets in environment/secret storage, not in project property files.
- Resolve duplicate property keys explicitly during refactor.
- Treat third-party widget bundles as controlled dependencies, not ad-hoc dumps.

## Audit Support

`scripts/sf4_project_audit.py` now reports hygiene warnings for:

- duplicate keys in `.site.property.php`
- non-empty secret-like literals in `.site.property.php`
- archives/cache dirs/manifest files under `grid/block`

## Cleanup Workflow

1. Run audit and capture warnings.
2. Classify each finding:
   - remove,
   - relocate,
   - or explicitly allow with comment in task notes.
3. Re-run audit and confirm warning reduction.
4. Add regression checks for affected pages/widgets after cleanup.

## Safe Handling Note

If potential secrets are detected in tracked files:

1. Rotate compromised values where applicable.
2. Replace literals with environment-backed configuration.
3. Avoid printing secret values in reports/logs.

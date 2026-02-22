# View->Block Linkage Remediation

## Goal

Close gaps where views reference block codes without corresponding block templates in project or system layer.

## Workflow

1. Generate linkage report:
   - `python3 scripts/sf4_project_audit.py --site-root <root> --site-dir <site_dir> --show-summary --link-report-json <links.json> --link-report-csv <links.csv>`
2. Inspect summary and missing counts by section.
3. Preview scaffolding:
   - `python3 scripts/scaffold_missing_blocks.py --site-root <root> --site-dir <site_dir> --report-json <links.json> --limit 20`
4. Apply scaffolding in controlled batches:
   - `python3 scripts/scaffold_missing_blocks.py --site-root <root> --site-dir <site_dir> --report-json <links.json> --limit 20 --apply`
5. Replace generated placeholders with real block implementations.
6. Re-run audit and ensure missing count is reduced to target level.

## Safety Rules

- Start with dry-run.
- Use `--limit` to keep changes reviewable.
- Avoid forcing overwrite unless intentional (`--force`).
- Commit in small batches by section.

## Suggested Prioritization

1. Header/footer/main-top/main-bottom (critical page shell).
2. Sidebar and navigation-related blocks.
3. Home variants and optional promo blocks.
4. Rare/legacy view codes.


---
name: sf4
description: Implement and modernize SIMAI Framework 4 (SF4) projects on Bitrix using safe project-layer overrides. Use when tasks involve `simai.data` structure, grid/view/block page assembly, template areas, `simai:sf.*` components, site/section/page properties, iblock/highloadblock setup, wizard actions, or migration/update workflows in SF4.
---

# SIMAI Framework 4

## Quick Start

1. Run `python3 scripts/sf4_project_audit.py --site-root <project_root>` to detect `simai.data`, validate critical files, and verify `grid_view_*` mappings.
2. Read `references/project-layout.md` for path conventions and layer boundaries.
3. Choose a task route:
   - Grid, layout, block, or view task: read `references/grid-and-block-workflow.md`.
   - Production-like composition patterns: read `references/production-patterns.md`.
   - Settings, config, or property task: read `references/config-and-data.md`.
   - Component, iblock, or HL-block task: read `references/components-catalog.md`.
   - Iblock/HL creation standard: read `references/iblock-hl-standard.md`.
   - Wizard install/update/import task: read `references/wizard-actions.md`.
   - Missing `view -> block` bindings remediation: read `references/linkage-remediation.md`.
   - QA/regression verification: read `references/qa-regression.md`.
   - Data hygiene and secret handling: read `references/hygiene-and-secrets.md`.
   - Update and migration artifacts: read `references/update-artifacts.md`.
   - Ready-made execution recipes: read `references/task-playbooks.md`.
   - Debugging and recovery: read `references/troubleshooting.md`.
4. Apply changes in project layer first. Edit system layer only when user explicitly asks.
5. Validate syntax and rendering, then clear relevant cache.

## Non-Negotiable Rules

- Keep `/simai`, `/bitrix/templates/simai.framework`, and `/bitrix/components/simai` immutable by default.
- Place project customizations in `{site_dir}/simai.data`.
- Keep block metadata and params near block code: `.description.php`, `.parameters.php`, `lang/<lang>/`.
- Keep `grid_view_*` values aligned with real folders in `simai.data/grid/view/.../<code>/`.
- Keep row/column/area parameter naming consistent with SF4 grid patterns.
- Check file permissions for `simai.data` when changes do not persist.
- Do not commit archives/cache/vendor artifacts inside `simai.data/grid/block`.
- Keep secret-like values out of `.site.property.php` when possible; prefer environment-backed storage.
- For schema/data/update tasks, always prepare migration notes and rollback plan (explicitly state "no changes" when applicable).
- For non-trivial tasks, keep smoke/regression evidence in a checklist or QA report.

## Execution Workflow

1. Identify active site and data layer.
2. Identify change scope:
   - Page composition and layout.
   - Block/component implementation.
   - Configuration or inheritance.
   - Data schema (iblock/HL).
   - Wizard/install/update pipeline.
3. Modify only relevant layer.
4. Validate:
   - PHP syntax for touched files.
   - Presence of required files (`template.php`, `.parameters.php`, `.description.php`, `lang`).
   - Runtime behavior on target pages.
   - Smoke/regression status with evidence for touched risk areas.
5. Clear relevant cache and retest.

## Task Routing

### Grid, View, Block, and Template Areas

- Read `references/grid-and-block-workflow.md`.
- Read `references/production-patterns.md` for real-world area/view/block conventions.
- For step-by-step execution, read `references/task-playbooks.md` sections 1, 2, and 9.
- Use area templates in `simai.data/template/area/.../template.php` to select active view by property.
- Build pages by composing rows/columns/areas in view `template.php` files.
- Add or override blocks under `simai.data/grid/block/<section>/<code>/`.

### Linkage Remediation

- Read `references/linkage-remediation.md`.
- Use `sf4_project_audit.py` with `--link-report-json` to capture full view-to-block linkage.
- Use `scaffold_missing_blocks.py` in dry-run mode first, then apply in small `--limit` batches.
- For step-by-step execution, read `references/task-playbooks.md` section 9.
- Re-run audit after each batch and keep missing count trending down.

### Settings and Inheritance

- Read `references/config-and-data.md`.
- For step-by-step execution, read `references/task-playbooks.md` sections 3 and 4.
- Edit schema files in `simai.data/config/*.config.php`.
- Edit values in `simai.data/.site.property.php` and section/page `/.property.php`.
- Respect precedence: user > page > section > site.

### Components, Iblocks, and HL-Blocks

- Read `references/components-catalog.md`.
- Read `references/iblock-hl-standard.md` before creating new entities.
- For step-by-step execution, read `references/task-playbooks.md` sections 5 and 6.
- Reuse `simai:sf.grid`, `simai:sf.iblock.*`, `simai:sf.highloadblock.grid`, `simai:sf.wizard`.
- Configure iblock edit forms with `.iblock.config.php` and `.iblock.section.config.php`.
- Use wizard import/export flows for package-style iblock/HL migration.

### Wizard Actions and Deployment

- Read `references/wizard-actions.md`.
- Read `references/update-artifacts.md` for mandatory update outputs.
- For step-by-step execution, read `references/task-playbooks.md` sections 7 and 10.
- Ensure action code matches action folder name.
- Keep install/update chains reproducible and file-safe.
- Stop and ask user when expected wizard config is missing.

### Quality and Regression

- Read `references/qa-regression.md`.
- Read `references/hygiene-and-secrets.md`.
- Read `references/update-artifacts.md`.
- For step-by-step execution, read `references/task-playbooks.md` sections 11 and 12.
- Use templates in `references/artifacts/` for migration notes, upgrade notes, regression checklist, and QA report.
- Keep risk and evidence explicit in every verification summary.

## Scripts

- Audit current project:
  - `python3 scripts/sf4_project_audit.py --site-root <project_root> --site-dir <site_dir>`
- Export full `view -> block` linkage report:
  - `python3 scripts/sf4_project_audit.py --site-root <project_root> --site-dir <site_dir> --link-report-json <path.json> --link-report-csv <path.csv>`
- Scaffold new block:
  - `python3 scripts/create_sf4_block.py --site-root <project_root> --site-dir <site_dir> --section <section> --code <block_code>`
- Scaffold new view:
  - `python3 scripts/create_sf4_view.py --site-root <project_root> --site-dir <site_dir> --area <area> --code <view_code>`
- Preview block scaffold without writes:
  - `python3 scripts/create_sf4_block.py --site-root <project_root> --site-dir <site_dir> --section <section> --code <block_code> --dry-run`
- Preview view scaffold without writes:
  - `python3 scripts/create_sf4_view.py --site-root <project_root> --site-dir <site_dir> --area <area> --code <view_code> --dry-run`
- Preview missing-block remediation scaffold without writes:
  - `python3 scripts/scaffold_missing_blocks.py --site-root <project_root> --site-dir <site_dir> --report-json <path.json> --limit 20`
- Apply missing-block remediation scaffold:
  - `python3 scripts/scaffold_missing_blocks.py --site-root <project_root> --site-dir <site_dir> --report-json <path.json> --limit 20 --apply`

## When To Ask User

- Multiple valid site roots or site dirs exist and target is unclear.
- Required config file is missing (for example `.wizard.config.php` or `*.config.php` expected by flow).
- Task requests direct system-layer edits that break update-safe policy.
- Task depends on undocumented project-specific behavior (custom editor entrypoints, custom deploy policy).

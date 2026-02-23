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
   - Full-site baseline patterns from real project study: read `references/field-study-university-local.md`.
   - Page route map + modernization template for large sites: read `references/page-map-and-modernization.md`.
   - Real page modernization cases by route type: read `references/page-modernization-cases.md`.
   - Frontend markup/class pattern task: read `references/ui-catalog.md`.
   - UI intent-to-page routing: read `references/ui-source-map.md`.
   - SF4 class shortlist and composition rules: read `references/ui-class-cheatsheet.md`.
   - Ready markup starters for common blocks: read `references/ui-markup-recipes.md`.
   - Interactive dependency mapping: read `references/ui-interactive-dependencies.md`.
   - Interaction attributes for SF4/Bootstrap-like widgets: read `references/ui-interaction-attributes.md`.
   - Frontend accessibility baseline: read `references/ui-a11y-checklist.md`.
   - Demo-vs-production asset policy: read `references/ui-asset-policy.md`.
   - Backend knowledge map from `/ru/bx`: read `references/bx-backend-source-map.md`.
   - `simai.storage` implementation patterns: read `references/storage-api-playbook.md`.
   - Universal property editor patterns: read `references/property-editor-playbook.md`.
   - `sf.grid` editor behavior and safety notes: read `references/sfgrid-editor-features.md`.
   - Critical backend anti-regression guides: read `references/backend-critical-guides.md`.
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
- For markup tasks, prefer classes and structures validated by SF4 UI catalog (`/ru/ui`) or project CSS; avoid introducing unknown class names blindly.
- Before introducing new frontend classes, inspect current project usage with `scripts/sf4_markup_inventory.py`.
- Before shipping interactive changes, inspect project markers/assets with `scripts/sf4_interactive_audit.py`.
- Do not move docs-only frontend assets (`highlight`, `bootstrap-docs`, `clipboard`) into production templates by default.
- Keep accessibility support attributes (`aria-*`, `tabindex`, `.sr-only`) intact during refactor.
- In package/source templates, do not concatenate `SITE_ID` for `IBLOCK_TYPE`/`IBLOCK_CODE` where replacement flow expects canonical placeholders.
- Avoid `DOMContentLoaded` wrappers in dynamically loaded component templates; use explicit init calls and/or event delegation.
- If template outputs `Block\\Edit::add*Area(...)`, wrapper must keep `position-relative`.
- Prefer `SIMAI\\Main\\Page\\Asset::load()` for framework package assets instead of scattered direct `addJs/addCss`.
- Before release on backend-heavy tasks, run `scripts/sf4_backend_risk_scan.py` and resolve critical findings.
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
- Read `references/field-study-university-local.md` when task targets a full existing SF4 site, not an isolated template.
- Read `references/page-map-and-modernization.md` to classify page route type before changing large/legacy sites.
- Read `references/page-modernization-cases.md` for concrete Type A/B/C modernization examples from a real site.
- Read `references/sfgrid-editor-features.md` for advanced `sf.grid` editor behavior and constraints.
- Read `references/ui-catalog.md` when task also includes frontend markup changes.
- For step-by-step execution, read `references/task-playbooks.md` sections 1, 2, and 9.
- Use area templates in `simai.data/template/area/.../template.php` to select active view by property.
- Build pages by composing rows/columns/areas in view `template.php` files.
- Add or override blocks under `simai.data/grid/block/<section>/<code>/`.

### Frontend Markup, Utilities, and UI Components

- Read `references/ui-catalog.md`.
- Read `references/ui-source-map.md`.
- Read `references/ui-class-cheatsheet.md`.
- Read `references/ui-markup-recipes.md`.
- For step-by-step execution, read `references/task-playbooks.md` section 13.
- Use `/ru/ui` catalog pages as the primary source for class combinations and markup structure.
- Keep markup adjustments inside project-layer blocks/views unless task explicitly asks to modify system templates.
- Run class inventory when refactor touches multiple blocks/views:
  - `python3 scripts/sf4_markup_inventory.py --site-root <project_root> --site-dir <site_dir> --top 80`
- Verify desktop/mobile rendering and state behavior (hover, focus, validation, dropdown/modal states where applicable).

### Frontend Interaction, Assets, and Accessibility

- Read `references/ui-interactive-dependencies.md`.
- Read `references/ui-interaction-attributes.md`.
- Read `references/ui-a11y-checklist.md`.
- Read `references/ui-asset-policy.md`.
- For step-by-step execution, read `references/task-playbooks.md` section 14.
- Inventory project interactive markers and dependency signals:
  - `python3 scripts/sf4_interactive_audit.py --site-root <project_root> --site-dir <site_dir> --top 80`
- Validate keyboard, focus, and accessibility semantics for changed interactive widgets.

### Backend Data, Property, and API Patterns

- Read `references/bx-backend-source-map.md`.
- Read `references/storage-api-playbook.md`.
- Read `references/property-editor-playbook.md`.
- Read `references/backend-critical-guides.md`.
- For step-by-step execution, read `references/task-playbooks.md` section 15.
- Run backend risk scan for guide-level pitfalls:
  - `python3 scripts/sf4_backend_risk_scan.py --site-root <project_root> --site-dir <site_dir>`
- Use scan output to validate:
  - `IBLOCK_TYPE`/`IBLOCK_CODE` patterns,
  - dynamic init strategy (`DOMContentLoaded` misuse),
  - `Block\Edit` overlay wrapper positioning,
  - asset loading strategy consistency.

### Linkage Remediation

- Read `references/linkage-remediation.md`.
- Use `sf4_project_audit.py` with `--link-report-json` to capture full view-to-block linkage.
- Use `scaffold_missing_blocks.py` in dry-run mode first, then apply in small `--limit` batches.
- For step-by-step execution, read `references/task-playbooks.md` section 9.
- Re-run audit after each batch and keep missing count trending down.

### Settings and Inheritance

- Read `references/config-and-data.md`.
- Read `references/property-editor-playbook.md` when task includes `simai:sf.property.edit` schemas or save cycle behavior.
- For step-by-step execution, read `references/task-playbooks.md` sections 3 and 4.
- Edit schema files in `simai.data/config/*.config.php`.
- Edit values in `simai.data/.site.property.php` and section/page `/.property.php`.
- Respect precedence: user > page > section > site.

### Components, Iblocks, and HL-Blocks

- Read `references/components-catalog.md`.
- Read `references/storage-api-playbook.md` when project uses `simai.storage` data model.
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
- Inventory frontend classes in project templates:
  - `python3 scripts/sf4_markup_inventory.py --site-root <project_root> --site-dir <site_dir> --top 80`
- Lookup where a class is used:
  - `python3 scripts/sf4_markup_inventory.py --site-root <project_root> --site-dir <site_dir> --class sf-form-control --class theme-dark`
- Export markup inventory report to JSON:
  - `python3 scripts/sf4_markup_inventory.py --site-root <project_root> --site-dir <site_dir> --json-out <path.json>`
- Audit interactive markers and asset usage in templates:
  - `python3 scripts/sf4_interactive_audit.py --site-root <project_root> --site-dir <site_dir> --top 80`
- Show detailed lines for selected interactive markers:
  - `python3 scripts/sf4_interactive_audit.py --site-root <project_root> --site-dir <site_dir> --marker sf_modal_attr --marker inputmask_attr`
- Export interactive audit to JSON:
  - `python3 scripts/sf4_interactive_audit.py --site-root <project_root> --site-dir <site_dir> --json-out <path.json>`
- Scan backend integration risks from `/ru/bx` guides:
  - `python3 scripts/sf4_backend_risk_scan.py --site-root <project_root> --site-dir <site_dir>`
- Export backend risk scan to JSON:
  - `python3 scripts/sf4_backend_risk_scan.py --site-root <project_root> --site-dir <site_dir> --json-out <path.json>`
- Build page route map with active views, key blocks, and override hotspots:
  - `python3 scripts/sf4_site_map.py --site-root <project_root> --site-dir <site_dir>`
- Export page route map to JSON:
  - `python3 scripts/sf4_site_map.py --site-root <project_root> --site-dir <site_dir> --json-out <path.json> --json`

## When To Ask User

- Multiple valid site roots or site dirs exist and target is unclear.
- Required config file is missing (for example `.wizard.config.php` or `*.config.php` expected by flow).
- Task requests direct system-layer edits that break update-safe policy.
- Task depends on undocumented project-specific behavior (custom editor entrypoints, custom deploy policy).

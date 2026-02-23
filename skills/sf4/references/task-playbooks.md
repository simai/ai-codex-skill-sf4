# SF4 Task Playbooks

## 1) Create Or Override A Block

Goal:

- Add new block or safely override existing one in project layer.

Steps:

1. Identify target section and block code from active view.
2. Create scaffold:
   - `python3 scripts/create_sf4_block.py --site-root <root> --site-dir <site_dir> --section <section> --code <code>`
3. Implement `template.php` logic.
4. Define editor params in `.parameters.php`.
5. Define localized labels in `lang/<lang>/.description.php` and `.parameters.php`.
6. Bind params in view (`ROW_*_AREA_*__<BLOCK>__...` keys).
7. Validate on page, then clear cache.

## 2) Build Or Modify A View Layout

Goal:

- Compose page area from rows/columns/blocks through `simai:sf.grid`.

Steps:

1. Determine active area and `grid_view_*` code.
2. If this is a full legacy site, read `references/field-study-university-local.md` first.
3. Open `{site_dir}/simai.data/grid/view/<area>/<code>/template.php`.
4. Modify:
   - row count/order
   - column widths and adaptivity
   - area template assignments
   - row conditions by property keys
5. Ensure every referenced block exists in project or system layer.
6. Run audit:
   - `python3 scripts/sf4_project_audit.py --site-root <root> --site-dir <site_dir>`
7. Clear cache and verify rendering.

## 3) Add New Page Variant By Properties

Goal:

- Keep one codebase, switch composition by settings inheritance.

Steps:

1. Add new view folder under `grid/view/<area>/<new_code>/`.
2. Copy base `template.php` and adjust composition.
3. Set `grid_view_* = <new_code>`:
   - globally in `.site.property.php`, or
   - per section/page in `/.property.php`.
4. Validate inheritance and fallback behavior.

## 4) Update Site/Section/Page Config Schema

Goal:

- Expose new setting in SF4 config UI and runtime.

Steps:

1. Add schema entry in `.site.config.php` or `.structure.config.php`.
2. Add localization entries under `config/lang/<lang>/`.
3. Set value in `.site.property.php` or `/.property.php`.
4. Read setting in template/view/block runtime code via `Property::getValue(...)`.
5. Verify UI visibility, conditions, and runtime behavior.

## 5) Configure Iblock Editor Forms

Goal:

- Standardize data editing UX for iblock elements/sections.

Steps:

1. Edit `.iblock.config.php` for element forms.
2. Edit `.iblock.section.config.php` for section forms.
3. Keep field type/template/condition consistent.
4. Verify form loads in admin/public editor entrypoints.
5. Validate save cycle and expected property persistence.

## 6) HL-Block Data Flow

Goal:

- Render and manage highload entities through SF4-compatible components and migration actions.

Steps:

1. Use `simai:sf.highloadblock.grid` for table-like output.
2. For package migrations, use wizard archive import/export actions with HL support.
3. Validate linked-field mappings when showing HL references in UI.

## 7) Wizard Install/Update Pipeline Change

Goal:

- Modify install/update process without breaking reproducibility.

Steps:

1. Locate wizard entry script and actual config file.
2. Verify `.wizard.config.php` exists before editing action chain.
3. Verify runtime payload strategy:
   - static `master/<wizard>/data/*` in source, or
   - installer-assembled `master/<wizard>/data/*` at deployment time.
4. Add/adjust actions with explicit inputs/outputs/conditions.
5. Confirm action code equals folder name in `/simai/wizard/action/<code>/`.
6. Confirm action resolution order is acceptable:
   - wizard-local override first,
   - global action fallback second.
7. Run dry validation in controlled environment.

## 17) Inspect Or Patch System Layer (`/simai`) Safely

Goal:

- Analyze or update framework-level `/simai` internals with explicit risk control.

Steps:

1. Read `references/system-layer-simai.md`.
2. Confirm task explicitly requires system-layer change (not solvable in `simai.data`/override layer).
3. Classify change surface:
   - `simai/config` (asset/font/framework registries),
   - `simai/property` (universal property type templates),
   - `simai/block` (system default blocks),
   - `simai/wizard` (actions/master packages),
   - `simai/admin` bridge endpoints.
4. Snapshot current state and check for drift:
   - config->filesystem package consistency,
   - action folder/code consistency,
   - expected wizard config file presence.
5. Apply minimal patch and keep backward compatibility.
6. Validate:
   - `php -l` for touched files,
   - smoke run on affected editors/pages/wizard stages.
7. Record migration/rollback and residual risks in artifact notes.

## 8) Create New Iblock or HL-Block By Standard

Goal:

- Introduce new data entities in a way compatible with SF4 runtime, editors, and migration workflows.

Steps:

1. Read `references/iblock-hl-standard.md`.
2. Choose naming according to project pattern and environment.
3. Create entity (iblock/HL) with required fields.
4. Wire schema and editors in `simai.data/config`.
5. Wire rendering in SF4 blocks/components.
6. Add or update wizard migration steps if entity must be package-delivered.
7. Validate end-to-end: render, edit, migrate.

## 9) Remediate Missing View->Block Links

Goal:

- Close `view -> block` gaps fast while keeping edits reviewable and reversible.

Steps:

1. Generate a linkage report from real project state:
   - `python3 scripts/sf4_project_audit.py --site-root <root> --site-dir <site_dir> --show-summary --link-report-json <links.json> --link-report-csv <links.csv>`
2. Review missing items and prioritize by section/business criticality.
3. Run dry-run scaffolding for first batch:
   - `python3 scripts/scaffold_missing_blocks.py --site-root <root> --site-dir <site_dir> --report-json <links.json> --limit 20`
4. Apply scaffold for the same batch:
   - `python3 scripts/scaffold_missing_blocks.py --site-root <root> --site-dir <site_dir> --report-json <links.json> --limit 20 --apply`
5. Replace generated placeholders with real template and parameter logic.
6. Re-run audit and confirm missing count drops.
7. Repeat in small batches until target is met.

## 10) Deliver Update With Migration/Upgrade Artifacts

Goal:

- Ship SF4 updates with explicit migration, rollback, and post-update guidance.

Steps:

1. Read `references/update-artifacts.md`.
2. Collect diff and classify impact (layout/config/data/wizard).
3. Confirm whether schema/data changes exist. Do not assume "none".
4. Execute change and run smoke/regression checks.
5. Fill artifacts using templates:
   - `references/artifacts/migration-notes.md` (always)
   - `references/artifacts/upgrade-notes.md`
   - `references/artifacts/regression-checklist.md`
   - `references/artifacts/qa-report.md` (for high-risk scope)
6. Ensure rollback and idempotency statements are explicit.
7. Include artifact summary in final delivery.

## 11) Run SF4 QA and Regression Pass

Goal:

- Verify changed SF4 scope with repeatable checks and evidence model.

Steps:

1. Read `references/qa-regression.md`.
2. Define smoke checks for changed pages/areas.
3. Define focused regression around adjacent risk zones.
4. Run static safety checks (`php -l`, debug artifact scan, layer-boundary check).
5. Run runtime checks and capture evidence.
6. Record results using:
   - `references/artifacts/regression-checklist.md`, and optionally
   - `references/artifacts/qa-report.md`
7. Mark residual risks and required follow-up tests.

## 12) Harden Project Hygiene And Secret Handling

Goal:

- Remove risky artifacts and configuration smells from `simai.data` without breaking runtime behavior.

Steps:

1. Read `references/hygiene-and-secrets.md`.
2. Run project audit and collect hygiene warnings.
3. Classify findings:
   - archive/cache/vendor artifact in block dirs,
   - duplicate property keys,
   - secret-like literals in `.site.property.php`.
4. Apply cleanup in controlled batches (small, reviewable diffs).
5. Re-run audit to confirm warning reduction.
6. Run focused smoke/regression on affected pages/widgets.
7. Document what was removed, relocated, or accepted as an intentional exception.

## 13) Build Or Refactor Frontend Markup By SF4 UI Catalog

Goal:

- Implement or modernize SF4 markup using validated `/ru/ui` patterns while preserving project behavior.

Steps:

1. Read:
   - `references/ui-catalog.md`
   - `references/ui-source-map.md`
   - `references/ui-class-cheatsheet.md`
   - `references/ui-markup-recipes.md`
   - `references/component-template-resolution.md` (when page is component-heavy)
2. For large existing projects, add `references/field-study-university-local.md`.
3. Inspect current project class baseline:
   - `python3 scripts/sf4_markup_inventory.py --site-root <root> --site-dir <site_dir> --top 80`
4. Select the target pattern source:
   - layout, component, utility, decor, content, action, or snippet.
5. Confirm target implementation layer:
   - page composition in `grid/view/.../template.php`, or
   - block markup in `grid/block/.../template.php`.
6. Port minimal markup skeleton from closest SF4 UI example.
7. Bind dynamic data/params and keep class naming aligned with SF4 conventions.
8. Avoid introducing new classes unless project CSS already defines them.
9. Validate:
   - desktop/mobile breakpoints,
   - interaction states (focus/open/hover/validation where relevant),
   - text/content overflow with real data.
10. Run `sf4_project_audit.py` and smoke checks, then clear cache and retest pages.
11. Re-run class inventory and compare hotspots for unexpected class drift:
   - `python3 scripts/sf4_markup_inventory.py --site-root <root> --site-dir <site_dir> --class sf-form-control --class theme-dark`

## 14) Add Or Refactor Interactive UI Safely

Goal:

- Implement interactive SF4 frontend behavior with explicit dependency mapping, clean asset policy, and baseline accessibility.

Steps:

1. Read:
   - `references/ui-interactive-dependencies.md`
   - `references/ui-interaction-attributes.md`
   - `references/ui-a11y-checklist.md`
   - `references/ui-asset-policy.md`
2. Run baseline interactive audit:
   - `python3 scripts/sf4_interactive_audit.py --site-root <root> --site-dir <site_dir> --top 80`
3. Choose target interaction pattern:
   - modal/dropdown/tooltip/popover/swiper/form-mask/fancybox.
4. Implement or update markup attributes in block/view templates.
5. Connect required JS/CSS dependencies in project layer.
6. Ensure no docs-only assets are introduced into production templates.
7. Run accessibility checklist for changed controls.
8. Validate runtime:
   - open/close/toggle behavior,
   - keyboard and focus flow,
   - mobile and desktop behavior,
   - no console errors.
9. Re-run interactive audit with focused marker checks:
   - `python3 scripts/sf4_interactive_audit.py --site-root <root> --site-dir <site_dir> --marker sf_modal_attr --marker dropdown_toggle --marker inputmask_attr`
10. Clear cache and rerun smoke checks on affected pages.

## 15) Implement Backend Data/Settings By `/ru/bx` Patterns

Goal:

- Build or modernize SF4 backend logic using `simai.storage`, universal properties, and anti-regression guide rules from `/ru/bx`.

Steps:

1. Read:
   - `references/bx-backend-source-map.md`
   - `references/storage-api-playbook.md`
   - `references/property-editor-playbook.md`
   - `references/sfgrid-editor-features.md`
   - `references/backend-critical-guides.md`
2. For full existing projects, add `references/field-study-university-local.md` as baseline context.
3. Identify target backend scope:
   - storage CRUD/events/search,
   - property editor schema/persistence,
   - `sf.grid` editor behavior,
   - package update safety patterns.
4. Implement changes in project layer/config while preserving update-safe boundaries.
5. For `simai.storage` writes, ensure sort/search updates and access constraints are handled.
6. For property schemas, validate field types, conditions, include/entity parameters, and save cycle.
7. For `sf.grid` editor changes, verify `COMPONENT_ID`, edit mode boundaries, and persistence behavior.
8. Run backend risk scan:
   - `python3 scripts/sf4_backend_risk_scan.py --site-root <root> --site-dir <site_dir>`
9. Resolve or explicitly justify findings for:
   - `IBLOCK_TYPE`/`IBLOCK_CODE` + `SITE_ID` concatenation,
   - `DOMContentLoaded` misuse in dynamic templates,
   - `Block\Edit::add*Area` without `position-relative`,
   - inconsistent asset loading strategy.
10. Run smoke/regression checks and clear cache.
11. Record migration/rollback notes for any schema or data-impacting changes.

## 16) Modernize One Existing Page In A Full SF4 Site

Goal:

- Safely modernize a real page with route-aware edits and minimal regressions.

Steps:

1. Read `references/page-map-and-modernization.md`.
2. Read `references/page-modernization-cases.md`.
3. For component-heavy route (Type C), read `references/component-template-resolution.md`.
4. Build route map snapshot:
   - `python3 scripts/sf4_site_map.py --site-root <root> --site-dir <site_dir> --json-out <map.json> --json`
5. Classify target page type:
   - template-driven area/view/block route,
   - direct `simai:sf.grid` page,
   - component-heavy section page.
6. Identify exact files for minimal change surface.
7. For Type C route, map actual template resolution:
   - `python3 scripts/sf4_component_template_map.py --site-root <root> --site-dir <site_dir> --component simai:sf.iblock.list --component bitrix:main.include`
8. Implement layout/markup/logic changes in project layer.
9. Validate:
   - `php -l` for touched files,
   - `python3 scripts/sf4_project_audit.py --site-root <root> --site-dir <site_dir>`.
10. If UI changed, run:
   - `python3 scripts/sf4_markup_inventory.py --site-root <root> --site-dir <site_dir> --top 80`
   - `python3 scripts/sf4_interactive_audit.py --site-root <root> --site-dir <site_dir> --top 80`
11. Clear cache and run smoke/regression on target and neighboring pages.

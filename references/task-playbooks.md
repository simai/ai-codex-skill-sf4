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
2. Open `{site_dir}/simai.data/grid/view/<area>/<code>/template.php`.
3. Modify:
   - row count/order
   - column widths and adaptivity
   - area template assignments
   - row conditions by property keys
4. Ensure every referenced block exists in project or system layer.
5. Run audit:
   - `python3 scripts/sf4_project_audit.py --site-root <root> --site-dir <site_dir>`
6. Clear cache and verify rendering.

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
3. Add/adjust actions with explicit inputs/outputs/conditions.
4. Confirm action code equals folder name in `/simai/wizard/action/<code>/`.
5. Run dry validation in controlled environment.

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

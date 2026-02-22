# Grid, View, and Block Workflow

## Area To View Binding

- Area template path pattern:
  - `{site_dir}/simai.data/template/area/<area_path>/template.php`
- Typical logic:
  - Read property `grid_view_<area>`
  - Build path `{site_dir}/simai.data/grid/view/<mapped_area>/<code>/template.php`
  - Include file if it exists

Example areas:

- `header` -> `grid_view_header` -> `grid/view/header/<code>/template.php`
- `footer` -> `grid_view_footer` -> `grid/view/footer/<code>/template.php`
- `main/top` -> `grid_view_main_top` -> `grid/view/main/top/<code>/template.php`
- `main/bottom` -> `grid_view_main_bottom` -> `grid/view/main/bottom/<code>/template.php`
- `sidebar/left` -> `grid_view_sidebar_left` -> `grid/view/sidebar/left/<code>/template.php`
- `sidebar/right` -> `grid_view_sidebar_right` -> `grid/view/sidebar/right/<code>/template.php`

## View Structure

Expected files:

- `.description.php`
- `template.php`
- `lang/<lang>/.description.php`
- optional preview assets (for editor UI)

View `template.php` usually calls:

- `IncludeComponent("simai:sf.grid", ".default", [...])`

The call stores full page composition:

- rows (`ROW_*`)
- columns (`ROW_<r>_COL_<c>_*`)
- areas (`ROW_<r>_COL_<c>_AREA_<a>_*`)
- optional row conditions (`ROW_<r>_USE_CONDITION`, comparison/value)

## Block Structure

Expected files for a reusable block:

- `.description.php`
- `.parameters.php`
- `template.php`
- `lang/<lang>/.description.php`
- `lang/<lang>/.parameters.php`
- optional assets (`style.css`, `script.js`, local assets)

Path pattern:

- `{site_dir}/simai.data/grid/block/<section>/<code>/`

## Block Parameter Naming

- Use uppercase folder code as block prefix.
- Replace dot with underscore for component parameter transport.

Example:

- Block code `custom.button`
- Prefix in template/params: `CUSTOM.BUTTON__...`
- Grid-level transport key: `CUSTOM_BUTTON__...`

## Safe Override Procedure

1. Locate block usage in active view (`...AREA_*_TEMPLATE`).
2. Copy or create project block in `simai.data/grid/block/<section>/<code>/`.
3. Keep `.description.php` and `.parameters.php` synchronized with template expectations.
4. Adjust view parameters for that area entry.
5. Validate frontend output and editor fields.

## Page Assembly Procedure

1. Confirm target area and active view code in properties.
2. Open active view folder and inspect rows/columns/areas.
3. Add, remove, reorder, or condition rows in `simai:sf.grid` params.
4. Add required blocks under matching section path.
5. Keep modifiers responsive (`WIDTH_XL/LG/MD/SM/XS`) when adaptive mode is used.
6. Clear cache and verify rendered page.

## Typical Failure Modes

- View code set in property but folder missing.
- Block referenced by view but block folder missing.
- Parameter key mismatch (`.` vs `_` conversion issue).
- Missing language files causing empty labels in editors.
- Cache not cleared after file changes.


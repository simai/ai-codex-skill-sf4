# SF4 Page Map And Modernization Template

## Contents

1. Goal
2. Build page map automatically
3. Baseline snapshot (`/ru`)
4. Route types for real pages
5. Practical modernization template
6. Regression checklist for page modernization

## 1) Goal

Use a repeatable method to map real SF4 pages to:

- active `grid_view_*` selections,
- view templates and key block templates,
- section/page property overrides,
- top-level component usage patterns,
- direct `simai:sf.grid` pages outside `simai.data`.

Then modernize pages safely with minimal regressions.

For concrete route-specific examples, also read `references/page-modernization-cases.md`.
For component-heavy pages, also read `references/component-template-resolution.md`.

## 2) Build Page Map Automatically

Use:

```bash
python3 scripts/sf4_site_map.py --site-root <project_root> --site-dir <site_dir>
```

Machine-readable output:

```bash
python3 scripts/sf4_site_map.py --site-root <project_root> --site-dir <site_dir> --json-out <path.json> --json
```

What it returns:

- `active_views` from `.site.property.php`
- `active_view_templates` with `BLOCK_SECTION` and unique `ROW_*_AREA_*_TEMPLATE` block codes
- `.property.php` overrides for `grid_view_*`, `sidebar_show`, `show_title`, `show_breadcrumb`, `layout_sidebar_type`
- top-level section `index.php` component usage counters
- direct `simai:sf.grid` usage outside `simai.data`

## 3) Baseline Snapshot (`/ru`)

Observed on the university baseline:

- active views:
  - `grid_view_header=005`
  - `grid_view_footer=default`
  - `grid_view_home=default`
  - `grid_view_main_top=default`
  - `grid_view_main_bottom=default`
  - `grid_view_sidebar_left=default`
  - `grid_view_sidebar_right=default`
- active view key-block counts:
  - header: 18
  - footer: 14
  - home: 27
  - main/top: 4
  - main/bottom: 10
  - sidebar left/right: 4
- top-level index signals:
  - `simai:sf.iblock.list` dominates
  - selective `simai:sf.iblock.section`, `simai:sf.iblock.table`, `simai:sf.feedback*`
  - `bitrix:main.include` is frequent among bitrix components
- direct `simai:sf.grid` pages outside `simai.data` include:
  - `ru/students/service/detail.php`

Use this snapshot as routing guidance, not as a strict invariant.

## 4) Route Types For Real Pages

### Type A: Template-driven page (most sections)

Rendering route:

1. `local/templates/simai.framework/header.php`
2. `simai.data/template/template.php`
3. `template/area/*`
4. selected `grid/view/.../<code>/template.php`
5. `grid/block/<section>/<code>/template.php`

Change surface:

- preferred in `grid/block/...` and sometimes `grid/view/...`
- optional behavior flags in `.property.php` and `.site.property.php`

### Type B: Direct `simai:sf.grid` page

Rendering route is page-local and may bypass default area composition for core content.

Change surface:

- page file itself first
- then block templates referenced by that page-local grid

### Type C: Component-heavy section index

Page is mostly component orchestration (`simai:sf.iblock.*`, `bitrix:*`).

Typical examples:

- `ru/contacts/index.php`
- `ru/natsionalnyy-proekt-nauka-i-universitety/index.php`

Change surface:

- section `index.php`
- component templates under `local/templates/simai.framework/components/...`
- section/page properties
- before editing templates, resolve actual source with `sf4_component_template_map.py`

## 5) Practical Modernization Template

Use this sequence for a single page modernization.

1. Identify page route type (A/B/C) with `sf4_site_map.py` and page source.
2. Capture current binding context:
   - active `grid_view_*`,
   - local `.property.php` overrides,
   - block/component templates used by the page.
3. Define minimal change scope:
   - visual/layout only,
   - behavior/interactions,
   - data/component logic.
4. Edit only required layer:
   - Type A: prefer `simai.data/grid/block/...`
   - Type B: page-local `simai:sf.grid` + referenced blocks
   - Type C: page orchestration and component template overrides
5. Validate syntax and bindings:
   - `php -l` on touched files
   - `python3 scripts/sf4_project_audit.py --site-root <root> --site-dir <site_dir>`
6. For frontend-heavy changes:
   - `python3 scripts/sf4_markup_inventory.py --site-root <root> --site-dir <site_dir> --top 80`
   - `python3 scripts/sf4_interactive_audit.py --site-root <root> --site-dir <site_dir> --top 80`
7. Clear cache and run smoke checks on page and adjacent sections.
8. Record regression evidence and residual risks.

## 6) Regression Checklist For Page Modernization

- target page renders without PHP/runtime errors
- expected header/footer/sidebar behavior preserved for the route type
- title/breadcrumb/sidebar flags from `.property.php` still respected
- key interactive controls (modal/dropdown/form/search/menu) still work
- no unexpected class drift for core wrappers (`sf-*`, `theme-*`, `t-*`, grid classes)
- no new missing `view -> block` links introduced

# SF4 Field Study: Full Site Baseline

## Purpose

Capture a real full-size SF4 project profile to guide practical implementation and modernization tasks.

This reference is for pattern calibration when the task is not a toy example but a production-like website with many sections, views, blocks, and data schemas.

## Baseline Topology

Use generic mapping:

- Site root: `<site_root>`
- Active locale/site dir: `<site_dir>` (example: `/ru`)
- Project data layer: `<site_root>/<site_dir>/simai.data`
- System template loader: `<site_root>/local/templates/simai.framework`
- SF4 asset source: `<site_root>/simai/asset/simai.framework/sf4.master`

Important practical nuance:

- In some environments, `/bitrix/templates/simai.framework` may be an alias/shortcut file and not a physical template directory.
- Runtime-safe reference for template loader is `<site_root>/local/templates/simai.framework`.

## Runtime Chain Observed In Practice

1. `local/templates/simai.framework/header.php` and `footer.php` include `SF_DATA_PATH . "/template/template.php"`.
2. `simai.data/template/property.php` merges site/section/page/user properties.
3. `simai.data/template/area/*/template.php` selects active view by `grid_view_*`.
4. Active view (`grid/view/.../<code>/template.php`) composes page via `simai:sf.grid`.
5. Grid areas map to `grid/block/<section>/<code>/template.php`.

## Scale Profile (Production-Like)

Observed on the baseline project:

- `grid/view`: dozens of templates across `header`, `home`, `main/top`, `main/bottom`, `footer`, `sidebar`.
- `grid/block`: hundreds of block templates, including content-heavy and service/admin blocks.
- `template/area`: extended zones beyond basic header/footer/main/sidebar.
- `config`: full set of site/structure/iblock/section config schemas.

Implication:

- Always run project audit before refactor.
- Assume drift and legacy variants exist (`default`, numeric codes, `DEV`, `EMPTY`, dotted codes).

## Observed Snapshot Metrics (Example)

Sample scan metrics from the baseline project:

- `grid/view` files: `130`
- `grid/block` files: `742`
- `template/area` files: `24`
- view templates discovered by audit: `36`
- `view -> block` links: total `417`, resolved `331`, missing `86`
- missing-link hotspots: mostly `home`, then `homepage`, then rare `header` entries

Interactive scan sample:

- `include_component`: `131`
- `aria_attr`: `50`
- `sf_modal_attr`: `15`
- `sf_src_attr`: `7`

Use these numbers as a complexity signal, not as strict thresholds.

## Active View Pattern

Typical property-driven bindings:

- `grid_view_header`
- `grid_view_footer`
- `grid_view_home`
- `grid_view_main_top`
- `grid_view_main_bottom`
- `grid_view_sidebar_left`
- `grid_view_sidebar_right`

Do not hardcode expected view names. Read effective values from `.site.property.php` plus section/page inheritance.

## Extended Template Areas In Real Use

In addition to core areas, full projects often use:

- `template/area/button`
- `template/area/script/top`
- `template/area/script/bottom`
- `template/area/service/top/*`
- `template/area/service/bottom/*`
- `template/area/notification`

These areas can affect behavior, admin UX, consent widgets, and auxiliary scripts. Do not remove them during visual refactor without explicit requirement.

## Frontend Pattern Signals

Real project templates commonly show:

- heavy class-driven composition (`sf-*`, `theme-*`, `t-*`, utility classes)
- mixed static and dynamic class fragments
- interaction attributes (`sf-modal`, `sf-src`, `aria-*`)
- distributed asset loading via `Asset::load` plus selective `addJs/addCss` in blocks

Workflow recommendation:

1. Run class inventory:
   - `python3 scripts/sf4_markup_inventory.py --site-root <site_root> --site-dir <site_dir> --top 80`
2. Run interactive marker audit:
   - `python3 scripts/sf4_interactive_audit.py --site-root <site_root> --site-dir <site_dir> --top 80`
3. Refactor with minimal drift from existing class language.

## Backend/Data Pattern Signals

Real full projects frequently combine:

- full `.site.config.php` and `.structure.config.php` schemas
- large `.iblock.config.php` and `.iblock.section.config.php` editor declarations
- `entity` fields targeting `\Bitrix\Iblock\Section` and section-code selectors
- rich section/page property inheritance
- public/editor integrations in service/admin template areas

Workflow recommendation:

1. Run backend risk scan:
   - `python3 scripts/sf4_backend_risk_scan.py --site-root <site_root> --site-dir <site_dir>`
2. Resolve critical findings before shipping.
3. Keep migration and rollback notes for schema/data-impacting changes.

## Typical Risk Surface In Large SF4 Sites

- Missing `view -> block` links due historic view variants.
- Archive/cache/vendor artifacts inside `grid/block`.
- Legacy `SITE_ID` concatenation patterns in template-level iblock references.
- `DOMContentLoaded` wrappers in templates that may be loaded dynamically.
- Mixed asset strategy (package loads plus scattered direct includes).

Mitigation baseline:

- `sf4_project_audit.py` with linkage summary.
- Batch scaffold only after dry-run (`scaffold_missing_blocks.py`).
- Keep changes small and re-audit each batch.

## Practical Use

Use this field study when task text implies:

- "work with the whole site",
- "modernize existing SF4 project",
- "build/refactor pages from real grids and blocks",
- "align frontend and backend behavior without regressions".

This reference should be read together with:

- `references/project-layout.md`
- `references/system-layer-simai.md`
- `references/grid-and-block-workflow.md`
- `references/production-patterns.md`
- `references/page-map-and-modernization.md`
- `references/page-modernization-cases.md`
- `references/component-template-resolution.md`
- `references/config-and-data.md`
- `references/task-playbooks.md`

Quick route-map command:

```bash
python3 scripts/sf4_site_map.py --site-root <site_root> --site-dir <site_dir>
```

Sample E2E checklist artifact for Type A/B/C route verification:

- `references/artifacts/e2e-university-ru-type-abc.md`

Sample component-template mapping artifacts:

- `references/artifacts/university-ru-component-template-map.md`
- `references/artifacts/university-ru-component-template-map.json`

Sample system-layer study artifact:

- `references/artifacts/university-simai-layer-notes.md`

# SF4 Real Page Modernization Cases (University Baseline)

## Contents

1. Purpose
2. Case A: Template-driven page
3. Case B: Direct `simai:sf.grid` page
4. Case C: Component-heavy page
5. Shared anti-regression checks

## 1) Purpose

Use concrete page routes from a production-like SF4 site to reduce guesswork during modernization.

This file complements:

- `references/page-map-and-modernization.md`
- `references/field-study-university-local.md`
- `references/component-template-resolution.md`
- `references/task-playbooks.md` section 16

## 2) Case A: Template-driven page

Example pages:

- `ru/about/index.php`
- `ru/worldskills-russia/index.php`

Route characteristics:

- Page file mostly has `header.php` / `footer.php` and optional static HTML.
- Core composition comes from template areas and active views:
  - `ru/simai.data/template/area/main/top/template.php`
  - `ru/simai.data/grid/view/main/top/default/template.php`
  - `ru/simai.data/grid/block/main/*`

Typical modernization targets:

- Page title wrapper/style via:
  - `ru/simai.data/grid/block/main/page.title/template.php`
- Banner/include-top row behavior via:
  - `ru/simai.data/grid/view/main/top/default/template.php`
- Section/page flags in `/.property.php` (`show_title`, `show_breadcrumb`, `show_banner_main`, `sidebar_show`)

Safe change strategy:

1. Confirm active views with `sf4_site_map.py`.
2. Change one layer first:
   - block markup in `grid/block/main/...`, or
   - row structure/conditions in `grid/view/main/top/default/template.php`.
3. Keep condition keys (`show_title`, `show_banner_main`, `include_top_area`) stable.
4. Validate on 2-3 template-driven pages, not only one target page.

## 3) Case B: Direct `simai:sf.grid` page

Primary example:

- `ru/students/service/detail.php`

Route characteristics:

- Page contains direct `IncludeComponent("simai:sf.grid", ...)`.
- Grid is assembled in page params (`ROW_*`, `ROW_ORDER`, `BLOCK_SECTION`).
- Section/page overrides are defined in:
  - `ru/students/service/.property.php`

Observed config signals for this page:

- `BLOCK_SECTION = service-about`
- row templates include: `banner`, `images`, `description`, `specialist`, `reviews`, `faq`, `docs`, `priceEducation`, `feedback`, `map`
- page-level overrides disable generic wrappers:
  - `sidebar_show=none`
  - `show_title=N`
  - `show_breadcrumb=N`
  - `use_page_container=N`

Primary editable files:

- page orchestration:
  - `ru/students/service/detail.php`
- referenced block templates:
  - `ru/simai.data/grid/block/service-about/<block_code>/template.php`
- route-specific properties:
  - `ru/students/service/.property.php`

Safe change strategy:

1. Keep `BLOCK_SECTION` and row-template names aligned with existing block folders.
2. If reordering rows, update both `ROW_ORDER` and relevant `ROW_*` declarations.
3. Preserve `HIDE_ICONS` behavior tied to grid edit mode.
4. After changes, verify page with and without element code context.

## 4) Case C: Component-heavy page

Primary examples:

- `ru/contacts/index.php`
- `ru/natsionalnyy-proekt-nauka-i-universitety/index.php`

Route characteristics:

- Page is mostly orchestration of `simai:sf.*` + `bitrix:*` components.
- Modernization impact often spans both page file and component templates.
- Actual template source can be local override, local component source, or bitrix component source.

Useful related template paths from baseline:

- `local/templates/simai.framework/components/simai/sf.iblock.list/contacts/template.php`
- `local/templates/simai.framework/components/bitrix/map.yandex.view/contacts/template.php`

Typical modernization targets:

- component params in section page (`COUNT`, `AREA`, `DISPLAY_TYPE`, modifiers, AJAX flags)
- component markup wrappers/classes in local template overrides
- include-file fragments (`simai.data/include/*.php`) used by `bitrix:main.include`

Safe change strategy:

1. Start from page-level component params (lowest-risk, high-impact changes).
2. Move to component-template markup only for confirmed UI requirements.
3. Resolve source first with `sf4_component_template_map.py` before editing template files.
4. Preserve edit overlays and frame mode behavior in templates.
5. Recheck dynamic pieces (maps, tabs, feedback forms) after markup updates.

## 5) Shared Anti-Regression Checks

Apply for all cases:

1. Syntax and structure:
   - `php -l <touched_file.php>`
   - `python3 scripts/sf4_project_audit.py --site-root <project_root> --site-dir <site_dir>`
2. Route verification:
   - `python3 scripts/sf4_site_map.py --site-root <project_root> --site-dir <site_dir>`
3. For markup-heavy changes:
   - `python3 scripts/sf4_markup_inventory.py --site-root <project_root> --site-dir <site_dir> --top 80`
4. For interactive changes:
   - `python3 scripts/sf4_interactive_audit.py --site-root <project_root> --site-dir <site_dir> --top 80`
5. Runtime smoke:
   - target page renders
   - title/breadcrumb/sidebar rules stay consistent with `/.property.php`
   - no regressions in adjacent section pages

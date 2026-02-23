# `simai.data` Runtime, Settings, and Template Model

## Why This Matters

In SF4, `simai.data` is the project layer that drives:

- site/page appearance,
- area/view/block composition,
- property inheritance,
- per-user runtime overrides.

Most modernization tasks are settings and template tasks, even when the request sounds like "just layout".

## Placement Rules In Multisite

- `simai.data` is site-scoped, not global.
- Path pattern:
  - `<site_root>/<site_dir>/simai.data`
- In Bitrix multisite-by-folders, each site folder has its own `simai.data`.
- Runtime site context is derived from `SITE_DIR` and mapped to:
  - `SF_SITE_DIR`,
  - `SF_DATA_DIR`,
  - `SF_DATA_PATH`.

## Canonical `simai.data` Structure

- `admin/`
  - proxy admin endpoints that forward to module admin handlers (`config.site.php`, `config.section.php`, `config.page.php`, `config.demo.php`, iblock editors).
- `config/`
  - `.site.config.php` for site-level schema.
  - `.structure.config.php` for section/page schema.
  - `.demo.config.php` for per-user demo customization schema.
  - `.iblock.config.php` for public element edit forms.
  - `.iblock.section.config.php` for public section edit forms.
- `grid/`
  - `view/` stores composition presets selected by `grid_view_*`.
  - `block/` stores site-level block implementations and overrides.
- `image/`, `include/`, `modal/`, `svg/`
  - site assets and include fragments used by settings and blocks.
- `template/`
  - site-specific template assembly (`template.php`, `property.php`, `style.php`, `js.php`, `meta.php`, `area/*`).
- `.site.property.php`
  - persisted site-level values.

Related outside `simai.data`:

- section/page values are stored in `/.property.php` in the site tree.
- section display metadata is also written to `/.section.php` by section editor flow.

## Settings Storage Levels and Priority

Effective order:

- `site` -> `section` -> `page` -> `user` -> optional global overrides.

Practical source files/services:

- Site values:
  - `simai.data/.site.property.php` via `\SIMAI\Main\Configuration\Site`.
- Section values:
  - `/.property.php` (`section` key) via `\SIMAI\Main\Configuration\Section`.
- Page values:
  - `/.property.php` (`page[filename]` key) via `\SIMAI\Main\Configuration\Page`.
- User values:
  - session storage via `\SIMAI\Main\Configuration\Property` (`storageId = "user"`).

## Runtime Merge Point (`template/property.php`)

Site template merge flow:

1. load `simai.data/.site.property.php`;
2. merge recursive section values (`Section::getRecursionArray($dir)`);
3. merge page values (`Page::getArray($page)`); 
4. merge user session values (`Property::getArray("user")`);
5. merge optional global runtime overrides (`$GLOBALS["SF_PROPERTY"]`);
6. compute derived layout keys:
   - `layout_pagewrap`,
   - `layout_container`,
   - `layout_container_size`,
   - `main_width`;
7. persist merged runtime snapshot:
   - `Property::setArray(SF_SITE_DIR, $arSiteProperty)`.

Important runtime behavior:

- non-admin users are forced to `development_mode = N`;
- URL params `property_code/property_value` can write user-level overrides;
- `partner` URL param forces user `demo_mode = N`.

## How Template Assembly Works

Universal template entry:

- `local/templates/simai.framework/header.php` and `footer.php` (project-local template variant)
- `bitrix/templates/simai.framework/header.php` and `footer.php` (legacy/global template variant)

Both include:

- `SF_DATA_PATH . "/template/template.php"` (site-specific template).

Site template pipeline (`simai.data/template/template.php`):

1. include `property.php` (merge and compute runtime properties);
2. include `panel.php`;
3. include `style.php` and `js.php`;
4. render body/layout using `Property::getValue(SF_SITE_DIR, ...)`;
5. include template areas via `IncludeArea::includeTemplateArea(...)`;
6. include `meta.php` in footer phase.

## Area -> View -> Grid -> Block Chain

1. `template/area/<area>/template.php` picks active view from `grid_view_*`.
2. Selected file:
   - `simai.data/grid/view/<area_path>/<code>/template.php`.
3. View calls `simai:sf.grid` with row/column/area params.
4. `simai:sf.grid` resolves each area block directory with `\SIMAI\Main\Block\Section::getDir(...)`:
   - first `simai.data` path,
   - then framework `/simai` path.
5. If site block exists, it wins; otherwise framework block is used.

This is the core update-safe override mechanism for layout blocks.

## Editing Flows (Admin + Public)

### Site settings editor

- Proxy:
  - `<site_dir>/simai.data/admin/config.site.php`
- Module handler:
  - `/local/modules/simai.framework/admin/config.site.php` (typical for project-local module install)
  - `/bitrix/modules/simai.framework/admin/config.site.php` (legacy/global module install)
- Behavior:
  - loads `.site.config.php`,
  - renders `simai:sf.property.edit`,
  - writes normalized values to `.site.property.php` via `Site::setValue(...)`.

### Section settings editor

- Handler merges:
  - global `.structure.config.php` + optional section-local `/.structure.config.php`.
- Saves:
  - section values to `/.property.php` (`section` key),
  - section title and properties to `/.section.php`.

### Page settings editor

- Uses `.structure.config.php`.
- Saves:
  - page values to `/.property.php` (`page[filename]` key),
  - page prolog metadata updates (`title`, `description`, `keywords`) in page file.

### Demo mode editor (user level)

- Uses `.demo.config.php`.
- Saves user overrides into session storage (`Property::setValue("user", ...)`).
- Reset clears user session properties (`Property::clear("user")`).

### `simai:sf.property.edit` component behavior

`simai:sf.property.edit` normalizes input by field type and either:

- writes to file (`TYPE = file`), or
- returns array to caller (`TYPE = array`) for handler-specific persistence.

Special case:

- `include` with `sf4.editor` / `sf4.script` writes directly to target include file path.

## What To Change For Typical Tasks

- New setting visible in site editor:
  - update `simai.data/config/.site.config.php`,
  - optionally `config/lang/<lang>/...`,
  - persist defaults/values in `.site.property.php` or editor flow.
- Section/page-specific behavior:
  - ensure key exists in `.structure.config.php`,
  - use `/.property.php` for override scope.
- Visual composition switch:
  - change `grid_view_*` values,
  - ensure matching `grid/view/.../<code>/template.php` exists.
- Custom block behavior:
  - implement under `simai.data/grid/block/...`,
  - avoid direct edits in `/simai/block` unless explicitly required.

## Practical Before/After Examples

### 1) Switch Header View For One Section

Context:

- Keep global header view unchanged, switch only for a section subtree.

Before (`/<site_dir>/.property.php`):

```php
<?php
$arDirProperties = [
    "grid_view_header" => "001",
];
```

After (`/<site_dir>/admission/.property.php`):

```php
<?php
$arDirProperties = [
    "grid_view_header" => "005",
];
```

Also required:

- `simai.data/grid/view/header/005/template.php` must exist.
- Area template (`template/area/header/template.php`) must read `grid_view_header`.

Expected result:

- only `/admission/*` gets header view `005`; other sections still use site default.

### 2) Add New Site Setting And Use It In Template

Context:

- Add `show_breadcrumbs` toggle in site settings and render breadcrumbs conditionally.

Before (`simai.data/config/.site.config.php`):

```php
<?php
return [
    "layout_container" => ["type" => "list"],
];
```

After (`simai.data/config/.site.config.php`):

```php
<?php
return [
    "layout_container" => ["type" => "list"],
    "show_breadcrumbs" => [
        "type" => "checkbox",
        "default" => "Y",
    ],
];
```

Value (`simai.data/.site.property.php`):

```php
<?php
return [
    "show_breadcrumbs" => "Y",
];
```

Usage (`simai.data/template/template.php` or area/view template):

```php
<?php if (\SIMAI\Main\Configuration\Property::getValue(SF_SITE_DIR, "show_breadcrumbs") === "Y"): ?>
    <?php $APPLICATION->IncludeComponent("bitrix:breadcrumb", ".default", []); ?>
<?php endif; ?>
```

Expected result:

- setting appears in site editor;
- runtime value is available after merge in `template/property.php`.

### 3) Override A Framework Block Without Touching `/simai`

Context:

- Replace output of a standard block with project-specific markup.

Before:

- only framework block exists:
  - `/simai/block/header/logo/template.php`

After:

- create site override:
  - `<site_dir>/simai.data/grid/block/header/logo/template.php`
  - `<site_dir>/simai.data/grid/block/header/logo/.parameters.php`
  - `<site_dir>/simai.data/grid/block/header/logo/.description.php`

Minimal override template:

```php
<div class="sf-header-logo custom-logo">
    <a href="/"><img src="<?=SITE_TEMPLATE_PATH?>/images/logo.svg" alt=""></a>
</div>
```

Expected result:

- `simai:sf.grid` resolves project block first, so site block is used;
- framework block remains untouched and available as fallback.

## Verification Checklist

1. Confirm active site dir and corresponding `simai.data`.
2. Confirm schema file contains edited key.
3. Confirm persistence target:
   - site `.site.property.php`,
   - section/page `/.property.php`,
   - user session (`demo` mode).
4. Confirm merged runtime value in `template/property.php` context.
5. Confirm selected area view exists (`grid_view_*` -> folder).
6. Confirm referenced blocks exist (site override or framework fallback).
7. Clear cache and verify on target page as both admin and non-admin user.

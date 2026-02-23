# SF4 System Layer (`/simai`) Map

## Contents

1. Purpose
2. What `/simai` contains
3. Runtime and ownership boundaries
4. Wizard architecture (`sf.wizard` / `sf.wizard.stage`)
5. Property type architecture (`simai/property/*`)
6. System block architecture (`simai/block/*`)
7. Asset registry and package selection
8. Practical rules for project work

## 1) Purpose

Describe the system-level SF4 layer under `<project_root>/simai`.

This is the source layer for framework mechanics and reusable defaults. For project delivery tasks, treat it as read-only by default and apply changes in site project layer (`<site_dir>/simai.data`) unless task explicitly requires framework-level patching.

## 2) What `/simai` contains

Top-level system folders:

- `simai/admin`:
  - admin endpoints and bridge scripts (mostly wrappers to `bitrix/modules/simai.*` admin files).
- `simai/asset`:
  - registry-targeted package directories for SF4 CSS/JS and third-party libs.
- `simai/block`:
  - system default block templates for grid sections (`header`, `home`, `main`, `sidebar`, `footer`, `feedback`).
- `simai/config`:
  - framework-level registries: asset/font/framework options.
- `simai/property`:
  - universal property type renderers and templates used by property editors.
- `simai/wizard`:
  - universal action engine and master packages for install/update/import flows.

## 3) Runtime And Ownership Boundaries

Default policy:

- System layer (`/simai`, `/bitrix/components/simai`, base template) is framework source.
- Project layer (`<site_dir>/simai.data`, `local/templates/.../components/...`) is implementation/customization layer.

For project modernization:

1. Change project layer first.
2. Touch `/simai` only if user explicitly asks for framework-level fix or packaging change.
3. If system layer is changed, document migration/rollback impact explicitly.

## 4) Wizard Architecture (`sf.wizard` / `sf.wizard.stage`)

Entry components:

- `local/components/simai/sf.wizard`
- `local/components/simai/sf.wizard.stage`

Mechanics:

- Wizard reads config file (`WIZARD_CONFIG_FILE`) and stores mutable state in `SIMAI\Main\Configuration\Property` by wizard code.
- Stage execution resolves action file in order:
  1. `<wizard_dir>/action/<code>/action.php`
  2. fallback `/simai/wizard/action/<code>/action.php`
- Action conditions support comparison operators (`==`, `!=`, `>`, `<`, `>=`, `<=`) and optional AND/OR condition grouping.

Action package model (`/simai/wizard/action/<code>/`):

- required: `action.php`, `.description.php`, `lang/ru/*`
- optional: `ajax.php`, `class.php` or `classes.php`

Master package model (`/simai/wizard/master/<master_code>/`):

- optional `index.php` launcher
- optional `.wizard.config.php`
- data payload under `data/` (`site`, `config`, `iblock`, `bitrix`)

## 5) Property Type Architecture (`simai/property/*`)

Each property type folder (for example `string`, `list`, `entity`, `include`) usually contains:

- `.description.php`
- `edit.php`, `filter.php`, `view.php`
- `templates/<variant>/{edit.php,filter.php,view.php}`
- `lang/ru/*`

Template variants are critical for editor UX. Examples:

- checkbox: `.default`, `sf4`, `sf4.image`, `sf4.switch`
- list: `.default`, `sf4`, `sf4.button`, `sf4.image.card`, `sf4.image.list`, `sf4.radio`
- include: `.default`, `sf4`, `sf4.editor`, `sf4.script`

Some variants add asset/editor behavior:

- entity template uses `/simai/admin/sf_property_entity_search.php` dialog helper.
- map template injects Yandex Maps API and map-specific assets.

## 6) System Block Architecture (`simai/block/*`)

Section folders:

- `header`, `home`, `main`, `sidebar`, `footer`, `feedback`

Block folder convention:

- `template.php`
- `.description.php`
- optional `.parameters.php`
- optional local assets/includes (`style.css`, `script.js`, helper PHP includes)

Typical parameter pattern:

- `.parameters.php` defines group/property schema used by grid editor.
- runtime values are passed via `$arBlockProperty[...]` and often feed `simai:sf.iblock.*`, `simai:sf.menu`, `simai:sf.feedback*` components.

`empty` blocks are present as stubs in each major section and may intentionally omit `template.php`.

## 7) Asset Registry And Package Selection

Config sources:

- `simai/config/.asset.config.php`
- `simai/config/.font.config.php`
- `simai/config/.framework.config.php`

Asset usage model:

- package name resolved by `Asset::load(<package>)`
- package config points to concrete `dir/version/files`
- runtime expects config and filesystem package versions to match

Font config model:

- key -> metadata (`name`, `type`) + either external `link` or local `family`

## 8) Practical Rules For Project Work

1. Treat `/simai` as framework source; prefer project overrides.
2. For wizard changes, keep `action` code and folder name identical.
3. For component-heavy pages, map template source first before editing markup.
4. Before changing asset package versions, verify both config and filesystem payload.
5. For property editor changes, verify template variant supports required interaction type (dialog/map/html editor/multi-select).
6. If system-layer edits are unavoidable, attach migration notes and regression checklist.

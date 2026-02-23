# System Layer Notes: `university.local/simai`

Observation date:

- 2026-02-23

Scope:

- `<project_root>/simai`

## 1) Structure Snapshot

Top folders present:

- `admin`, `asset`, `block`, `config`, `property`, `wizard`

System block section sizes:

- `home`: 37
- `header`: 36
- `footer`: 26
- `main`: 15
- `sidebar`: 7
- `feedback`: 5

Property types discovered:

- `checkbox`, `color`, `complex`, `datetime`, `entity`, `file`, `html`, `include`, `link`, `list`, `map`, `number`, `phone`, `sort`, `string`, `text`, `url`

Wizard actions discovered:

- action folders: 48
- with `ajax.php`: 10
- with `class.php/classes.php`: 4
- all contain `action.php`, `.description.php`, `lang/ru`

## 2) Important Runtime Findings

1. `simai/admin/*` files are mostly bridge wrappers to module admin endpoints under `bitrix/modules/simai.*`.
2. `sf.wizard` action resolution uses local wizard action first, then global fallback `/simai/wizard/action/<code>/action.php`.
3. `simai.sf4university/index.php` references `.wizard.config.php`, but that config file is not present in this snapshot.
4. `simai.sveden/.wizard.config.php` exists and references valid action codes.

## 3) Config Drift / Integrity Notes

Asset config checks:

- `bootstrap` package configured as `bootstrap-4.1.0`, but filesystem contains `bootstrap-4.1.3` only.
- `sf-icon` package points to `/plugin/icon/css/icon.css`, file is missing in current `sf4.master` path.

Framework config checks:

- `site_property` points to `/ru/simai.data/config/.site.property.php` (missing in this project).
- `site_nav_config` points to `/ru/simai.data/config/.nav.config.php` (missing in this project).

Font config checks:

- duplicate keys detected (later value overrides earlier in PHP array):
  - `pt_sans_narrow`
  - `noto_serif`
  - `cormorant_garamond`

## 4) Practical Implication For Skill Usage

- Use `/simai` as source map and fallback reference.
- For project tasks, edit `simai.data`/project overrides unless framework patch is explicitly requested.
- For wizard/asset-level tasks, validate config-to-filesystem consistency before release.
- Treat missing wizard config and asset/version drift as explicit risk flags in QA summary.

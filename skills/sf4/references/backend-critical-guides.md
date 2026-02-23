# SF4 Backend Critical Guides

## Goal

Enforce backend practices from `/ru/bx/guides` that prevent recurring regressions in SF4 projects.

## 1) `IBLOCK_TYPE` / `IBLOCK_CODE` In Package Sources

Guide:

- `guides/iblock-type-iblock-code.php`

Rule:

- in distributable/public source templates, keep canonical placeholder-like codes (`sf_ru_*`, `sf-ru-*`) where project process expects them.
- do not concatenate `SITE_ID` directly in component parameters inside source package templates.

Why:

- installation/update flows perform code replacement automatically.
- manual interpolation creates mismatch with wizard/updater replacement logic.

## 2) Avoid `DOMContentLoaded` In Component Templates

Guide:

- `guides/domcontentloaded.php`

Rule:

- avoid `document.addEventListener("DOMContentLoaded", ...)` inside component templates that may load via AJAX/modal.
- prefer immediate init, explicit `init*()` calls after insertion, and/or delegated events.

Why:

- dynamic content often appears after the initial DOMContentLoaded event already fired.

## 3) `position-relative` For Public Editor Overlays

Guide:

- `guides/public-editor-position-relative.php`

Rule:

- wrapper element around `Block\Edit::add*Area(...)` output must include `position-relative`.

Why:

- overlay uses absolute positioning and otherwise can attach to wrong visual container.

## 4) Asset Loading Policy For Framework Packages

Related API docs:

- `api/asset_load.php`

Rule:

- for framework package libraries use `SIMAI\Main\Page\Asset::load("<package>")`.
- avoid scattering direct `addJs/addCss` where package loading is expected.

Why:

- central config and version/fallback logic live in the SF4 asset manager.

## Practical Pre-Release Checks

1. No `SITE_ID` interpolation for iblock type/code in package-level templates.
2. No `DOMContentLoaded` wrappers in dynamically loaded component templates.
3. All public-edit wrappers with `Block\Edit::add*Area` have `position-relative`.
4. Framework library loading uses `Asset::load` where applicable.

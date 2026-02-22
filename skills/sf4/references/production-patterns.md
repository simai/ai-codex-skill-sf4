# SF4 Production Patterns

## Goal

Capture real-world SF4 patterns observed on live project templates so implementation choices match production usage.

## Extended Template Areas

Beyond basic header/footer/main/sidebar selectors, production projects often include:

- `template/area/button/template.php`
- `template/area/script/top/template.php`
- `template/area/script/bottom/template.php`
- `template/area/service/top/*/template.php`
- `template/area/service/bottom/*/template.php`

Use these areas when page composition requires service widgets, admin/demo panels, or extra script slots.

## View Code Conventions In Practice

Common view code styles:

- numeric: `01`, `010`, `030`
- semantic: `default`, `empty`
- environment/debug: `DEV`, `EMPTY`
- dot notation: `WIDGET.SIDEBAR`

Do not assume view code is lowercase-only.

## Advanced View Composition

Complex views may use:

- custom row IDs (`ROW_first_*`) alongside numeric row IDs
- large `ROW_ORDER` sequences for explicit composition control
- heavy per-area parameter binding (`ROW_*_AREA_*__<BLOCK>__...`)

When modernizing such views, preserve existing row keys and order semantics unless task explicitly asks to simplify.

## Advanced Block Pattern: Include Chain

A frequent block pattern for complex content cards:

- dynamic filter assembly from block params
- include-based extension points:
  - `SOURCE_INCLUDE`
  - `INCLUDE_BEFORE`
  - `INCLUDE_AFTER`
  - `INCLUDE_EPILOG`

If block logic is hardcoded to project-specific iblock IDs/codes, treat migration as a separate controlled step.

## Section Naming Drift

`BLOCK_SECTION` values may differ from folder conventions in some views (for example `home` vs `homepage`).
Always resolve against actual block paths before refactoring.

## Practical Rule

Before changing production-like views/blocks:

1. Snapshot current `grid/view` and `grid/block` references.
2. Validate all referenced templates exist.
3. Keep functional behavior equivalent before any structural cleanup.

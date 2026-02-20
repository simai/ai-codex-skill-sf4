# Components and Data Components

## Core SF4 Components

- `simai:sf.grid`
  - Base page composition engine (rows, columns, areas, conditions).
  - Component source example: `/bitrix/components/simai/sf.grid`.
- `simai:sf.iblock.list`
  - Generic iblock listing with many display templates.
  - Component source example: `/bitrix/components/simai/sf.iblock.list`.
- `simai:sf.highloadblock.grid`
  - HL-block grid/table renderer.
  - Component source example: `/bitrix/components/simai/sf.highloadblock.grid`.
- `simai:sf.wizard`
  - Wizard container and stage execution.
  - Component source example: `/bitrix/components/simai/sf.wizard`.
- `simai:sf.wizard.stage`
  - Wizard stage renderer.
  - Component source example: `/bitrix/components/simai/sf.wizard.stage`.

## `simai:sf.grid` Notes

- Reads block section from `BLOCK_SECTION`.
- Resolves block template path through `SF_DATA_DIR/grid/block/<section>/<code>/`.
- Reads block parameter schema from block `.parameters.php`.
- Supports row-level condition checks via site properties.

## `simai:sf.iblock.list` Notes

- Used by many project blocks to render cards/sliders/lists.
- Common parameters:
  - iblock type/code
  - section/filter
  - count/sort
  - template modifiers and area composition

## `simai:sf.highloadblock.grid` Notes

- Selects target HL-block by `HLBLOCK_ID`.
- Allows selecting displayed fields.
- Supports linked HL-block field display mapping in parameters.

## Data Layer Alignment

Use component configuration with:

- iblock/section config schemas in `simai.data/config`
- site properties in `simai.data/.site.property.php`
- section/page properties in `/.property.php`

## When To Use Which Layer

- Need layout composition or block orchestration: edit `grid/view` and `grid/block`.
- Need data list rendering behavior: update block template params and corresponding component call.
- Need content editor forms: update `.iblock.config.php` or `.iblock.section.config.php`.
- Need HL reference-table rendering: use `simai:sf.highloadblock.grid`.


# SF4 UI Catalog For Markup Tasks

## Goal

Use SF4 UI catalog pages (`/ru/ui`) as a practical source of valid class combinations and component markup when building or refactoring frontend in SF4 blocks and views.

Primary reference URL:

- `https://sf4.simai.pro/ru/ui/`

Companion references:

- `references/ui-source-map.md`
- `references/ui-class-cheatsheet.md`
- `references/ui-modifier-strategy.md`
- `references/ui-markup-recipes.md`
- `references/ui-interactive-dependencies.md`
- `references/ui-interaction-attributes.md`
- `references/ui-a11y-checklist.md`
- `references/ui-asset-policy.md`

## What Is Inside `/ru/ui`

- `layout`
  - grid/container/column composition patterns.
- `component`
  - cards, buttons, forms, dropdown, modal, navigation, table-adjacent UI, and more.
- `utility`
  - typography, spacing, flex/display, width/height, position, z-index, visibility helpers.
- `decor`
  - colors, borders, shadows, patterns, themes.
- `content`
  - typography/content-level snippets, icons/images/links/table markup.
- `action`
  - interaction and animation-style examples.
- `snippet`
  - compact reusable fragments.

## When To Use This Reference

- Build new block markup in `simai.data/grid/block/.../template.php`.
- Refactor existing SF4 block layout to modernize look while preserving behavior.
- Align custom templates with existing SF4 class language (`sf-*`, `t-*`, `theme-*`).
- Select utility-class strategy before adding custom CSS.

## Class And Markup Rules

1. Prefer patterns/classes already demonstrated in `/ru/ui`.
2. Keep SF4 semantic classes (`sf-*`, `t-*`, `theme-*`) as primary anchors.
3. Use utility/grid classes consistently (`row`, `col-*`, spacing/display helpers).
4. Do not invent new class names unless project stylesheet explicitly defines them.
5. For form elements, start from `component/form/*` examples and preserve label/input/help/error structure.
6. For cards/lists/navigation, start from component examples and only then adapt content bindings.
7. For one-off spacing/typography/alignment changes, use utility/modifier classes first (`ml-*`, `mt-*`, `t-*`, `c-text-*`, `d-*`).
8. Add new custom classes only for repeated/reusable behavior, not for single-node tweaks.

## Implementation Workflow

1. Identify target layer:
   - layout composition change: `grid/view/.../template.php`
   - block markup change: `grid/block/.../template.php`
2. Find nearest UI example in `/ru/ui` by intent (layout/component/utility).
3. Port minimal working markup skeleton first.
4. Bind runtime data and block params without changing visual skeleton prematurely.
5. Validate breakpoints, interactive states, and text overflow on real data.
6. Keep diffs small and reviewable; isolate structural changes from business logic changes.

## Validation Checklist

- PHP syntax valid for touched templates.
- Referenced block/view paths still resolve.
- No unknown class names introduced unintentionally.
- Desktop/mobile rendering verified.
- Required interaction states verified (hover/focus/active/open where relevant).
- Cache cleared and rerun smoke checks on affected pages.

## Practical Search Hints

From project root, quickly find similar existing usage:

```bash
rg -n "sf-title|sf-form|theme-light|theme-dark|t-[0-9]" simai.data
```

Find where a specific class is already used in block templates:

```bash
rg -n "sf-form-control|sf-example|sf-link" simai.data/grid/block
```

Inventory actual class usage before/after refactor:

```bash
python3 scripts/sf4_markup_inventory.py --site-root <project_root> --site-dir <site_dir> --top 80
```

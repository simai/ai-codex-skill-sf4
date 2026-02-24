# SF4 Utility-Modifier Strategy

## Goal

Keep markup changes lightweight and consistent by preferring existing SF4 utility/modifier classes before introducing new custom CSS classes.

Primary reference pages:

- `https://sf4.simai.pro/ru/ui/content/typography.php`
- `https://sf4.simai.pro/ru/ui/utility/space.php`
- `https://sf4.simai.pro/ru/ui/utility/typography.php`
- `https://sf4.simai.pro/ru/ui/utility/display-property.php`
- `https://sf4.simai.pro/ru/ui/utility/flexbox.php`

## Modifier-First Decision Rule

1. If change is typography-only (size/weight/secondary tone):
   - use `t-*`, `t--*`, `t-bold`, `t-regular`, `c-text-*`.
2. If change is spacing-only:
   - use margin/padding helpers first (`m*`, `p*`, `ml-*`, `mr-*`, `mt-*`, `mb-*`, `mx-*`, `my-*`).
3. If change is alignment/layout-only:
   - use display/flex/position helpers (`d-*`, `justify-content-*`, `align-items-*`, `float-*`, etc.).
4. Add new custom class only when:
   - same visual behavior repeats across multiple places, or
   - SF4 utilities cannot express the behavior safely.

## Practical Examples

### Example A: Local heading offset in filter panel

Preferred:

```html
<div class="my-1 ml-2 investmap-filter-prop-title">Целевая аудитория</div>
```

Not preferred for one-off offset:

```html
<div class="my-1 investmap-filter-prop-title investmap-filter-prop-title--offset">...</div>
```

### Example B: Secondary helper line

Preferred:

```html
<div class="t--2 c-text-secondary mt-1">Выбрано: 0</div>
```

## Anti-Patterns

- Creating a custom class for a one-line spacing tweak that `ml-*`/`mt-*` already covers.
- Duplicating utility semantics in CSS (`.title-small {font-size: ...}`) when `t-*` exists.
- Mixing many custom classes with no reusable intent.
- Replacing semantic SF4 class with utility-only markup (keep base semantic class, add modifiers on top).

## Quick Check Before Commit

1. Base semantic class is preserved (`sf-*` or project semantic class).
2. One-off visual tweaks are handled by utilities/modifiers.
3. New CSS class exists only when there is a clear reuse need.
4. No conflict with existing project utility usage (check via `sf4_markup_inventory.py` when needed).

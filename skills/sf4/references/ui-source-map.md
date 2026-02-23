# SF4 UI Source Map (`/ru/ui`)

## Goal

Speed up markup tasks by mapping common frontend intents to concrete SF4 UI catalog sections/pages.

Reference root:

- `https://sf4.simai.pro/ru/ui/`

## Choose Source By Task

### Page/Grid Composition

Use when building whole-page structure, columns, responsive composition:

- `layout/grid.php`
- `layout/page.php`
- `layout/responsive-utilities.php`
- `utility/flexbox.php`
- `utility/display-property.php`
- `utility/space.php`
- `utility/width.php`
- `utility/height.php`

Apply in:

- `simai.data/grid/view/.../template.php`

### Card/List/Content Blocks

Use when building content-heavy areas and reusable blocks:

- `component/card.php`
- `component/list-group.php`
- `component/navigation.php`
- `content/typography.php`
- `content/table.php`
- `content/link.php`

Apply in:

- `simai.data/grid/block/.../template.php`

### Forms And Inputs

Use when implementing editable controls, filters, subscribe/contact forms:

- `component/form/field.php`
- `component/form/select.php`
- `component/form/checkbox.php`
- `component/form/radio.php`
- `component/form/switch.php`
- `component/form/validation.php`
- `component/form/search.php`
- `component/form/mask.php`

Apply in:

- `simai.data/grid/block/.../template.php`

### Interactive UI

Use when adding toggles/menus/popups/interactive wrappers:

- `component/dropdown.php`
- `component/modal.php`
- `component/popover.php`
- `component/tooltip.php`
- `component/scroll.php`
- `component/scrollspy.php`
- `action/hover.php`
- `action/transition.php`

Apply in:

- block templates + required JS/CSS connection points in project layer.

### Themes, Decor, and Visual Skin

Use when updating visual tone without changing content model:

- `decor/theme.php`
- `decor/color.php`
- `decor/border.php`
- `decor/shadow.php`
- `decor/pattern.php`
- `utility/typography.php`

Apply in:

- block/view markup classes and modifier params.

## Fast Routing Rules

1. If task says "собрать страницу" or "пересобрать сетку":
   - start from `layout/*` + `utility/space.php`.
2. If task says "сделать/переделать блок":
   - start from `component/*` or `content/*`.
3. If task says "форма" or "валидация":
   - start from `component/form/*`.
4. If task says "тема/цвет/оформление":
   - start from `decor/*` + `utility/typography.php`.

## Safety Notes

- Treat `/ru/ui` as pattern source; final availability depends on styles/scripts connected in target project.
- Do not assume every example page implies every dependency is enabled in production.
- Prefer project-layer overrides in `simai.data` and keep system layer immutable by default.
- For interactive patterns, continue with:
  - `references/ui-interactive-dependencies.md`
  - `references/ui-interaction-attributes.md`
  - `references/ui-a11y-checklist.md`
  - `references/ui-asset-policy.md`

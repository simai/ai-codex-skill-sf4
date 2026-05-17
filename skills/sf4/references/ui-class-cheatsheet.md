# SF4 UI Class Cheatsheet

## Goal

Provide a practical shortlist of high-signal class families used in SF4 UI catalog so markup tasks stay consistent with framework style.

## Core SF4 Families

### `sf-*` (component semantics)

Typical classes:

- `sf-title`
- `sf-title-underline-left`
- `sf-title-underline-center`
- `sf-title-underline-center-double`
- `sf-code`
- `sf-example`
- `sf-form`
- `sf-form-label`
- `sf-form-control`
- `sf-form-select`
- `sf-form-check`
- `sf-form-check-input`
- `sf-form-switch`
- `sf-form-switch-input`
- `sf-link`
- `sf-scroll`
- `sf-scroll-x`
- `sf-close`

Use for:

- primary component structure and SF4 UI semantics.

Underline alignment rule:

- use `sf-title-underline-center` when the title itself or its wrapper is
  centered with `t-center`, `t-lgcenter`, `text-center`, or
  `justify-content-center`;
- use `sf-title-underline-left` only for left-aligned titles;
- when a block appends a global title style such as
  `title_homepage_style=sf-title-underline-left mb-3`, normalize it per block
  if the block title is centered instead of changing the shared site property.

### `t-*` (typography scale/alignment)

Typical classes:

- `t-1`, `t-2`, `t-3`, `t-4`, `t-5`
- `t--2`
- `t-bold`, `t-regular`
- `t-center`

Use for:

- text hierarchy and typography tuning.

### `theme-*` (theme context)

Typical classes:

- `theme-light`
- `theme-dark`

Use for:

- light/dark section-level visual context.

### `c-*` (color tokens)

Typical classes:

- `c-default`
- `c-text-secondary`
- `c-white`

Use for:

- text and simple color-token application.

## Grid And Utility Families

### Layout/grid

- `row`
- `col-*` (`col-6`, `col-sm`, `col-sm-6`, `col-md-4`, `col-md-6`, `col-md-8`, `col-lg-4`, `col-lg-8`, `col-xl-4`, `col-xl-8`)

Use for:

- structural page/block layout.

### Spacing and display

- `p-2`, `p-3`, `p-4`, `p-5`
- `m-4`
- directional spacing: `ml-*`, `mr-*`, `mt-*`, `mb-*`, `mx-*`, `my-*`
- `d-flex`, `d-inline-block`
- `align-items-center`, `align-center`

Use for:

- spacing rhythm and quick alignment.

### Size and visual helpers

- `w-50`, `w-100`
- `h-50`
- `text-center`, `text-muted`
- `bg-gray-100`, `bg-white`
- `align-middle`

Use for:

- local sizing, background, and utility-level visual adjustments.

### Button component

Use the SF4 button contract before adding project CSS:

- base: `btn`
- semantic type: `btn-primary`, `btn-secondary`, `btn-success`,
  `btn-info`, `btn-warning`, `btn-danger`, `btn-link`
- shape/style: `btn-rounded`, `btn-square`, `btn-outline`,
  `btn-rounded btn-outline`, `btn-square btn-outline`
- feedback: `waves-effect`, `waves-light`

Do not create a project class only to set button color, radius, padding, or
standard hover behavior when these modifiers cover the case. Project classes on
buttons are allowed for scope hooks, layout placement, missing interaction, or a
documented visual gap only.

## Modifier-First Quick Map

Use this order before creating a new class:

1. Typography tweak:
   - `t-*`, `t--*`, `t-bold`, `t-regular`, `c-text-*`.
2. Spacing tweak:
   - `ml-*`, `mt-*`, `mb-*`, `mx-*`, `my-*`, `p-*`.
3. Alignment/layout tweak:
   - `d-*`, `justify-content-*`, `align-items-*`, `float-*`.
4. New class:
   - only when behavior repeats and cannot be expressed by utilities.

Example (preferred for local heading indent):

```html
<div class="my-1 ml-2 investmap-filter-prop-title">Целевая аудитория</div>
```

## Recommended Composition Order

1. Base semantic class (`sf-*`).
2. Layout class (`row`/`col-*`/container context).
3. Utility modifiers (spacing/display/align/size).
4. Theme/color classes (`theme-*`, `c-*`) last.

## Anti-Patterns

- Adding custom class names before trying existing SF4 class combinations.
- Adding custom class names for one-off spacing/typography tweaks already covered by utilities.
- Mixing unrelated component classes on one node without a structural reason.
- Building new form markup without checking `component/form/*` examples first.
- Breaking responsive structure by replacing `col-*` logic with ad-hoc wrappers.

## Quick Validation

- Class names are reused from `/ru/ui` or already present in project CSS.
- Typography classes (`t-*`) preserve heading hierarchy.
- Form classes preserve label-control-feedback semantics.
- Layout classes keep responsive behavior on mobile and desktop.

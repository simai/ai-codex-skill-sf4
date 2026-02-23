# SF4 Interaction Attribute Patterns

## Goal

Keep interactive markup consistent with SF4 UI catalog patterns and reduce broken behavior caused by missing or malformed attributes.

## SF4 Modal Attribute Pattern

Typical trigger attributes:

- `sf-modal`
- `sf-src`
- `sf-close-modifier`
- `sf-modal-modifier`
- `sf-content-modifier`

Use when:

- opening inline/remote modal content from button/link triggers.

## Dropdown Attribute Pattern

Typical attributes:

- `data-toggle="dropdown"`
- `aria-haspopup="true"`
- `aria-expanded="false"`
- linkage via `aria-labelledby`

Use when:

- adding dropdown buttons/links and aligned menu blocks.

## Form Mask Attribute Pattern

Typical attributes:

- `data-inputmask="'alias': 'email'"`
- `data-inputmask="'mask': '+7 (999) 999-99-99'"`
- `data-inputmask-alias="datetime"`
- `data-inputmask-inputformat="hh:MM"`
- `data-inputmask-placeholder="чч:мм"`

Use when:

- phone/date/email/time mask behavior is required.

## Accessibility-Related Attributes In Interactive Markup

Common attributes in `/ru/ui` examples:

- `aria-label`
- `aria-hidden`
- `tabindex="-1"` for disabled keyboard targets where applicable
- `role="group"` in grouped controls

Use when:

- building navigation, pagination, grouped controls, icon-only controls.

## Validation Rules

1. Keep attribute names and casing consistent with selected pattern.
2. Do not add interaction attributes without corresponding JS dependency.
3. Do not remove `aria-*` or `tabindex` helpers during visual refactor.
4. Verify that toggled states update expected attributes at runtime.

# SF4 Frontend Accessibility Checklist

## Goal

Apply a minimal but practical accessibility pass to SF4 markup and interactive components, based on patterns used in `/ru/ui`.

## Core Patterns From Catalog

- Screenreader utilities:
  - `.sr-only`
  - `.sr-only-focusable`
- Pagination/navigation semantics:
  - `aria-label` on `nav`
  - helper text with `.sr-only`
  - `tabindex="-1"` for disabled links where applicable
- Icon semantics:
  - `aria-hidden="true"` for decorative icons
- Group semantics:
  - `role="group"` with proper labelling in grouped controls

## Checklist Before Delivery

1. Every interactive control is keyboard reachable and has visible focus.
2. Icon-only or ambiguous controls have accessible labels (`aria-label` or visible text).
3. Decorative icons are marked with `aria-hidden="true"`.
4. Navigation/pagination wrappers have meaningful `aria-label`.
5. Disabled navigation items are not focus traps (`tabindex`/state behavior verified).
6. Form fields keep explicit labels (`for` + `id`) and readable validation feedback.
7. Modal/dropdown open-close flow is keyboard-usable.
8. Screenreader-only helper text remains in markup where required.

## Scope Notes

- This checklist is a baseline for SF4 delivery quality, not a full WCAG audit.
- For high-traffic or public services, follow with dedicated accessibility QA.

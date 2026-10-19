# Frontend Markup And Interaction

- Prefer classes and structures validated by the SF4 UI catalog (`/ru/ui`) or
  project CSS; do not introduce unknown class names blindly.
- For one-off visual tweaks prefer existing utility/modifier classes (`ml-*`,
  `mt-*`, `t-*`, `c-text-*`, `d-*`) before adding custom CSS classes.
- Keep utility-first refactors pragmatic: do not replace stable custom classes
  that control pseudo-elements, third-party widget skins (calendar/slider) or
  component-specific JS hooks.
- Before introducing new classes inspect project usage with
  `scripts/sf4_markup_inventory.py`; before shipping interactive changes
  inspect markers/assets with `scripts/sf4_interactive_audit.py`.
- Do not move docs-only assets (`highlight`, `bootstrap-docs`, `clipboard`)
  into production templates by default.
- Keep accessibility attributes (`aria-*`, `tabindex`, `.sr-only`) intact.
- Avoid `DOMContentLoaded` wrappers in dynamically loaded component templates;
  use explicit init calls and/or event delegation.
- If a template outputs `Block\Edit::add*Area(...)`, the wrapper keeps
  `position-relative`.
- Prefer `SIMAI\Main\Page\Asset::load()` for framework package assets instead
  of scattered direct `addJs/addCss`.
- For expandable filter UIs choose one behavior mode (single-open accordion or
  multi-open panels) and keep `Set*Block`, `Handle*Switcher` and
  `Normalize*Panels` logic consistent with it.
- Verify desktop/mobile rendering, keyboard/focus semantics and states (hover,
  focus, validation, dropdown/modal) for changed widgets.

# UX Implementation Contract

Use this reference when `$sf4` implements an interface designed or reviewed by `$ux`.

## Rule

Do not treat `$ux` output as generic design prose. Convert it into SF4 page composition and project-layer implementation steps.

## Required Mapping

- `Scenario`: user, primary action, success state.
- `Page composition`: area template, active view, rows/columns, blocks.
- `Project layer`: paths under `{site_dir}/simai.data` that should change.
- `Component templates`: `simai:sf.*` components or local template overrides.
- `Classes/utilities`: SF4 UI catalog classes and project utilities to reuse before custom CSS.
- `Interactive behavior`: dropdown, modal, accordion, validation, input mask, slider, calendar, event delegation.
- `States`: empty, loading, error, success, disabled.
- `Acceptance`: desktop/mobile rendering, focus/keyboard, state behavior, cache clear and smoke target.

## Output Back To `$ux`

If SF4 constraints change the design, report:

```markdown
UX deviation:
SF4 composition reason:
Alternative:
Retest point:
```

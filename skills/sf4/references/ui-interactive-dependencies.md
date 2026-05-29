# SF4 Interactive Dependencies

## Goal

Map interactive frontend patterns from SF4 UI catalog (`/ru/ui`) to required assets and init rules so markup changes stay functional in real projects.

Companion references:

- `references/ui-interaction-attributes.md`
- `references/ui-a11y-checklist.md`
- `references/ui-asset-policy.md`

## Observed Dependency Patterns In `/ru/ui`

Examples found in catalog pages:

- `component/fancybox.php`: `Asset::getInstance()->load("fancybox")`
- `component/form/mask.php`: `Asset::getInstance()->addJs("/simai/asset/inputmask-4.x/js/jquery.inputmask.bundle.min.js")`
- `component/form/validation.php`: `Asset::getInstance()->addJs("/simai/asset/mask/js/jquery.inputmask.bundle.min.js")`
- `action/animate.php`: `SIMAI\Main\Page\Asset::getInstance()->load("animate")`
- `component/swiper.php`: `new Swiper(...)` init examples

## Dependency Map By UI Intent

### Modal / Overlay (`sf-modal`)

- Markup pattern: attributes like `sf-modal`, `sf-src`, `sf-close-modifier`, `sf-modal-modifier`, `sf-content-modifier`.
- Expected runtime: SF4 modal JS behavior from project/theme assets.
- Validation: modal opens/closes, focus is returned, overlay scroll behavior is correct.

### Dropdown / Tooltip / Popover

- Markup pattern: `data-toggle="dropdown"` and related Bootstrap-like attributes.
- Expected runtime: Bootstrap JS stack and required position engine for tooltip/popover in your stack.
- Validation: menu/tooltip opens, closes, and positions correctly on desktop/mobile.

### Swiper Sliders

- Markup pattern: `swiper-container` and navigation/pagination nodes.
- Expected runtime: Swiper library + explicit init script (`new Swiper(...)`).
- Validation: swipe, arrows, pagination, breakpoint settings, loop behavior.
- When a slider is built from an SF4 grid/list template, do not leave the
  `swiper-wrapper` controlled by grid layout. After Swiper initializes, the
  wrapper must be `display:flex`, `flex-wrap:nowrap`, slides must not shrink,
  and grid helpers that reset `margin` must not suppress Swiper spacing.
- Check the actual Swiper version class in the rendered page. Some SF4 projects
  add `swiper-container-horizontal` instead of `swiper-container-initialized`;
  scope slider CSS to the class that is really present, not only to the newest
  Swiper examples.
- For multiple sliders on one page, bind navigation controls by unique IDs or a
  scoped parent, not by shared global selectors like `.swiper-button-next`.

### Input Mask / Form Validation

- Markup pattern: `data-inputmask`, `data-inputmask-alias`, `data-inputmask-inputformat`.
- Expected runtime: jQuery Inputmask bundle and init call (`$("input").inputmask()` or scoped selector).
- Validation: mask formatting, invalid/valid states, submit behavior.

### Fancybox

- Markup pattern: link/button triggers per Fancybox integration.
- Expected runtime: Fancybox assets loaded in project layer.
- Validation: open/close, media content render, scroll lock, keyboard close.

## Integration Rules

1. Do not assume `/ru/ui` demo page automatically mirrors production assets.
2. Connect required JS/CSS explicitly in project layer before changing markup behavior.
3. Keep dependency setup near changed block/view or shared project entrypoint, based on project convention.
4. Avoid adding interactive markup without corresponding runtime dependency.
5. Test interactive states on both desktop and mobile.

## Audit Commands

Baseline audit:

```bash
python3 scripts/sf4_interactive_audit.py --site-root <project_root> --site-dir <site_dir> --top 80
```

Focused markers:

```bash
python3 scripts/sf4_interactive_audit.py --site-root <project_root> --site-dir <site_dir> --marker sf_modal_attr --marker dropdown_toggle --marker inputmask_attr
```

## Quick Verification Checklist

- Required assets are connected in target environment.
- Init code executes exactly once per rendered widget instance.
- No console errors after page load and interaction.
- Keyboard interaction works where relevant (open, close, focus).
- Behavior survives cache clear and page reload.

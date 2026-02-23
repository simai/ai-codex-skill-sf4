# SF4 Component Template Resolution And Markup Edit Rules

## Contents

1. Goal
2. Resolution priority
3. Build component-template map
4. How to decide where to edit
5. Fallback-heavy templates
6. Validation checklist

## 1) Goal

When page markup is built through components (not grid blocks), identify the actual template source before editing.

This avoids changing wrong files and reduces regressions on component-heavy pages.

## 2) Resolution Priority

For `IncludeComponent("vendor:component", "template", ...)` use this order:

1. `local/templates/simai.framework/components/<vendor>/<component>/<template>/template.php`
2. `local/components/<vendor>/<component>/templates/<template>/template.php`
3. `bitrix/components/<vendor>/<component>/templates/<template>/template.php`

If explicit template folder is missing but `.default` exists, runtime may fallback to `.default`.

## 3) Build Component-Template Map

Use:

```bash
python3 scripts/sf4_component_template_map.py --site-root <project_root> --site-dir <site_dir>
```

Machine-readable:

```bash
python3 scripts/sf4_component_template_map.py --site-root <project_root> --site-dir <site_dir> --json-out <path.json>
```

Focused details for selected components:

```bash
python3 scripts/sf4_component_template_map.py --site-root <project_root> --site-dir <site_dir> --component simai:sf.iblock.list --component simai:sf.iblock.detail
```

## 4) How To Decide Where To Edit

For each target page/component call:

1. Resolve source by map (`local_override`, `local_component_source`, `bitrix_component_source`, fallback flags).
2. If `local_override` exists, edit only override template.
3. If only source template exists, create override template in project layer and apply changes there.
4. Keep component params in page file consistent with template expectations (`AREA`, modifiers, source fields, sort/pager options).

## 5) Fallback-Heavy Templates

If map shows `unresolved_with_default_fallback`:

- Verify page behavior visually.
- Decide explicitly:
  - create named override template and pin behavior, or
  - keep `.default` fallback and document that choice.

Do not silently assume named template exists.

## 6) Validation Checklist

1. `php -l` for touched page and template files.
2. Re-run component map:
   - unresolved/fallback entries should be expected and explained.
3. If markup changed:
   - `python3 scripts/sf4_markup_inventory.py --site-root <project_root> --site-dir <site_dir> --top 80`
4. If interactive controls changed:
   - `python3 scripts/sf4_interactive_audit.py --site-root <project_root> --site-dir <site_dir> --top 80`
5. Run smoke on target and neighboring component-heavy pages.

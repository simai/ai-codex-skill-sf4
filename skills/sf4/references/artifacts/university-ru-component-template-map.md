# Component Template Map Snapshot: `/ru`

Generated from:

```bash
python3 scripts/sf4_component_template_map.py --site-root <project_root> --site-dir /ru --json-out references/artifacts/university-ru-component-template-map.json
```

## Metrics

- scanned page files (excluding `simai.data`): `585`
- pages with `IncludeComponent(...)`: `187`
- component include records: `325`
- unique components: `30`

## Top Components

- `simai:sf.iblock.list`: `194`
- `simai:sf.iblock.detail`: `30`
- `bitrix:main.include`: `25`
- `simai:sf.iblock.section`: `20`
- `simai:sf.iblock.table`: `8`

## Template Resolution Sources

- `local_component_source`: `119`
- `unresolved_with_default_fallback`: `113`
- `local_override`: `46`
- `bitrix_component_source`: `34`
- `unresolved`: `13`

Interpretation:

- Most page-level component calls resolve to component-source templates (`local/components/.../templates/...`).
- A large set of named templates is absent and likely falls back to `.default` in source.
- Project-specific visual changes should start from `local/templates/simai.framework/components/...` (override layer).

## Practical Hotspots

`simai:sf.iblock.list` template usage highlights:

- explicit source/default usage: `.default`, `sf-photo-card`, `sf-video-card`
- project override usage: `faq`, `sf-doc-list-tag`, `appeal`, `appeal_detail`, `reviews`, `presentation`, `tag`
- fallback-heavy names: `tag-sveden`, `empty`, `location`, `sf-group-select`, `employee-sveden-tag`, `table-aspirant-*`

`simai:sf.iblock.detail` template usage highlights:

- mostly `.default` from component source
- project override usage: `sf-room`, `zakupki`
- fallback-heavy names: `sf-property-tag-discipline`, `title-program`

`bitrix:map.yandex.view`:

- `contacts` resolved to local override template
- `.default` resolved to bitrix component source

## Where To Edit Markup First

1. If `local_override` exists for the used template, edit there.
2. If only `local_component_source`/`bitrix_component_source` exists, create project override template and edit in override layer.
3. If `unresolved_with_default_fallback`, verify runtime output and either:
   - create explicit override template with requested name, or
   - keep `.default` intentionally and update component params/docs.

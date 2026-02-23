# SF4 Property Editor Playbook (`simai:sf.property.edit`)

## Goal

Design and maintain SF4 settings forms using the universal property system with predictable schema and persistence behavior.

## Core Files

- `simai.data/config/.site.config.php` and `simai.data/config/.structure.config.php` for project settings schemas.
- In documented examples (`/ru/bx/property`):
  - `.config.php` defines form schema;
  - `.value.php` stores values;
  - save path uses `\SIMAI\Main\IO\Setting::saveToFile(...)`.

## Component Integration Pattern

Typical runtime:

- build `CONFIG` from schema;
- build `VALUES` from saved values;
- pass both to `simai:sf.property.edit`.

Important:

- keep additional hidden values explicit (for example site dir context);
- avoid silent schema changes without migration note.

## Field Schema Keys (Practical)

Common keys per property:

- `name`
- `type`
- `template`
- `default`
- `multiple` (`Y|N`)
- `inactive` (`Y|N`)
- `condition` (dependency map)
- `parameter` (template-specific options)

## Field Types Frequently Used

- `checkbox` (`sf4.checkbox`, `sf4.switch`, `sf4.image`)
- `color`
- `datetime`
- `entity` (for iblock/other entity bindings)
- `include` (editor/script include templates)
- `link`
- `file`

## Conditions And Dependencies

- Use `condition` maps for dynamic visibility.
- Keep dependencies simple and explicit:
  - one-field condition first;
  - only then multi-field conditions.
- For conditional fields, define deterministic defaults to avoid empty-state ambiguity.

## `include` Type Safety Notes

- For editable include templates (for example `sf4.editor`, `sf4.script`), writes may target real files.
- Restrict and validate file paths before saving.
- Treat include-backed values as code changes, not just content changes.

## Save Cycle Checklist

1. Schema loaded and parsed without duplicate keys.
2. Submitted values normalized by type (checkbox/link/file/map/etc.).
3. Values persisted to expected file location.
4. UI reload reflects saved state.
5. Runtime code reads updated values correctly.

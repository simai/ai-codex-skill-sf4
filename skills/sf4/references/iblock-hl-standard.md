# Iblock and HL-Block Standard (SF4)

## Scope

Use this standard when creating or modernizing data entities for SF4 projects:

- Bitrix infoblocks and infoblock types.
- Highload blocks (HL-blocks) used as registries/references.
- SF4 integration points (`simai:sf.iblock.*`, `simai:sf.highloadblock.grid`, wizard actions, config schemas).

## Baseline Requirements

- Bitrix modules:
  - `iblock` required.
  - `highloadblock` required for HL entities.
- SIMAI modules:
  - `simai.framework` required.
  - `simai.property` recommended for unified field rendering.
  - `simai.property4field` / `simai.property4iblock` when project uses them.

## Naming Conventions

Follow project conventions and keep names stable across environments.

Observed SF4 patterns in this workspace:

- Iblock type: `sf_<SITE_ID>_<domain>` (example: `sf_s1_content`, `sf_s1_catalog`).
- Iblock code: `sf-<SITE_ID>-<entity>` (example: `sf-s1-news`, `sf-s1-service`).

For multisite map modules, keep two separated type domains:

- Object data type: `sf_<SITE_ID>_map_data`.
- Reference type: `sf_<SITE_ID>_map_ref`.
- Object/reference iblocks under these types must follow `sf-<SITE_ID>-<suffix>` (for example `sf-ru-map-education`, `sf-ru-mo`).
- Normalize site code before build: lowercase latin/digits, separators only (`_` in type id, `-` in iblock code).

Guidelines:

- Use lowercase latin symbols, digits, `_` and `-`.
- Use semantic singular/plural consistently per project policy.
- Prefer code-based references (`IBLOCK_CODE`) for migration safety.

## Creation Checklist For New Iblock

1. Define purpose and usage surface:
   - list/detail/section/table/calendar/filter.
2. Define type and code using project naming pattern.
3. Define required fields/properties.
4. Add/edit editor schema:
   - `{site_dir}/simai.data/config/.iblock.config.php`
   - `{site_dir}/simai.data/config/.iblock.section.config.php`
5. Add localization keys in config language files.
6. Bind in SF4 blocks/components via `IBLOCK_TYPE` + `IBLOCK_CODE`.
7. Validate in target pages and editor forms.

## Creation Checklist For New HL-Block

1. Define table purpose and field model.
2. Create HL-block and UF fields.
3. Expose read model via `simai:sf.highloadblock.grid` when table UI is needed.
4. Configure linked HL/user field mappings in component parameters.
5. Validate filters/sorts/pagination and link rendering.

## Migration and Packaging Standard

Use wizard archive workflows for portable delivery:

- Import:
  - `iblock.import.archive`
  - `iblock.import.archive.sveden` (for project-specific packages).
- Export:
  - `iblock.export.archive`

HL data support is implemented in archive action classes. Use package tests in controlled environment before production rollout.

## Integration Contract

For each new entity, define:

1. Source of truth:
   - code/type/table name.
2. Rendering points:
   - which SF4 blocks/views/components consume entity.
3. Editor points:
   - which config schema and forms edit entity fields.
4. Migration path:
   - wizard action chain and package files.
5. Rollback plan:
   - backup + reversible changes.

## Validation Checklist

1. Entity exists and resolves by code/type.
2. All component references work (`IBLOCK_TYPE`, `IBLOCK_CODE`, HL ID/field mapping).
3. Editor forms render and save expected fields.
4. Wizard import/export passes in test environment.
5. Cache cleared and frontend reflects updated data.
6. For HL-backed navigation or page structures that are projected into cached
   runtime arrays, validate the projection itself: parent-child order, sibling
   order by `SORT`, page/section links, and cache refresh. Do not accept a
   portal/menu fix based only on the HL rows existing or the page returning
   `200`.

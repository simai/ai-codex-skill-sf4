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

For new editable project content in an SF4 site, use the same convention unless
the source solution already has a stricter domain convention:

- Iblock type: `sf_<SITE_ID>_<domain>` where `<domain>` describes the content
  family (`content`, `home`, `help`, `catalog`, `org`, etc.).
- Iblock code: `sf-<SITE_ID>-<entity>` where `<entity>` describes the rendered
  object (`hero`, `process-step`, `shelter`, `review`, `news`, etc.).

For multisite map modules, keep two separated type domains:

- Object data type: `sf_<SITE_ID>_map_data`.
- Reference type: `sf_<SITE_ID>_map_ref`.
- Object/reference iblocks under these types must follow `sf-<SITE_ID>-<suffix>` (for example `sf-ru-map-education`, `sf-ru-mo`).
- Normalize site code before build: lowercase latin/digits, separators only (`_` in type id, `-` in iblock code).

Guidelines:

- Use lowercase latin symbols, digits, `_` and `-`.
- Use semantic singular/plural consistently per project policy.
- Prefer code-based references (`IBLOCK_CODE`) for migration safety.

HL/user field naming:

- HL-block class/code names should use the stable SF prefix without separators
  when the target Bitrix API expects a PHP-like class identifier (for example
  `SFPortalStructure`). Do not force `_` or `-` into HL class names.
- HL table names should be lowercase and stable, with separators between site,
  project, and entity parts where the target table naming policy allows them
  (for example `sf_portal_structure` or a stricter project-specific variant).
- User field codes for SF-owned HL entities should use the `UF_SF_` prefix.
- Treat older portal course examples as naming source maps, not as a reason to
  override a stricter current project convention.

## Creation Checklist For New Iblock

1. Define purpose and usage surface:
   - list/detail/section/table/calendar/filter.
2. Check existing solution iblock types and iblocks first. Reuse or extend an
   existing matching entity when it already represents the same content family.
3. If no suitable entity exists, define a new type and code using the SF4
   project naming pattern.
4. Define required fields/properties.
5. Add/edit editor schema:
   - `{site_dir}/simai.data/config/.iblock.config.php`
   - `{site_dir}/simai.data/config/.iblock.section.config.php`
6. Add localization keys in config language files.
7. Bind in SF4 blocks/components via `IBLOCK_TYPE` + `IBLOCK_CODE`.
8. Prefer standard SF4 rendering components (`simai:sf.iblock.list`,
   `simai:sf.iblock.detail`, `simai:sf.iblock.section`, filters/tables) before
   writing custom `CIBlockElement` loops.
9. Validate in target pages and editor forms.

## Creation Checklist For New HL-Block

1. Define table purpose and field model.
2. Define HL class/code, table name, and `UF_SF_` field codes before creating
   the entity.
3. Create HL-block and UF fields.
4. Expose read model via `simai:sf.highloadblock.grid` when table UI is needed.
5. Configure linked HL/user field mappings in component parameters.
6. Validate filters/sorts/pagination and link rendering.

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

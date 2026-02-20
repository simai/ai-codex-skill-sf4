# Config, Property, and Data Rules

## Config Schemas

Primary schema files:

- `{site_dir}/simai.data/config/.site.config.php`
- `{site_dir}/simai.data/config/.structure.config.php`
- `{site_dir}/simai.data/config/.demo.config.php`
- `{site_dir}/simai.data/config/.iblock.config.php`
- `{site_dir}/simai.data/config/.iblock.section.config.php`

Language labels:

- `{site_dir}/simai.data/config/lang/<lang>/...`

## Value Storage

- Site-level values:
  - `{site_dir}/simai.data/.site.property.php`
- Section and page values:
  - `/{site_path}/.property.php` across section tree
- Session/user overrides:
  - merged in runtime by SF4 property service

Precedence:

- user > page > section > site

## Runtime Merge Point

Project template usually includes:

- `{site_dir}/simai.data/template/property.php`

This file merges:

- site property
- recursive section property
- page property
- user/session property
- optional global property overrides

## Iblock and Section Editor Schemas

Use:

- `.iblock.config.php` for element edit forms
- `.iblock.section.config.php` for section edit forms

Field declarations usually include:

- `name`
- `type` (`string`, `number`, `datetime`, `file`, `list`, `checkbox`, `html`, `entity`, ...)
- optional `template`, `multiple`, `condition`, `parameter`

## Asset Strategy

For this workspace, project-level assets are loaded through:

- `{site_dir}/simai.data/template/style.php`
- `{site_dir}/simai.data/template/js.php`

System asset registry exists in:

- `/simai/config/.asset.config.php`

Treat project `simai.data/config/.asset.config.php` as optional and verify actual runtime usage before relying on it.

## Settings Change Checklist

1. Update schema in the correct `*.config.php` file.
2. Update values in `.site.property.php` or section/page `.property.php`.
3. Ensure related view/block folders exist when changing `grid_view_*`.
4. Verify permissions allow writing in `simai.data`.
5. Clear relevant cache and retest.


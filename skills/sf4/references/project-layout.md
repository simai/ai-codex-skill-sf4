# SF4 Project Layout

## Path Mapping Example

- Site root: `<site_root>`
- Active site dir example: `<site_dir>` (for example `/ru`)
- Project data layer: `<site_root>/<site_dir>/simai.data`
- Project template entrypoint: `<site_root>/<site_dir>/simai.data/template/template.php`
- System template loader: `<site_root>/local/templates/simai.framework/header.php` and `<site_root>/local/templates/simai.framework/footer.php`
- Compatibility note: `<site_root>/bitrix/templates/simai.framework` can be an alias/shortcut instead of a physical directory in some deployments.
- Framework module: `<site_root>/local/modules/simai.framework`
- System block library: `<site_root>/simai/block`
- Wizard actions: `<site_root>/simai/wizard/action`

## Canonical Layer Model

- System layer (updateable):
  - `/simai`
  - `/bitrix/templates/simai.framework`
  - `/bitrix/components/simai`
  - `/local/modules/simai.framework` (module source)
- Project layer (safe customization target):
  - `{site_dir}/simai.data`
  - `/{site_dir}/.property.php` in section/page tree

## Key Project Directories Under `simai.data`

- `template/`:
  - `template.php`, `style.php`, `js.php`, `panel.php`, `property.php`
  - `area/<area>/template.php` selectors for header/footer/main/sidebar and service/script areas
- `grid/`:
  - `view/<area>/<code>/template.php`
  - `block/<section>/<code>/template.php`
- `config/`:
  - `.site.config.php`, `.structure.config.php`, `.demo.config.php`
  - `.iblock.config.php`, `.iblock.section.config.php`
- `.site.property.php`: site-level values, including `grid_view_*`

## Runtime Binding Chain

1. Site template calls `simai.data/template/template.php`.
2. `template/property.php` merges site, section, page, and user properties.
3. Template area files choose active view code via `Property::getValue(SF_SITE_DIR, 'grid_view_*')`.
4. Selected view file calls `simai:sf.grid`.
5. Grid resolves block templates from `simai.data/grid/block/<section>/<code>/`.

## Fast Integrity Checklist

- `simai.data/.site.property.php` exists.
- `simai.data/config/.site.config.php` and `.structure.config.php` exist.
- `simai.data/template/template.php` exists and includes `style.php`, `js.php`, `property.php`.
- Every `grid_view_*` code in `.site.property.php` has matching `grid/view/.../<code>/template.php`.
- Every block referenced by a view exists in `grid/block/<section>/<code>/`.

# SF4 Backend Source Map (`/ru/bx`)

## Goal

Use `/ru/bx` as a primary backend knowledge base for SF4 project implementation, modernization, and regression-safe fixes.

Reference root:

- `https://sf4.simai.pro/ru/bx/`

## High-Value Sections

### `storage` (highest priority for backend data workflows)

Core pages:

- `storage/index.php`
- `storage/api.php`
- `storage/etinity.php`
- `storage/sample.php`
- `storage/complex.php`

Use when:

- designing data model on `simai.storage`;
- implementing CRUD, property logic, sets, search, events;
- replacing/avoiding iblock/HL where storage is the project standard.

### `property`

Core pages/files:

- `property/index.php`
- `property/.config.php`
- `property/.value.php`

Use when:

- building and maintaining universal settings forms (`simai:sf.property.edit`);
- defining field types, templates, conditions, and include/entity parameters.

### `structure`

Core pages:

- `structure/structure.php`
- `structure/configuration.php`
- `structure/include.php`
- `structure/menu.php`

Use when:

- clarifying layer boundaries (`/simai`, `simai.data`, module layer);
- resolving settings-level precedence and config file ownership.

### `api`

Core pages:

- `api/constant.php`
- `api/asset_load.php`

Use when:

- applying `SF_*` constants correctly;
- loading frontend packages through `SIMAI\Main\Page\Asset::load()`.

### `components`

Core pages:

- `components/sfgrid.php`
- `components/sfiblocklist.php`
- `components/sfiblockdetail.php`

Use when:

- implementing component-level behavior;
- using modern `sf.grid` editor features (presets, dnd order, categories, modifier editor).

### `guides`

Core pages:

- `guides/iblock-type-iblock-code.php`
- `guides/domcontentloaded.php`
- `guides/public-editor-position-relative.php`

Use when:

- avoiding common integration regressions during updates and template refactors.

## Suggested Read Order By Task

1. Unknown backend behavior:
   - `structure/*` then `api/*`.
2. Data entity implementation:
   - `storage/*`, then `property/*`.
3. Grid/component behavior:
   - `components/sfgrid.php` and `components/sfiblock*.php`.
4. Pre-release sanity:
   - `guides/*` mandatory pass.

## Companion References In This Skill

- `references/storage-api-playbook.md`
- `references/property-editor-playbook.md`
- `references/sfgrid-editor-features.md`
- `references/backend-critical-guides.md`

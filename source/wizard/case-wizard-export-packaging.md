# Wizard Export Packaging Sample

Source sample:

```text
/Users/rim/Downloads/wizard.export/wizard.export
```

This sample is a compact SF4 universal master used by developers to package a solution into a `.last_version` install tree. It is useful as a baseline for SF4 solution export/packaging requests, but it is not a ready-to-run master in the current inspected environment without adaptation.

## File Inventory

```text
wizard.export/
  index.php
  .wizard.config.php
  .property.config.php
  .htaccess
  config/
    .test.data.php
    .test.save.data.php
  image/
    bg_sf.png
    bg_space.jpg
    city_bg.jpg
    space_2_bg.jpg
    wizard_bg.jpg
```

There is no `data/` directory in the sample. The master builds an output tree under the target document root:

```text
/.last_version/
  install/
    bitrix/
    iblock/
    ru/
      config/
      php_interface/
      root/
      site/
```

## Launcher Contract

`index.php` is a standard `simai:sf.wizard` launcher:

- includes `prolog_before.php`;
- loads `simai.framework`;
- resolves `$dirWizard = Wizard::getLocal(__DIR__)`;
- passes `WIZARD_DIR`, `WIZARD_TEMP_DIR`, `WIZARD_CONFIG_FILE`;
- runs AJAX mode with `AJAX_TIME_STEP=5`, `AJAX_TIME_INTERVAL=2`, `CACHE_TYPE=N`.

For a new SF4 packaging master, this launcher is a valid starting shape.

## Visual Contract

`.wizard.config.php` description defines:

- `name`: `Мастер упаковки`;
- `code`: `wizard_export`;
- `stage_renew`: `Y`;
- `logo`: `image/bg_space.jpg`;
- `background.image`: `image/city_bg.jpg`;
- `background.color`: `#263238`;
- `color.primary`: `#E53935`;
- `color.secondary`: `#2196F3`;
- SF4 modifier classes for page body, wrapper, action area, navigation and copyright.

The sample confirms that packaging masters can use the same visual controls as install/import masters. Visual configuration stays in `.wizard.config.php`, not in a legacy Bitrix wrapper wizard.

## Action Chain

The inspected chain has 18 active actions:

| # | Action | Purpose | Risk |
|---|---|---|---|
| 1 | `file.copy` | Copy module/framework/components/templates/support modules/media/wizard into `/.last_version/install/...` | filesystem write |
| 2 | `site.export.data` | Export site settings into wizard data storage | read/export |
| 3 | `mail.export.data` | Export mail event data into wizard data storage | read/export |
| 4 | `mail-templates.export.data` | Export mail templates into wizard data storage | read/export |
| 5 | `usergroup.export.data` | Export selected user group settings | read/export |
| 6 | `iblocktype.export.data` | Export iblock type definitions | read/export |
| 7 | `option.export.data` | Export selected module options | read/export |
| 8 | `file.copy` | Copy public files and `urlrewrite.php` into `/.last_version/install/ru/...` | filesystem write |
| 9 | `iblock.export.archive` | Export all non-`delete` iblocks into archive folder | archive export |
| 10 | `data.export.file` | Write site settings storage to `.site.config.php` | filesystem write |
| 11 | `data.export.file` | Write mail event storage to `mail.config.php` | filesystem write |
| 12 | `data.export.file` | Write mail template storage to `mail-templates.config.php` | filesystem write |
| 13 | `data.export.file` | Write user group storage to `.usergroup.config.php` | filesystem write |
| 14 | `data.export.file` | Write module option storage to `.option.config.php` | filesystem write |
| 15 | `data.export.file` | Write iblock type storage to `.iblocktype.config.php` | filesystem write |
| 16 | `file.create` | Create `ru/php_interface/dbconn.add.php` with `SF_SOLUTION` constant | filesystem write |
| 17 | `file.encode.win1251` | Convert language files in `/.last_version/` | filesystem write |
| 18 | `info` | Finish message | read-only |

The sample has commented final steps for `file.zip` and `file.delete`. A production-grade packaging master should make archive creation explicit and keep cleanup disabled until the generated tree is verified.

## Packaging Lessons

- The export master is source-site oriented: it reads/copies from a working Bitrix/SF4 installation and builds a distributable install tree.
- The output path `/.last_version` is hard-coded. For SF4 skill use, prefer a parameterized or documented output directory and never run against a live site without backup/rollback.
- `CIBlock::GetList()` is used to export every iblock except type `delete`. For reusable packaging, the iblock list should usually be explicit or filtered by solution prefix.
- The master packages both code/files and dynamic data. This makes it a better baseline for full solution packaging than import-only masters.
- `data_output_code` and `data_input_code` form a storage pipeline: export action writes named storage, then `data.export.file` persists that storage into install config files.
- `file.create` can generate package-level PHP interface snippets, but these snippets must be merged on install; blind overwrite of `php_interface` files is unsafe.
- `file.encode.win1251` is legacy marketplace/distribution hygiene. Use it only when the target distribution requires win1251 language files.

## Current Audit Result

Read-only audit evidence:

```text
source/output/wizard-audit/wizard-export-sample.json
source/output/wizard-readiness/wizard-export-sample.json
source/output/wizard-readiness/wizard-export-sample.md
```

Summary after validator update:

- actions: 18;
- errors: 5;
- warnings: 1;
- missing action files: 2;
- missing payloads: 3;
- high-risk side effects: 10;
- readiness: `blocked`;
- controlled execution: `false`.

Current blockers in the inspected environment:

- `mail.export.data` action file was not found in the available global action libraries.
- `mail-templates.export.data` action file was not found in the available global action libraries.
- `/bitrix/modules/simai.sf4conf` source module was not present under the chosen site root.
- `/bitrix/modules/simai.filebackup` source module was not present under the chosen site root.
- `/bitrix/wizards/simai/simai.sf4conf` source wizard was not present under the chosen site root.
- `data/` directory is absent in the sample, which is acceptable for this export-master shape but should stay visible.

## Specialist Rule

When a user asks to package an SF4 solution through the universal master, use this sample as the export-chain baseline:

1. Inventory source solution code, public files, templates, modules, media, iblocks, HL blocks, mail events, options and site settings.
2. Replace hard-coded `simai.sf4conf`, `/ru`, `/.last_version` and full-iblock export assumptions with the requested solution scope.
3. Ensure every action code exists in the target action library or add a reviewed master-local action.
4. Generate into a controlled output directory first.
5. Validate package tree, archives and generated config files before zipping.
6. Keep `file.zip` and cleanup as separate reviewed steps.
7. Run `sf4_wizard_audit.py`, `sf4_wizard_readiness.py` and rollback-plan checks before any execution outside a disposable environment.

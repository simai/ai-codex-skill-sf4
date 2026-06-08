# Universal Wizard Action Contracts

This file captures action-level contracts from the inspected SF4 universal wizard sources.

Primary evidence:

- `/Users/rim/Sites/university.test/simai/wizard/action`
- `/Users/rim/Sites/sf4.test/simai/wizard/action`
- `/Users/rim/Sites/sf4.test/simai/wizard/master/simai.sveden/.wizard.config.php`
- `skills/sf4/references/wizard-actions.md`
- `skills/sf4/references/system-layer-simai.md`

## Contract Template

For every action, capture:

- `code`: action folder name and config code. Must match the folder.
- `entry`: required `action.php`; optional `ajax.php`, `class.php`, `classes.php`.
- `input`: data read from `$arResult["DATA"][DATA_INPUT_CODE]` or direct `PARAMETER` references.
- `output`: writes to `ACTION.OUTPUT` and optionally `$arResult["DATA"][DATA_OUTPUT_CODE]`.
- `parameters`: expected `.wizard.config.php` `parameter` shape.
- `side effects`: filesystem, database, options, URL rewrite, module registration, property storage.
- `progress`: stage status and counters/state keys.
- `ajax`: whether execution is in stage polling or action-local AJAX.
- `requirements`: Bitrix modules, SF4 modules, PHP extensions, admin rights.
- `idempotency`: rerun behavior and duplicate risk.
- `rollback`: practical rollback boundary.
- `failure modes`: evidence-backed checks before execution.

## Priority Action Table

| Action | Input | Output | Parameters | Side effects | Progress/AJAX | Requirements | Idempotency | Rollback |
|---|---|---|---|---|---|---|---|---|
| `iblock.import.archive` | Optional selected site from `DATA_INPUT_CODE`, usually `site_config.site`. Existing `DATA_OUTPUT_CODE` is used as completed-file map. | `DATA[DATA_OUTPUT_CODE][SOURCE] = SOURCE` per imported archive; final `STAGE.STATUS = SUCCESS` via AJAX success call. | Array of rows: `SOURCE`, `DESTINATION`, `SITE`. `SOURCE` is archive path, `DESTINATION` is iblock type, `SITE` target site id. | Creates/updates iblock types, iblocks, properties, enum values, section UFs, sections, elements, prop values, section-element links, rights, messages, SEO, fields, forms, highload blocks. | `action.php` prints JS queue; `ajax.php` imports each archive; final AJAX request with `success=y` marks stage success. No stage counter; queue index lives in browser JS. | Admin user, `simai.framework`, `iblock`, `XMLReader`, `ZipArchive`, import class file. | Partially idempotent only if class update logic matches by XML/code; rerun can overwrite/update and may duplicate where matching keys are weak. Completed-file map exists but the skip check is commented in inspected action. | Restore DB backup for iblocks/HL/options; remove imported iblocks/HL manually only if package scope is known. Keep archive list as rollback inventory. |
| `iblock.export.archive` | Direct action parameters; no required wizard input. Can write to `DATA_OUTPUT_CODE`. | `DATA[DATA_OUTPUT_CODE][IBLOCK_CODE] = IBLOCK_CODE`; final `STAGE.STATUS = SUCCESS` via AJAX success call. | `DESTINATION` folder path relative to document root; `IBLOCK` array of iblock codes to export. | Writes XML and zip archive files into destination folder. Exports iblock metadata, properties, enums, section UFs, sections, elements, files, rights, messages, SEO, forms, fields and highload blocks. | `action.php` prints JS queue; `ajax.php` exports one iblock per AJAX call; final success AJAX marks stage success. | Admin user, `simai.framework`, `iblock`, `XMLReader`, `ZipArchive`, writable destination directory. | Re-running overwrites or recreates export files for the same iblock code; safe for packaging if destination is clean. | Delete generated archive/XML files. No DB rollback needed for export itself. |
| `iblockconfig.import.data` | Reads site id by parameter indirection: `PARAMETER.SITE.ARRAY` and `PARAMETER.SITE.KEY`, commonly `site_config.site`. | Normally no business output; writes lower-cased `ACTION.OUTPUT` if configured. | `SITE` map with `ARRAY`/`KEY`; `FILE.IBLOCK.CONFIG`, `FILE.IBLOCK.LANG`; optional `FILE.IBLOCKSECTION.CONFIG`, `FILE.IBLOCKSECTION.LANG`; `FILE.TMP`. | Merges wizard config arrays into target site `simai.data/config/.iblock.config.php`, `lang/ru/.iblock.config.php`, optionally `.iblock.section.config.php` and language file. Uses tmp files and escapes/restores `Loc::getMessage(...)` calls. | Synchronous in `action.php`; sets `SUCCESS` or `ERROR`. | Admin user, `simai.framework`, `iblock`, existing target site, existing target config/lang files, readable wizard config files, writable target config directory. | Re-run merges arrays again using `array_merge`; same keys are overwritten by wizard values. Safe when package keys are stable, risky if target custom keys collide. | Restore previous `simai.data/config` files from backup or VCS. Tmp files are not enough as rollback. |
| `file.copy` | Optional `DATA_INPUT_CODE` array for placeholder replacement in destination, for example `#dir#` or `#site#`. | Usually no output; writes lower-cased `ACTION.OUTPUT` if configured. | Array of copy rows: `SOURCE`, `DESTINATION`, optional `REWRITE = N`, optional `NAME`. Paths pass through `Wizard::getRoot`. | Copies files/directories with `CopyDirFiles`. May overwrite destination unless `REWRITE=N`. | Stage-polling action with `ACTION.DATA.STEP_COPY`; continues as `WORK` until all rows processed. | Admin user, `simai.framework`, all source paths must exist, destination parent must be writable. | Re-run is safe only when overwrite is intended. With `REWRITE=N`, existing files remain; with overwrite, user changes can be replaced. | Restore copied destination files from backup; for additive copies, remove known copied paths. |
| `replace.code` | Requires `DATA_INPUT_CODE` with at least `site`; also uses target site's `DIR` from `CSite`. | Usually no output; writes lower-cased `ACTION.OUTPUT` if configured. | Inspected action ignores row contents and scans calculated directories. Config still declares `parameter` for stage metadata. | Recursively edits writable PHP files under `/simai/grid/` and under each first-level directory of the selected site except `bitrix`, `upload`, `simai`. Replaces `sf_ru_` with `sf_<site>_` and `sf-ru-` with `sf-<site>-`. | Stage-polling action with `ACTION.DATA.STEP_COPY` over discovered directories. | Admin user, `simai.framework`, valid Bitrix site, writable PHP files. | Not generally reversible because it rewrites all matching PHP content. Re-running for the same site is mostly no-op after replacement; running for a different site can produce mixed codes. | Restore changed PHP tree from backup/VCS. Prefer dry inventory before live execution. |

## Additional Core Actions To Contract Next

These actions are already observed in `simai.sveden` and module packages and should be promoted into the table after source review:

- `site.choice.sveden`: collects selected site, directory, SF4 mode and rename flag; gates the Next button and writes `site_config`.
- `site.update.sveden`: updates/creates site/template binding for the selected target.
- `urlrewrite.add`: reads config payload and adds Bitrix rewrite rules adapted to selected site directory.
- `data.import.file`: includes a PHP array payload and writes it to `ACTION.OUTPUT`, optionally applying input overlays.
- `option.import.data`: writes Bitrix options from imported data through `COption::SetOptionString`.
- `shortlink.import.data`: imports shortlink data used by solution routes.
- `iblocktype.import.data`: creates missing iblock types and rewrites `_ru_` type ids to selected site id where needed.
- `file.rename`, `file.create`, `file.delete`, `file.zip`, `file.unzip`: file operation actions with rollback risk proportional to overwrite/delete behavior.

## Long-Running Action Patterns

Two different long-running patterns exist:

1. Stage polling:
   - action stores progress in `$arResult["ACTION"]["DATA"]`;
   - action leaves `STAGE.STATUS = WORK`;
   - `simai:sf.wizard.stage` epilog reloads the same stage until status becomes `SUCCESS`;
   - examples: `file.copy`, `replace.code`, `file.zip`, `file.unzip`.

2. Action-local AJAX:
   - `action.php` renders JS queue and disables/enables navigation;
   - `ajax.php` performs each unit of work;
   - final `success=y` request updates persisted wizard state to `SUCCESS`;
   - examples: `iblock.import.archive`, `iblock.export.archive`.

Specialist rule: do not convert one pattern into the other without checking template navigation behavior and persisted state writes.

## Data Key Rules

- `DATA_INPUT_CODE` means the action receives `$arResult["DATA"][<code>]`.
- `DATA_OUTPUT_CODE` means action output is copied to `$arResult["DATA"][<code>]`.
- Some actions use `PARAMETER` indirection instead of `DATA_INPUT_CODE`; for example `iblockconfig.import.data` reads `PARAMETER.SITE.ARRAY/KEY`.
- The wizard runtime normalizes config keys to uppercase, while many action outputs are lowered by `Wizard::setArrayKeyLow`.
- Site-aware packages commonly pass `site_config` with keys: `site`, `dir`, `sf4`, `rename_public`, `master`.

## Safety Rules

- Always require admin context for these inspected actions; each priority action checks `$USER->IsAdmin()`.
- Treat DB-writing actions as backup-required in live/staging environments.
- For archive import/export, verify `XMLReader` and `ZipArchive` before presenting the action as executable.
- Before `file.copy`, `replace.code`, `file.rename` or delete-like actions, capture exact source/destination inventory.
- Before `iblockconfig.import.data`, save current `simai.data/config` files.
- Before `iblock.import.archive`, list every archive and expected iblock/highload object.

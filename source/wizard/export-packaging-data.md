# Export And Data Packaging Notes

This file focuses on how to prepare data before it is consumed by a universal wizard.

## `iblock.export.archive` Purpose

`iblock.export.archive` is the inspected action that creates archive payloads for later `iblock.import.archive` use.

Observed files:

- `/Users/rim/Sites/university.test/simai/wizard/action/iblock.export.archive/action.php`
- `/Users/rim/Sites/university.test/simai/wizard/action/iblock.export.archive/ajax.php`
- `/Users/rim/Sites/university.test/simai/wizard/action/iblock.export.archive/class.php`

## Required Parameters

In `.wizard.config.php` the action expects:

```php
"parameter" => array(
    "destination" => "/path/relative/to/document/root/",
    "iblock" => array(
        "sf-ru-news",
        "sf-ru-document",
    ),
)
```

Runtime normalization makes keys uppercase inside the action:

- `PARAMETER.DESTINATION`
- `PARAMETER.IBLOCK`

## Export Runtime Flow

1. `action.php` validates:
   - `DESTINATION` exists and is a directory under `$_SERVER["DOCUMENT_ROOT"]`;
   - `IBLOCK` list exists;
   - PHP classes `XMLReader` and `ZipArchive` exist.
2. `action.php` renders a JavaScript queue from `PARAMETER.IBLOCK`.
3. For each iblock code, JS posts to `ajax.php`:
   - `wizard`;
   - `output`;
   - `URL_DATA_FILE_FOLDER`;
   - `IBLOCK_CODE`.
4. `ajax.php` resolves the real iblock by `CODE`.
5. `ajax.php` creates `SimaiIblockXMLPack` and calls:
   - `Init`;
   - `StartExport`;
   - `ExportIblocks`;
   - `ExportProperties`;
   - `ExportPropEnums`;
   - `ExportSectionUF`;
   - `ExportSections`;
   - `ExportElements`;
   - `ExportPropValues`;
   - `ExportSectionElements`;
   - `ExportRights`;
   - `ExportMessages`;
   - `ExportSEO`;
   - `ExportForms`;
   - `ExportFields`;
   - `ExportHB`;
   - `EndExport`;
   - `ZipExport`.
6. `ajax.php` writes `DATA[DATA_OUTPUT_CODE][IBLOCK_CODE] = IBLOCK_CODE`.
7. Final AJAX call with `success=y` sets `STAGE.STATUS = SUCCESS`.

## What Gets Exported

The class function map shows support for:

- iblock metadata;
- properties;
- property enum values;
- section user fields;
- sections;
- elements;
- element files;
- element property values;
- section-element links;
- rights;
- messages;
- SEO settings;
- forms;
- fields;
- highload blocks.

The presence of `ExportHB` and `ExportHblockHB` means this archive path is highload-aware. A specialist should prefer it over hand-built partial data when a package must include HL structures tied to the solution.

## Destination Rules

- Destination must already exist before action execution.
- It is relative to document root in config, then resolved as `$_SERVER["DOCUMENT_ROOT"] . DESTINATION`.
- For clean packages, use a dedicated temporary export directory, then move only validated `*.zip` archives into `data/iblock`.
- Do not export directly into a production module source folder without reviewing generated files.

## Naming Rules

Observed universal packages store exported archives as:

- `data/iblock/sf-ru-news.zip`;
- `data/iblock/sf-ru-document.zip`;
- `data/iblock/form-appeal-common.zip`;
- `data/iblock/sf-org-link.zip`.

Recommended rule:

- archive filename should match source iblock code;
- package can keep canonical `sf-ru-...` names and let import/replace flow adapt to target site;
- if the package targets a fixed non-RU site, document the transformation explicitly in `.wizard.config.php`.

## Highload Packaging

When highload blocks are needed:

1. Use `iblock.export.archive` from an environment where the HL definitions and rows are already correct.
2. Confirm the export class included `ExportHB`.
3. Import the archive in a disposable target and confirm `SetImportHblocks` creates/updates expected highload blocks.
4. Record HL entities in the package manifest or master notes; archive filenames alone do not reveal all included HL payloads.

## Verification Before Shipping An Archive

For each archive:

- file exists in `data/iblock`;
- filename is referenced by `.wizard.config.php` `SOURCE`;
- target `DESTINATION` iblock type is correct;
- target `SITE` is present or derived from `site_config.site`;
- archive opens with `ZipArchive`;
- expected XML file exists inside archive;
- source environment had all required files in `/upload` if elements reference files;
- package was smoke-imported in a disposable Bitrix/SF4 environment.

## Export Playbook

1. Prepare a source site with correct iblocks, sections, elements, forms, SEO, rights and HL rows.
2. Create or use an export master/action with `iblock.export.archive`.
3. Set `DESTINATION` to a clean writable export folder.
4. List iblock codes in `PARAMETER.IBLOCK`.
5. Run export as admin in a non-production environment.
6. Move generated archives into the module/master package:
   - universal master: `data/iblock/*.zip`;
   - installer source: `install/iblock/*.zip` or `install/wizard/data/iblock/*.zip` depending on packaging shape.
7. Update `.wizard.config.php` import action list.
8. Run import smoke in a clean target.
9. Save evidence: archive list, expected iblock types/codes, target site transformation, HL presence.

## Full Solution Export Chain

The developer `wizard.export` sample shows a broader export chain for packaging a whole SF4 solution into `/.last_version/install`:

```text
file.copy
site.export.data
mail.export.data
mail-templates.export.data
usergroup.export.data
iblocktype.export.data
option.export.data
file.copy
iblock.export.archive
data.export.file x6
file.create
file.encode.win1251
info
```

Use this as the baseline when the packaging target is a distributable solution package, not only `data/iblock/*.zip`.

Important distinctions:

- `*.export.data` actions read current Bitrix/SF4 state and place normalized data into wizard storage via `data_output_code`.
- `data.export.file` consumes that storage via `data_input_code` and writes generated PHP config files into the output install tree.
- The output files named in `data.export.file` are generated artifacts, not required source payloads.
- `iblock.export.archive` produces archive payloads for later import masters and can include highload data through the inspected export class.
- `file.copy` stages are source-site dependent and must be scoped before use; copying all framework, module, component, media and public files is too broad for many reusable SF4 packages.

For SF4 productized packaging, prefer:

- explicit module/component/template/public path allowlists;
- explicit iblock code allowlists;
- controlled output directory;
- audit/readiness/rollback evidence before enabling final `file.zip` or cleanup.

## Export Failure Modes

- Destination directory missing.
- Iblock code cannot be resolved to `IBLOCK_ID`.
- `XMLReader` or `ZipArchive` missing.
- Source files referenced by elements are absent or unreadable.
- Large data set causes browser/AJAX interruption; rerun may leave partial output files.
- HL export succeeds but target import lacks required Bitrix highload module or field types.

## Legacy Data Conversion Note

Legacy packages (`simai.fund`, `simai.educenter`, `simai.school`) store iblock/HL demo data as PHP arrays. To convert them into archive-based universal master packages:

1. Install legacy data into a disposable Bitrix environment.
2. Verify generated iblocks and highload blocks.
3. Use `iblock.export.archive` against the resulting real entities.
4. Replace legacy PHP-array import stages with `iblock.import.archive` stages.
5. Keep original PHP-array source as provenance until the archive import is verified.

# Action Library Inventory

## Source Coverage

`university.test` contains 46 action folders.

`sf4.test` contains 14 action folders focused on the compact `simai.sveden` installation/update flow.

## Action Families

### User Input And Choice

- `agreement`
- `dir.choice`
- `language.choice`
- `site.choice`
- `site.choice.install`
- `site.choice.sveden`

Purpose: collect operator choices and write them into the shared wizard `DATA` bus.

Important pattern: these actions often render form controls and use AJAX to write selected values into `Property` before enabling Next.

### File And Directory Operations

- `dir.make`
- `file.add`
- `file.copy`
- `file.create`
- `file.delete`
- `file.encode.win1251`
- `file.rename`
- `file.unzip`
- `file.zip`

Purpose: prepare filesystem payload, copy public files/templates, rename existing sections, create files, pack/unpack archives.

Important pattern: long operations use action-local step counters such as `STEP_COPY`, `STEP_ZIP`, `STEP_UNZIP`.

### Data And Option Storage

- `data.add.config`
- `data.add.property`
- `data.export.file`
- `data.import.file`
- `option.export.data`
- `option.import.data`
- `shortlink.export.data`
- `shortlink.import.data`
- `usergroup.export.data`
- `usergroup.import.data`

Purpose: move structured arrays between files, Bitrix options, short links, groups and the wizard shared data bus.

Important pattern: `data.import.file` requires a PHP file returning an array, then optionally overlays input values into each nested output row.

### Site Operations

- `site.create`
- `site.export.data`
- `site.import.data`
- `site.translate`
- `site.update`
- `site.update.sveden`

Purpose: create/update Bitrix site records, copy or translate site payload, apply templates and site settings.

Important pattern: site-aware actions use `CSite` and selected `site_config`.

### URL And Code Migration

- `prepare.urlrewrite`
- `urlrewrite.add`
- `replace.code`
- `cut.names`
- `restore.names`
- `redirect`

Purpose: update URL rewrite rules, rewrite generated code placeholders, adapt `sf_ru_*` and `sf-ru-*` codes to selected site, and route final steps.

Important pattern: `replace.code` recursively scans writable PHP files and replaces codes such as `sf_ru_` -> `sf_<site>_`.

### Iblock And Highloadblock Operations

- `iblock.export.archive`
- `iblock.import.archive`
- `iblock.import.archive.sveden`
- `iblock.translate`
- `iblockconfig.import.data`
- `iblocksection.import.data`
- `iblocktype.export.data`
- `iblocktype.import.data`

Purpose: export/import Bitrix iblock and highloadblock structures, merge edit-form config, translate iblock content and create type definitions.

Important patterns:

- imports require `XMLReader`, `ZipArchive`, and sometimes `DOMDocument`;
- archive imports use an action-specific `ajax.php`;
- import class handles iblocks, properties, enums, section UFs, sections, elements, rights, messages, SEO, fields, forms and highloadblocks;
- `iblockconfig.import.data` merges existing project config with wizard config through temporary files and `Loc::getMessage` escaping.

### Validation And Final Output

- `install.check`
- `translate.check`
- `info`

Purpose: block execution when prerequisites are missing, check translation readiness, and render final message with substituted placeholders.

## Compact `sf4.test` Actions

- `data.import.file`
- `file.copy`
- `file.rename`
- `iblock.import.archive`
- `iblock.import.archive.sveden`
- `iblockconfig.import.data`
- `iblocktype.import.data`
- `info`
- `option.import.data`
- `replace.code`
- `shortlink.import.data`
- `site.choice.sveden`
- `site.update.sveden`
- `urlrewrite.add`

## High-Risk Actions For Deep Notes

1. `iblock.import.archive`
2. `iblock.import.archive.sveden`
3. `iblockconfig.import.data`
4. `site.update.sveden`
5. `file.copy`
6. `replace.code`
7. `site.create`
8. `site.translate`
9. `file.zip` / `file.unzip`

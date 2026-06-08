# Universal Wizard Iblock/HL Manifest Assistant

`scripts/sf4_wizard_iblock_manifest.py` creates a read-only draft of explicit
iblock/highload manifest entries for SF4 universal wizard packaging.

It is a review helper. It does not execute PHP, Bitrix, wizard actions, iblock
export/import, highload export/import or write to runtime folders.

## Safety Contract

The helper:

- reads a local `--source` directory;
- inspects zip filenames/member lists with Python `zipfile`;
- scans legacy PHP-array/config files as text only;
- writes only under `source/output`;
- never includes PHP files for evaluation.

## Basic Usage

SF4 universal wizard data payload:

```bash
python3 scripts/sf4_wizard_iblock_manifest.py \
  --source /Users/rim/Sites/test.test/bitrix/modules/simai.sf4biblio/install/wizard/data \
  --label simai.sf4biblio \
  --base-manifest source/output/wizard-export-inventory/simai.sf4university.export/manifest.draft.json
```

Legacy Bitrix wizard data:

```bash
python3 scripts/sf4_wizard_iblock_manifest.py \
  --source /Users/rim/Sites/test.test/bitrix/modules/simai.fund/install/wizards/simai/fund/site/services/iblock/data/ru \
  --label simai.fund.legacy
```

## Output

```text
source/output/wizard-iblock-manifest/<label>/
  iblock-manifest.report.json
  iblock-manifest.report.md
  iblock-manifest.draft.json
  builder-manifest.patch.json
  builder-manifest.merged.draft.json   # only with --base-manifest
```

## Discovery Rules

The assistant detects:

- `data/iblock/*.zip` and archive-like `sf-*`/`form-*` zip names;
- zip validity, member count, `export.xml` presence and highload-like member
  hints;
- legacy `iblocks.php` codes, iblock types and names;
- legacy `highload.php` names and table names;
- shallow SF4 `.iblock.config.php` top-level codes as `config_only_codes`.

## Manifest Rules

- `manifest_draft.iblocks` is an explicit allowlist candidate for
  `sf4_wizard_export_builder.py`.
- `config_only_codes` are never added automatically to the export allowlist.
- `highload_entries` are reported separately because they require a supported
  highload export/import path or confirmation that the chosen archive action
  handles them.
- A merged builder manifest is still a draft and must be audited/readiness
  checked before any generated master is used.

## Example Evidence

- `source/output/wizard-iblock-manifest/simai.sf4biblio/iblock-manifest.report.json`:
  archive payload example, `44` iblock archive entries.
- `source/output/wizard-iblock-manifest/simai.fund.legacy/iblock-manifest.report.json`:
  legacy PHP-array example, `27` iblocks and `2` highload entries.

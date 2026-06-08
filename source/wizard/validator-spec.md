# `sf4_wizard_audit.py` Read-Only Validator Spec

This validator specification is implemented by `scripts/sf4_wizard_audit.py`.

Goal: inspect a universal wizard package without executing the master and report missing files, broken action contracts and risky side effects.

## Invocation Draft

```bash
python3 scripts/sf4_wizard_audit.py \
  --site-root /path/to/site \
  --master /simai/wizard/master/simai.example \
  --module-root /path/to/bitrix/modules/simai.example \
  --json source/output/wizard-audit/simai.example.json
```

Supported modes:

- `--master`: inspect a runtime master already under `/simai/wizard/master/<code>`.
- `--module-root`: inspect module source and installer bridge before runtime copy.
- `--config`: inspect a standalone `.wizard.config.php`.
- `--strict-live`: require backup/rollback notes for live-like paths; still read-only.

## Checks

### Master Structure

- `index.php` exists.
- `.wizard.config.php` exists.
- `data/` exists or installer assembly path is documented.
- `image/` assets referenced by config exist.
- optional `action/` overrides have valid action package files.

### Config Shape

- config file returns an array.
- top-level `description` exists.
- top-level `action` exists and is a non-empty array.
- `description.code` exists and is stable-looking.
- action entries include `name`, `code`, `parameter`.
- action condition syntax is valid enough to be interpreted by runtime.
- `DATA_INPUT_CODE` references a known upstream `DATA_OUTPUT_CODE` unless it is intentionally external.

### Action Resolution

For every action code:

1. check master-local action path:
   - `<master>/action/<code>/action.php`;
2. check global fallback:
   - `<site-root>/simai/wizard/action/<code>/action.php`;
3. report missing action;
4. report code/folder mismatch.

### Payload Resolution

For path-like parameters:

- resolve `Wizard::getLocal(__DIR__)` relative to master config;
- resolve document-root paths;
- preserve placeholders like `#dir#` and report them as runtime-dependent;
- verify `SOURCE` files/directories exist where deterministic;
- verify zip files exist and are readable;
- verify destination parent directories where deterministic.

### Archive Checks

For `iblock.import.archive` and variants:

- every `SOURCE` archive exists;
- archive can be opened by `ZipArchive`;
- archive contains at least one XML-like payload;
- `DESTINATION` iblock type exists in package plan or is site-transformable;
- `SITE` is present or can be derived from input.

For `iblock.export.archive`:

- destination folder exists;
- `IBLOCK` list is non-empty;
- source site has iblocks with listed codes if connected Bitrix inspection is available.

### Runtime Requirements

Report requirements inferred by actions:

- admin user required;
- `simai.framework`;
- `iblock`;
- `highloadblock` when archive/export includes HL indicators or action class uses HL APIs;
- `XMLReader`;
- `ZipArchive`;
- writable destination/config/temp directories.

### Side-Effect Risk

Classify each action:

- `read_only`: export or checks only, no DB writes;
- `filesystem_write`: copy/unzip/rename/delete/replace;
- `db_write`: iblock/HL/site/options/URL rewrite import;
- `global_runtime_write`: module copy, `/simai` copy, `/bitrix/components`, `php_interface`.

Risk flags:

- overwrites possible;
- deletes/renames possible;
- global `/simai` or `/bitrix` write;
- non-reversible code replacement;
- DB import without manifest;
- config merge without backup path.

### Installer Bridge

When `--module-root` is provided:

- locate `install/index.php`;
- detect `CopyDirFiles` into `/simai/wizard/master/<module>/data`;
- detect direct assembly from `install/bitrix`, `install/ru/config`, `install/iblock`, `install/ru/php_interface`, `install/ru/root`, `install/ru/site`;
- detect zip extraction of `config.zip`, `medialibrary.zip`, module zips;
- detect wrapper wizard copy to `/bitrix/wizards/simai/<module>`;
- detect final redirect to `/simai/wizard/master/<module>/`.

### Visual Contract

- referenced logo exists;
- referenced background image exists;
- required `modifier` keys exist or defaults are known;
- legacy wrapper has preview assets if package includes Bitrix wizard list integration.

## JSON Output Draft

```json
{
  "schema_version": "1.0.0",
  "master_code": "simai.example",
  "status": "warning",
  "summary": {
    "actions": 12,
    "missing_actions": 0,
    "missing_payloads": 2,
    "high_risk_side_effects": 4
  },
  "findings": [
    {
      "severity": "error",
      "code": "missing_payload",
      "path": "/simai/wizard/master/simai.example/data/iblock/sf-ru-news.zip",
      "action": "iblock.import.archive"
    }
  ],
  "actions": [
    {
      "code": "file.copy",
      "resolved_action": "/simai/wizard/action/file.copy/action.php",
      "risk": "filesystem_write",
      "inputs": ["site_config"],
      "outputs": [],
      "requirements": ["admin", "simai.framework"]
    }
  ]
}
```

## Non-Goals

- No live wizard execution.
- No DB writes.
- No filesystem writes except optional report output.
- No automatic repair.
- No secret collection.

## Implementation Notes

- Use PHP parser or a controlled PHP include only in a sandboxed/read-only context for config arrays; avoid brittle regex as the primary parser.
- For source-only module packages, static analysis of `install/index.php` can be approximate; report confidence.
- Keep path resolution explicit in the report so a human can verify installer-generated payloads.
- Start with deterministic checks for `.wizard.config.php`, action resolution and payload existence before attempting deeper Bitrix runtime inspection.

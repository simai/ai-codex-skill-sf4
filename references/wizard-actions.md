# Wizard Actions and Deployment Flows

## Wizard Entry Pattern

Typical wizard entry script:

1. Resolve wizard directory (`WIZARD_DIR`).
2. Pass config file (`WIZARD_CONFIG_FILE` usually `.wizard.config.php`).
3. Run `simai:sf.wizard`.

Example path:

- `/simai/wizard/master/<wizard_code>/index.php`

## Action Storage

Action path:

- `/simai/wizard/action/<action_code>/`

Common files:

- `.description.php`
- `action.php` or `class.php`
- optional `lang/<lang>/...`

## Critical Conventions

- Keep action code equal to folder name.
- Keep wizard action chain deterministic and idempotent where possible.
- Keep file operations explicit (`source`, `destination`, `rewrite` policy).
- Keep import data structure documented (`data.import.file`, `option.import.data`, `iblock*` actions).

## Common Action Chain Fragments

- Site setup:
  - `site.choice.install`
  - `site.update` or variant (`site.update.sveden`)
- File operations:
  - `file.copy`
  - `file.rename`
  - `file.create`
  - `file.delete`
- Data and config:
  - `data.import.file`
  - `data.add.config`
  - `option.import.data`
  - `usergroup.import.data`
  - `iblocktype.import.data`
- Iblock/HL migration:
  - `iblock.import.archive` (supports highload-block import logic in class implementation)

## HL-Block Migration Note

`iblock.import.archive`/`iblock.export.archive` class implementations include `highloadblock` handling. Use them for package-style migration when project requires HL structure transfer.

## Known Risk To Check In This Workspace

- `simai.sf4university` wizard entry points reference `.wizard.config.php`, but the file is not present in inspected directories.
- Treat missing wizard config as blocker and ask user before implementing wizard-related changes.

## Wizard Task Checklist

1. Confirm target wizard directory and actual config file availability.
2. Confirm action chain and data input/output codes.
3. Confirm file permissions in target directories.
4. Confirm iblock/HL package files exist before import.
5. Run in controlled environment and verify stage status transitions.


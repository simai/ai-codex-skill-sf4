# Wizard Actions and Deployment Flows

## Wizard Entry Pattern

Typical wizard entry script:

1. Resolve wizard directory (`WIZARD_DIR`).
2. Pass config file (`WIZARD_CONFIG_FILE` usually `.wizard.config.php`).
3. Run `simai:sf.wizard`.

Example path:

- `/simai/wizard/master/<wizard_code>/index.php`

## Runtime Execution Model (Verified)

Execution chain in SF4 wizard runtime:

1. Bitrix solution wizard entry can redirect to SF runtime master:
   - `/bitrix/wizards/<vendor>/<solution>/wizard.php` -> `/simai/wizard/master/<wizard_code>/`.
2. Master `index.php` includes `simai:sf.wizard` and passes:
   - `WIZARD_DIR`,
   - `WIZARD_CONFIG_FILE`,
   - AJAX timing options.
3. `simai:sf.wizard`:
   - loads `.wizard.config.php`,
   - normalizes key case,
   - resolves current stage and stage status,
   - binds action input/output by `DATA_INPUT_CODE` and `DATA_OUTPUT_CODE`,
   - persists runtime state in `SIMAI\Main\Configuration\Property` by wizard code.
4. `simai:sf.wizard.stage` template executes action by including resolved `action.php`.
5. Action file updates:
   - `STAGE.STATUS` (`NEW`/`WORK`/`SUCCESS`/`ERROR`),
   - action-local `DATA`,
   - optional action `OUTPUT`,
   - shared wizard `DATA`.
6. UI enables Next/Prev based on stage status and action flags.

Action resolution order:

1. Wizard-local action override:
   - `/simai/wizard/master/<wizard_code>/action/<action_code>/action.php`
2. Global action fallback:
   - `/simai/wizard/action/<action_code>/action.php`

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
- Keep every action idempotent where feasible when rerun from saved stage state.

## Data Payload Assembly During Install

In packaged solutions, `master/<wizard_code>/data` may be generated at install time, not stored in VCS/source as-is.

Typical module-installer copy pipeline:

1. `install/bitrix` -> `/simai/wizard/master/<wizard_code>/data/bitrix`
2. `install/<lang>/config` -> `/simai/wizard/master/<wizard_code>/data/config`
3. `install/iblock` -> `/simai/wizard/master/<wizard_code>/data/iblock`
4. `install/<lang>/php_interface` -> `/simai/wizard/master/<wizard_code>/data/php_interface`
5. `install/<lang>/root` -> `/simai/wizard/master/<wizard_code>/data/root`
6. `install/<lang>/site` -> `/simai/wizard/master/<wizard_code>/data/site`

Implication:

- Missing `data/*` inside source package is not always an error.
- First verify module/solution installer that assembles runtime payload before blocking work.

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
3. Confirm installer-generated `data/*` payload exists in runtime master directory.
4. Confirm action folder/file resolution path (local override vs global fallback).
5. Confirm file permissions in target directories.
6. Confirm iblock/HL package files exist before import.
7. Confirm required PHP extensions for import actions (`XMLReader`, `ZipArchive`, `DOMDocument`).
8. Run in controlled environment and verify stage status transitions.
9. Verify long-running import actions switch stage from `WORK` to `SUCCESS` through AJAX endpoint.

## Fast Debug Pattern For Failing Wizard

1. Open current stage config and verify `CODE`, `DATA_INPUT_CODE`, `DATA_OUTPUT_CODE`.
2. Resolve effective action file path and confirm it exists.
3. Validate source payload files referenced by action parameters.
4. Check action writes status back to property storage.
5. If stage stays `WORK`, inspect corresponding action AJAX handler:
   - request keys,
   - status finalization logic,
   - partial import state updates.

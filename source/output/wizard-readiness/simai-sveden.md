# Wizard Readiness: simai.sveden

- readiness_status: `needs_rollback_plan`
- controlled_execution_allowed: `false`
- audit_status: `ready`
- master: `/Users/rim/Sites/sf4.test/simai/wizard/master/simai.sveden`
- config: `/Users/rim/Sites/sf4.test/simai/wizard/master/simai.sveden/.wizard.config.php`

## Summary

- actions: `19`
- errors: `0`
- findings: `0`
- high_risk_side_effects: `16`
- missing_actions: `0`
- missing_payloads: `0`
- warnings: `0`

## Findings

- none

## Side Effects

- db_write: `data.import.file`, `data.import.file`, `iblock.import.archive`, `iblock.import.archive.sveden`, `iblocktype.import.data`, `option.import.data`, `shortlink.import.data`, `site.update.sveden`, `urlrewrite.add`
- filesystem_write: `file.copy`, `file.copy`, `file.copy`, `file.copy`, `file.rename`, `iblockconfig.import.data`, `replace.code`
- read_only: `info`, `info`, `site.choice.sveden`

## Backup And Rollback Required

- `file.copy` (filesystem_write): destination file/directory inventory and backup before action; rollback: restore backup or remove copied/generated paths by inventory
- `file.copy` (filesystem_write): destination file/directory inventory and backup before action; rollback: restore backup or remove copied/generated paths by inventory
- `iblockconfig.import.data` (filesystem_write): destination file/directory inventory and backup before action; rollback: restore backup or remove copied/generated paths by inventory
- `urlrewrite.add` (db_write): DB backup or exact export of affected Bitrix entities/options before action; rollback: restore DB backup or run reviewed cleanup/delete script for created entities
- `site.update.sveden` (db_write): DB backup or exact export of affected Bitrix entities/options before action; rollback: restore DB backup or run reviewed cleanup/delete script for created entities
- `file.rename` (filesystem_write): destination file/directory inventory and backup before action; rollback: restore backup or remove copied/generated paths by inventory
- `file.copy` (filesystem_write): destination file/directory inventory and backup before action; rollback: restore backup or remove copied/generated paths by inventory
- `file.copy` (filesystem_write): destination file/directory inventory and backup before action; rollback: restore backup or remove copied/generated paths by inventory
- `replace.code` (filesystem_write): destination file/directory inventory and backup before action; rollback: restore backup or remove copied/generated paths by inventory
- `data.import.file` (db_write): DB backup or exact export of affected Bitrix entities/options before action; rollback: restore DB backup or run reviewed cleanup/delete script for created entities
- `shortlink.import.data` (db_write): DB backup or exact export of affected Bitrix entities/options before action; rollback: restore DB backup or run reviewed cleanup/delete script for created entities
- `option.import.data` (db_write): DB backup or exact export of affected Bitrix entities/options before action; rollback: restore DB backup or run reviewed cleanup/delete script for created entities
- `data.import.file` (db_write): DB backup or exact export of affected Bitrix entities/options before action; rollback: restore DB backup or run reviewed cleanup/delete script for created entities
- `iblocktype.import.data` (db_write): DB backup or exact export of affected Bitrix entities/options before action; rollback: restore DB backup or run reviewed cleanup/delete script for created entities
- `iblock.import.archive` (db_write): DB backup or exact export of affected Bitrix entities/options before action; rollback: restore DB backup or run reviewed cleanup/delete script for created entities
- `iblock.import.archive.sveden` (db_write): DB backup or exact export of affected Bitrix entities/options before action; rollback: restore DB backup or run reviewed cleanup/delete script for created entities

## Stop Conditions

- stop if audit JSON is stale relative to master/config files
- stop if live target, site root, user permissions or backup path are not explicit
- stop before controlled execution until backup and rollback evidence exists
- stop if write action destination scope is broader than approved target
- stop before DB import unless DB backup and cleanup strategy are reviewed

## Next Actions

- write backup and rollback plan for every write action
- define controlled environment and stop conditions
- ask ops/tester gatekeepers before live or staging execution

# Wizard Readiness: wizard-export-sample

- readiness_status: `blocked`
- controlled_execution_allowed: `false`
- audit_status: `blocked`
- master: `/Users/rim/Downloads/wizard.export/wizard.export`
- config: `/Users/rim/Downloads/wizard.export/wizard.export/.wizard.config.php`

## Summary

- actions: `18`
- errors: `5`
- findings: `6`
- high_risk_side_effects: `10`
- missing_actions: `2`
- missing_payloads: `3`
- warnings: `1`

## Findings

- `missing_action_file`
- `missing_master_data`
- `missing_payload`

## Side Effects

- filesystem_write: `data.export.file`, `data.export.file`, `data.export.file`, `data.export.file`, `data.export.file`, `data.export.file`, `file.copy`, `file.copy`, `file.create`, `file.encode.win1251`
- read_only: `iblock.export.archive`, `iblocktype.export.data`, `info`, `mail-templates.export.data`, `mail.export.data`, `option.export.data`, `site.export.data`, `usergroup.export.data`

## Backup And Rollback Required

- `file.copy` (filesystem_write): destination file/directory inventory and backup before action; rollback: restore backup or remove copied/generated paths by inventory
- `file.copy` (filesystem_write): destination file/directory inventory and backup before action; rollback: restore backup or remove copied/generated paths by inventory
- `data.export.file` (filesystem_write): destination file/directory inventory and backup before action; rollback: restore backup or remove copied/generated paths by inventory
- `data.export.file` (filesystem_write): destination file/directory inventory and backup before action; rollback: restore backup or remove copied/generated paths by inventory
- `data.export.file` (filesystem_write): destination file/directory inventory and backup before action; rollback: restore backup or remove copied/generated paths by inventory
- `data.export.file` (filesystem_write): destination file/directory inventory and backup before action; rollback: restore backup or remove copied/generated paths by inventory
- `data.export.file` (filesystem_write): destination file/directory inventory and backup before action; rollback: restore backup or remove copied/generated paths by inventory
- `data.export.file` (filesystem_write): destination file/directory inventory and backup before action; rollback: restore backup or remove copied/generated paths by inventory
- `file.create` (filesystem_write): destination file/directory inventory and backup before action; rollback: restore backup or remove copied/generated paths by inventory
- `file.encode.win1251` (filesystem_write): destination file/directory inventory and backup before action; rollback: restore backup or remove copied/generated paths by inventory

## Stop Conditions

- stop if audit JSON is stale relative to master/config files
- stop if live target, site root, user permissions or backup path are not explicit
- stop until all audit error findings are resolved
- stop before controlled execution until backup and rollback evidence exists
- stop if write action destination scope is broader than approved target
- stop until every deterministic payload path exists and archives open

## Next Actions

- fix missing config/action/payload blockers
- re-run sf4_wizard_audit.py
- re-run sf4_wizard_readiness.py

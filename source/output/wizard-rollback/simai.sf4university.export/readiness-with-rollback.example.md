# Wizard Readiness: simai.sf4university.export

- readiness_status: `ready_for_review`
- controlled_execution_allowed: `false`
- audit_status: `ready`
- master: `/Users/rim/Documents/GitHub/ai-codex-skill-sf4/source/output/wizard-export-inventory/simai.sf4university.export/builder/simai.sf4university.export/master/simai.sf4university.export`
- config: `/Users/rim/Documents/GitHub/ai-codex-skill-sf4/source/output/wizard-export-inventory/simai.sf4university.export/builder/simai.sf4university.export/master/simai.sf4university.export/.wizard.config.php`

## Summary

- actions: `14`
- errors: `0`
- findings: `0`
- high_risk_side_effects: `8`
- missing_actions: `0`
- missing_payloads: `0`
- warnings: `0`

## Findings

- none

## Side Effects

- filesystem_write: `data.export.file`, `data.export.file`, `data.export.file`, `data.export.file`, `file.copy`, `file.copy`, `file.create`, `file.encode.win1251`
- read_only: `iblock.export.archive`, `iblocktype.export.data`, `info`, `option.export.data`, `site.export.data`, `usergroup.export.data`

## Backup And Rollback Required

- `file.copy` (filesystem_write): destination file/directory inventory and backup before action; rollback: restore backup or remove copied/generated paths by inventory
- `file.copy` (filesystem_write): destination file/directory inventory and backup before action; rollback: restore backup or remove copied/generated paths by inventory
- `data.export.file` (filesystem_write): destination file/directory inventory and backup before action; rollback: restore backup or remove copied/generated paths by inventory
- `data.export.file` (filesystem_write): destination file/directory inventory and backup before action; rollback: restore backup or remove copied/generated paths by inventory
- `data.export.file` (filesystem_write): destination file/directory inventory and backup before action; rollback: restore backup or remove copied/generated paths by inventory
- `data.export.file` (filesystem_write): destination file/directory inventory and backup before action; rollback: restore backup or remove copied/generated paths by inventory
- `file.create` (filesystem_write): destination file/directory inventory and backup before action; rollback: restore backup or remove copied/generated paths by inventory
- `file.encode.win1251` (filesystem_write): destination file/directory inventory and backup before action; rollback: restore backup or remove copied/generated paths by inventory

## Rollback Plan Evidence

- plan_status: `rollback_plan_ready`
- execution_approval: `false`
- evidence_mode: `example_only_not_execution_evidence`
- incomplete_items: `0`
- items: `8`
- missing_field_count: `0`
- ready_items: `8`
- review_missing_count: `0`

## Stop Conditions

- stop if audit JSON is stale relative to master/config files
- stop if live target, site root, user permissions or backup path are not explicit
- stop before controlled execution until backup and rollback evidence exists
- stop if write action destination scope is broader than approved target

## Next Actions

- review action chain and visual contract
- replace example-only rollback evidence with real backup artifacts before execution
- ask ops/tester gatekeepers before live or staging execution

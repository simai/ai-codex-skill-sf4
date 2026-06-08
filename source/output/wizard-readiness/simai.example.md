# Wizard Readiness: simai.example

- readiness_status: `needs_rollback_plan`
- controlled_execution_allowed: `false`
- audit_status: `ready`
- master: `/Users/rim/Documents/GitHub/ai-codex-skill-sf4/source/output/wizard-skeleton/simai.example/master/simai.example`
- config: `/Users/rim/Documents/GitHub/ai-codex-skill-sf4/source/output/wizard-skeleton/simai.example/master/simai.example/.wizard.config.php`

## Summary

- actions: `4`
- errors: `0`
- findings: `0`
- high_risk_side_effects: `2`
- missing_actions: `0`
- missing_payloads: `0`
- warnings: `0`

## Findings

- none

## Side Effects

- db_write: `urlrewrite.add`
- filesystem_write: `iblockconfig.import.data`
- read_only: `info`, `site.choice.sveden`

## Backup And Rollback Required

- `iblockconfig.import.data` (filesystem_write): destination file/directory inventory and backup before action; rollback: restore backup or remove copied/generated paths by inventory
- `urlrewrite.add` (db_write): DB backup or exact export of affected Bitrix entities/options before action; rollback: restore DB backup or run reviewed cleanup/delete script for created entities

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

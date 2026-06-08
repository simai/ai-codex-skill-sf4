# Wizard Rollback Plan Template: simai.example

- readiness_status: `needs_rollback_plan`
- evidence_mode: `template`
- master: `/Users/rim/Documents/GitHub/ai-codex-skill-sf4/source/output/wizard-skeleton/simai.example/master/simai.example`

## Items

### 02-iblockconfig.import.data-filesystem

- action: `iblockconfig.import.data`
- risk: `filesystem_write`
- required_backup: destination file/directory inventory and backup before action
- required_rollback: restore backup or remove copied/generated paths by inventory
- target_scope:
- backup_artifact:
- backup_method:
- rollback_artifact:
- rollback_method:
- verification_method:
- owner:
- stop_condition:

### 03-urlrewrite.add-database

- action: `urlrewrite.add`
- risk: `db_write`
- required_backup: DB backup or exact export of affected Bitrix entities/options before action
- required_rollback: restore DB backup or run reviewed cleanup/delete script for created entities
- target_scope:
- backup_artifact:
- backup_method:
- rollback_artifact:
- rollback_method:
- verification_method:
- owner:
- stop_condition:

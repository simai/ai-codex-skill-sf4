# Wizard Rollback Plan Template: simai.sf4university.export

- readiness_status: `needs_rollback_plan`
- evidence_mode: `example_only_not_execution_evidence`
- master: `/Users/rim/Documents/GitHub/ai-codex-skill-sf4/source/output/wizard-export-inventory/simai.sf4university.export/builder/simai.sf4university.export/master/simai.sf4university.export`

## Items

### 01-file.copy-filesystem

- action: `file.copy`
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

### 06-file.copy-filesystem

- action: `file.copy`
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

### 08-data.export.file-filesystem

- action: `data.export.file`
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

### 09-data.export.file-filesystem

- action: `data.export.file`
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

### 10-data.export.file-filesystem

- action: `data.export.file`
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

### 11-data.export.file-filesystem

- action: `data.export.file`
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

### 12-file.create-filesystem

- action: `file.create`
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

### 13-file.encode.win1251-filesystem

- action: `file.encode.win1251`
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

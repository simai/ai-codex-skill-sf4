# Wizard Rollback Plan Template: simai.sveden

- readiness_status: `needs_rollback_plan`
- evidence_mode: `template`
- master: `/Users/rim/Sites/sf4.test/simai/wizard/master/simai.sveden`

## Items

### 02-file.copy-filesystem

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

### 03-file.copy-filesystem

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

### 04-iblockconfig.import.data-filesystem

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

### 05-urlrewrite.add-database

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

### 06-site.update.sveden-database

- action: `site.update.sveden`
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

### 07-file.rename-filesystem

- action: `file.rename`
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

### 08-file.copy-filesystem

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

### 09-file.copy-filesystem

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

### 10-replace.code-filesystem

- action: `replace.code`
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

### 11-data.import.file-database

- action: `data.import.file`
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

### 12-shortlink.import.data-database

- action: `shortlink.import.data`
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

### 13-option.import.data-database

- action: `option.import.data`
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

### 14-data.import.file-database

- action: `data.import.file`
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

### 15-iblocktype.import.data-database

- action: `iblocktype.import.data`
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

### 16-iblock.import.archive-database

- action: `iblock.import.archive`
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

### 17-iblock.import.archive.sveden-database

- action: `iblock.import.archive.sveden`
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

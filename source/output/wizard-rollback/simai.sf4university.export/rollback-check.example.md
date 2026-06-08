# Wizard Rollback Plan Check: simai.sf4university.export

- plan_status: `rollback_plan_ready`
- execution_approval: `false`
- evidence_mode: `example_only_not_execution_evidence`

## Summary

- incomplete_items: `0`
- items: `8`
- missing_field_count: `0`
- ready_items: `8`
- review_missing_count: `0`

## Review Missing Fields

- none

## Items

- `01-file.copy-filesystem` file.copy (filesystem_write): ready; missing: none
- `06-file.copy-filesystem` file.copy (filesystem_write): ready; missing: none
- `08-data.export.file-filesystem` data.export.file (filesystem_write): ready; missing: none
- `09-data.export.file-filesystem` data.export.file (filesystem_write): ready; missing: none
- `10-data.export.file-filesystem` data.export.file (filesystem_write): ready; missing: none
- `11-data.export.file-filesystem` data.export.file (filesystem_write): ready; missing: none
- `12-file.create-filesystem` file.create (filesystem_write): ready; missing: none
- `13-file.encode.win1251-filesystem` file.encode.win1251 (filesystem_write): ready; missing: none

## Stop Conditions

- This checker does not approve live execution.
- Real backup artifacts must exist and be reviewed by ops/tester before controlled execution.
- If target scope changes, regenerate readiness and rollback plan.

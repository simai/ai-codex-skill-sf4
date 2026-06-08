# Wizard Rollback Plan Check: simai.example-filled-demo

- plan_status: `rollback_plan_ready`
- execution_approval: `false`
- evidence_mode: `example_only_not_execution_evidence`

## Summary

- incomplete_items: `0`
- items: `2`
- missing_field_count: `0`
- ready_items: `2`
- review_missing_count: `0`

## Review Missing Fields

- none

## Items

- `02-iblockconfig.import.data-filesystem` iblockconfig.import.data (filesystem_write): ready; missing: none
- `03-urlrewrite.add-database` urlrewrite.add (db_write): ready; missing: none

## Stop Conditions

- This checker does not approve live execution.
- Real backup artifacts must exist and be reviewed by ops/tester before controlled execution.
- If target scope changes, regenerate readiness and rollback plan.

# SF4 Update Artifacts

## Goal

Standardize update deliverables for SF4 tasks that affect schema, data, behavior, or deployment flow.

## When Required

Apply this flow when task includes one or more:

- wizard install/update action changes
- iblock/highloadblock schema or data changes
- behavior changes requiring admin action after deploy
- migration/import/export changes

## Mandatory Artifacts

1. `Migration Notes` (always, even if no data/schema changes)
2. `Upgrade Notes` (when admins/devops must perform actions)
3. `Regression Checklist` (for every non-trivial update)
4. `QA Report` (for high-risk or broad-scope updates)

Templates:

- `references/artifacts/migration-notes.md`
- `references/artifacts/upgrade-notes.md`
- `references/artifacts/regression-checklist.md`
- `references/artifacts/qa-report.md`

## Update Procedure

1. Collect scope from diff/changed files.
2. Classify impact:
   - runtime layout/components
   - config/property model
   - data/schema
   - wizard/install pipeline
3. Define rollback and idempotency expectations.
4. Execute change and run smoke/regression checks.
5. Fill required artifacts with factual outcomes.

## Data and Rollback Policy

- Do not assume "no migration needed"; explicitly confirm.
- Migration steps must be repeat-safe or guarded.
- Rollback plan must be explicit, including "not applicable" rationale.
- If destructive data steps are required, require clear user confirmation.

## Minimum Delivery Bundle

For update tasks, response should include:

1. changed file list
2. short behavior-impact summary
3. migration/upgrade notes
4. regression status
5. unresolved risks and follow-up checks

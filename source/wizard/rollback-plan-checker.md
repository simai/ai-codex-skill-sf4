# Universal Wizard Rollback Plan Checker

`scripts/sf4_wizard_rollback_plan.py` creates and checks backup/rollback plan artifacts from readiness JSON.

It is read-only. It does not create backups, execute rollback commands, run Bitrix/PHP/wizard actions, import data or change live files.

## Generate Template

```bash
python3 scripts/sf4_wizard_rollback_plan.py \
  --readiness source/output/wizard-readiness/simai.example.json \
  --label simai.example \
  --template-json source/output/wizard-rollback/simai.example/template.json \
  --template-markdown source/output/wizard-rollback/simai.example/template.md \
  --check-json source/output/wizard-rollback/simai.example/check-empty.json
```

Expected for a new template:

- check status `rollback_plan_incomplete`;
- every write action has required empty fields;
- `execution_approval` stays `false`.

## Check Filled Plan

```bash
python3 scripts/sf4_wizard_rollback_plan.py \
  --plan source/output/wizard-rollback/simai.example/filled-example.json \
  --check-json source/output/wizard-rollback/simai.example/check-filled-example.json \
  --check-markdown source/output/wizard-rollback/simai.example/check-filled-example.md
```

The checker requires these fields per write action:

- `target_scope`;
- `backup_artifact`;
- `backup_method`;
- `rollback_artifact`;
- `rollback_method`;
- `verification_method`;
- `owner`;
- `stop_condition`.

It also requires review fields:

- `ops_reviewer`;
- `tester_reviewer`;
- `approved_scope`;
- `review_date`;
- `approval_note`.

## Statuses

| Status | Meaning |
| --- | --- |
| `rollback_plan_missing` | Readiness requires rollback artifacts but only a template exists. |
| `rollback_plan_incomplete` | Required action or review fields are missing. |
| `rollback_plan_ready` | Required fields are present. This is not live execution approval. |
| `rollback_plan_not_required` | Readiness has no write actions requiring rollback planning. |

## Specialist Rule

`rollback_plan_ready` means the plan is structurally filled. Live/staging execution still requires explicit scope, real artifacts, ops/tester review and applicable federation gates.

## Use With Readiness

After a filled plan is checked, pass its check report back to readiness:

```bash
python3 scripts/sf4_wizard_readiness.py \
  --audit source/output/wizard-export-inventory/simai.sf4university.export/audit.json \
  --rollback-check source/output/wizard-rollback/simai.sf4university.export/rollback-check.example.json \
  --label simai.sf4university.export \
  --json source/output/wizard-rollback/simai.sf4university.export/readiness-with-rollback.example.json \
  --markdown source/output/wizard-rollback/simai.sf4university.export/readiness-with-rollback.example.md
```

Expected for example-only evidence:

- readiness status can become `ready_for_review`;
- `controlled_execution_allowed` remains `false`;
- `rollback_plan.execution_approval` remains `false`.

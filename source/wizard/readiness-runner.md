# Universal Wizard Readiness Runner

`scripts/sf4_wizard_readiness.py` turns `sf4_wizard_audit.py` JSON into a human review board before controlled wizard execution.

It is read-only. It does not execute Bitrix, PHP, wizard actions, imports, DB writes or live file operations.

## Usage

```bash
python3 scripts/sf4_wizard_readiness.py \
  --audit source/output/wizard-skeleton/simai.example/audit.json \
  --rollback-check source/output/wizard-rollback/simai.example/check-filled-example.json \
  --label simai.example \
  --json source/output/wizard-readiness/simai.example.json \
  --markdown source/output/wizard-readiness/simai.example.md
```

`--rollback-check` is optional. It accepts JSON produced by
`scripts/sf4_wizard_rollback_plan.py` and lets readiness distinguish a missing
rollback plan from a structurally filled plan.

## Readiness Statuses

| Status | Meaning |
| --- | --- |
| `blocked` | Audit has errors or status `blocked`; do not proceed. |
| `needs_payload` | Deterministic payload or archive gaps remain. |
| `needs_rollback_plan` | Structure is valid, but write actions require backup/rollback before controlled execution. |
| `ready_for_review` | No audit blockers, no payload gaps and no write actions; human review can continue. |

When write actions exist, `ready_for_review` can also mean a rollback check was
provided with `rollback_plan_ready`. This still does not mean runtime execution
is allowed. `controlled_execution_allowed` stays `false` unless write actions
have real rollback evidence and execution approval.

## Review Board Sections

- audit summary;
- finding codes;
- payload gaps;
- side effects by risk;
- backup/rollback required per write action;
- rollback plan evidence, when `--rollback-check` is provided;
- stop conditions;
- next actions.

## Specialist Rule

After every non-trivial `sf4_wizard_audit.py` run, generate a readiness report before proposing live, staging or controlled execution. A ready audit is not the same as execution readiness when write actions are present.

For packaging/export masters, the safe chain is:

```text
inventory -> manifest -> builder -> audit -> rollback check -> readiness
```

Example-only rollback evidence may make readiness `ready_for_review`, but must
not be treated as permission to run the generated master.

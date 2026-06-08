# SF4 Wizard Rollback Readiness Layer

## Goal

Сделать rollback readiness layer для SF4 universal wizard export packaging:
rollback-plan example для generated `simai.sf4university.export`, checker/readiness
evidence, source/specialist/graph refs, workflow and gates.

## Done When

- Есть rollback-plan example for generated `simai.sf4university.export`.
- `scripts/sf4_wizard_rollback_plan.py` validates the example with
  `rollback_plan_ready`.
- `scripts/sf4_wizard_readiness.py` can consume rollback check evidence and no
  longer blocks only because rollback plan is missing.
- `controlled_execution_allowed` remains false for example-only evidence.
- Specialist/source/graph refs describe the standard chain:
  inventory -> manifest -> builder -> audit -> rollback -> readiness.
- Verification and graph/federation gates pass.
- Kaizen is recorded.

## Safe Boundary

Allowed:

- read repo-local generated package evidence under `source/output`;
- write repo-local scripts/docs/source/output/workflow;
- generate JSON/Markdown rollback and readiness evidence;
- run local Python validators.

Forbidden:

- execute Bitrix/PHP runtime;
- run wizard actions;
- create backups in real site roots;
- copy generated masters into `/Users/rim/Sites/*` or module install folders;
- mutate DB, iblocks, HL blocks, options, mail templates, user groups or files in
  live/staging/project roots.

## Gates

- federation route: primary `sf4`, companions `bitrix`, `tester`, confidence
  `high`.
- preflight: success.
- evidence: `source/output/action-gates/action-gate-report-20260608081427.json`.

## Workstreams

- Readiness/rollback contract update.
- Rollback-plan example and reports.
- Specialist/source/graph integration.
- Verification and Kaizen.

## Batches

### Batch 1: Route, workflow and contract review

- status: completed
- work:
  - run federation route/preflight;
  - create workflow;
  - inspect readiness and rollback checker contract.

### Batch 2: Readiness integration

- status: completed
- work:
  - add optional rollback check input to readiness runner;
  - keep live execution approval separate from structural rollback readiness.

### Batch 3: Example evidence

- status: completed
- work:
  - generate filled example rollback plan for `simai.sf4university.export`;
  - check the plan;
  - re-run readiness with rollback check evidence.

### Batch 4: Source and graph refs

- status: completed
- work:
  - update source docs and specialist;
  - update graph capability refs if needed.

### Batch 5: Verification and sync

- status: completed
- work:
  - run syntax/JSON/acceptance checks;
  - run graph contract, skill sync, federation verify and route checks;
  - ingest Kaizen.

## Current Status

Goal status: completed.

Batches 1-5 completed. Rollback readiness layer is implemented and verified for
the generated `simai.sf4university.export` package in safe/offline mode.

## Evidence Log

- `source/output/action-gates/action-gate-report-20260608081427.json`: preflight passed.
- `scripts/sf4_wizard_readiness.py`: added optional `--rollback-check` evidence input.
- `source/output/wizard-rollback/simai.sf4university.export/rollback-plan.example.json`: example rollback plan generated for `8` write actions.
- `source/output/wizard-rollback/simai.sf4university.export/rollback-check.example.json`: check status `rollback_plan_ready`.
- `source/output/wizard-rollback/simai.sf4university.export/readiness-with-rollback.example.json`: readiness `ready_for_review`, controlled execution `false`.
- `source/wizard/readiness-runner.md`: documented `--rollback-check`.
- `source/wizard/rollback-plan-checker.md`: documented readiness integration.
- `skills/sf4/specialists/universal-wizard.md`: specialist chain updated.
- `graph/specs/objects/capability-sf4-universal-wizard-specialist.json`: new workflow/evidence refs added.
- JSON validation passed for graph capability and generated rollback/readiness reports.
- `python3 -m py_compile`: passed for all SF4 wizard helper scripts.
- `scripts/sf4_wizard_acceptance.py --manifest source/wizard/acceptance-fixtures.json`: passed.
- `git diff --check`: passed.
- `scripts/mirai_graph_contract_gate.py`: passed, canonical write is not allowed by gate output.
- `skill-change-detect.sh --skill sf4`: changed skill source detected, blockers `0`.
- `skill-graph-sync.sh --skill sf4`: synced latest evidence under `graph/generated/mirai_graph/*/skill-graph-sync-sf4-20260608081753-*`.
- `federation-verify.sh --profile admin --no-write`: passed, blockers `0`.
- `federation-route-check.sh --profile admin --json`: passed, routes `64/64`.
- route smoke for `подготовить rollback readiness evidence для SF4 universal wizard export packaging без запуска runtime`: primary `sf4`, companions `bitrix,tester`, confidence `high`.
- safety route smoke for `проверить rollback readiness universal wizard export package`: primary `ops`, confidence `high`; this is expected when wording implies rollback/backup review rather than SF4 package construction.

## Kaizen

Lessons Learned:

- Rollback readiness needs two separate booleans: structurally filled rollback
  plan and actual runtime execution approval.
- Example-only rollback evidence is useful for training the specialist and
  validating the chain, but it must not unlock execution.
- Route wording matters: rollback/backup-only wording correctly pulls `ops`;
  SF4 universal wizard packaging wording stays with `sf4` plus `bitrix/tester`.

Process Improvements:

- Standard export-package proof chain is now:
  inventory -> manifest -> builder -> audit -> rollback check -> readiness.
- Readiness reports should always expose rollback evidence mode so humans can
  distinguish examples, dry-runs and real reviewed artifacts.

Skill/Federation Improvement Candidates:

- Add a dedicated federation routing fixture for "SF4 universal wizard rollback
  readiness evidence without runtime execution" so the `sf4`/`ops` boundary is
  explicit.
- Extend rollback checker later to support a real-artifact mode that checks
  local backup file existence without executing rollback.

Follow-up Proposals:

- Build an iblock/HL manifest assistant that reads exported data structures and
  proposes explicit builder manifest entries.
- Add a comparison report between developer `wizard.export` chains and generated
  builder output.
- Add a real-artifact rollback fixture in `source/output` when a disposable
  source environment is available.

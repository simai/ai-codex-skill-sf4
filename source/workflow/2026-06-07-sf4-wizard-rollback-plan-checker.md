# SF4 Wizard Rollback Plan Checker

## Goal

Сделать read-only rollback plan template/checker для универсального SF4 мастера: он принимает readiness JSON, генерирует план по write actions и проверяет заполненность backup/rollback evidence перед возможным переводом `needs_rollback_plan` к review-ready состоянию.

## Done When

- Есть `scripts/sf4_wizard_rollback_plan.py`.
- Есть документация rollback plan contract.
- Есть rollback templates для `simai.example` и `simai.sveden`.
- Checker отличает пустой template от заполненного demo-плана.
- Specialist source и `SKILL.md` знают rollback plan step.
- Graph capability refs указывают на runner/docs/evidence.
- Пройдены syntax/JSON/readiness/acceptance/graph/federation gates.
- Kaizen зафиксирован.

## Safe Boundary

Allowed:

- читать readiness JSON;
- писать rollback plan templates/check reports в `source/output`;
- обновлять repo-local scripts/source/skill/graph refs.

Forbidden:

- выполнять wizard runtime URL;
- запускать Bitrix PHP imports/actions;
- создавать реальные backup archives;
- импортировать iblock/HL archives;
- менять `/Users/rim/Sites/*`, `/simai`, `/bitrix`, public roots;
- менять DB/options/urlrewrite.

## Gates

- federation route: primary `sf4`, companions `bitrix`, `tester`, confidence `high`.
- preflight: success.
- evidence: `source/output/action-gates/action-gate-report-20260607143156.json`.

## Batches

### Batch 1: Workflow and checker

- status: completed
- work: create workflow, rollback plan checker and docs.
- checks: Python syntax.

### Batch 2: Templates and check reports

- status: completed
- work: generate rollback templates for `simai.example` and `simai.sveden`; prove empty template is incomplete and filled demo can be ready.
- checks: JSON validation and status checks.

### Batch 3: Specialist and graph refs

- status: completed
- work: update `SKILL.md`, specialist, graph capability and source index.
- checks: graph JSON validation.

### Batch 4: Verification and sync

- status: completed
- work: readiness/acceptance regression, graph contract, skill graph sync, federation verify/route-check.
- checks: no blockers.

### Batch 5: Kaizen

- status: completed
- work: record lessons and next proposal.

## Current Status

- Batch 1: completed.
- Batch 2: completed.
- Batch 3: completed.
- Batch 4: completed.
- Batch 5: completed.

Goal status: completed.

## Evidence Log

- `source/output/action-gates/action-gate-report-20260607143156.json`: preflight passed.
- `python3 -m py_compile scripts/sf4_wizard_rollback_plan.py`: passed.
- `source/output/wizard-rollback/simai.example/check-empty.json`: `rollback_plan_incomplete`, items `2`.
- `source/output/wizard-rollback/simai-sveden/check-empty.json`: `rollback_plan_incomplete`, items `16`.
- `source/output/wizard-rollback/simai.example/check-filled-example.json`: `rollback_plan_ready`, example-only evidence, execution approval `false`.
- `python3 -m json.tool graph/specs/objects/capability-sf4-universal-wizard-specialist.json`: passed.
- `python3 -m json.tool source/wizard/source-index.json`: passed.
- `python3 -m json.tool source/output/wizard-rollback/simai.example/check-empty.json`: passed.
- `python3 -m json.tool source/output/wizard-rollback/simai.example/check-filled-example.json`: passed.
- `python3 -m json.tool source/output/wizard-rollback/simai-sveden/check-empty.json`: passed.
- `python3 -m py_compile scripts/sf4_wizard_audit.py scripts/sf4_wizard_acceptance.py scripts/sf4_wizard_skeleton.py scripts/sf4_wizard_readiness.py scripts/sf4_wizard_rollback_plan.py`: passed.
- `python3 scripts/sf4_wizard_acceptance.py --manifest source/wizard/acceptance-fixtures.json --json source/output/wizard-acceptance/report.json --quiet`: passed.
- `python3 scripts/mirai_graph_contract_gate.py`: passed, `canonical_write_allowed=false`.
- `git diff --check`: passed.
- `skill-change-detect.sh`: changed; required evidence, federation proposal, route-check, runtime-context and specialist-promotion; blockers none.
- `skill-graph-sync.sh --skill sf4`: passed.
- generated sync evidence:
  - `graph/generated/mirai_graph/skill-source-changes/skill-graph-sync-sf4-20260607143559/skill-source-change-evidence.json`
  - `graph/generated/mirai_graph/runtime-kit/skill-graph-sync-sf4-20260607143559-verify/runtime-kit-verify.json`
  - `graph/generated/mirai_graph/runtime-context/skill-graph-sync-sf4-20260607143559-context/context-pack.json`
  - `graph/generated/mirai_graph/federation-change/skill-graph-sync-sf4-20260607143559-federation-proposal/federation-change-proposal.json`
  - `graph/generated/mirai_graph/specialist-promotion/skill-graph-sync-sf4-20260607143559-specialist-sf4-universal-wizard/specialist-promotion-proposal.json`
- `federation-verify.sh --profile admin --no-write`: passed, blockers none.
- `federation-route-check.sh --profile admin --json`: passed, 64/64.
- route smoke `сформировать rollback plan универсального мастера SF4 по readiness JSON`: primary `sf4`, companions `bitrix`, `tester`, confidence `high`.

## Kaizen

Lessons Learned:

- Rollback readiness must be a separate artifact, not a prose note in the readiness report. It has different owners and evidence requirements.
- A structurally filled rollback plan is still not live execution approval. The checker therefore keeps `execution_approval=false` even for `rollback_plan_ready`.
- Duplicate action codes, such as repeated `file.copy`, need stable item ids with action index to avoid ambiguous rollback items.

Process Improvements:

- Generate rollback templates directly from readiness JSON after every `needs_rollback_plan` verdict.
- Keep empty templates intentionally failing with non-zero exit so automation cannot mistake a blank plan for evidence.
- Use example-only filled plans only to test checker behavior; real plans must point to real backup/rollback artifacts.

Skill/Federation Improvement Candidates:

- Add a future evidence-existence mode that verifies local backup/rollback artifact paths when an ops-approved working directory exists.
- Add mapping from action parameters to more precise target scopes for `file.copy`, `urlrewrite.add`, and `iblock.import.archive`.

Follow-up Proposals:

- Next useful batch: controlled execution package builder in propose-only mode. It should combine audit, readiness and rollback plan checks into one human-approved launch package with scope, commands, backups, stop conditions and QA expectations, without executing the wizard.

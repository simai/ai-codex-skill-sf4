# SF4 Wizard Package Readiness Runner

## Goal

Сделать read-only readiness runner для универсального SF4 мастера: он принимает audit JSON от `sf4_wizard_audit.py` и формирует human review board перед controlled execution.

## Done When

- Есть `scripts/sf4_wizard_readiness.py`.
- Есть документация формата readiness report.
- Есть reports для generated skeleton и реального `simai.sveden`.
- Specialist source и `SKILL.md` знают readiness step.
- Graph capability refs указывают на runner/docs/evidence.
- Пройдены syntax/JSON/audit/acceptance/graph/federation gates.
- Kaizen зафиксирован.

## Safe Boundary

Allowed:

- читать audit JSON;
- писать readiness reports в `source/output`;
- обновлять repo-local scripts/source/skill/graph refs.

Forbidden:

- выполнять wizard runtime URL;
- запускать Bitrix PHP imports/actions;
- импортировать iblock/HL archives;
- менять `/Users/rim/Sites/*`, `/simai`, `/bitrix`, public roots;
- менять DB/options/urlrewrite.

## Gates

- federation route: primary `sf4`, companions `bitrix`, `tester`, confidence `high`.
- preflight: success.
- evidence: `source/output/action-gates/action-gate-report-20260607141657.json`.

## Batches

### Batch 1: Workflow and runner

- status: completed
- work: create workflow, readiness runner and docs.
- checks: Python syntax, JSON examples.

### Batch 2: Reports

- status: completed
- work: generate readiness reports for skeleton and `simai.sveden`.
- checks: expected statuses and markdown review boards.

### Batch 3: Specialist and graph refs

- status: completed
- work: update `SKILL.md`, specialist, graph capability and source index.
- checks: graph JSON validation.

### Batch 4: Verification and sync

- status: completed
- work: acceptance regression, graph contract, skill graph sync, federation verify/route-check.
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

- `source/output/action-gates/action-gate-report-20260607141657.json`: preflight passed.
- `python3 -m py_compile scripts/sf4_wizard_readiness.py`: passed.
- `source/output/wizard-readiness/simai.example.json`: `needs_rollback_plan`, controlled execution `false`, write actions `2`.
- `source/output/wizard-readiness/simai-sveden.json`: `needs_rollback_plan`, controlled execution `false`, write actions `16`.
- `python3 -m json.tool graph/specs/objects/capability-sf4-universal-wizard-specialist.json`: passed.
- `python3 -m json.tool source/wizard/source-index.json`: passed.
- `python3 -m json.tool source/output/wizard-readiness/simai.example.json`: passed.
- `python3 -m json.tool source/output/wizard-readiness/simai-sveden.json`: passed.
- `python3 -m py_compile scripts/sf4_wizard_audit.py scripts/sf4_wizard_acceptance.py scripts/sf4_wizard_skeleton.py scripts/sf4_wizard_readiness.py`: passed.
- `python3 scripts/sf4_wizard_acceptance.py --manifest source/wizard/acceptance-fixtures.json --json source/output/wizard-acceptance/report.json --quiet`: passed.
- `python3 scripts/mirai_graph_contract_gate.py`: passed, `canonical_write_allowed=false`.
- `git diff --check`: passed.
- `skill-change-detect.sh`: changed; required evidence, federation proposal, route-check, runtime-context and specialist-promotion; blockers none.
- `skill-graph-sync.sh --skill sf4`: passed.
- generated sync evidence:
  - `graph/generated/mirai_graph/skill-source-changes/skill-graph-sync-sf4-20260607142033/skill-source-change-evidence.json`
  - `graph/generated/mirai_graph/runtime-kit/skill-graph-sync-sf4-20260607142033-verify/runtime-kit-verify.json`
  - `graph/generated/mirai_graph/runtime-context/skill-graph-sync-sf4-20260607142033-context/context-pack.json`
  - `graph/generated/mirai_graph/federation-change/skill-graph-sync-sf4-20260607142033-federation-proposal/federation-change-proposal.json`
  - `graph/generated/mirai_graph/specialist-promotion/skill-graph-sync-sf4-20260607142033-specialist-sf4-universal-wizard/specialist-promotion-proposal.json`
- `federation-verify.sh --profile admin --no-write`: passed, blockers none.
- `federation-route-check.sh --profile admin --json`: passed, 64/64.
- route smoke `сформировать readiness report универсального мастера SF4 по audit JSON`: primary `sf4`, companions `bitrix`, `tester`, confidence `high`.

## Kaizen

Lessons Learned:

- A structural audit can be `ready` while execution is still not ready. The readiness layer must explicitly separate "package shape valid" from "safe to execute".
- Write actions should default to `needs_rollback_plan`; this keeps the specialist from treating `file.copy`, `iblockconfig.import.data`, `urlrewrite.add` or `iblock.import.archive` as harmless.
- Markdown review boards are useful for human review, while JSON keeps graph/evidence automation deterministic.

Process Improvements:

- Run readiness after every non-trivial audit, especially before advising controlled/staging/live execution.
- Keep readiness statuses conservative: `blocked`, `needs_payload`, `needs_rollback_plan`, `ready_for_review`.
- Use readiness output as the source for ops/tester handoff rather than rewriting side-effect lists manually.

Skill/Federation Improvement Candidates:

- Add optional rollback-plan input later, so readiness can verify that every write action has a concrete backup and rollback artifact.
- Add a batch comparing readiness reports across masters to identify common missing rollback patterns.

Follow-up Proposals:

- Next useful batch: implement a rollback-plan template/checker for wizard readiness reports, so `needs_rollback_plan` can become an evidence-backed `ready_for_review` when backup/rollback artifacts exist.

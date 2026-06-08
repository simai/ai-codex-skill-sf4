# SF4 Universal Wizard Specialist Acceptance

## Goal

Сделать acceptance-пакет для `SF4 Universal Wizard Specialist`, который проверяет специалиста на реальных данных универсального мастера и module installer bridge без выполнения мастеров, PHP-кода Bitrix, импорта архивов или live/data writes.

## Scale

- requested_level: continuation after goal discussion
- recommended_level: milestone-sized acceptance batch
- project_mode: internal training/productization
- owner_skill: `sf4`
- coordinator: `teamlead`
- companions: `bitrix`, `tester`, `graph`

## Done When

- Есть durable workflow для acceptance-пакета.
- Есть матрица acceptance-сценариев по реальным мастерам и модулям.
- Есть fixture manifest с expected invariants для `sf4_wizard_audit.py`.
- Есть read-only runner, который заново запускает аудит и сверяет expected invariants.
- Specialist source содержит acceptance scenarios и evidence policy.
- Graph capability source refs знают о acceptance package.
- Пройдены validator checks, JSON checks, graph contract gate, skill change detect/sync, federation verify и route check.
- Kaizen зафиксирован в этом workflow.

## Safe Boundary

Allowed:

- писать только в repo-local skill/source/graph/scripts artifacts;
- читать реальные wizard/module paths;
- запускать только read-only audit/acceptance скрипты;
- писать JSON reports в `source/output`.

Forbidden:

- выполнять `/simai/wizard/master/*` через веб/runtime;
- запускать Bitrix PHP imports или wizard actions;
- изменять `/Users/rim/Sites/*`;
- импортировать iblock/HL архивы;
- копировать/удалять public/runtime files;
- менять DB, options, urlrewrite, site settings.

## Gates

- federation route: `sf4`, companions `bitrix`, `tester`, confidence `high`.
- preflight: `env_policy_gate`, `repo_hygiene_gate`, `source_policy_gate` passed.
- evidence: `source/output/action-gates/action-gate-report-20260607140218.json`.

## Workstreams

1. Acceptance corpus
   - `source/wizard/acceptance-matrix.md`
   - `source/wizard/acceptance-fixtures.json`
2. Acceptance runner
   - `scripts/sf4_wizard_acceptance.py`
3. Specialist raw source
   - `skills/sf4/specialists/universal-wizard.md`
4. Graph source refs and generated evidence
   - `graph/specs/objects/capability-sf4-universal-wizard-specialist.json`
   - `graph/generated/mirai_graph/...`

## Batches

### Batch 1: Workflow and fixtures

- status: completed
- work: create workflow, acceptance matrix, fixture manifest.
- checks: JSON manifest validation.
- evidence: files under `source/wizard`.

### Batch 2: Runner

- status: completed
- work: create `sf4_wizard_acceptance.py`, run against real fixture manifest.
- checks: acceptance run success and JSON report.
- evidence: `source/output/wizard-acceptance/report.json`.

### Batch 3: Specialist and graph refs

- status: completed
- work: add acceptance scenarios to specialist source and update capability source refs.
- checks: graph JSON validation and graph contract gate.
- evidence: diff and gate outputs.

### Batch 4: Sync and federation verification

- status: completed
- work: run skill-change-detect, skill-graph-sync, federation verify, route check.
- checks: no blockers.
- evidence: generated graph artifacts and command outputs.

### Batch 5: Kaizen

- status: completed
- work: record lessons, process improvements, follow-up proposals.
- checks: workflow contains final evidence and next step.

## Acceptance Scenarios

- `simai-sveden-ready-runtime-master`: full runtime master with 19 actions, visual assets and high-risk side effects classified.
- `simai-sf4university-missing-config`: blocked runtime master with missing `.wizard.config.php` evidence.
- `simai-sf4biblio-module-bridge`: prebuilt module package bridge with `install/wizard/data`, config/media/module archives and wrapper redirect signals.
- `simai-sf4med-module-bridge`: prebuilt module package bridge with wrapper redirect and runtime master data assembly.
- `simai-sf4university-assembled-module-bridge`: assembled module bridge with config, iblock, php_interface, root and site install payloads.

## Current Status

- Batch 1: completed.
- Batch 2: completed.
- Batch 3: completed.
- Batch 4: completed.
- Batch 5: completed.

Goal status: completed.

## Evidence Log

- `source/output/action-gates/action-gate-report-20260607140218.json`: federation preflight passed.
- `source/output/wizard-acceptance/report.json`: acceptance runner passed 5/5 scenarios.
- `python3 -m json.tool source/wizard/acceptance-fixtures.json`: passed.
- `python3 -m json.tool graph/specs/objects/capability-sf4-universal-wizard-specialist.json`: passed.
- `python3 -m py_compile scripts/sf4_wizard_audit.py scripts/sf4_wizard_acceptance.py`: passed.
- `python3 scripts/mirai_graph_contract_gate.py`: passed, `canonical_write_allowed=false`.
- `skill-change-detect.sh`: changed; specialist promotion, route-check and federation proposal required; blockers none.
- `skill-graph-sync.sh --skill sf4`: passed.
- generated sync evidence:
  - `graph/generated/mirai_graph/skill-source-changes/skill-graph-sync-sf4-20260607140638/skill-source-change-evidence.json`
  - `graph/generated/mirai_graph/runtime-kit/skill-graph-sync-sf4-20260607140638-verify/runtime-kit-verify.json`
  - `graph/generated/mirai_graph/runtime-context/skill-graph-sync-sf4-20260607140638-context/context-pack.json`
  - `graph/generated/mirai_graph/federation-change/skill-graph-sync-sf4-20260607140638-federation-proposal/federation-change-proposal.json`
  - `graph/generated/mirai_graph/specialist-promotion/skill-graph-sync-sf4-20260607140638-specialist-sf4-universal-wizard/specialist-promotion-proposal.json`
- `federation-verify.sh --profile admin --no-write`: passed, blockers none.
- `federation-route-check.sh --profile admin --json`: passed, 64/64.
- route smoke `проверить acceptance пакет универсального мастера SF4`: primary `sf4`, companions `bitrix`, `tester`, confidence `high`.

## Kaizen

Lessons Learned:

- The universal wizard specialist needs executable acceptance, not only a prose checklist. Real-data fixtures make regressions visible when parser logic or source assumptions change.
- Expected invariants should stay stable and focused: status, summary counters, blocker codes, visual asset resolution and installer bridge signals. Full JSON snapshots would be too brittle because absolute paths and report metadata can change.
- Missing runtime master config must remain an explicit blocked scenario in the training set; it prevents the specialist from inventing a wizard config from nearby payload files.

Process Improvements:

- Keep `source/wizard/acceptance-fixtures.json` as the first place to add new real master/module cases.
- Run `scripts/sf4_wizard_acceptance.py` after changing `sf4_wizard_audit.py`, `universal-wizard.md` or wizard packaging guidance.
- Treat installer bridge scenarios separately from runtime master scenarios; source modules can assemble `data/*` during install and should not be judged only by source tree shape.

Skill/Federation Improvement Candidates:

- Add more fixtures when a real master with HL-only payload or custom master-local actions is available.
- Consider promoting a compact routing fixture for "acceptance пакет универсального мастера SF4" if this workflow becomes frequent.

Follow-up Proposals:

- Next useful batch: add a master skeleton generator in propose-only/dry-run mode that emits a candidate `/simai/wizard/master/<code>` tree and `.wizard.config.php` from the specialist contracts, without writing to live project paths.

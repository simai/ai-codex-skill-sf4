# SF4 Wizard Skeleton Generator

## Goal

Сделать безопасный dry-run/propose-only генератор skeleton универсального SF4 мастера, который создаёт кандидатную структуру мастера и `.wizard.config.php` в `source/output`, проверяется read-only audit tooling и не изменяет live/runtime проекты.

## Done When

- Есть workflow с safe boundary, батчами, evidence и Kaizen.
- Есть `scripts/sf4_wizard_skeleton.py`.
- Скрипт генерирует proposal package только в разрешённый output-каталог.
- Скрипт создаёт master tree: `index.php`, `.wizard.config.php`, `image/*`, `data/*`, optional wrapper skeleton.
- Есть пример spec/manifest в `source/wizard`.
- Сгенерированный пример проходит `sf4_wizard_audit.py`.
- Specialist source и graph capability refs знают о generator.
- Пройдены syntax/JSON/audit/acceptance/graph/federation gates.

## Safe Boundary

Allowed:

- писать в repo-local `source/output/wizard-skeleton/*`;
- писать `source/wizard/*`, `scripts/*`, `skills/sf4/specialists/*`, `graph/specs/*`;
- читать real action library under `/Users/rim/Sites/*`;
- запускать read-only audit/acceptance.

Forbidden:

- писать в `/Users/rim/Sites/*`;
- выполнять wizard URL/runtime;
- запускать Bitrix PHP imports/actions;
- менять DB/options/urlrewrite;
- копировать файлы в `/simai`, `/bitrix`, public site roots.

## Gates

- federation route: primary `sf4`, companions `bitrix`, `tester`, confidence `high`.
- preflight: success.
- evidence: `source/output/action-gates/action-gate-report-20260607140925.json`.

## Batches

### Batch 1: Workflow and design

- status: completed
- work: define safe generator contract.
- evidence: this workflow.

### Batch 2: Generator implementation

- status: completed
- work: add script and example spec.
- checks: Python syntax, JSON validation.

### Batch 3: Generated example and audit

- status: completed
- work: generate example package under `source/output/wizard-skeleton`, audit it against real action library.
- checks: audit status `ready`.

### Batch 4: Specialist and graph refs

- status: completed
- work: add generator guidance to specialist and graph refs.
- checks: graph JSON validation, contract gate.

### Batch 5: Federation sync and Kaizen

- status: completed
- work: skill-change-detect, skill-graph-sync, federation verify, route check, workflow Kaizen.
- checks: no blockers.

## Current Status

- Batch 1: completed.
- Batch 2: completed.
- Batch 3: completed.
- Batch 4: completed.
- Batch 5: completed.

Goal status: completed.

## Evidence Log

- `source/output/action-gates/action-gate-report-20260607140925.json`: preflight passed.
- `python3 -m py_compile scripts/sf4_wizard_skeleton.py`: passed.
- `python3 -m json.tool source/wizard/skeleton-example.json`: passed.
- `python3 scripts/sf4_wizard_skeleton.py --code simai.example --name "SIMAI Example" --profile config --wrapper --force`: generated proposal.
- `python3 scripts/sf4_wizard_audit.py --site-root /Users/rim/Sites/sf4.test --master /Users/rim/Documents/GitHub/ai-codex-skill-sf4/source/output/wizard-skeleton/simai.example/master/simai.example --json source/output/wizard-skeleton/simai.example/audit.json`: passed, status `ready`, actions `4`, findings `0`, high-risk `2`.
- Note: relative `--master` with external `--site-root` resolves under site root; examples now use absolute master path.
- `python3 -m json.tool graph/specs/objects/capability-sf4-universal-wizard-specialist.json`: passed.
- `python3 -m json.tool source/wizard/source-index.json`: passed.
- `python3 scripts/sf4_wizard_acceptance.py --manifest source/wizard/acceptance-fixtures.json --json source/output/wizard-acceptance/report.json --quiet`: passed.
- `python3 scripts/mirai_graph_contract_gate.py`: passed, `canonical_write_allowed=false`.
- `git diff --check`: passed.
- `skill-change-detect.sh`: changed; required evidence, federation proposal, route-check, runtime-context and specialist-promotion; blockers none.
- `skill-graph-sync.sh --skill sf4`: passed.
- generated sync evidence:
  - `graph/generated/mirai_graph/skill-source-changes/skill-graph-sync-sf4-20260607141342/skill-source-change-evidence.json`
  - `graph/generated/mirai_graph/runtime-kit/skill-graph-sync-sf4-20260607141342-verify/runtime-kit-verify.json`
  - `graph/generated/mirai_graph/runtime-context/skill-graph-sync-sf4-20260607141342-context/context-pack.json`
  - `graph/generated/mirai_graph/federation-change/skill-graph-sync-sf4-20260607141342-federation-proposal/federation-change-proposal.json`
  - `graph/generated/mirai_graph/specialist-promotion/skill-graph-sync-sf4-20260607141342-specialist-sf4-universal-wizard/specialist-promotion-proposal.json`
- `federation-verify.sh --profile admin --no-write`: passed, blockers none.
- `federation-route-check.sh --profile admin --json`: passed, 64/64.
- route smoke `сгенерировать skeleton универсального мастера SF4 в dry-run режиме`: primary `sf4`, companions `bitrix`, `tester`, confidence `high`.

## Kaizen

Lessons Learned:

- A skeleton generator must enforce output path safety. The script refuses paths outside `source/output`, which keeps "делай" from becoming a live `/simai` write.
- Generated skeleton audit needs an absolute `--master` path when `--site-root` points to a real action library. This was caught by the first audit run and documented in the example.
- A proposal generator should include placeholder payload files and images so `sf4_wizard_audit.py` can validate structure and action resolution immediately.

Process Improvements:

- Use `scripts/sf4_wizard_skeleton.py` before hand-authoring a new universal master; then modify the generated proposal and re-run audit.
- Keep profiles small and explicit: `minimal`, `config`, `iblock`. Larger solution-specific chains should be built from audited real examples, not hidden inside the generator.
- Keep generated proposal output ignored under `source/output`; promote only reviewed methodology/tooling into tracked skill sources.

Skill/Federation Improvement Candidates:

- Add future profiles only after studying at least one real master using that chain, for example a public/template copy profile or module-zip profile.
- Add an optional machine-readable backup/rollback checklist generator once rollback examples are studied from real deployments.

Follow-up Proposals:

- Next useful batch: create a "wizard package readiness checklist" runner that takes a generated or real master audit JSON and emits a human review board: payload gaps, side effects, backup/rollback TODOs and live stop conditions.

# SF4 Wizard Export Inventory Helper

## Goal

Создать read-only inventory helper для SF4 export packaging: локальный site inventory -> `manifest.draft.json` -> export builder -> audit/readiness evidence -> specialist/graph integration.

## Done When

- Есть `scripts/sf4_wizard_export_inventory.py`.
- Скрипт принимает `--site-root`, `--solution-code`, `--site-dir`.
- Скрипт read-only находит доступные SIMAI modules, components, templates, public dir, media library, `urlrewrite.php` and wizard action library.
- Скрипт формирует `manifest.draft.json` для `sf4_wizard_export_builder.py`.
- Скрипт может запустить цепочку builder -> audit -> readiness in `source/output`.
- Есть пример на `/Users/rim/Sites/university.test`.
- Specialist/source/graph refs обновлены.
- Пройдены syntax, JSON, generated PHP, audit, readiness, acceptance, graph/federation gates.
- Kaizen зафиксирован.

## Safe Boundary

Allowed:

- читать локальный site root;
- читать action library names;
- писать только repo-local scripts/docs and `source/output`;
- запускать local Python builder/audit/readiness.

Forbidden:

- выполнять Bitrix/PHP runtime;
- запускать generated master URL;
- запускать wizard actions;
- создавать `/.last_version` in real site root;
- копировать файлы в `/Users/rim/Sites/*`, `/simai`, `/bitrix`;
- экспортировать/import iblocks/HL through Bitrix runtime;
- менять DB/options/urlrewrite/live/staging.

## Gates

- federation route: primary `sf4`, companions `bitrix`, `tester`, confidence `high`.
- preflight: success.
- evidence: `source/output/action-gates/action-gate-report-20260608080010.json`.

## Workstreams

- Inventory script.
- Generated manifest and package evidence.
- Specialist/source/graph integration.
- Verification and Kaizen.

## Batches

### Batch 1: Workflow and design

- status: completed
- work:
  - create workflow;
  - define safe boundary;
  - inspect builder contract and local source signals.

### Batch 2: Inventory implementation

- status: completed
- work:
  - implement read-only scanner;
  - build manifest draft;
  - optionally run builder/audit/readiness.

### Batch 3: Example and reports

- status: completed
- work:
  - run on `/Users/rim/Sites/university.test`;
  - generate manifest, builder report, audit and readiness.

### Batch 4: Integration

- status: completed
- work:
  - update source docs;
  - update specialist/SKILL;
  - update graph refs.

### Batch 5: Verification and sync

- status: completed
- work:
  - run syntax/JSON/acceptance checks;
  - run graph contract, skill sync, federation verify and route checks.

## Current Status

Goal status: completed.

Batches 1-5 completed. Read-only source-site inventory helper is implemented,
documented, exercised on `/Users/rim/Sites/university.test`, and connected to
the SF4 universal wizard specialist references and graph capability object.

## Evidence Log

- `source/output/action-gates/action-gate-report-20260608080010.json`: preflight passed.
- `scripts/sf4_wizard_export_inventory.py`: helper implemented.
- `source/wizard/export-inventory-helper.md`: helper contract documented.
- `source/output/wizard-export-inventory/simai.sf4university.export/inventory.json`: local site inventory created.
- `source/output/wizard-export-inventory/simai.sf4university.export/manifest.draft.json`: draft manifest created.
- `source/output/wizard-export-inventory/simai.sf4university.export/run-report.json`: chain status `chain_complete`.
- `source/output/wizard-export-inventory/simai.sf4university.export/builder/simai.sf4university.export/builder-report.json`: generated package report, actions `14`.
- `php -l source/output/wizard-export-inventory/simai.sf4university.export/builder/simai.sf4university.export/master/simai.sf4university.export/index.php`: passed.
- `php -l source/output/wizard-export-inventory/simai.sf4university.export/builder/simai.sf4university.export/master/simai.sf4university.export/.wizard.config.php`: passed.
- `source/output/wizard-export-inventory/simai.sf4university.export/audit.json`: audit `ready`, actions `14`, errors `0`, warnings `0`, high-risk side effects `8`.
- `source/output/wizard-export-inventory/simai.sf4university.export/readiness.json`: readiness `needs_rollback_plan`, controlled execution `false`.
- JSON validation passed for source index, graph object, inventory report, manifest draft, run report, audit report and readiness report.
- `python3 -m py_compile` passed for all SF4 wizard helper scripts.
- `scripts/sf4_wizard_acceptance.py --manifest source/wizard/acceptance-fixtures.json`: passed.
- `git diff --check`: passed.
- `python3 scripts/mirai_graph_contract_gate.py`: passed, canonical write is not allowed by gate output.
- `skill-change-detect.sh --skill sf4`: changed skill source detected, blockers `0`.
- `skill-graph-sync.sh --skill sf4`: synced latest evidence under `graph/generated/mirai_graph/*/skill-graph-sync-sf4-20260608080547-*`.
- `federation-verify.sh --profile admin --no-write`: passed, blockers `0`.
- `federation-route-check.sh --profile admin --json`: passed, routes `64/64`.
- route smoke for `собрать manifest упаковки SF4 решения через read-only inventory helper`: primary `sf4`, companions `bitrix,tester`, confidence `high`.

## Kaizen

Lessons Learned:

- Inventory-first packaging removes manual guessing before building export
  masters: the draft manifest is evidence-backed by local filesystem signals.
- For export-package solution codes ending in `.export`, including the base
  module code is a useful default when the module exists locally.
- `mail.export.data` and `mail-templates.export.data` remain optional sample
  actions: the current helper must not require them until they exist in the
  local action library.
- Readiness correctly keeps controlled execution blocked until a rollback plan
  is present, even when generated package audit is clean.

Process Improvements:

- Standard packaging flow should be: site inventory -> manifest review -> export
  builder -> audit -> readiness -> rollback plan -> controlled execution.
- Generated export packages should stay under `source/output` until the user
  explicitly approves copying them into a Bitrix module/wizard location.
- Every packaging helper should produce both machine-readable JSON and a short
  operator report so a future specialist can cite exact evidence.

Skill/Federation Improvement Candidates:

- Add deeper iblock/HL auto-discovery later, but keep it read-only and evidence
  marked because reliable semantic export still depends on Bitrix runtime
  ownership.
- Extend action contract docs when missing mail export actions are implemented
  or mapped to supported alternatives.
- Promote the inventory helper as the default first step for requests like
  "упаковать решение через универсальный мастер".

Follow-up Proposals:

- Create a rollback plan example for the generated
  `simai.sf4university.export` package and run `sf4_wizard_rollback_plan.py`.
- Add an iblock/HL manifest assistant that reads local exported data structures
  and proposes builder manifest entries without executing Bitrix runtime.
- Add a comparison report between a developer-provided `wizard.export` chain and
  a generated builder package to explain which actions were preserved, replaced
  or skipped.

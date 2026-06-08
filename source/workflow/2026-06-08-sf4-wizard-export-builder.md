# SF4 Wizard Export Package Builder

## Goal

Создать controlled export package builder для SF4 универсального мастера упаковки решений: manifest -> generated `wizard.export`-style master -> read-only audit/readiness evidence -> specialist/graph integration.

## Done When

- Есть manifest contract для export packaging.
- Есть `scripts/sf4_wizard_export_builder.py`.
- Есть пример manifest на реальных локальных путях.
- Generator пишет только в `source/output`.
- Generated master проходит static audit/readiness.
- Specialist/source/graph refs обновлены.
- Пройдены syntax, JSON, audit, readiness, acceptance, graph/federation gates.
- Kaizen зафиксирован.

## Safe Boundary

Allowed:

- читать локальные action libraries and source folders;
- писать repo-local scripts/docs/examples/reports;
- генерировать proposals under `source/output`;
- запускать static audit/readiness.

Forbidden:

- запускать generated master URL;
- выполнять wizard actions;
- создавать `/.last_version` в real site root;
- копировать файлы в `/Users/rim/Sites/*`, `/simai`, `/bitrix`;
- экспортировать/import iblock/HL through Bitrix runtime;
- менять DB/options/urlrewrite/live/staging.

## Gates

- federation route: primary `sf4`, companions `bitrix`, `tester`, confidence `high`.
- preflight: success.
- evidence: `source/output/action-gates/action-gate-report-20260608072410.json`.

## Workstreams

- Builder script and manifest contract.
- Example manifest and generated package evidence.
- Specialist/source/graph integration.
- Verification and Kaizen.

## Batches

### Batch 1: Workflow and design

- status: completed
- work:
  - create workflow;
  - define safe builder boundary;
  - inspect existing skeleton generator and local source paths.

### Batch 2: Builder implementation

- status: completed
- work:
  - implement manifest parser;
  - generate `index.php`, `.wizard.config.php`, images, README, manifest copy;
  - support file copy, dynamic data export, iblock archive export, generated data files, php_interface snippets, optional encode/zip/cleanup.

### Batch 3: Example and reports

- status: completed
- work:
  - create example manifest;
  - generate sample export master;
  - run audit/readiness.

### Batch 4: Integration

- status: completed
- work:
  - update source docs;
  - update specialist;
  - update graph refs.

### Batch 5: Verification and sync

- status: completed
- work:
  - run syntax/JSON/acceptance checks;
  - run graph contract, skill sync, federation verify and route checks.

## Current Status

- Batch 1: completed.
- Batch 2: completed.
- Batch 3: completed.
- Batch 4: completed.
- Batch 5: completed.

Goal status: completed.

## Evidence Log

- `source/output/action-gates/action-gate-report-20260608072410.json`: preflight passed.
- `scripts/sf4_wizard_export_builder.py`: builder implemented.
- `source/wizard/export-builder.md`: manifest contract documented.
- `source/wizard/export-builder-example.json`: example manifest on real local paths.
- `source/output/wizard-export-builder/simai.example.export/builder-report.json`: generated package report, actions `14`.
- `source/output/wizard-export-builder/simai.example.export/master/simai.example.export/.wizard.config.php`: generated export master config.
- `php -l source/output/wizard-export-builder/simai.example.export/master/simai.example.export/index.php`: passed.
- `php -l source/output/wizard-export-builder/simai.example.export/master/simai.example.export/.wizard.config.php`: passed.
- `source/output/wizard-export-builder/simai.example.export/audit.json`: audit `ready`, actions `14`, errors `0`, warnings `0`, high-risk side effects `8`.
- `source/output/wizard-export-builder/simai.example.export/readiness.json`: readiness `needs_rollback_plan`, controlled execution `false`.
- `python3 -m json.tool source/wizard/source-index.json`: passed.
- `python3 -m json.tool source/wizard/export-builder-example.json`: passed.
- `python3 -m json.tool graph/specs/objects/capability-sf4-universal-wizard-specialist.json`: passed.
- `python3 -m py_compile scripts/sf4_wizard_audit.py scripts/sf4_wizard_acceptance.py scripts/sf4_wizard_skeleton.py scripts/sf4_wizard_export_builder.py scripts/sf4_wizard_readiness.py scripts/sf4_wizard_rollback_plan.py`: passed.
- `python3 scripts/sf4_wizard_acceptance.py --manifest source/wizard/acceptance-fixtures.json --json source/output/wizard-acceptance/report.json --quiet`: passed.
- `git diff --check`: passed.
- `python3 scripts/mirai_graph_contract_gate.py`: passed, `canonical_write_allowed=false`.
- `skill-change-detect.sh`: changed; required evidence, federation proposal, route-check, runtime-context and specialist-promotion; blockers none.
- `skill-graph-sync.sh --skill sf4`: passed.
- generated sync evidence:
  - `graph/generated/mirai_graph/skill-source-changes/skill-graph-sync-sf4-20260608073142/skill-source-change-evidence.json`
  - `graph/generated/mirai_graph/runtime-kit/skill-graph-sync-sf4-20260608073142-verify/runtime-kit-verify.json`
  - `graph/generated/mirai_graph/runtime-context/skill-graph-sync-sf4-20260608073142-context/context-pack.json`
  - `graph/generated/mirai_graph/federation-change/skill-graph-sync-sf4-20260608073142-federation-proposal/federation-change-proposal.json`
  - `graph/generated/mirai_graph/specialist-promotion/skill-graph-sync-sf4-20260608073142-specialist-sf4-universal-wizard/specialist-promotion-proposal.json`
- `federation-verify.sh --profile admin --no-write`: passed, blockers none; warning exists for unrelated dirty/unsynced `graph` skill repo.
- `federation-route-check.sh --profile admin --json`: passed, 64/64.
- route smoke `упаковать существующее SF4 решение через manifest export builder универсального мастера`: primary `sf4`, companions `bitrix`, `tester`, confidence `high`.

## Kaizen

Lessons Learned:

- `wizard.export` logic should become a manifest-driven generator, not a copied master. The developer sample is valuable as an action algorithm, while project-specific paths and action availability must be generated from explicit allowlists.
- A packaging master can be audit-ready while still not executable. Readiness must remain `needs_rollback_plan` until backup/rollback is filled for write actions.
- Mail export actions are optional capability, not a default requirement, because current inspected action library does not contain `mail.export.data` or `mail-templates.export.data`.

Process Improvements:

- For "упаковать решение через универсальный мастер", run export-builder first, then audit/readiness, then rollback plan. Do not start from install/import skeleton.
- Use explicit iblock allowlists by default; broad `CIBlock::GetList()` export is only acceptable for developer snapshots.
- Keep `archive.enabled=false` and `cleanup.enabled=false` in generated review examples.

Skill/Federation Improvement Candidates:

- Add a future `--inspect-source-site` helper that can propose manifest allowlists from a local SF4 site without executing Bitrix actions.
- Add action-contract docs for export-only actions such as `site.export.data`, `usergroup.export.data`, `option.export.data` and `data.export.file`.

Follow-up Proposals:

- Next batch: implement a source-site inventory helper for export manifests.
- Later batch: add a filled rollback-plan example for `simai.example.export`, still without live execution approval.

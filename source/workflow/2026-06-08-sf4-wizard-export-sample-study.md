# SF4 Wizard Export Sample Study

## Goal

Изучить присланный образец `/Users/rim/Downloads/wizard.export/wizard.export` и встроить подтверждённые знания в подготовку специалиста по универсальному SF4 мастеру, особенно для сценария упаковки решений.

## Done When

- Образец инвентаризирован read-only.
- Описана логика export/packaging chain.
- Источник добавлен в `source/wizard` corpus.
- Specialist и graph capability знают новый packaging baseline.
- Read-only audit/readiness evidence создан.
- Проверки source/JSON/graph/federation пройдены или блокер зафиксирован.

## Safe Boundary

Allowed:

- читать `/Users/rim/Downloads/wizard.export/wizard.export`;
- читать action libraries в локальных проектах;
- писать repo-local source docs, graph refs, scripts и reports;
- запускать static audit/readiness.

Forbidden:

- выполнять `index.php` мастера;
- запускать wizard actions;
- писать в `/Users/rim/Sites/*`, `/simai`, `/bitrix`, DB или live/staging;
- создавать `/.last_version` на реальном сайте;
- импортировать/экспортировать реальные iblocks через Bitrix runtime.

## Gates

- federation route: primary `sf4`, companions `bitrix`, `tester`, confidence `high`.
- preflight: success.
- evidence: `source/output/action-gates/action-gate-report-20260608070831.json`.

## Batches

### Batch 1: Inventory

- status: completed
- work:
  - listed files and directories in the sample;
  - read `index.php`, `.wizard.config.php`, `.property.config.php`, demo config files;
  - confirmed active action chain and visual config.
- evidence:
  - `/Users/rim/Downloads/wizard.export/wizard.export/.wizard.config.php`;
  - `/Users/rim/Downloads/wizard.export/wizard.export/index.php`.

### Batch 2: Audit and readiness

- status: completed
- work:
  - ran `sf4_wizard_audit.py` against the sample;
  - fixed audit classification for export/data-export actions;
  - reran audit/readiness.
- evidence:
  - `source/output/wizard-audit/wizard-export-sample.json`;
  - `source/output/wizard-readiness/wizard-export-sample.json`;
  - `source/output/wizard-readiness/wizard-export-sample.md`.
- result:
  - audit status: `blocked`;
  - readiness status: `blocked`;
  - controlled execution allowed: `false`.

### Batch 3: Corpus and specialist update

- status: completed
- work:
  - created `source/wizard/case-wizard-export-packaging.md`;
  - updated `source/wizard/README.md`;
  - updated `source/wizard/source-index.json`;
  - updated `source/wizard/packaging-matrix.md`;
  - updated `source/wizard/export-packaging-data.md`;
  - updated `skills/sf4/specialists/universal-wizard.md`;
  - updated graph capability refs.

### Batch 4: Verification

- status: completed
- work:
  - ran JSON/source checks;
  - ran wizard acceptance regression;
  - ran graph contract and federation checks;
  - recorded final evidence.

## Current Status

- Batch 1: completed.
- Batch 2: completed.
- Batch 3: completed.
- Batch 4: completed.

Goal status: completed.

## Evidence Log

- `source/output/action-gates/action-gate-report-20260608070831.json`: preflight passed.
- `php -l /Users/rim/Downloads/wizard.export/wizard.export/.wizard.config.php`: passed.
- `php -l /Users/rim/Downloads/wizard.export/wizard.export/.property.config.php`: passed.
- `php -l /Users/rim/Downloads/wizard.export/wizard.export/index.php`: passed.
- `source/output/wizard-audit/wizard-export-sample.json`: audit `blocked`, actions `18`, errors `5`, warnings `1`, high-risk side effects `10`.
- `source/output/wizard-readiness/wizard-export-sample.json`: readiness `blocked`, controlled execution `false`.
- `python3 -m json.tool source/wizard/source-index.json`: passed.
- `python3 -m json.tool graph/specs/objects/capability-sf4-universal-wizard-specialist.json`: passed.
- `python3 -m json.tool source/output/wizard-audit/wizard-export-sample.json`: passed.
- `python3 -m json.tool source/output/wizard-readiness/wizard-export-sample.json`: passed.
- `python3 -m py_compile scripts/sf4_wizard_audit.py scripts/sf4_wizard_acceptance.py scripts/sf4_wizard_skeleton.py scripts/sf4_wizard_readiness.py scripts/sf4_wizard_rollback_plan.py`: passed.
- `python3 scripts/sf4_wizard_acceptance.py --manifest source/wizard/acceptance-fixtures.json --json source/output/wizard-acceptance/report.json --quiet`: passed.
- `git diff --check`: passed.
- `python3 scripts/mirai_graph_contract_gate.py`: passed, `canonical_write_allowed=false`.
- `skill-change-detect.sh`: changed; required evidence, federation proposal, route-check, runtime-context and specialist-promotion; blockers none.
- `skill-graph-sync.sh --skill sf4`: passed.
- generated sync evidence:
  - `graph/generated/mirai_graph/skill-source-changes/skill-graph-sync-sf4-20260608071506/skill-source-change-evidence.json`
  - `graph/generated/mirai_graph/runtime-kit/skill-graph-sync-sf4-20260608071506-verify/runtime-kit-verify.json`
  - `graph/generated/mirai_graph/runtime-context/skill-graph-sync-sf4-20260608071506-context/context-pack.json`
  - `graph/generated/mirai_graph/federation-change/skill-graph-sync-sf4-20260608071506-federation-proposal/federation-change-proposal.json`
  - `graph/generated/mirai_graph/specialist-promotion/skill-graph-sync-sf4-20260608071506-specialist-sf4-universal-wizard/specialist-promotion-proposal.json`
- `federation-verify.sh --profile admin --no-write`: passed, blockers none.
- `federation-route-check.sh --profile admin --json`: passed, 64/64.
- route smoke `упаковать решение SF4 через универсальный мастер wizard.export`: primary `sf4`, companions `bitrix`, `tester`, confidence `high`.

## Current Findings

The sample is an export master, not an import/install master. It packages a current Bitrix/SF4 site into an install tree:

```text
/.last_version/install/{bitrix,iblock,ru}
```

The chain copies files, exports dynamic Bitrix/SF4 data into wizard storage, writes generated config files, exports iblock archives, creates a `php_interface` snippet and performs encoding conversion.

It is a useful baseline for future requests like "упаковать решение SF4 через универсальный мастер". It is not safe to run as-is because it has hard-coded `simai.sf4conf`, `/ru`, `/.last_version` and broad iblock-copy assumptions.

Current local blockers:

- missing `mail.export.data` action file;
- missing `mail-templates.export.data` action file;
- missing source path `/bitrix/modules/simai.sf4conf`;
- missing source path `/bitrix/modules/simai.filebackup`;
- missing source path `/bitrix/wizards/simai/simai.sf4conf`;
- absent `data/` directory, acceptable for source-site export shape but visible.

## Kaizen

Lessons Learned:

- Export/packaging masters need a separate baseline from install/import masters.
- `data.export.file` targets are generated outputs; validators must not require these files before export execution.
- Full-site export via `CIBlock::GetList()` is useful for developer snapshots, but productized SF4 packages need explicit allowlists.
- Final zip/cleanup should be separated from generation and only enabled after audit.

Process Improvements:

- For packaging requests, start with source inventory and output-dir plan before skeleton generation.
- Classify export actions as read/export and generated-file actions as filesystem writes.
- Keep readiness blocked until missing action files and source paths are resolved.

Skill/Federation Improvement Candidates:

- Add a future controlled export package builder that can generate a parameterized `wizard.export`-style master from a manifest.
- Extend audit to distinguish generated output paths from input payload paths for more actions when their contracts are documented.

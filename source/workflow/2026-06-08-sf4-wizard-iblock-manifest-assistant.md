# SF4 Wizard Iblock/HL Manifest Assistant

## Goal

Создать read-only iblock/HL manifest assistant для SF4 universal wizard export
packaging: анализ локальных exported/config data structures, draft manifest
entries, source/specialist/graph refs, workflow, example evidence and gates.

## Done When

- Есть `scripts/sf4_wizard_iblock_manifest.py`.
- Скрипт читает только локальные folders/files and writes only under
  `source/output`.
- Скрипт находит iblock/HL archive-like data, PHP-array legacy data and SF4
  config hints where available.
- Скрипт формирует `iblock-manifest.draft.json` with explicit `iblocks` entries
  suitable for export builder review.
- Есть example evidence from real local solution/wizard data.
- Source docs, specialist and graph capability refs are updated.
- Verification and graph/federation gates pass.
- Kaizen is recorded.

## Safe Boundary

Allowed:

- read local source folders and generated package evidence;
- parse file names, zip member names and shallow PHP-array/config text hints;
- write repo-local source/output/docs/workflow only;
- run local Python validation.

Forbidden:

- execute Bitrix/PHP runtime;
- include PHP files for evaluation;
- run wizard actions;
- export/import iblocks or HL blocks;
- write to `/Users/rim/Sites/*`, DB, `/bitrix`, `/simai`, module install folders
  or live/staging/runtime paths.

## Gates

- federation route: primary `sf4`, companions `bitrix`, `tester`, confidence
  `high`.
- preflight: success.
- evidence: `source/output/action-gates/action-gate-report-20260608082427.json`.

## Workstreams

- Contract discovery.
- Assistant implementation.
- Example evidence.
- Specialist/source/graph integration.
- Verification and Kaizen.

## Batches

### Batch 1: Route, workflow and contract review

- status: completed
- work:
  - run federation route/preflight;
  - create workflow;
  - inspect export builder/inventory manifest and iblock/HL examples.

### Batch 2: Assistant implementation

- status: completed
- work:
  - implement read-only iblock/HL manifest assistant;
  - support zip, config and legacy PHP-array hints without executing PHP.

### Batch 3: Example evidence

- status: completed
- work:
  - run assistant on real local module/wizard data;
  - generate draft manifest and report under `source/output`.

### Batch 4: Source and graph refs

- status: completed
- work:
  - document helper contract;
  - update specialist/SKILL/source index/graph capability.

### Batch 5: Verification and sync

- status: completed
- work:
  - run syntax/JSON/acceptance checks;
  - run graph contract, skill sync, federation verify and route checks;
  - ingest Kaizen.

## Current Status

Goal status: completed.

Batches 1-5 completed. Read-only iblock/HL manifest assistant is implemented,
documented, exercised on SF4 archive payload and legacy PHP-array wizard data,
and synced through graph/federation gates.

## Evidence Log

- `source/output/action-gates/action-gate-report-20260608082427.json`: preflight passed.
- `scripts/sf4_wizard_iblock_manifest.py`: read-only assistant implemented.
- `source/output/wizard-iblock-manifest/simai.sf4biblio/iblock-manifest.report.json`: SF4 archive payload example, iblocks `44`, highload `0`.
- `source/output/wizard-iblock-manifest/simai.sf4biblio/builder-manifest.merged.draft.json`: builder manifest draft with explicit iblock allowlist.
- `source/output/wizard-iblock-manifest/simai.fund.legacy/iblock-manifest.report.json`: legacy PHP-array data example, iblocks `27`, highload `2`.
- `source/wizard/iblock-manifest-assistant.md`: helper contract documented.
- `source/wizard/source-index.json`: helper/evidence refs added.
- `skills/sf4/SKILL.md`: helper command added.
- `skills/sf4/specialists/universal-wizard.md`: helper role and examples added.
- `graph/specs/objects/capability-sf4-universal-wizard-specialist.json`: helper source/evidence refs added.
- JSON validation passed for source index, graph capability and generated helper reports.
- `python3 -m py_compile`: passed for all SF4 wizard helper scripts.
- `scripts/sf4_wizard_acceptance.py --manifest source/wizard/acceptance-fixtures.json`: passed.
- `git diff --check`: passed.
- `scripts/mirai_graph_contract_gate.py`: passed, canonical write is not allowed by gate output.
- `skill-change-detect.sh --skill sf4`: changed skill source detected, blockers `0`.
- `skill-graph-sync.sh --skill sf4`: synced latest evidence under `graph/generated/mirai_graph/*/skill-graph-sync-sf4-20260608083046-*`.
- `federation-verify.sh --profile admin --no-write`: passed, blockers `0`.
- `federation-route-check.sh --profile admin --json`: passed, routes `64/64`.
- route smoke for `подготовить iblock highload manifest allowlist для SF4 universal wizard export packaging без запуска runtime`: primary `sf4`, companions `bitrix,tester`, confidence `high`.

## Kaizen

Lessons Learned:

- Existing solution data has at least two materially different iblock packaging
  shapes: SF4 universal zip payloads and legacy PHP-array wizard data.
- Iblock archive filenames are good allowlist candidates, but SF4 config keys
  are only hints because config may contain forms/properties/views unrelated to
  exported archive availability.
- Highload hints need separate treatment; they should not be silently merged
  into iblock export lists.

Process Improvements:

- The packaging chain should add an allowlist review step before export builder
  when a solution has many iblock archives:
  inventory -> iblock manifest -> builder -> audit -> rollback -> readiness.
- Config-only and highload signals must remain visible in reports so a human can
  decide whether additional action contracts are needed.

Skill/Federation Improvement Candidates:

- Add a future `real_artifact` mode for iblock manifest assistant that validates
  expected archive files against a reviewed manifest without executing Bitrix.
- Add highload-specific export/import action contract notes once the exact
  supported universal action path is confirmed.

Follow-up Proposals:

- Build a developer-chain comparison report: developer `wizard.export` sample vs
  generated inventory/builder/iblock-manifest chain.
- Add a manifest apply helper that merges reviewed `builder-manifest.patch.json`
  into an export manifest only under `source/output`.
- Prepare a disposable-runtime checklist for actually running generated export
  masters when user explicitly approves a Bitrix environment.

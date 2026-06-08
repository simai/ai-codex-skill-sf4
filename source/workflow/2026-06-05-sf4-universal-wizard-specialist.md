# SF4 Universal Wizard Specialist Source Pack

## Goal

Prepare a source corpus under `source/wizard/` for a future dedicated SF4 Universal Wizard specialist.

## Done When

- `source/wizard/` contains a clear index of real-world source folders.
- Runtime logic of `simai:sf.wizard` and `simai:sf.wizard.stage` is captured.
- Action library inventory from `university.test` and `sf4.test` is captured.
- `simai.sveden` and `simai.sf4university` case notes are separated.
- Training backlog for the future specialist is explicit.
- No canonical skill source is changed before owner-approved apply plan.

## Source Inputs

- `/Users/rim/Sites/university.test/simai/wizard`
- `/Users/rim/Sites/sf4.test/simai/wizard`
- `skills/sf4/references/wizard-actions.md`
- `skills/sf4/references/system-layer-simai.md`

## Batches

### Batch 1 - Source Corpus Scaffold

Status: completed

Create initial files in `source/wizard/` from read-only analysis of real wizard folders.

Evidence:

- Federation route primary skill: `sf4`.
- Preflight gate status: success.
- Gate evidence: `source/output/action-gates/action-gate-report-20260605194835.json`.

### Batch 2 - Deep Action Notes

Status: completed

Expand each action family with exact parameter contracts, input/output data keys, side effects, idempotency rules and failure modes.

Progress:

- Added module install wizard sources from `test.test`.
- Captured legacy Bitrix `wizard_sol` model and newer SF4 wrapper-to-universal-master model.
- Added training plan stages for master creation, data packaging, visual design, action contracts and QA.
- Added first action contract table for `iblock.import.archive`, `iblock.export.archive`, `iblockconfig.import.data`, `file.copy`, `replace.code`.
- Added packaging matrix for universal master data, module installer assembly and legacy PHP-array data.
- Added export/data packaging notes for highload-aware `iblock.export.archive`.
- Added master blueprint, visual contract, read-only validator spec and specialist apply plan.

Evidence:

- `source/wizard/module-install-wizard-study.md`
- `source/wizard/training-plan.md`
- Gate evidence: `source/output/action-gates/action-gate-report-20260605202155.json`.
- Gate evidence: `source/output/action-gates/action-gate-report-20260605225403.json`.
- `source/wizard/action-contracts.md`
- `source/wizard/packaging-matrix.md`
- `source/wizard/export-packaging-data.md`
- `source/wizard/master-blueprint.md`
- `source/wizard/visual-contract.md`
- `source/wizard/validator-spec.md`
- `source/wizard/specialist-apply-plan.md`

### Batch 3 - Specialist Draft

Status: in progress

Convert source corpus into a proposed specialist profile and owner-approved apply plan.

Progress:

- `source/wizard/specialist-apply-plan.md` now defines proposed canonical targets, required gates and tracking decision.

## Gates

- Do not edit `skills/sf4/SKILL.md`, `rules/`, `references/`, `specialists/` or graph canonical files until the source pack is reviewed.
- Treat live wizard execution and site writes as out of scope for this phase.
- Keep secrets, credentials and private runtime logs out of the corpus.
- When promoting this corpus into skill source, run skill graph sync and federation verification.

## Lessons Learned

- The current SF4 skill has wizard coverage, but not a dedicated stateful orchestration specialist.
- Real wizard knowledge must distinguish master scenario, action library, payload package, generated installer payload and runtime storage.

## Process Improvements

- Future specialist preparation should start with source corpus files, not direct edits to `SKILL.md`.
- Missing `.wizard.config.php` in a master folder should be recorded as an evidence-backed blocker, not assumed away.

## Skill/Federation Improvement Candidates

- Add an SF4 Universal Wizard specialist after source pack review.
- Add graph capability detail for master/action/stateful wizard runtime.
- Add QA checklist for action contracts, payload presence and long-running AJAX state transitions.

## Follow-up Proposals

- Review `source/wizard/` with the user.
- Fill per-action deep notes for the highest-risk actions first: `iblock.import.archive`, `iblockconfig.import.data`, `site.update.sveden`, `file.copy`, `replace.code`.

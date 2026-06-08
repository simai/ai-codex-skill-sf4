# SF4 Universal Wizard Source Pack

This directory is a staging corpus for preparing a dedicated SF4 Universal Wizard specialist.

It is intentionally separate from canonical skill files. These notes collect real-world evidence and working hypotheses before any owner-approved specialist or skill-source update.

## Current Sources

- `/Users/rim/Sites/university.test/simai/wizard`
- `/Users/rim/Sites/sf4.test/simai/wizard`
- `skills/sf4/references/wizard-actions.md`
- `skills/sf4/references/system-layer-simai.md`

## Files

- `source-index.json` - machine-readable source inventory.
- `runtime-model.md` - how the universal wizard runtime works.
- `action-library-inventory.md` - action catalogue and families.
- `case-simai-sveden.md` - concrete `simai.sveden` install/update chain.
- `case-simai-sf4university.md` - payload case with missing runtime config evidence.
- `case-wizard-export-packaging.md` - developer sample for packaging a solution into `/.last_version/install` through a universal export master.
- `module-install-wizard-study.md` - module install wizard patterns from legacy and newer SF4 solution packages.
- `action-contracts.md` - per-action contracts for the highest-risk universal wizard actions.
- `packaging-matrix.md` - packaging matrix for master data, config, archives, public files, modules and legacy PHP-array data.
- `export-packaging-data.md` - focused notes for preparing iblock/highload archive data through `iblock.export.archive`.
- `export-builder.md` - manifest-driven generator for `wizard.export`-style solution packaging masters.
- `export-builder-example.json` - example export manifest on real local source paths.
- `export-inventory-helper.md` - read-only site inventory helper that drafts export-builder manifests and evidence.
- `iblock-manifest-assistant.md` - read-only iblock/HL manifest helper for archive/config/legacy data.
- `rollback-plan-checker.md` - backup/rollback plan template/check flow and readiness integration.
- `master-blueprint.md` - target structure and checklist for a new universal master.
- `visual-contract.md` - visual configuration contract for SF4 universal masters and legacy Bitrix wizard previews.
- `validator-spec.md` - read-only `sf4_wizard_audit.py` validator specification.
- `specialist-apply-plan.md` - proposed path for promoting this corpus into canonical SF4 skill sources.
- `specialist-brief.md` - proposed specialist scope, responsibilities and boundaries.
- `training-plan.md` - staged plan for turning this corpus into a specialist.
- `open-questions.md` - unresolved evidence gaps.

## Working Rule

Do not promote these files into `skills/sf4/*`, graph specs or specialist definitions until the source pack is reviewed and an apply plan is approved.

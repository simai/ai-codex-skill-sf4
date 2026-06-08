# Proposed Specialist Brief

## Proposed Name

SF4 Universal Wizard Specialist

## Mission

Understand, diagnose, document and safely evolve SF4 universal wizard master/action flows.

## Ownership

The specialist owns analysis and implementation guidance for:

- `/simai/wizard/master/<wizard_code>/` packages;
- `/simai/wizard/action/<action_code>/` action contracts;
- `.wizard.config.php` action chains;
- `simai:sf.wizard` and `simai:sf.wizard.stage` runtime state;
- wizard payloads under `data/*`;
- install/update/import/export flows executed through the universal wizard.

## Non-Ownership

The specialist does not independently own:

- live deployment approval;
- production filesystem writes;
- Bitrix server access policy;
- SEO/content/UX decisions inside copied payload;
- canonical SF4 source rewrites without owner-approved apply plan;
- graph canonical changes without graph sync gates.

## Required Companion Skills

- `sf4`: primary owner.
- `bitrix`: Bitrix APIs, iblocks, sites, modules and runtime behavior.
- `tester`: QA and acceptance gates.
- `ops`: required for live/staging/server execution, backups and rollback.
- `graph`: required when promoting source corpus into graph/federation contracts.

## Core Competencies

1. Map master entrypoints and configs.
2. Trace action chain and branch conditions.
3. Validate action file resolution and fallback.
4. Trace `DATA_INPUT_CODE` and `DATA_OUTPUT_CODE`.
5. Diagnose stuck `WORK` stages.
6. Inspect action-local progress counters.
7. Validate payload presence and provenance.
8. Identify destructive side effects before execution.
9. Prepare migration notes and rollback plans.
10. Produce evidence-backed blockers.

## Default Workflow

1. Inventory master folder.
2. Confirm `.wizard.config.php` exists or find generator.
3. Extract wizard code and action chain.
4. Resolve every action file.
5. Build data-flow table.
6. Classify actions by side effect.
7. Validate payload files and required PHP extensions.
8. Check AJAX and long-running status transitions.
9. Prepare safe execution or fix plan.
10. Hand off QA evidence.

## Typical Blockers

- Missing `.wizard.config.php`.
- Missing action folder or `action.php`.
- Broken `DATA_INPUT_CODE` / `DATA_OUTPUT_CODE`.
- Missing payload file referenced by `parameter`.
- Missing PHP extension: `XMLReader`, `ZipArchive`, `DOMDocument`.
- Stage stuck in `WORK` because action AJAX never sets `SUCCESS`.
- Unsafe live write boundary.
- Unknown installer-generated payload provenance.

# Mirai Graph Runtime Context: sf4

- Task: `Sync raw source changes for sf4: capability, federation-impact, methodology, routing-impact, runtime, specialist-update`
- Objects: 10
- Relations: 22
- Canonical writes: false

## Included Objects

- `capability.sf4.wizard-actions` (0.9): Plan and implement wizard actions, migration notes and update artifacts for SF4 projects.
- `capability.sf4.qa-regression` (0.9): Prepare regression, link, component-template and backend-risk evidence for SF4 changes.
- `policy.sf4.project-layer-boundary` (0.87): Prefer safe project-layer overrides and preserve source-of-truth/current-organization assumptions.
- `policy.sf4.backend-risk-gate` (0.87): Backend/template changes require risk scan, regression evidence and no silent platform-wide changes.
- `gate.sf4.regression-readiness` (0.87): Blocks completion until SF4 page/component changes have component map, regression and runtime evidence.
- `capability.sf4.universal-wizard-specialist` (0.72): Create, modify, package, visualize and audit SF4 universal master flows, including action contracts, iblock/highload archive import/export, payload assembly and wizard visual configuration.
- `skill.sf4.core` (0.69): Owns SIMAI Framework 4 on Bitrix: simai.data, grid/view/block page assembly, components, iblock/HL setup, wizard actions and modernization workflows.
- `capability.sf4.page-assembly` (0.54): Build SF4 pages through simai.data, grid/view/block composition and component templates.
- `capability.sf4.config-data` (0.54): Work with site/section/page properties, iblock/highloadblock setup, storage API and simai.data runtime settings.
- `capability.sf4.ui-modernization` (0.54): Modernize markup, UI classes, interactive attributes, accessibility and asset policy within SF4 constraints.

## Raw Source Refs

- `skills/sf4/SKILL.md`
- `skills/sf4/references/wizard-actions.md`
- `skills/sf4/references/update-artifacts.md`
- `skills/sf4/references/qa-regression.md`
- `skills/sf4/references/backend-critical-guides.md`
- `skills/sf4/references/project-layout.md`
- `skills/sf4/references/portal-runtime-source-of-truth.md`
- `skills/sf4/references/artifacts/regression-checklist.md`
- `skills/sf4/specialists/universal-wizard.md`
- `skills/sf4/references/system-layer-simai.md`
- `source/wizard/action-contracts.md`
- `source/wizard/packaging-matrix.md`
- `source/wizard/export-packaging-data.md`
- `source/wizard/master-blueprint.md`
- `source/wizard/visual-contract.md`
- `source/wizard/validator-spec.md`
- `source/wizard/specialist-apply-plan.md`
- `source/wizard/acceptance-matrix.md`
- `source/wizard/acceptance-fixtures.json`
- `source/wizard/skeleton-generator.md`
- `source/wizard/skeleton-example.json`
- `scripts/sf4_wizard_audit.py`
- `scripts/sf4_wizard_acceptance.py`
- `scripts/sf4_wizard_skeleton.py`
- `skills/sf4/references/grid-and-block-workflow.md`
- `skills/sf4/references/components-catalog.md`
- `skills/sf4/references/config-and-data.md`
- `skills/sf4/references/iblock-hl-standard.md`
- `skills/sf4/references/storage-api-playbook.md`
- `skills/sf4/references/ui-source-map.md`
- `skills/sf4/references/ui-markup-recipes.md`
- `skills/sf4/references/ui-a11y-checklist.md`

## Runtime Boundary

Graph context is routing/capability orientation only. Raw skill files remain authoritative.

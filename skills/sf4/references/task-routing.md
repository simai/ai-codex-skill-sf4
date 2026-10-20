# SF4 Task Routing

Load only the route that matches the task. Step-by-step recipes are in
`task-playbooks.md` (section numbers below). Commands: `scripts-catalog.md`.
Rules per area: `../rules/`.

## Start

1. Run `sf4_project_audit.py` (detects `simai.data`, validates critical files,
   verifies `grid_view_*` mappings).
2. Read `project-layout.md` for path conventions and layer boundaries.
3. Pick one route below.

## Grid, View, Block And Template Areas

- `grid-and-block-workflow.md`; `production-patterns.md` for real-world
  area/view/block conventions; `sfgrid-editor-features.md` for `sf.grid` editor
  behavior.
- `system-layer-simai.md` when framework-level block/property/wizard context
  from `/simai` is needed.
- Full existing site: `page-map-and-modernization.md` (classify route type
  A/B/C first); the project's own baseline and case notes live in the project
  repository.
- `ui-catalog.md` when markup changes too.
- Playbooks: sections 1, 2, 9, 16. Rules: `../rules/project-layer-structure.md`.

## Frontend Markup, Utilities And UI Components

- `ui-catalog.md`, `ui-source-map.md`, `ui-class-cheatsheet.md`,
  `ui-modifier-strategy.md`, `ui-markup-recipes.md`.
- `ux-implementation-contract.md` when a `$ux` screen spec or handoff exists or
  the task starts from interface design.
- `component-template-resolution.md` for component-heavy pages.
- Use `/ru/ui` catalog pages as the primary source for class combinations;
  keep markup in project-layer blocks/views.
- Playbook: section 13. Rules: `../rules/frontend-markup.md`.

## Frontend Interaction, Assets And Accessibility

- `ui-interactive-dependencies.md`, `ui-interaction-attributes.md`,
  `ui-a11y-checklist.md`, `ui-asset-policy.md`.
- Inventory markers with `sf4_interactive_audit.py`.
- Playbook: section 14. Rules: `../rules/frontend-markup.md`.

## Backend Data, Property And API Patterns

- `bx-backend-source-map.md`, `storage-api-playbook.md`,
  `property-editor-playbook.md`, `backend-critical-guides.md`.
- Run `sf4_backend_risk_scan.py`.
- Playbook: section 15. Rules: `../rules/backend-data.md`.

## Linkage Remediation

- `linkage-remediation.md`; audit with `--link-report-json`, then
  `scaffold_missing_blocks.py` dry-run and small `--apply` batches.
- Playbook: section 9.

## Settings And Inheritance

- `config-and-data.md`, `simai-data-settings-runtime.md` (template merge,
  admin/public save flow, multisite rules).
- `solution-customization-technology.md` when settings are the first step of
  adapting an existing solution to a client design.
- `portal-runtime-source-of-truth.md` for portal/host-mode or tenant content.
- `property-editor-playbook.md` for `simai:sf.property.edit` schemas and save
  cycle.
- Playbook: sections 3, 4, 18.

## Components, Iblocks And HL-Blocks

- `components-catalog.md` (for `simai:sf.iblock.list`/`detail` on `.default`
  use its deep sections first: runtime pipeline, `AREA`/`SOURCE_*` mapping,
  template parameter groups); `iblock-hl-standard.md` before creating entities.
- `storage-api-playbook.md` when the project uses `simai.storage`;
  `component-template-resolution.md` for `IncludeComponent(...)` orchestration.
- Playbook: sections 5, 6, 8. Rules: `../rules/backend-data.md`.

## Wizard Actions And Deployment

- `wizard-actions.md`; `../specialists/universal-wizard.md` for universal
  master creation, package data, action contract changes, iblock/HL archive
  export/import, visual configuration or read-only audit.
- `system-layer-simai.md` for action/master folder conventions and fallback
  action resolution; `update-artifacts.md` for mandatory update outputs.
- Playbook: sections 7, 10. Stop when expected wizard config is missing.

## Quality And Regression

- `qa-regression.md`, `hygiene-and-secrets.md`, `update-artifacts.md`;
  templates in `artifacts/` (migration notes, upgrade notes, regression
  checklist, QA report).
- Playbook: sections 11, 12. Keep risk and evidence explicit.

## Debugging

- `troubleshooting.md`; settings/assembly drift: playbook section 18.

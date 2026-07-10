---
name: sf4
description: Implement and modernize SIMAI Framework 4 (SF4) projects on Bitrix using safe project-layer overrides. Use when tasks involve `simai.data` structure, grid/view/block page assembly, template areas, `simai:sf.*` components, site/section/page properties, iblock/highloadblock setup, wizard actions, or migration/update workflows in SF4.
---

# SIMAI Framework 4

`sf4` owns SF4 project-layer structure, `simai.data`, grids, views, blocks,
template areas, SF components, properties, iblock/HL mapping and wizard flows.

Before cross-owner work, load
[rules/skill-mesh-balance.md](./rules/skill-mesh-balance.md).

## Mirai Graph Runtime Entry

Use current federation/Mirai Graph context for substantial routing, gates and
companions. Raw SF4 sources remain authoritative for platform methodology and
judgement; graph-only runtime is forbidden.

Load [FULL_RUNTIME_PLAYBOOK.md](./FULL_RUNTIME_PLAYBOOK.md) for detailed task
routing, system-layer study, UI catalogs, wizard/package operations, backend
risk rules, portal host-mode QA, migration or release work. For a narrow task,
load only the directly relevant reference named below.

## Core Workflow

1. Identify site root, site dir, active layer and source/runtime copies.
2. Run `python3 scripts/sf4_project_audit.py --site-root <root>` when a project
   tree is available.
3. Classify the task: page composition, block/component, settings/inheritance,
   data schema, wizard/update, frontend interaction or linkage remediation.
4. Load the matching reference from the full playbook; do not load the entire
   catalog for a bounded change.
5. Modify project layer first, normally `{site_dir}/simai.data`.
6. Validate syntax, required companion files, runtime markers and the touched
   regression surface; clear relevant cache and retest.
7. If source and deployed copies coexist, reconcile both and record evidence.

## Non-Negotiable Boundaries

- Keep `/simai`, `/bitrix/templates/simai.framework` and
  `/bitrix/components/simai` immutable unless explicitly authorized.
- In portal projects use `simai.portal`; do not introduce `simai.framework`.
- Keep `grid_view_*` aligned with real view folders and metadata/params/lang
  adjacent to block code.
- Never edit generated `/bitrix/cache/js/*`; identify the true JS source.
- Preserve accessibility attributes, editor overlays and required
  `position-relative` wrappers.
- Prefer existing SF4 utilities/classes and project CSS over invented classes.
- Schema/update work requires migration and rollback notes.
- HTTP 200 alone is not portal/runtime acceptance.
- Implement SEO/UX contracts through SF4 surfaces without redefining them.

## Reference Selection

- grid/view/block: `references/grid-and-block-workflow.md`;
- settings/data: `references/config-and-data.md` and
  `references/simai-data-settings-runtime.md`;
- components/entities: `references/components-catalog.md` and
  `references/iblock-hl-standard.md`;
- frontend/interactions: `references/ui-catalog.md`,
  `references/ui-interactive-dependencies.md`, `references/ui-a11y-checklist.md`;
- wizard/update: `references/wizard-actions.md` and
  `references/update-artifacts.md`;
- QA/recovery: `references/qa-regression.md` and
  `references/troubleshooting.md`.

## Output

Return target layer, changed paths, loaded references, migration/rollback
impact, checks and runtime evidence, blockers and the smallest next action.

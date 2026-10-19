# SF4 Non-Negotiable Rules

These rules apply to every `sf4` task. Detailed per-area rules live in
`../rules/`.

## Layer Ownership

- Keep `/simai`, `/bitrix/templates/simai.framework` and
  `/bitrix/components/simai` immutable by default. Edit the system layer only
  when the user explicitly asks; use `references/task-playbooks.md` section 17.
- Place project customizations in `{site_dir}/simai.data`; modify only the
  layer relevant to the task.
- In portal projects `simai.portal` replaces `simai.framework`. Do not require
  or include `simai.framework` in portal modules or portal demo payloads.
- If module source and deployed site copy coexist, sync touched assets to both
  locations and retest on the target site.

## Source Of Truth

- Mirai Graph context is the first machine-readable index for routing, gates
  and companions; raw `sf4` sources stay authoritative for methodology,
  judgement and final domain verdicts (Hybrid SOT, never graph-only runtime).
  Sensitive, runtime, security and safe-write decisions require raw-source
  fallback and the relevant owner gate.
- Never edit generated `/bitrix/cache/js/*`. For interactive bugfixes identify
  the JS source first (`template.php` inline script, template `script.js` or
  another included asset) and edit only source files.
- For existing SF4 solution customization pass the Solution Technology
  Acceptance chain first (`../rules/solution-acceptance-chain.md`). A page that
  works by smoke but bypasses the chain is only a technical prototype.

## Evidence

- Schema, data and update tasks always carry migration notes and a rollback
  plan (state "no changes" explicitly when applicable).
- Non-trivial tasks keep smoke/regression evidence in a checklist or QA report.
- In portal/host-mode runtime `HTTP 200` is not SF4 acceptance: verify page
  class, required blocks/content markers, current organization/source
  selection, host-mode include paths, editor/admin context and regression
  sentinels (`references/portal-runtime-source-of-truth.md`).

## Contract Boundaries

- When implementing an SEO Contract from `$seo`, do not redesign SEO decisions
  inside `$sf4`. Implement it through SF4 surfaces: grids, views, blocks,
  `simai.data`, template areas, page/section properties, `simai:sf.*`
  components, visible content blocks, headings, breadcrumbs, internal links,
  media/alt and public route behavior. If SF4 constraints conflict with the
  contract, report a blocker to `$seo` instead of silently changing
  URL/canonical/meta/content decisions.
- A `$ux` handoff is mapped explicitly to SF4 area/view/block/component
  structure before markup is edited.

# Skill Mesh Balance

`$sf4` owns SIMAI Framework 4 project-layer implementation on Bitrix:
`simai.data`, grid/view/block page assembly, template areas, `simai:sf.*`
components, site/section/page properties, iblock/HL setup patterns, wizard
actions, SF4 migration/update workflows, and safe project-layer overrides.

## Does Not Own

- Generic Bitrix platform facts and marketplace/module policy owned by
  `$bitrix`.
- SF5/Larena implementation contracts owned by `$sf5` and `$larena`.
- Portalization strategy owned by `$orgportal`.
- Documentation methodology/content owned by `$docs`.
- SEO Contract decisions owned by `$seo`.
- UX acceptance owned by `$ux`.
- QA evidence owned by `$tester`.
- Runtime/deploy mitigation owned by `$ops`.

## Companion Contracts

- Use `$bitrix` for Bitrix module, iblock, admin, installer, marketplace, and
  safe-write facts beyond SF4 project-layer rules.
- Use `$orgportal` when converting individual SF4 solutions into organization
  portals.
- Use `$seo` and `$ux` as contract owners for public/search and UI changes.
- Use `$tester` for smoke/regression evidence and `$ops` for runtime issues.
- Use `$docs` for substantial documentation structure and content.
- For SF4 -> SF5 or other reference-adaptive checks, `$sf4` owns the source
  behavior: `simai.data`, grid/view/block, template area, component/property,
  iblock/HL, wizard, and project-layer source-of-truth facts. `$tester` owns
  invariant evidence; `$sf5` or another target skill owns target adaptation.

## Handoff

Return affected SF4 routes, `simai.data` paths, grid/view/block bindings,
template areas, component/property changes, project-layer constraints, evidence,
blockers, and the companion skill expected to review.

For reference-adaptive handoff, also return reference behavior, mandatory
invariants, allowed target adaptations, source-of-truth notes, and regression
risks that must remain visible.

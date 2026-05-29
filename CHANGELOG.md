# Changelog

## Unreleased

### Changed

- Added SF4 solution customization guidance for Figma-to-SF4 work: translate
  visible design into editable data models first, prefer `simai:sf.iblock.*`
  components, keep one root `simai:sf.grid` per view, validate public editor
  dialogs, and preserve component/template/cache conventions.
- Clarified iblock property semantics for SF4 solution customization: use
  `SIMAI: Чекбокс` (`simai_checkbox`) for `Y`/`N` flags and keep repeated
  template headings, labels, empty states, and CTA text in template language
  files instead of central iblock elements.
- Added a calculated-indicator rule for SF4 solution customization: do not
  store operational totals such as pets, goal, collected, left, and progress as
  magic central-element fields when they can be calculated from linked pets,
  volunteers, needs, intakes, orders, or deliveries.
- Added related media/history routing guidance for SF4 detail pages: model
  design photo albums as linked iblock sections, vary layout by album count,
  make album/history cards actionable, organize album sections as a hierarchy,
  prefer generic gallery route names, and verify target routes before linking.
- Clarified nested-component editing guidance: component templates that display
  linked editable datasets should call child Bitrix/SF4 components and expose
  child edit areas instead of rendering everything from manual arrays.
- Extended the nested-component rule to related detail-page sections such as
  current needs, help history/deliveries, and reviews: filter child
  `simai:sf.iblock.list` components by the central entity relation so public
  edit mode edits the actual child elements.
- Clarified that shared process/checklist sections should also use nested
  list components when their steps live in an iblock, even if they are not
  filtered by the central entity.
- Added a cardinality QA rule for SF4 detail templates: validate several
  central elements with zero/one/many related records and fix uneven spacing in
  shared component/CSS layers, not in individual demo content.
- Clarified that SF4 section/page `.property.php` files for solution routes
  must use the `return ['section' => ..., 'page' => ...]` format; legacy
  `$arDirProperties` can leave inherited sidebars or containers active.
- Added a header-to-hero continuity rule: when the header background continues
  the hero background, use an explicit `flush_bottom`-style context and verify
  zero geometry gap between the header area/shell and the hero block, not only
  matching computed colors.
- Added a slider implementation rule for Figma-to-SF4 customization: carousel
  controls and dots in design require a real dynamic slider with browser-checked
  navigation, media ratio and grid fallback, not decorative arrows on a static
  list.

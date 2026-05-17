# SF4 Solution Customization Technology

Use this reference when a project customizes an existing SF4 solution for a
client design or a new site concept.

## Core Rule

Do not start from an ad-hoc page. Start from the solution.

The first implementation question is:

```text
Which existing SF4 setting, section/page property, view, block, component, or
dynamic source should own this change?
```

Only create new code after those primitives are mapped.

## Gate 1: Site Settings Baseline

Before changing templates or routes, bring the site as close as possible to the
client design through site-level settings.

Inspect:

- `<site_dir>/simai.data/config/.site.config.php`;
- `<site_dir>/simai.data/config/lang/<lang>/.site.config.php`;
- `<site_dir>/simai.data/.site.property.php`;
- active `grid_view_*` folders under `simai.data/grid/view`;
- runtime merge in `simai.data/template/property.php`.

Typical setting groups:

- project mode: `demo_mode`, `expert_mode`;
- brand: `organization_name`, `organization_logo`,
  `organization_logo__theme_dark`, `organization_copyright`,
  `site_favicon`;
- contacts: `organization_email`, `administration_email`,
  `organization_phone`, `organization_address`, `organization_worktime`,
  `organization_map`;
- parent organization: `use_organization_parent`, `organization_parent_*`;
- SEO and structured preview: `title`, `title_browser`, `description`,
  `keywords`, `meta_image`;
- leader/person demo data: `chief_*`;
- colors: `site_primary_color`, `site_secondary_color`, `body_theme`,
  `body_background_color`, `pagewrap_background_color`;
- header/footer: `header_*`, `footer_*`;
- banners: `show_banner_header`, `show_banner_sidebar`,
  `show_banner_main`, `show_banner_footer`;
- menu: `menu_*`, `menu_brand_*`, `menu_social`;
- social ids and external links: `social_*`, `widget_*`;
- script areas: `script_top`, `script_bottom`, and include files under
  `simai.data/template/area/script/*/template.php`;
- typography: `body_font`, `title_font`, `title_font_weight`;
- grid views: `grid_view_header`, `grid_view_footer`, `grid_view_home`,
  `grid_view_main_top`, `grid_view_main_bottom`,
  `grid_view_sidebar_left`, `grid_view_sidebar_right`.

Acceptance:

- demo mode is off when the project is no longer a generic demo;
- obvious base-solution demo identity is removed or replaced;
- unknown real client contacts are not invented;
- logo and favicon are taken from the client design or confirmed client
  materials, preferably as SVG, and wired through SF4 settings rather than
  hardcoded into templates;
- SEO defaults and structured preview image are set or cleared from demo values;
- demo person data, parent organization, social ids/urls, and third-party demo
  scripts are removed unless confirmed by the client;
- brand colors and basic layout regions are set through site settings;
- banners/widgets/social blocks are enabled only when they are part of the
  target design or confirmed client content;
- every `grid_view_*` value resolves to a real folder;
- target route still renders after settings are applied.

## Gate 2: Section/Page Properties

If the target page needs a different header/footer/sidebar/title/banner behavior
than the rest of the site, use section or page properties before editing
templates.

Inspect:

- `/<site_dir>/.property.php`;
- section subtree `/.property.php`;
- page-specific property storage when used by the solution;
- `simai.data/config/.structure.config.php`.

Use this for page-specific:

- `grid_view_header`;
- `grid_view_footer`;
- `grid_view_main_top`;
- `grid_view_main_bottom`;
- `grid_view_sidebar_left`;
- `grid_view_sidebar_right`;
- `show_title`;
- `show_breadcrumb`;
- `show_banner_*`;
- layout/sidebar settings.

## Gate 3: View/Block Mapping

After settings and properties, map the target route to the SF4 assembly chain:

```text
route -> template -> area -> grid_view_* -> view -> sf.grid -> block -> component/data source
```

Decide whether the change is:

- existing view selection;
- new project-layer view under `simai.data/grid/view/...`;
- project-layer block override under `simai.data/grid/block/...`;
- component template override;
- new reusable component/module;
- temporary prototype.

### Header/Footer Areas

For `header` and `footer`, do not start with page-level custom HTML. Work
through SF4 regions:

1. inspect active `grid_view_header` and `grid_view_footer`;
2. inspect existing views under `simai.data/grid/view/header` and
   `simai.data/grid/view/footer`;
3. inspect existing blocks under `simai.data/grid/block/header` and
   `simai.data/grid/block/footer`;
4. tune site/page settings first: `menu_*`, `menu_brand_*`, `organization_*`,
   `footer_*`, `show_*`;
5. if the existing view is not enough, create a project-layer view under
   `simai.data/grid/view/<area>/<project-code>`;
6. if existing blocks are not enough, create a narrow project-layer block under
   `simai.data/grid/block/<area>/<project-code>` and keep the source data model.

Prefer `header/menu.main` for navigation before creating a custom menu block:
it already supports brand, Bitrix main menu, dropdowns, search, CTA button,
mobile menu, fullscreen/fixed behavior and visual settings. A project-specific
menu block is allowed only after `menu.main` settings and view modifiers are
proven insufficient.

When a project-specific menu block is needed, keep it in the SF4 project layer
first: `simai.data/grid/block/header/<project-code>`. Preserve the dynamic
source, for example Bitrix main menu, site settings, or an existing component
data source. Do not create a partial `/local/templates/<site-template>/...`
directory only to host one component template: Bitrix may switch
`SITE_TEMPLATE_PATH` to that local template folder, and pages can lose the
framework `header.php/footer.php` if the full template is not mirrored.

If a Figma design does not describe interaction behavior, do not leave the
component with generic or awkward defaults. Define the missing interaction in
the project style: hover/focus, keyboard escape, outside-click close, mobile
open/close state, aria attributes, and a screenshot/browser acceptance check.

When implementing visual container effects from design, such as translucent
backgrounds, blur, glass panels, shadows, or rounded header shells, first verify
the real HTML emitted by `sf.grid` and the selected view/block. Do not assume
that a framework wrapper like `.navigation-container` exists in every assembly.
Attach the effect to the actual stable project-layer element, keep any
framework wrapper selector only as a fallback, and verify computed style plus a
browser screenshot.

Treat visible navigation affordances as requirements, not decoration. If the
design shows dropdown markers near menu items, the SF4 implementation must
support at least a second menu level through the project/Bitrix menu source:
child `.menu.php` files, existing menu component data, or another editable
source of truth. A chevron without child items and open/close behavior is not an
acceptable implementation. When the dropdown layout is not specified in the
design, choose a simple project-style interaction: hover/focus and first-click
open on desktop, Escape/outside-click close, visible focus states, and a mobile
fallback that keeps child links reachable.

For mobile header menus, do not dump all submenu levels open by default when the
desktop design implies dropdown navigation. Use a vertical accordion pattern:
top-level links remain reachable, submenu toggles are separate buttons with
`aria-expanded`, child lists are collapsed by default, and closing the mobile
panel resets open submenu state. Verify that the mobile panel creates a real
overlay layer with its own background and sufficient `z-index`; page content
must not visually overlap menu text. The mobile panel should align to the same
outer visual bounds as the header shell/container unless the design explicitly
shows a full-bleed menu.

Acceptance:

- the region is selected through `grid_view_header` or `grid_view_footer`;
- new view/block lives in the project layer, not in the solution core;
- the main route of an adapted solution must keep the shared SF4 shell unless
  the user explicitly approves a standalone prototype. Do not ship `/ru/` or
  another primary route through `prolog_before` + custom standalone HTML when
  the task is to adapt the existing solution. Use `bitrix/header.php`,
  `bitrix/footer.php`, site settings and the relevant `grid_view_*` areas so
  header, footer, service areas, SEO/meta, scripts and future settings continue
  to work as one solution;
- menu content remains editable through Bitrix menu or the existing data source;
- dropdown markers in the design map to real second-level menu behavior and
  editable child menu sources;
- mobile navigation uses collapsed accordion behavior for child levels and is
  checked as an overlay, not just as visible links;
- translucent/blurred visual containers are applied to real emitted wrappers
  and verified in browser, not only to expected framework wrappers;
- logo/brand assets come from SF4 settings;
- cookie notification settings are part of the first site-settings baseline:
  remove demo domains/texts, set client/project-safe copy and links, and choose
  a position/width that does not visually conflict with the header/search;
- project-layer markup uses SF4 UI catalog, components and utility classes
  first: `sf-*`, `t-*`, `theme-*`, `c-*`, `btn`, `form-control`, layout,
  spacing, display and alignment utilities;
- when SF4 has a component or modifier for the element, use it before writing a
  project class. Buttons must use the SF4 button contract (`btn`,
  `btn-primary`/`btn-secondary`, size modifiers such as `btn-1`,
  icon-only `btn-icon`, `btn-rounded`/`btn-square`/`btn-outline`,
  `waves-effect`/`waves-light`) unless a documented framework gap requires a
  small project-layer extension. Pick the closest standard SF4 variant instead
  of reproducing the Figma pixels with custom CSS: for a ~50px design button use
  the large `btn-1` variant, use the default radius for normal rounded corners,
  and reserve `btn-rounded` for full/pill buttons;
- custom CSS/classes are limited to project scope, state hooks, missing
  interactions, icons, exact asset sizing or proven framework gaps; they must
  not become a parallel visual framework;
- expandable header search must keep a safe responsive boundary: do not let the
  open field overlap the brand/logo or visually glue to it on wide screens.
  Prefer geometry-based sizing from the emitted header elements
  (`brand.right + gap` to the search/form edge) when the header has flexible
  columns, glass containers, or project-specific padding. Viewport-only formulas
  are fragile after layout changes. Verify the open state by computed rects and
  screenshot on the target desktop width;
- desktop, mobile and relevant interaction states are checked with
  browser/screenshot evidence;
- obsolete demo panels, widgets and unrelated menu items are removed.

## Gate 4: Dynamic Data Analogy

Repeated or editable content must follow the base solution data model by
analogy: iblocks, highload blocks, storage tables, site settings, component
params, or existing list/detail routes. Static markup is a temporary fallback
only when explicitly labelled.

When a client-design main page already exists as a large temporary view, do not
rewrite it into a full new system in one pass. Decompose it section by section:
create one narrow project-layer block under
`simai.data/grid/block/<area>/<project-code>`, connect it through the current
view via `simai:sf.grid`, preserve the existing dynamic data source or fallback,
sync and smoke-test the page, then move to the next section. This keeps the
runtime page working while gradually converting the prototype into a normal SF4
assembly.

For iblock-backed lists and detail pages, first try the universal SF4
components before creating custom readers: `simai:sf.iblock.list` for lists and
`simai:sf.iblock.detail` for details. Their `.default` templates support many
`SOURCE_*` mappings, modifiers, buttons, images, properties, include areas and
layout options. A project block may wrap these components to provide a section
heading, tuned params, modifiers or item include snippets, but it should not
replace the component with a manual `CIBlockElement` loop unless the standard
component path is proven insufficient and the reason is documented.

## BuddyDinner Lesson

The `/ru/donate/` payment flow worked technically, but the first implementation
was too ad-hoc: it created a standalone page with inline layout instead of first
using site settings, page properties, and the existing SF4 view/block model.

For similar projects, `sf4` must stop before coding and produce:

- source solution primitive map;
- site settings baseline;
- section/page property plan;
- view/block/component mapping;
- acceptance checks.

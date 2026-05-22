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

When translating a Figma design into an SF4 solution, do not treat the picture
as only a layout specification. First translate the visible design into a
functional data model:

- what entities are visible on the screen;
- which existing solution entities already represent them;
- where each entity should be stored: site settings, include file, iblock,
  highload block, custom table/module, or external integration;
- which fields and properties are required;
- how entities are related to each other;
- which list/detail routes, filters, actions, permissions and editor surfaces
  are needed.

Only after this source-of-truth map is clear, choose the visual representation:
grid rows, include files, `simai:sf.iblock.*` components, component templates,
or project-layer blocks. This prevents static replicas of Figma screens and
keeps the result editable, reusable and compatible with solution updates.

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

When moving a standalone/list/detail prototype into the normal SF4 shell, verify
the inherited page geometry before tuning the component template. A page can
render the correct header and footer but still be visually wrong because the
standard template keeps inherited sidebars or a constrained `main_width`, for
example `sf-main-area col-md-8`. First set the section/page properties that
describe the route contract:

- `sidebar_show => none` when the design has no left/right sidebars;
- `use_page_container => N` when the project view already owns its own
  containers and section widths;
- `show_title`, `show_breadcrumb`, `show_banner_main` according to the design;
- `main_modifier` only for ordering/link-theme classes that the shell needs.

Then verify in the browser that the target page content lives under the shared
SF4 header/footer, the main area has the expected column width such as
`col-md-12`, and no old standalone wrapper or broad reset CSS hides normal SF4
areas.

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

Do not duplicate header views or blocks only because the header appears on
different backgrounds. Model the difference as a page/header context contract:
for example `mode=static|over-hero`,
`background=white|mint|dark|transparent`,
`surface=glass|white|plain`, `contrast=dark|light`, and
`width=default|wide|full`. The page or hero scene chooses the context before
the shared `grid_view_header` renders, while the single project-layer header
block converts context into modifier classes. Pages without a hero must still
work through a safe static default such as `static + white background + dark
contrast`; the header must not depend on a hero area being present.

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
- different header backgrounds are handled by parameters/context modifiers on
  the shared header view/block, not by creating separate header copies for
  home, dark hero and inner pages;
- project views that include `simai:sf.grid` must preserve the grid editor
  hooks: never hardcode `HIDE_ICONS => "Y"` for active editable grids. Follow
  the standard SF4 pattern and switch icons by `grid_edit_mode`, for example
  `Property::getValue(SF_SITE_DIR, "grid_edit_mode") == "Y" ? "N" : "Y"`.
  Also do not hide normal solution areas from active page CSS/JS with broad
  `display:none!important`; standalone reset code is allowed only in an
  isolated fallback wrapper, not in the normal `bitrix/header.php` flow;
- custom header/menu layers must not block Bitrix public editing controls. If a
  project header needs high `z-index` in public mode, add an explicit
  `grid_edit_mode` class/condition that lowers project `z-index` and restores
  Bitrix component toolbar clickability in edit mode;
- after changing a file that contains an editable `IncludeComponent`, reload
  the public page before testing the component editor. Bitrix stores `src_line`
  in the generated toolbar at page render time; if the file was edited and the
  component moved from that line, `component_props.php` can return an empty
  popup body and the UI may stay on "Загрузка..." indefinitely;
- when the public component editor stays on "Загрузка...", verify the exact
  dialog request, not only the direct settings URL. The real Bitrix popup uses
  `component_props.php?...&bxsender=core_window_cdialog` with `Bx-Ajax: true`
  and the current admin session. A direct `200` without AJAX headers is not
  sufficient evidence. If the AJAX request returns an auth script or `500`,
  refresh/re-authenticate the admin session first; if the same authenticated
  request returns a full `publicComponentDialogManager` payload, the component
  source is parseable and the remaining issue is the browser session/dialog
  state, not the SF4 view itself;
- project grid block `.description.php` files must `return` an array with at
  least `NAME`. Do not only assign `$arTemplateDescription`: `sf.grid`
  parameter loading calls `SIMAI\Main\Block\Section::getNameList()`, requires
  the description file, and then indexes the result as an array. A scalar return
  can make `component_props.php` answer `500` and leave the public editor stuck
  on "Загрузка...";
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

For client-facing SF4 solution adaptation, treat editability as a delivery
requirement, not an enhancement. The finished site must be maintainable by the
client/content manager through Bitrix/SF4 editing surfaces. Therefore:

- do not keep real page content only in PHP arrays, static HTML, or template
  literals except as an explicitly temporary scaffold;
- place repeated or content-managed data in existing suitable iblocks whenever
  the source solution already has the right entity;
- if the source solution has no suitable entity, create a new iblock by analogy
  using SF4 naming (`sf_<SITE_ID>_<domain>` for type and
  `sf-<SITE_ID>-<entity>` for iblock code);
- expose fields through SF4/Bitrix editor forms and project config schemas so
  the client can edit content without changing code;
- use standard SF4 components first: `simai:sf.iblock.list` for lists,
  `simai:sf.iblock.detail` for detail pages, and related `simai:sf.iblock.*`
  components for sections, filters, tables or calendars;
- custom blocks may wrap these components and tune parameters/modifiers, but
  should not replace them with manual readers unless the standard component path
  is proven insufficient and the reason is documented.

When a client-design main page already exists as a large temporary view, do not
rewrite it into a full new system in one pass. Decompose it section by section:
create one narrow project-layer block under
`simai.data/grid/block/<area>/<project-code>`, connect it through the current
view via `simai:sf.grid`, preserve the existing dynamic data source or fallback,
sync and smoke-test the page, then move to the next section. This keeps the
runtime page working while gradually converting the prototype into a normal SF4
assembly.

During that staged conversion, the final structure for each area should still be
one active view with one root `simai:sf.grid`; the design sections become grid
rows/areas inside it. Avoid leaving several sibling `simai:sf.grid` calls in the
same `home`/`main` view after the section has been stabilized. Multiple
independent grids in one area are acceptable only as a short-lived migration
scaffold and must be collapsed before the area is considered ready for editor
handoff.

For static or semi-static section wrappers, prefer the standard include block
before creating a project block. Put editable fragments under
`simai.data/include/<area-or-page>/...`, connect them through the existing
`custom.include.file` grid block, and keep the root area assembled by
`simai:sf.grid`. The include file may contain plain markup, section headings,
or calls to standard SF4 components such as `simai:sf.iblock.list`. Create a
new `simai.data/grid/block/<area>/<project-code>` only when the section needs a
reusable parameterized grid block, custom block metadata, or behavior that the
standard include block cannot represent cleanly. This keeps simple Figma
sections editable and avoids one-off blocks that only output static HTML.
The include block must preserve the public editor contract: in normal mode it
may hide icons, but in `grid_edit_mode` it must pass `HIDE_ICONS => "N"` to
`bitrix:main.include` or the corresponding component. Otherwise the page looks
grid-based in code but the content manager cannot open the include/component
settings from the public editing surface.

If a Figma fragment visually groups several dynamic lists into one shared
background panel, keep the group as one grid row/include file and render each
list inside it through its own standard component call. Do not create several
independent rows only to approximate the visual group, because the page editor
will expose a misleading structure and future maintainers will tune spacing in
the wrong place. Use one wrapper include for the shared surface, then separate
iblock-backed component calls for each editable data set inside the wrapper.

For iblock-backed lists and detail pages, first try the universal SF4
components before creating custom readers: `simai:sf.iblock.list` for lists and
`simai:sf.iblock.detail` for details. Their `.default` templates support many
`SOURCE_*` mappings, modifiers, buttons, images, properties, include areas and
layout options. A project block may wrap these components to provide a section
heading, tuned params, modifiers or item include snippets, but it should not
replace the component with a manual `CIBlockElement` loop unless the standard
component path is proven insufficient and the reason is documented.

For detail pages derived from a client design, do not treat the screenshot as a
set of independent visual blocks. First build the detail data contract: primary
entity, route key, editable fields, statistics, media/gallery, child collections,
related lists, actions, and future module boundaries. Store repeated detail
sections in iblocks or existing solution entities by analogy, for example
`<entity>-gallery`, `<entity>-report`, `<entity>-need`, or existing news/photo
iblocks with a relation property. Render the page from that contract and keep a
temporary fallback only for bootstrapping. The acceptance check must include the
admin/editability path for the new fields, not only the public screenshot.

Classify each visible value before creating a property:

- own attribute of the primary element: store on the primary element, for
  example city, address, phone, email, verification status, short description,
  direct contact data or a directly configured weekly target;
- taxonomy/filter facet: use sections, list properties or reference entities,
  for example help category, city, pet type, shelter size and verification
  status used by list filters;
- child entity: create a related iblock/module entity and link it back to the
  primary element, for example pets, volunteers, needs, photo albums, reviews,
  reports, deliveries, orders or donations;
- derived aggregate: compute from child entities or from an explicitly
  documented aggregate source, for example pet count, dogs/cats split, found
  home count, volunteer count, collected amount for the last 7 days and progress
  percent.

Do not create manual string/number properties for derived values only because
they appear in the design. If the design reveals a real registry behind a
number, model that registry first and derive the number from it. If a temporary
editorial aggregate is needed for a demo, mark it as a temporary display source
and document the future source of truth.

Prefer real Bitrix element bindings (`E`) or another explicit relation contract
for child entities. A string field like `SHELTER_CODE` is acceptable only as a
temporary dev/demo bridge and must be called out in the architecture notes,
because administrators can mistype it and cannot select the related element
through the normal Bitrix UI.

For an iblock element detail page, preserve the Bitrix/SF4 detail contract:
the public URL is a CNC route such as `/ru/<section>/<element-code>/`, the real
entry point is the section-level `detail.php`, and the main rendering component
is usually `simai:sf.iblock.detail` with a project template under
`local/templates/.default/components/` or the active site template. Do not create
physical per-element pages such as `/ru/shelters/laska/index.php`; if routing
does not reach Bitrix, fix the front-controller/routing configuration instead
of turning elements into static pages.

The detail template can visually look like a landing page. That does not mean it
must be implemented as a grid. Use a customized `sf.iblock.detail` template when
the page is fundamentally one element plus related data. Use a grid only for
true page/area assembly where the site editor is expected to rearrange rows as a
page layout. The implementation choice follows the data contract and editing
model, not the absence of a sidebar.

Page-specific content belongs to the central element by default. Section
headings, explanatory copy, CTA text, contact intro, hero text, current goal
copy, and other data that describes this exact item must be stored in that
item's fields/properties or in child entities related to that item. Do not leave
such content as literals inside include files or templates. Keep templates as
rendering and component wiring only. Independent sections such as "other items",
generic news, or a site-wide CTA may read from their own source because they are
not owned by the central element.

When reading a design, infer the data model before implementing markup. A number
shown as a simple counter may be either a stored stat element or an aggregate
from real related entities; decide by product meaning and expected maintenance.
If the same concept appears elsewhere as cards, filters, statuses, or histories,
model the underlying entities instead of copying the number. Examples:

- pet counters may come from a pet registry with type and status
  (`in_shelter`, `found_home`) related to a shelter;
- weekly collection numbers may come from contribution/order records filtered by
  shelter, collected item, and date range;
- "what is needed" should usually be a need/request entity related to shelter
  and to a catalog of collected goods;
- shelter life photos should usually be linked photo-album sections or gallery
  entities, not loose images in template markup;
- reviews should be review elements related to the shelter;
- related shelters and generic news are independent lists, not central element
  properties.

For list filters from client designs, avoid decorative-only controls. Define a
simple URL contract first, usually `tag=<semantic-filter>` and `q=<search>`,
then map each UI chip/search field to an iblock filter consumed by
`simai:sf.iblock.list` through `FILTER` or `FILTER_NAME`. Store the filterable
flags in iblock properties such as `VERIFIED`, `URGENT`, `NEED_VOLUNTEERS`, not
in PHP-only arrays. Put shared filter rendering and filter-building helpers in a
project include such as `simai.data/include/<entity>/filter.php`, then reuse it
on the landing section and on the full catalog page. This gives a universal
pattern: teaser section links to a canonical catalog URL, catalog applies the
same parameters to the editable iblock list, and an AJAX version can be added
later without changing the data contract.

If the design has two filter levels, keep them separate in both UX and data:
category chips should represent semantic tags or a multiple list property
(`HELP_CATEGORY`, `AUDIENCE`, `SERVICE_TYPE`), while select/dropdown facets
represent orthogonal properties such as city, type, size, status or date. The
full catalog page owns the actual filtering; landing blocks should link to that
catalog with the same URL contract instead of running a disconnected local
filter. For list properties, do not assume that filtering by visible text or
XML_ID will always work in every Bitrix context; resolve enum IDs when needed
and test each public URL (`tag`, facet and `q`) against rendered item counts.

For tabbed landing sections where each tab changes the visible content, do not
hardcode the tabs as static markup unless they are truly decorative. Model each
tab as an active iblock element with stable `CODE`, sort, title/tab label,
description, image and button/link properties. Build the tab list from the same
iblock, choose the active element through a small URL contract such as
`project=<code>` or `type=<code>`, pass the selected code to
`simai:sf.iblock.list` through `FILTER_NAME`, and keep the section in an
editable include file. This keeps the page editable, makes deep links possible,
and avoids disconnected duplicated content between tabs and cards.

If the standard `.default` template can fetch the data but cannot reproduce a
critical card anatomy from the client design, create a narrow project component
template override under
`local/templates/<site-template>/components/simai/sf.iblock.list/<template>/`.
Keep the data source, sorting, filtering and edit actions in
`simai:sf.iblock.list`; customize only the item markup needed for the card. The
template must preserve Bitrix edit area hooks, use existing SF4 button/grid
classes where possible, and place custom CSS in the project view/block stylesheet
instead of modifying `/bitrix/components` or the base `simai.framework`
template.

Before adding such an override, check where the active site template physically
lives. If the active template is `/bitrix/templates/simai.framework` and the
project adds files under `/local/templates/simai.framework/components/...`,
Bitrix may resolve `SITE_TEMPLATE_PATH` to the new local folder. That local
folder then shadows the base template. In this case the project must either
copy/manage the full template intentionally, or add delegating
`local/templates/simai.framework/header.php` and `footer.php` that include the
base `/bitrix/templates/simai.framework/header.php` and `footer.php`. Never
leave a partial local template folder with only `components/`: the public page
can render without `<html>`, `<head>`, template assets, header and footer.
Acceptance for component-template overrides must include `curl`/browser checks
that the page still contains `<!DOCTYPE html>`, `<head>`, the project header,
main content and footer, not only the customized component markup.

For page-level views that need project CSS, register assets before the template
prints `ShowHead()`. If a page needs a custom view stylesheet, prefer the Bitrix
sequence `prolog_before -> SetTitle/SetPageProperty/addCss -> prolog_after ->
view content -> epilog`. Do not rely on `Asset::addCss()` from inside a view
that is included after `/bitrix/header.php`: depending on buffering and cache it
can miss the head output or force temporary body-level workarounds.

When converting a prototype that already has `data.php` arrays, keep those
arrays only as safe fallback while moving the real editable content into
iblocks. Add an idempotent seed/update script near the view or project tooling
that creates missing iblocks/properties, upserts starter elements, deactivates
obsolete demo elements, and can be rerun after sync. After conversion, verify
both the public markers and the Bitrix entities so the page does not silently
fall back to static data.

After a seed/update script changes the element set used by cached components
such as `simai:sf.iblock.list`, clear Bitrix component/managed cache before
browser acceptance. Do not trust the seed output alone: check the iblock
entities and then the rendered public HTML. A common failure mode is that the
iblock already contains the new active elements, while the public page still
shows the previous item count because the component cache was not refreshed.
If the site uses Bitrix composite HTML cache, also clear
`\Bitrix\Main\Composite\Page::getInstance()->deleteAll()` or verify with a
fresh URL that bypasses the static HTML cache. Component cache, managed cache
and composite cache are separate acceptance concerns.

When passing project block parameters through `simai:sf.grid`, use the exact
SF4 parameter naming convention:

```text
ROW_<row>_COL_<col>_AREA_<area>__<BLOCK_CODE_WITH_DOTS_REPLACED_BY_UNDERSCORES>__<PARAM>
```

Example:

```php
"ROW_4_COL_0_AREA_0__BUDDYDINNER_STORIES__TITLE" => "Выберите способ помощи",
```

Do not pass block params as
`ROW_4_COL_0_AREA_0_BUDDYDINNER.STORIES__TITLE` or
`ROW_4_COL_0_AREA_0__BUDDYDINNER.STORIES__TITLE`: those keys are ignored and
the block silently falls back to `.parameters.php` defaults.

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

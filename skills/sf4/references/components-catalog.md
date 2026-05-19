# SF4 `simai:sf.*` Components Catalog

## Scope

This catalog is based on real project source inspection of:

- `local/components/simai/sf.*`

It is intended for implementation and modernization tasks in SF4 projects, with focus on update-safe usage from project layer templates/blocks.

## Full Inventory (38 components)

### Composition and Block/Template Infrastructure

- `simai:sf.grid` (`.default`)
- `simai:sf.block` (`.default`)
- `simai:sf.block.view` (`.default`)
- `simai:sf.block.edit` (`.default`)
- `simai:sf.block.property` (`.default`, `block`, `col`)
- `simai:sf.block.row.property` (`.default`)
- `simai:sf.block.col.property` (`.default`)
- `simai:sf.template.include` (no template folder, runtime include loader)

### Iblock Data Components

- `simai:sf.iblock.list` (`.default` + 17 named templates)
- `simai:sf.iblock.detail` (`.default`, `sf-news`, `sf-property`, `sf-section`)
- `simai:sf.iblock.section` (`photo`, `sf-description`, `sf-list`, `sf-section`, `sf-select`, `sf-structure`, `sf-tree`)
- `simai:sf.iblock.filter` (`.default`)
- `simai:sf.iblock.table` (`.default`)
- `simai:sf.iblock.calendar` (`.default`)

### Forms and Feedback

- `simai:sf.feedback` (`.default`)
- `simai:sf.feedback.appeal` (`.default`, `sf-feed-university21`)
- `simai:sf.feedback.vote` (`.default`, `__.default`)
- `simai:sf.message` (`.default`)
- `simai:sf.photo.add` (`.default`)
- `simai:sf.video.add` (`.default`)

### Navigation, UI Services, and Utility Components

- `simai:sf.menu` (`navbar.multi`, `widget.navigation`)
- `simai:sf.menu.sections` (no templates)
- `simai:sf.breadcrumb` (`.default`)
- `simai:sf.section.main.map` (`.default`)
- `simai:sf.share` (`.default`)
- `simai:sf.swiper.nav` (`.default`, `sf-swiper-nav-circle-in`)
- `simai:sf.cookie.notification` (`.default`)
- `simai:sf.up` (`.default`)
- `simai:sf.weather` (`.default`)
- `simai:sf.rss.show` (`.default`)
- `simai:sf.promo` (`.default`)
- `simai:sf.banner.main` (`.default`)
- `simai:sf.user.list` (`.default`)

### Wizard and Property Editing

- `simai:sf.property.edit` (`.default`, `block`, `col`, `row`, `tab-block`)
- `simai:sf.wizard` (`.default`)
- `simai:sf.wizard.stage` (`.default`)

### Class-Based Components (without `component.php`)

- `simai:sf.highloadblock.grid` (`class.php`, `.default`)
- `simai:sf.pdf.viewer` (`class.php`, `.default`)

## Most Used Components: Deep Dive

### `simai:sf.iblock.list`

Use `simai:sf.iblock.list` as the first-choice renderer for repeated editable
content in SF4 projects: cards, banners, process steps, projects, reviews,
news, media lists, people, partners, shelters, products, services, reports and
similar lists. If the design requires a custom section shell, create a project
grid block that wraps `simai:sf.iblock.list` and configures its source mapping,
modifiers, include hooks and count. Do not replace editable list content with
static arrays or manual `CIBlockElement` loops unless the standard component
cannot satisfy the scenario and the exception is documented.

### Runtime pipeline

1. `component.php`
   - resolves iblock by `IBLOCK_ID` or `IBLOCK_CODE`,
   - applies section/filter/sort/pagination/permissions,
   - loads elements + properties + inherited properties,
   - sets breadcrumbs/title/meta when enabled.
2. `templates/.default/result_modifier.php`
   - builds dynamic `SOURCE_*` mapping for fields/properties/files/links,
   - computes `AREA_ORDER`, grid classes, image resize strategy, animation flags,
   - normalizes section/date/title/description/property output payload.
3. `templates/.default/template.php`
   - renders card or slider layouts from `AREA` and `ORDER`,
   - supports image/link/photo/video actions, include hooks, section title/link, pager.
4. `templates/.default/component_epilog.php`
   - optional include hook,
   - updates global timestamp marker (`$GLOBALS["TIME_CHANGE"]`).

### `.default` flexibility model

- 98 template parameters in real project.
- Main groups: `SOURCE`, `LAYOUT`, `VISUAL`, `MODIFIER`, `INCLUDE`, `BASE`.
- Core dynamic controls:
  - `AREA` + `AREA_ORDER` (content zones and order),
  - `SOURCE_*` mapping (which iblock fields/properties feed each zone),
  - `DISPLAY_TYPE` (`card`/`slider`),
  - `USE_GRID` + `COL_COUNT_*`,
  - image policies (`IMAGE_ASPECT_RATIO`, `IMAGE_ACTION`, hover/mask/svg options),
  - include hooks (`INCLUDE_BEFORE`, `INCLUDE_AFTER`, `INCLUDE_PICTURE`, `INCLUDE_EPILOG`),
  - style hooks via many `MODIFIER_*` class parameters.

### PHP 8 image ratio guard

On legacy SF4 portals, `simai:sf.iblock.list` `.default` can fatal in
`templates/.default/result_modifier.php` when `AREA` includes `image` and
`IMAGE_ASPECT_RATIO` is the literal string `property`. The modifier derives
ratio digits from the string and then divides them, so PHP 8 raises:

```text
Unsupported operand types: string / string
```

Do not patch the shared component first. Fix the project/solution layer that
passes the bad parameter, using one of the component-supported values:

- `original`;
- `manual` with explicit `IMAGE_MAX_WIDTH` / `IMAGE_MAX_HEIGHT`;
- `aspect-ratio-NxM`, for example `aspect-ratio-3x2`.

After the change, run `php -l` for touched public/grid files and smoke the page
that includes real image items. Pages with no image items may hide this defect.

### Available list templates

- `.default`
- `sf-banner-list`
- `sf-banner-single`
- `sf-banner-swiper`
- `sf-banner-swiper-multi`
- `sf-doc-card`
- `sf-doc-list`
- `sf-icon-card`
- `sf-map-yandex`
- `sf-news-card`
- `sf-news-slider`
- `sf-photo-card`
- `sf-photo-slider`
- `sf-review-slider`
- `sf-service-list`
- `sf-slider`
- `sf-video-card`
- `sf-video-slider`

### `simai:sf.iblock.detail`

### Runtime pipeline

1. `component.php`
   - resolves element by `ELEMENT_ID`/`ELEMENT_CODE`,
   - supports strict section check, 404 flow, permissions,
   - handles iblock detail navigation and inherited meta fields,
   - sets title/meta/canonical/breadcrumbs when enabled.
2. `templates/.default/result_modifier.php`
   - builds dynamic `SOURCE_*` mapping (fields/properties/doc/image/date),
   - prepares media payload (single image, gallery from `MORE_PHOTO`, video code),
   - prepares relation data payload (`RELATION_DATA`) for post-render includes,
   - builds prev/next navigation payload.
3. `templates/.default/template.php`
   - renders content by `AREA` + `ORDER`,
   - supports photo/video tabs, docs block, share block, prev/next block,
   - supports include hooks and modifier classes.
4. `templates/.default/component_epilog.php`
   - sets OpenGraph-like meta (`url`, `type`, `title`, `image`),
   - optionally executes relation includes and writes user property context.

### `.default` flexibility model

- 48 template parameters in real project.
- Main groups: `SOURCE`, `VISUAL`, `MODIFIER`, `INCLUDE`, `RELATION_DATA`.
- Core dynamic controls:
  - `AREA` + `AREA_ORDER`,
  - `SOURCE_*` mapping for image/date/title/description/doc/property/include,
  - `RELATION_DATA` + `SHOW_RELATION_DATA`,
  - document/media behavior in template,
  - share/nav/change-info toggles (`SHOW_SHARE`, `SHOW_NAV`, `SHOW_CHANGE_INFO`, etc).

### Available detail templates

- `.default`
- `sf-news`
- `sf-property`
- `sf-section`

## Practical Guidance

1. For reusable list-like blocks, prefer `simai:sf.iblock.list` with named template (`sf-news-card`, `sf-doc-card`, etc.) over editing `.default`.
2. Use `.default` only when you need full composable behavior (`AREA`, `SOURCE_*`, `MODIFIER_*`) and cannot fit a narrower named template.
3. Keep mapping consistency:
   - if you enable an area in `AREA`, provide corresponding `SOURCE_*` and `MODIFIER_*` values.
4. Keep edits in project layer:
   - override via template path priority (`local/templates/.../components/...`) before editing component source.
5. For detail pages with related content blocks, validate `RELATION_DATA` include files and user property side effects.
6. Re-test as admin and non-admin because cache/edit-mode branches differ.
7. When a project wrapper uses `simai:sf.iblock.list` `.default` for a custom
   Figma-like grid, remember that the component still renders Bootstrap column
   wrappers around each item. If `MODIFIER_ROW_AREA` switches the row to CSS
   grid or another custom layout, scope CSS to the component wrapper and reset
   direct child columns there (`max-width`, `flex`, `padding`, `margin`) instead
   of replacing the component with a manual loop.
8. `MODIFIER_ITEM_AREA` styles the inner item node, while title, description,
   include, and property zones are usually inside `.iblock-list-item-text`.
   For compact list rows or leaderboard layouts, either pass the appropriate
   text-area modifier if the template supports it, or scope project CSS to the
   text wrapper. Do not assume layout rules on the item node will affect its
   nested text areas.

## Data Layer Alignment

Use component configuration with:

- iblock/section config schemas in `simai.data/config`,
- site properties in `simai.data/.site.property.php`,
- section/page properties in `/.property.php`.

## Layer Decision

- Need layout composition: edit `simai.data/grid/view` and `simai.data/grid/block`.
- Need card/detail visual behavior: tune `simai:sf.iblock.list` / `simai:sf.iblock.detail` template params first.
- Need content editor forms: update `.iblock.config.php` / `.iblock.section.config.php`.
- Need HL entity tables: use `simai:sf.highloadblock.grid`.

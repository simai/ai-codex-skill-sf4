# Portal Runtime Source-Of-Truth

Use this reference when SF4 `simai.data` pages, blocks, templates, or component
params run inside a SIMAI organization portal or host-mode solution domain.

## Principle

SF4 runtime checks must prove where content comes from, not only that a page
renders.

A page can return `HTTP 200` and still be wrong when:

- a required area/block is empty;
- a block falls back to the wrong shared `simai.data` layer;
- a component uses a root section from another tenant;
- a host-mode URL hides the physical `/<solution>/` folder;
- an include/template path points to the public URL instead of the solution
  data layer.

## Required Runtime Assertions

For portal/SF4 dynamic pages, assert:

- active site/solution context;
- `SF_PUBLIC_SITE_DIR`, `SF_SITE_DIR`, and `SF_DATA_DIR` meaning in the current
  request;
- active `grid_view_*` values and expected view folders;
- required block section and block code;
- component params that select iblock type/code, section, element, template, or
  include path;
- current organization/root section marker when tenant content is involved;
- absence of known foreign markers from the project QA plan.

Project-specific IDs and domains belong in the project QA plan, not in this
global reference.

## Host-Mode Path Checks

When public URL and physical source diverge:

- public links, menus, `SECTION_URL`, and `DETAIL_URL` should remain public and
  host-mode friendly;
- include-like params (`SOURCE_INCLUDE`, `INCLUDE_*`, `INCLUDE_PICTURE`, modal
  include pages, SVG/mask assets) must resolve through the solution data path
  when the file lives under `/<solution>/simai.data`;
- two-component pages must point `SECTION_PAGE` to the real include file
  location;
- root `/simai.data` and `/<solution>/simai.data` are separate layers and must
  be audited separately.

After fixing an include/template path, verify both the visitor URL and the
resolved filesystem/source path.

## Page Class And Block Markers

For broad portal QA, classify pages before accepting them:

- home;
- static section;
- list;
- section-group list;
- detail;
- landing/detail;
- form;
- service page;
- profile/admin;
- legal/sveden;
- media/gallery.

For each page class, define required blocks, text markers, media markers,
links, dynamic source, forbidden markers, and roles.

## Editor/Admin Context

If employees edit the portal page, anonymous runtime smoke is insufficient.

Check:

- public admin panel and action set;
- edit wrappers/overlays around required blocks;
- settings modal or edit entrypoints;
- profile/admin paths;
- no broken links to non-existing host-mode paths.

## Retest After SF4 Fix

After changing SF4 templates, blocks, views, or component params:

1. run syntax/static checks for touched PHP files;
2. smoke the target page;
3. assert required block/content markers;
4. assert source-of-truth and tenant boundary;
5. retest relevant reference block when a reference exists;
6. run shared-runtime or sibling-solution regression sentinel.

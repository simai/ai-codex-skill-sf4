# SF4 Troubleshooting

## Change Is Not Visible

Checklist:

1. Confirm edited file is in project layer (`simai.data`) and not in system layer.
2. Clear relevant Bitrix cache/component cache.
3. Confirm view code in properties points to edited view folder.
4. Confirm block code in view matches block folder name exactly.

## Settings Saved But Behavior Did Not Change

Checklist:

1. Confirm value written to correct level:
   - site `.site.property.php`
   - section/page `/.property.php`
   - user/session override
2. Confirm precedence is not overriding your target value.
3. Confirm runtime reads correct property key.
4. Confirm file permissions allow writes in `simai.data`.

## Block Does Not Render

Checklist:

1. Confirm view contains correct `...AREA_*_TEMPLATE => "<block_code>"`.
2. Confirm block exists:
   - project: `simai.data/grid/block/<section>/<code>/template.php`
   - or system: `/simai/block/<section>/<code>/template.php`
3. Confirm `BLOCK_SECTION` in view matches expected block section.
4. Confirm no PHP parse errors in block files.

## Editor Fields Missing

Checklist:

1. Confirm `.parameters.php` returns expected param array.
2. Confirm language labels exist in `lang/<lang>/.parameters.php`.
3. Confirm parameter key naming matches template usage.
4. Confirm block/view metadata files are present.

## Wizard Stage Fails

Checklist:

1. Confirm runtime entry path:
   - wrapper wizard redirect (if used) points to `/simai/wizard/master/<wizard_code>/`,
   - master `index.php` points to valid `WIZARD_CONFIG_FILE`.
2. Confirm wizard config file path exists and is readable.
3. Confirm action folder/file exists for every action code.
4. Confirm action input/output data codes are valid and consistent across chain.
5. Confirm installer-generated `data/*` payload exists in runtime master directory.
6. Confirm import archives/files exist and are readable.
7. Confirm required modules (iblock/highloadblock) are installed.
8. Confirm required PHP extensions for archive/XML actions:
   - `XMLReader`,
   - `ZipArchive`,
   - `DOMDocument`.
9. Confirm stage status transition logic reaches `SUCCESS` (not stuck at `WORK`).
10. If stage uses AJAX import, check its handler request keys and final success flag logic.

## Wizard Opens But Next Is Disabled

Checklist:

1. Confirm current action really sets `STAGE.STATUS = SUCCESS`.
2. Confirm no forced `ERROR` overwrite at end of custom action.
3. For selector-style actions, verify AJAX handler stores expected output array.
4. Confirm `data_output_code` matches actual key used by next stage.
5. Confirm browser-side JS receives success response from action AJAX endpoint.

## Wizard Import Runs Partially And Stops

Checklist:

1. Confirm stage is designed for chunked execution (`AJAX_TIME_STEP` / `AJAX_TIME_INTERVAL`).
2. Confirm import action persists progress between calls (saved in wizard property state).
3. Confirm large archive entries exist and are readable.
4. Confirm no PHP fatal/timeout in action AJAX endpoint.
5. Confirm final AJAX call marks stage `SUCCESS`, not only intermediate chunks.

## Asset Loading Issues

Checklist:

1. Confirm project template includes `style.php` and `js.php`.
2. Confirm project CSS/JS paths are valid.
3. Confirm no duplicate conflicting includes.
4. Confirm runtime approach used by this project:
   - project template includes,
   - and/or system asset registry.

## Audit Shows Hygiene Warnings

Checklist:

1. Open `references/hygiene-and-secrets.md`.
2. Remove archive/cache/vendor artifacts from `grid/block` unless explicitly required.
3. Review duplicate keys in `.site.property.php` and keep only intended values.
4. Move secret-like literals out of tracked property files where possible.
5. Re-run `scripts/sf4_project_audit.py` and confirm warning reduction.

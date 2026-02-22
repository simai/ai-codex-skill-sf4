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

1. Confirm wizard config file path exists and is readable.
2. Confirm action folder exists for every action code.
3. Confirm action input/output data codes are valid.
4. Confirm import archives/files exist and are readable.
5. Confirm required modules (iblock/highloadblock) are installed.

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

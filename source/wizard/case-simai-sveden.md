# Case: simai.sveden

## Source Paths

- `/Users/rim/Sites/sf4.test/simai/wizard/master/simai.sveden`
- `/Users/rim/Sites/university.test/simai/wizard/master/simai.sveden`

## Why This Case Matters

`simai.sveden` is the best concrete training case for the future specialist because it has:

- working `index.php`;
- `.wizard.config.php`;
- action chain;
- site selection;
- conditional branch for existing SF4 site vs non-SF4 site;
- file payload;
- config payload;
- iblock zip payload;
- URL rewrite payload;
- final info stages.

## Runtime Entry

`index.php` calls `simai:sf.wizard` with:

- `WIZARD_DIR`
- `WIZARD_TEMP_DIR`
- `WIZARD_CONFIG_FILE`
- `AJAX_TIME_STEP = 3`
- `AJAX_TIME_INTERVAL = 1`
- `CACHE_TYPE = N`

## Wizard Code

The config description code is:

```text
simai_sveden
```

This is the key used for saved runtime state in `SIMAI\Main\Configuration\Property`.

## Main Data Flow

1. `site.choice.sveden`
   - writes `site_config`;
   - captures selected site, site directory, whether SF4 template is already used, and whether public section should be renamed.

2. `file.copy`
   - reads `site_config`;
   - copies template and public payload;
   - substitutes placeholders such as `#dir#`.

3. `iblockconfig.import.data`
   - merges wizard iblock edit-form config into existing `simai.data/config`.

4. `urlrewrite.add`
   - reads `urlrewrite.php` payload;
   - adapts rules if site dir is root;
   - adds missing rewrite rules.

5. `site.update.sveden`
   - applies site/template settings for non-SF4 branches.

6. `file.rename`
   - conditionally renames existing `sveden` section.

7. `replace.code`
   - replaces generated codes in copied PHP files according to selected site id.

8. `data.import.file`
   - reads config files into `DATA`, especially options and iblock types.

9. `shortlink.import.data`
   - installs short links from config payload.

10. `option.import.data`
    - writes Bitrix options from imported config.

11. `iblocktype.import.data`
    - creates missing iblock types, site-aware.

12. `iblock.import.archive` or `iblock.import.archive.sveden`
    - imports zip archives.
    - branch depends on whether the target site is already SF4.

13. `info`
    - renders final links.

## Conditional Branches

Observed conditions depend on `site_config`:

- `sf4 == Y`
- `sf4 != Y`
- `rename_public == Y`
- `rename_public != Y`

This is central to understanding why the same config contains duplicate-looking `file.copy`, `iblock.import.archive`, and `info` stages.

## Payloads In sf4.test

Config files:

- `data/config/.iblock.config.php`
- `data/config/.iblock.section.config.php`
- `data/config/.iblocksection.config.php`
- `data/config/.iblocktype.config.php`
- `data/config/.option.config.php`
- `data/config/.short.config.php`
- `data/config/.site.config.php`
- `data/config/urlrewrite.php`

Iblock archives:

- `data/iblock/sf-ru-biblio.zip`
- `data/iblock/sf-ru-document.zip`
- `data/iblock/sf-ru-eduprogram.zip`
- `data/iblock/sf-ru-food.zip`
- `data/iblock/sf-ru-info.zip`
- `data/iblock/sf-ru-sport.zip`
- `data/iblock/sf-ru-structure.zip`

## Specialist Takeaways

- Do not evaluate a wizard by files alone; evaluate the action chain and shared data bus.
- Similar stages can be intentional branches.
- Existing SF4 site and non-SF4 site paths differ.
- Missing payload files, missing action folders or broken data keys are real blockers.
- Long imports require AJAX success transition.

# Universal Master Blueprint

This blueprint describes the recommended structure for a new SF4 universal wizard master.

## Target Structure

```text
bitrix/modules/<module>/
  install/
    index.php
    wizard/
      <module>/
        .description.php
        wizard.php
        lang/ru/.description.php
        lang/ru/wizard.php
        images/
    wizard/data/                 # optional prebuilt package shape
    bitrix/                      # optional assembled package shape
    iblock/                      # optional assembled package shape
    ru/
      config/
      php_interface/
      root/
      site/

/simai/wizard/master/<module>/
  index.php
  .wizard.config.php
  image/
    logo.png
    wizard_bg.jpg
  data/
    bitrix/
    components/
    config/
    iblock/
    module/
    php_interface/
    public/
    root/
    site/
    template/
  action/                       # optional master-local overrides
```

## Bitrix Wrapper Wizard

Purpose: make the module visible through standard Bitrix solution wizard mechanics, then redirect to the universal master runtime.

Observed newer SF4 wrappers implement `SelectSiteStep::InitStep()` and redirect:

```php
$arDir = array_reverse(explode("/", __DIR__));
$nameModule = $arDir[0];
$wizard =& $this->GetWizard();
$wizard->solutionName = $nameModule;
LocalRedirect("/simai/wizard/master/" . $nameModule . "/");
```

Minimum wrapper files:

- `install/wizard/<module>/wizard.php`;
- `install/wizard/<module>/.description.php`;
- `install/wizard/<module>/lang/ru/*`;
- preview/icon assets if Bitrix wizard list should show them.

## Installer Bridge

`install/index.php` is responsible for preparing the runtime master before redirect.

Common duties:

- install/copy `simai.framework`;
- install/copy `simai.property`, `simai.property4iblock`, `simai.property4field`, `simai.bxeditor`, backup/filebackup modules when package needs them;
- copy components to `/bitrix/components/simai`;
- copy `/simai` framework runtime from the module/framework install payload;
- copy wrapper wizard to `/bitrix/wizards/simai/<module>`;
- create `/simai/wizard/master/<module>/data`;
- copy or assemble runtime data payload;
- unpack zips that the master expects as directories;
- register the module;
- redirect to `/simai/wizard/master/<module>/`.

## Master `index.php`

The master launcher includes `simai:sf.wizard`.

Required parameters:

- `WIZARD_DIR`;
- `WIZARD_TEMP_DIR`;
- `WIZARD_CONFIG_FILE`;
- `AJAX_TIME_STEP`;
- `AJAX_TIME_INTERVAL`;
- `AJAX_MODE=Y`;
- `CACHE_TYPE=N`.

Recommended asset setup mirrors `simai.sveden`:

- `lazysizes`;
- `jquery`;
- `popper`;
- `simai.framework`;
- `simai.bx-panel`;
- `font-awesome`;
- optional `fancybox`, `swiper` if UI needs them.

## `.wizard.config.php`

Required top-level keys:

- `description`;
- `action`.

`description` should define:

- `name`;
- `code`;
- `stage_renew`;
- `logo`;
- `author`;
- `copyright`;
- `background`;
- `color`;
- `modifier`.

`action` is an ordered array. Each action entry should define:

- `name`;
- `code`;
- optional `data_input_code`;
- optional `data_output_code`;
- optional `autocomplete`;
- optional `condition`;
- `parameter`.

## Recommended Base Action Chain

For a site-aware install/update master:

1. `site.choice.sveden` or project-specific `site.choice.*`
   - writes `site_config`.
2. Framework/template/component copy stages
   - `file.copy`, `file.unzip`, installer-prepared files.
3. Site update
   - `site.update` or `site.update.sveden`.
4. Public/root/site file copy
   - with `#dir#` placeholders from `site_config`.
5. Config merge
   - `iblockconfig.import.data`.
6. URL rewrite
   - `urlrewrite.add`.
7. Code/site transformation
   - `replace.code` only when package contains canonical `sf_ru_`/`sf-ru-` references.
8. Data import
   - `data.import.file`;
   - `option.import.data`;
   - `shortlink.import.data`;
   - `iblocktype.import.data`.
9. Archive import
   - `iblock.import.archive` or solution-specific variant.
10. Final message
   - `info`.

## Condition Rules

Use conditions to split SF4-existing-site and non-SF4-new-site branches.

Observed examples:

- if `site_config.sf4 != Y`, copy full templates and run site update;
- if `site_config.sf4 == Y`, merge into existing SF4 site and avoid full template replacement;
- if `site_config.rename_public == Y`, rename existing public folder before copying.

Specialist rule: every branch must leave the same required downstream data keys available.

## Master-Local Actions

Use `/simai/wizard/master/<module>/action/<code>/` only when:

- global action behavior is not correct for the package;
- the action is solution-specific and should not affect all masters;
- the action needs package-local templates/assets.

Keep the same package contract as global actions:

- `.description.php`;
- `action.php`;
- optional `ajax.php`;
- optional class file;
- lang files.

## Rollback Design

Before making a master executable in live/staging, define rollback per side effect:

- file copy/unzip: destination backup or remove list;
- config merge: backup `simai.data/config`;
- iblock import: DB backup or known object delete script;
- option import: previous option dump;
- URL rewrite: previous `urlrewrite.php`/Bitrix rewrite table state;
- PHP interface snippets: previous file copies and merge diff;
- module install: uninstall path and copied directory inventory.

## Acceptance Checklist

- Wrapper wizard redirects to the expected master URL.
- Installer bridge creates or copies every runtime file referenced by `.wizard.config.php`.
- Master `index.php` includes `simai:sf.wizard` with valid paths.
- `.wizard.config.php` exists and returns an array.
- Every action code resolves to master-local or global action file.
- Every `SOURCE` file/directory/archive exists after installer assembly.
- Every `DATA_INPUT_CODE` has an upstream `DATA_OUTPUT_CODE` or site choice source.
- Long-running actions have either stage counters or action-local AJAX finalization.
- Visual assets referenced by `description` exist.
- No live execution is performed without backup/rollback boundary.

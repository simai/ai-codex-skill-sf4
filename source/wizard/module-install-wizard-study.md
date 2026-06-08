# Module Install Wizard Study

## Sources Studied

Legacy Bitrix solution wizards:

- `/Users/rim/Sites/test.test/bitrix/modules/simai.fund/install/wizards`
- `/Users/rim/Sites/test.test/bitrix/modules/simai.educenter/install/wizards`
- `/Users/rim/Sites/test.test/bitrix/modules/simai.school/install/wizards`

SF4 universal wizard wrappers and payload packages:

- `/Users/rim/Sites/test.test/bitrix/modules/simai.sf4biblio/install/wizard`
- `/Users/rim/Sites/test.test/bitrix/modules/simai.sf4med/install/wizard`
- `/Users/rim/Sites/test.test/bitrix/modules/simai.sf4university/install/wizard`

## Main Finding

There are two related but different wizard generations.

Legacy solutions use Bitrix `wizard_sol` directly:

- `install/wizards/simai/<solution>/wizard.php`
- `site/services/main/*.php`
- `site/services/iblock/*.php`
- `site/services/iblock/data/ru/*.php`
- `site/templates/<template>`
- `site/public/<lang>`

Newer SF4 solutions use a wrapper Bitrix wizard to redirect into the SF4 universal wizard:

- `install/wizard/<module>/wizard.php`
- `LocalRedirect("/simai/wizard/master/" . $nameModule . "/")`
- `install/index.php` prepares `/simai/wizard/master/<module>/data/*`

## Legacy Wizard Pattern

The legacy `wizard.php` extends Bitrix wizard classes:

- `CSelectSiteWizardStep`
- `CSelectTemplateWizardStep`
- `CSelectThemeWizardStep`
- `CSiteSettingsWizardStep`
- `CDataInstallWizardStep`
- `CFinishWizardStep`

Important implementation patterns:

- `solutionName` is set in `SelectSiteStep`.
- Template screen renders preview/screenshot from `site/templates/<template>/lang/<lang>/`.
- Theme/settings step writes many `COption::SetOptionString` defaults.
- Settings step exposes checkboxes such as `siteInstallPublic` and `siteInstallDD`.
- Finish step sets `main:wizard_solution`.

## Legacy File And Template Setup

`site/services/main/template.php`:

- copies selected template into `/bitrix/templates/<template>`;
- attaches template to target site via `CSite::Update`;
- registers page property types through `CFileMan::SetPropstypes`;
- in school, replaces macros in header, footer and public files.

`site/services/main/files.php`:

- copies public files from `site/public/<LANGUAGE_ID>` into `WIZARD_SITE_PATH`;
- reads `data/urlrewrite_array.php`;
- adds missing rules through `CUrlRewriter::Add`.

## Legacy Dynamic Data Format

Legacy dynamic data is stored as PHP arrays in:

```text
site/services/iblock/data/ru/
```

Observed files:

- `types.php`
- `iblocks.php`
- `props.php`
- `sections.php`
- `elements.php`
- `fields.php`
- `forms.php`
- `seo.php`
- `highload.php`
- `highloadprops.php`
- `highloadelems.php`

`simai.fund` and `simai.educenter` include highload data files. `simai.school` has iblock files but no highload data files in the inspected folder.

This is important training material for understanding how old installers described structured entities before the newer zip-based SF4 archive flow.

## SF4 Wrapper Pattern

The wrapper `install/wizard/<module>/wizard.php` still declares Bitrix wizard steps, but `SelectSiteStep::InitStep()` immediately redirects:

```php
$arDir = array_reverse(explode("/", __DIR__));
$nameModule = $arDir[0];
$wizard =& $this->GetWizard();
$wizard->solutionName = $nameModule;
LocalRedirect("/simai/wizard/master/" . $nameModule . "/");
```

This means:

- Bitrix wizard registration is still used as an entrypoint.
- Actual installation UX and action execution happens in `/simai/wizard/master/<module>/`.
- The module installer must prepare master data before redirect.

## SF4 Module Install Payload Preparation

`install/index.php` for SF4 modules performs the bridge from module package to universal wizard runtime.

Observed responsibilities:

- copy `simai.framework` module into `/bitrix/modules/simai.framework`;
- copy framework components into `/bitrix/components/simai`;
- copy wrapper wizard into `/bitrix/wizards/simai/<module>`;
- copy `/simai` framework layer into site root;
- install/register companion modules such as:
  - `simai.property`;
  - `simai.property4iblock`;
  - `simai.property4field`;
  - `simai.bxeditor`;
  - `simai.backup`;
  - `simai.filebackup`.
- create `/simai/wizard/master/<module>/data`;
- copy module payload into `/simai/wizard/master/<module>/data`;
- redirect to `/simai/wizard/master/<module>/`.

Observed variants:

- `simai.sf4med`: copies `install/wizard/data` directly to `/simai/wizard/master/simai.sf4med/data`.
- `simai.sf4biblio`: copies `install/wizard/data`, then unpacks `config.zip` and `medialibrary.zip` into the master data directory.
- `simai.sf4university`: copies data from module `install/bitrix`, `install/ru/config`, `install/iblock`, `install/ru/php_interface`, `install/ru/root`, `install/ru/site`; also prepares `simai.sveden` master data as a dependency.

## SF4 Packaged Data Shape

Observed `simai.sf4biblio/install/wizard/data`:

- `components/simai.components.zip`
- `config.zip`
- `iblock/*.zip` with 44 archives
- `medialibrary.zip`
- `module/*.zip`
- `php_interface/dbconn.add.php`
- `php_interface/init.add.php`
- `public/public.zip`
- `public/site.ru.public.zip`
- `template/template.zip`
- `site/simai.data/*`

Observed `simai.sf4med/install/wizard/data`:

- `components/simai.components.zip`
- `config.zip`
- `iblock/*.zip` with 48 archives
- `medialibrary.zip`
- `module/*.zip`
- `php_interface/dbconn.add.php`
- `php_interface/init.add.php`
- `public/public.zip`
- `public/site.ru.public.zip`
- `template/template.zip`

Observed `simai.sf4university/install/wizard`:

- wrapper files only in the inspected `install/wizard` path;
- payload is prepared in `install/index.php` from other module install folders.

## Iblock And Highload Packaging

The universal master uses zip archives for iblock import:

```text
data/iblock/<iblock-code>.zip
```

The action family to learn deeply:

- `iblock.export.archive`
- `iblock.import.archive`
- `iblock.import.archive.sveden`

The export class writes an XML representation and can include highload blocks. The import class reads the archive and imports:

- iblocks;
- properties;
- property enums;
- section user fields;
- sections;
- elements;
- element property values;
- section-element links;
- rights;
- messages;
- SEO;
- fields;
- forms;
- highload blocks.

Training implication: to create data for a future master, the specialist must understand both:

- old PHP-array demo-data format from Bitrix wizards;
- newer zip archive format generated by export actions.

## Visual Design And Wizard Appearance

Legacy Bitrix wizards define visual selection through:

- `.description.php`;
- `css/panel.css`;
- `css/wizard.gif`;
- `css/wizard_clear.gif`;
- `images/solution.png`;
- template preview/screenshot images;
- custom `ShowStep()` HTML.

SF4 universal wizard appearance is controlled by `.wizard.config.php` description:

- `name`;
- `logo`;
- `background.color`;
- `background.image`;
- `background.position`;
- `background.repeat`;
- `background.size`;
- `background.attachment`;
- `color.primary`;
- `color.secondary`;
- `modifier.page_body`;
- `modifier.wizard_wrap`;
- `modifier.wizard_area`;
- `modifier.wizard_nav`;
- `modifier.wizard_copyright`.

Training implication: specialist must distinguish Bitrix wrapper wizard UI from SF4 universal wizard UI. In newer SF4 flow the visible installer design is mostly universal wizard config, not the wrapper class.

## Required Specialist Knowledge Expansion

The specialist must cover:

1. Creating a master wrapper in `install/wizard/<module>/wizard.php`.
2. Preparing `install/index.php` so runtime `/simai/wizard/master/<module>/data` is complete.
3. Creating `.wizard.config.php` action chains.
4. Packaging public files, templates, `simai.data`, config, php_interface and components.
5. Exporting iblocks and highload blocks through `iblock.export.archive`.
6. Importing packaged data through `iblock.import.archive`.
7. Designing wizard appearance through description/background/color/modifier config.
8. Updating existing masters safely without breaking runtime storage, data keys or action conditions.

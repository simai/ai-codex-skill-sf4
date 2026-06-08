# Universal Wizard Packaging Matrix

This matrix describes how files and dynamic data are prepared for SF4 universal masters.

Evidence sources:

- `/Users/rim/Sites/test.test/bitrix/modules/simai.sf4biblio/install/wizard/data`
- `/Users/rim/Sites/test.test/bitrix/modules/simai.sf4med/install/wizard/data`
- `/Users/rim/Sites/test.test/bitrix/modules/simai.sf4university/install`
- `/Users/rim/Sites/test.test/bitrix/modules/{simai.fund,simai.educenter,simai.school}/install/wizards`
- `/Users/rim/Sites/sf4.test/simai/wizard/master/simai.sveden`
- `/Users/rim/Downloads/wizard.export/wizard.export`

## Package Shapes

| Shape | Example | Source location | Runtime location | Notes |
|---|---|---|---|---|
| Prebuilt universal master data | `simai.sf4biblio`, `simai.sf4med` | `install/wizard/data/*` | `/simai/wizard/master/<module>/data/*` | Installer copies the whole data folder. `simai.sf4biblio` additionally unpacks `config.zip` and `medialibrary.zip` inside runtime data. |
| Assembled universal master data | `simai.sf4university`, `simai.sveden` dependency install | `install/bitrix`, `install/ru/config`, `install/iblock`, `install/ru/php_interface`, `install/ru/root`, `install/ru/site` | `/simai/wizard/master/<module>/data/{bitrix,config,iblock,php_interface,root,site}` | Missing `data/*` in module source is not automatically an error; inspect `install/index.php` first. |
| Source-site export master | `wizard.export` sample | Working Bitrix/SF4 site plus `/simai/wizard/master/<export>/` | `/.last_version/install/{bitrix,iblock,ru}` | Master copies current modules/templates/public files and exports dynamic settings/iblocks into an install tree. Good baseline for "package solution through universal master" requests, but hard-coded source paths must be adapted. |
| Legacy Bitrix wizard data | `simai.fund`, `simai.educenter`, `simai.school` | `install/wizards/simai/<solution>/site/services/iblock/data/ru/*.php` | Imported by legacy wizard service scripts | PHP-array format, not zip archive format. Fund and educenter include highload arrays. |

## Universal Master Payload Matrix

| Payload | Typical path | Packaging form | Consumed by | Required checks |
|---|---|---|---|---|
| Master launcher | `/simai/wizard/master/<module>/index.php` | PHP file | Browser entry; includes `simai:sf.wizard` | Defines `LANGUAGE_ID`, loads required assets, passes `WIZARD_DIR`, `WIZARD_TEMP_DIR`, `WIZARD_CONFIG_FILE`, AJAX settings and `CACHE_TYPE=N`. |
| Master config | `/simai/wizard/master/<module>/.wizard.config.php` | PHP file returning array | `simai:sf.wizard` | Must contain `description` and `action`; `description.code` is storage key. Missing config blocks universal master execution. |
| Visual images | `/simai/wizard/master/<module>/image/*` | PNG/JPG/GIF | Master template via `description.logo` and `description.background.image` | Paths should use `Wizard::getLocal(__DIR__)`; verify files exist. |
| Runtime temp | `/simai/wizard/master/<module>/temp` or `tmp` | Directory | Components/actions | Writable; not treated as source of truth. |
| Framework/templates | `data/bitrix/templates/*` or `data/template/template.zip` | Raw directory or zip | `file.copy`, installer unpack/copy | Clarify whether package targets `/bitrix/templates` or selected site `simai.data/template`. |
| Components | `data/bitrix/components/simai/*` or `data/components/simai.components.zip` | Raw directory or zip | Installer copy, `file.copy`, module installer | Match component namespace and target `/bitrix/components/simai`. |
| Public files | `data/site/*`, `data/root/*`, `data/public/public.zip`, `data/public/site.ru.public.zip` | Raw directory or zip | `file.copy`, `file.unzip`, installer bridge | Decide target: site root `#dir#`, document root, or universal data directory. |
| Config files | `data/config/.iblock.config.php`, `.iblock.section.config.php`, lang files, `urlrewrite.php` | Raw PHP files or `config.zip` | `iblockconfig.import.data`, `urlrewrite.add`, installer unzip | Verify target site has existing `simai.data/config` files before merge action. |
| Iblock archives | `data/iblock/*.zip` | XML zip from `iblock.export.archive` | `iblock.import.archive`, `iblock.import.archive.sveden` | Zip must contain CML-like XML expected by `SimaiIblockXMLUnpack`; verify `XMLReader`/`ZipArchive`. |
| Iblock type/config data | `data/config/*.php` or action data files | PHP array | `iblocktype.import.data`, `data.import.file` | Site-aware codes usually need `sf_<site>_...` or `sf-<site>-...` transformation. |
| Options | Config payload array | PHP array | `option.import.data` | Confirm module option owner and overwrite policy. |
| Shortlinks | Config payload array | PHP array | `shortlink.import.data` | Confirm old/new URL mapping and target site directory. |
| URL rewrite | `data/config/urlrewrite.php` | PHP array | `urlrewrite.add` | Rules must adapt to selected site root; duplicate rule behavior should be checked. |
| PHP interface snippets | `data/php_interface/dbconn.add.php`, `init.add.php` | PHP snippets | File append/copy action or installer-specific code | High risk: requires explicit merge/backup, not blind overwrite. |
| Module archives | `data/module/*.zip` | Module zip | Module installer | Used by `simai.sf4biblio` style installers to unpack framework/property modules before registering. |
| Bitrix module sources | `install/bitrix/modules/*` | Raw module directory | `install/index.php` | Used by `simai.sf4med`/`sf4university` style installers for direct `CopyDirFiles`. |
| Media library | `data/medialibrary.zip` | Zip | Installer unzip | Confirm extraction target; biblio extracts into runtime master data. |
| Master-local actions | `/simai/wizard/master/<module>/action/<code>/*` | PHP action package | Runtime action resolver before global fallback | Use only when package-specific behavior is required. |

## Legacy PHP-Array Data Matrix

Legacy solution wizards use `site/services/iblock/data/ru/*.php`:

| File | Purpose | Present in inspected solutions |
|---|---|---|
| `types.php` | Iblock type definitions | fund, educenter, school |
| `iblocks.php` | Iblock definitions | fund, educenter, school |
| `props.php` | Iblock properties | fund, educenter, school |
| `sections.php` | Section tree | fund, educenter, school |
| `elements.php` | Elements and values | fund, educenter, school |
| `fields.php` | Form/field metadata or iblock field settings depending on service script | fund, educenter, school |
| `forms.php` | Form definitions | fund, educenter, school |
| `seo.php` | SEO metadata | fund, educenter, school |
| `highload.php` | Highload block definitions | fund, educenter |
| `highloadprops.php` | Highload fields/properties | fund, educenter |
| `highloadelems.php` | Highload rows | fund, educenter |

Specialist rule: do not mix legacy PHP-array data and universal archive data in one action without an explicit migration layer.

## Packaging Flow For A New Universal Master

1. Decide whether the module will ship prebuilt `install/wizard/data` or assemble data from `install/bitrix`, `install/ru/*`, and `install/iblock`.
2. Create runtime master skeleton:
   - `index.php`;
   - `.wizard.config.php`;
   - `image/*`;
   - `data/*`;
   - optional `action/*`.
3. Add Bitrix wrapper wizard under `install/wizard/<module>/` if marketplace/module install should open the master through the standard wizard list.
4. Implement installer bridge in `install/index.php`:
   - copy/install framework modules;
   - copy components;
   - copy `/simai` wizard runtime;
   - copy wrapper wizard;
   - copy or assemble `/simai/wizard/master/<module>/data`;
   - unpack required zips;
   - redirect to `/simai/wizard/master/<module>/`.
5. Generate/export iblock archives through `iblock.export.archive` into `data/iblock/*.zip`.
6. Prepare config files and language files for `iblockconfig.import.data`.
7. Prepare public/template/component payloads and decide overwrite policy.
8. Verify every action `SOURCE` in `.wizard.config.php` exists after installer assembly, not only in module source.

## Packaging Flow For A Source-Site Export Master

Use this flow when the user asks to package an existing SF4 solution through the universal master rather than hand-building `data/*`:

1. Start from the `wizard.export` action chain, not from an import-only master.
2. Replace hard-coded solution paths such as `simai.sf4conf`, `/ru` and `/.last_version` with the requested solution code, site dir and controlled output dir.
3. Keep file copy stages separate from dynamic export stages:
   - modules/framework/components/templates/media/wrapper wizard;
   - public files and `urlrewrite.php`;
   - site/mail/usergroup/iblocktype/options data;
   - iblock/HL archives through `iblock.export.archive`;
   - generated install config files through `data.export.file`;
   - php_interface snippets through `file.create`.
4. Use an explicit iblock allowlist for reusable packages. Exporting all iblocks except type `delete` is acceptable for a one-off full-site snapshot, but too broad for a productized solution.
5. Treat `data.export.file` target files as generated outputs; they should not need to exist before execution.
6. Keep final `file.zip` and cleanup steps disabled until the generated `/.last_version` tree is audited.
7. Run read-only audit/readiness/rollback checks before any execution outside a disposable source environment.

## Common Packaging Mistakes

- Treating missing runtime `data/*` as an error without checking `install/index.php`.
- Shipping `.wizard.config.php` references to `data/config/*` that are only present after `config.zip` extraction.
- Forgetting language files for config merge actions.
- Using `sf_ru_` and `sf-ru-` in package code without a planned `replace.code` or site-aware import transformation.
- Including public/template zips but no unzip/copy action in the master chain.
- Running `iblock.import.archive` without confirming archive paths and PHP extensions.
- Blindly overwriting `php_interface/init.php` or `dbconn.php` instead of merging snippets.
- Copying a developer export master without replacing hard-coded source modules, site dir and output directory.
- Letting a full-site export include unrelated iblocks, options or public files that do not belong to the packaged solution.

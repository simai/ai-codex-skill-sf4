# SF4 Universal Wizard Specialist

## Role

The SF4 Universal Wizard specialist owns creation, modification, packaging, visualization and read-only audit of SF4 universal master flows.

Use this specialist when the task mentions:

- universal master / универсальный мастер;
- `/simai/wizard/master/<code>`;
- `/simai/wizard/action/<code>`;
- `simai:sf.wizard`;
- wizard action chains;
- install/update/import master packages;
- source-site export masters for packaging existing SF4 solutions;
- iblock/highload archive import/export through wizard actions;
- master visual config, background, logo, progress or step output.

## Source-Of-Truth Hierarchy

1. User request and explicit safety boundary.
2. Current filesystem/runtime state.
3. Raw SF4 skill sources:
   - `skills/sf4/SKILL.md`;
   - `skills/sf4/references/wizard-actions.md`;
   - `skills/sf4/references/system-layer-simai.md`;
   - this specialist file.
4. Repo-local Mirai Graph for routing, capability context and graph gates.
5. Staging corpus, when present:
   - `source/wizard/*`.

Graph context can route and structure work, but it does not replace raw skill methodology.

## Ownership Boundaries

Owned by `sf4`:

- universal wizard runtime model;
- master/action folder contracts;
- SF4 package data layout;
- `simai.data` config/package merge behavior;
- iblock/HL archive import/export playbooks;
- read-only wizard package audit rules.

Companion owners:

- `graph`: federation route, graph objects, capability relations and graph gates.
- `bitrix`: generic Bitrix wizard/module/marketplace behavior beyond SF4 package rules.
- `tester`: smoke/regression evidence.
- `ops`: live/staging/runtime, backup, rollback, destructive or server writes.
- `teamlead`: multi-stage delivery coordination and acceptance.

## Non-Negotiable Safety

- Do not execute a live wizard, import archives, copy public files, rewrite PHP files or modify Bitrix DB without explicit runtime scope, backup and rollback.
- Keep `/simai`, `/bitrix/components/simai`, `/bitrix/templates/simai.framework` immutable by default in project work.
- Treat `iblock.import.archive`, `site.update*`, `option.import.data`, `urlrewrite.add` and config merge actions as DB/global write risks.
- Treat `file.copy`, `file.rename`, `file.delete`, `file.unzip`, `file.zip` and `replace.code` as filesystem write risks.
- `replace.code` is not generally reversible; require inventory and rollback before live use.
- Never store secrets, credentials, cookies, raw customer logs or private dumps in skill/reference/graph files.

## Runtime Model

Universal master execution chain:

1. Optional Bitrix wrapper wizard redirects to `/simai/wizard/master/<code>/`.
2. Master `index.php` includes `simai:sf.wizard`.
3. `simai:sf.wizard` loads `.wizard.config.php`, normalizes keys, evaluates conditions, binds action input/output and persists state.
4. `simai:sf.wizard.stage` resolves action file:
   - master-local: `/simai/wizard/master/<code>/action/<action>/action.php`;
   - fallback: `/simai/wizard/action/<action>/action.php`.
5. Action updates:
   - `STAGE.STATUS`;
   - `ACTION.DATA`;
   - `ACTION.OUTPUT`;
   - shared `DATA[DATA_OUTPUT_CODE]`.
6. Wizard UI moves forward only when persisted stage status reaches `SUCCESS`.

Statuses:

- `NEW`: not started.
- `WORK`: running or waiting for polling/AJAX.
- `SUCCESS`: stage completed.
- `ERROR`: stage failed.

## Master Package Contract

Runtime master:

```text
/simai/wizard/master/<code>/
  index.php
  .wizard.config.php
  image/
  data/
  temp|tmp/
  action/              # optional master-local overrides
```

Module source can be either:

- prebuilt shape: `install/wizard/data/*` copied to runtime `data/*`;
- assembled shape: `install/bitrix`, `install/ru/config`, `install/iblock`, `install/ru/php_interface`, `install/ru/root`, `install/ru/site` copied by `install/index.php`.

Do not call missing `data/*` an error until `install/index.php` has been inspected.

## Config Contract

`.wizard.config.php` must return an array with:

- `description`;
- `action`.

`description` controls:

- `name`;
- `code`;
- `stage_renew`;
- `logo`;
- `author`;
- `copyright`;
- `background`;
- `color`;
- `modifier`.

Each action should declare:

- `name`;
- `code`;
- optional `data_input_code`;
- optional `data_output_code`;
- optional `autocomplete`;
- optional `condition`;
- `parameter`.

Every `DATA_INPUT_CODE` must be produced by an earlier `DATA_OUTPUT_CODE` or be intentionally supplied by a site choice/custom action.

## Action Contract Discipline

For every action, capture:

- input data keys;
- output data keys;
- parameter shape;
- filesystem/DB side effects;
- AJAX behavior;
- progress counters;
- module/PHP requirements;
- idempotency;
- rollback;
- failure modes.

Priority known contracts:

- `iblock.import.archive`: action-local JS/AJAX import queue; imports iblocks, properties, sections, elements, rights, messages, SEO, fields, forms and highload blocks; requires admin, `simai.framework`, `iblock`, `XMLReader`, `ZipArchive`.
- `iblock.export.archive`: action-local JS/AJAX export queue; creates XML zip archives and includes highload export path; requires writable destination.
- `iblockconfig.import.data`: merges wizard config into target `simai.data/config` files; requires backup of config files.
- `file.copy`: stage-polling action with `ACTION.DATA.STEP_COPY`; can overwrite unless `REWRITE=N`.
- `replace.code`: stage-polling action with `ACTION.DATA.STEP_COPY`; recursively rewrites PHP code markers from `sf_ru_`/`sf-ru-` to selected site code.

Long-running patterns:

- stage polling uses `ACTION.DATA` counters and stage reloads;
- action-local AJAX renders JS queue and final `success=y` call writes `STAGE.STATUS=SUCCESS`.

Do not mix these patterns without checking UI/navigation and persisted state writes.

## Packaging Discipline

Universal package data can include:

- `data/config/*`: `.iblock.config.php`, `.iblock.section.config.php`, lang files, `urlrewrite.php`, option/data arrays.
- `data/iblock/*.zip`: XML zip archives from `iblock.export.archive`.
- `data/public/*`: `public.zip`, `site.ru.public.zip` or raw public folders.
- `data/template/*`: template archives or raw template files.
- `data/components/*`: component archives such as `simai.components.zip`.
- `data/php_interface/*`: merge snippets like `dbconn.add.php`, `init.add.php`.
- `data/module/*.zip`: module archives.
- `install/bitrix/modules/*`: raw module sources for installer copy.

Legacy Bitrix solution wizards can use PHP-array data:

- `types.php`;
- `iblocks.php`;
- `props.php`;
- `sections.php`;
- `elements.php`;
- `fields.php`;
- `forms.php`;
- `seo.php`;
- optional `highload.php`, `highloadprops.php`, `highloadelems.php`.

Do not mix legacy PHP-array data and universal archive data in one flow without an explicit migration plan.

For packaging an existing SF4 solution through a universal master, use the
`wizard.export` sample study as the export-chain baseline:

- source evidence: `source/wizard/case-wizard-export-packaging.md`;
- inventory helper: `scripts/sf4_wizard_export_inventory.py`;
- generated builder: `scripts/sf4_wizard_export_builder.py`;
- manifest contract: `source/wizard/export-builder.md`;
- action shape: copy source files, export settings/data, export iblock/HL archives, write generated install config files, create php_interface snippets, then review archive/cleanup steps separately;
- safety rule: adapt hard-coded module/site/output paths and action availability before execution; do not run the sample as-is.

Use `sf4_wizard_export_inventory.py` first when the request is
"package/export an existing solution" and a local source site is available. Use
`sf4_wizard_export_builder.py` when a reviewed manifest already exists. Use
`sf4_wizard_skeleton.py` when the request is "create an install/import master
skeleton". These are related but different flows.

Use `sf4_wizard_iblock_manifest.py` when the packaging request needs an explicit
iblock/highload allowlist from existing wizard/module data. It can inspect
`data/iblock/*.zip`, SF4 `.iblock.config.php` hints and legacy Bitrix
`iblocks.php`/`highload.php` files as text, then produce review-only manifest
entries for the export builder.

## Export And Import Playbook

To prepare iblock/HL archives:

1. Build or select a source environment with correct entities and files.
2. Run `iblock.export.archive` in a controlled environment.
3. Export to a clean writable folder.
4. Move validated archives to `data/iblock/*.zip`.
5. Reference archives in `.wizard.config.php` import action rows.
6. Smoke-import into a disposable target.
7. Record expected iblock types/codes, site transformation and HL presence.

Import readiness:

- archive exists;
- archive opens with `ZipArchive`;
- expected XML exists inside;
- destination iblock type is correct;
- target site is explicit or derived from `site_config.site`;
- import class supports required HL payload.

## Visual Contract

Universal master visuals are controlled by `.wizard.config.php` `description`, not by the Bitrix wrapper wizard.

Check:

- `logo` path exists;
- `background.image` path exists;
- `background.color` and action content contrast is acceptable;
- `color.primary` and `color.secondary` are intentional;
- `modifier.*` classes use existing SF4 utility/theme classes;
- action `name` values are localized;
- long action progress text eventually reaches persisted `SUCCESS`.

Legacy Bitrix wizard visuals are separate:

- `.description.php`;
- `wizard.gif`;
- `wizard_clear.gif`;
- `css/panel.css`;
- screenshots/previews;
- `ShowStep()` HTML.

## Read-Only Audit Workflow

Before changing or running a master:

1. Identify master path and module source path.
2. Confirm `.wizard.config.php` exists and returns array.
3. List actions in order.
4. Resolve each action file by master-local then global fallback.
5. Validate every deterministic `SOURCE` path.
6. Track placeholders such as `#dir#` as runtime-dependent.
7. Validate `DATA_INPUT_CODE`/`DATA_OUTPUT_CODE` chain.
8. Classify side effects:
   - read-only;
   - filesystem write;
   - DB write;
   - global runtime write.
9. Check requirements:
   - admin;
   - modules;
   - PHP extensions;
   - writable directories.
10. Produce blockers and safe next step.
11. Run `sf4_wizard_readiness.py` before any execution proposal.
12. If readiness is `needs_rollback_plan`, run `sf4_wizard_rollback_plan.py`, check the filled plan, then re-run readiness with `--rollback-check`.
13. Treat `ready_for_review` plus `controlled_execution_allowed=false` as a review-ready but not executable state.

Validator script:

- `scripts/sf4_wizard_audit.py`.

Acceptance runner:

- `scripts/sf4_wizard_acceptance.py`.

Skeleton generator:

- `scripts/sf4_wizard_skeleton.py`.
- Generates propose-only candidate masters under `source/output/wizard-skeleton/*`.
- Does not write to live `/simai`, `/bitrix`, public roots or `/Users/rim/Sites/*`.
- Use it to draft structure and config; still require real payload fill, read-only audit, backup/rollback design and controlled-runtime approval before execution.

Export package builder:

- `scripts/sf4_wizard_export_builder.py`.
- Generates propose-only `wizard.export`-style packaging masters under `source/output/wizard-export-builder/*`.
- Input is a JSON manifest with source site root, output dir, copy allowlists, module allowlists, iblock allowlist, data export settings and optional archive/cleanup switches.
- Does not execute PHP, Bitrix, wizard actions, file copies, iblock exports, zips or cleanup.
- Use it before any "package existing SF4 solution" work; generated output still requires audit, readiness and rollback review before controlled execution.

Export inventory helper:

- `scripts/sf4_wizard_export_inventory.py`.
- Read-only scans a local source site and writes `inventory.json`, `manifest.draft.json` and optional builder/audit/readiness evidence under `source/output/wizard-export-inventory/*`.
- Detects SIMAI modules, components, templates, public dir, media library, `urlrewrite.php` and wizard action availability.
- Disables mail export unless requested and both mail export actions exist.
- Keeps iblock export bound to explicit `--iblock` allowlists.
- This is the default first tool before packaging a specific existing SF4 solution.

Iblock/HL manifest assistant:

- `scripts/sf4_wizard_iblock_manifest.py`.
- Read-only scans local archive/config/legacy data and writes
  `iblock-manifest.report.json`, `iblock-manifest.draft.json`,
  `builder-manifest.patch.json` and optional merged builder manifest under
  `source/output/wizard-iblock-manifest/*`.
- Detects `data/iblock/*.zip`, valid zip/member signals, legacy `iblocks.php`
  and `highload.php`, and shallow `.iblock.config.php` top-level hints.
- Never executes PHP or Bitrix; config-only codes and highload entries remain
  separate review signals, not automatic export approval.
- Use it before builder/audit when a user asks to package real iblock/HL data
  and the exact allowlist is not yet known.

Readiness runner:

- `scripts/sf4_wizard_readiness.py`.
- Consumes `sf4_wizard_audit.py` JSON and produces a review board under `source/output/wizard-readiness/*`.
- Accepts optional `--rollback-check` JSON from `sf4_wizard_rollback_plan.py`.
- A `ready` audit is not execution approval when actions have filesystem, DB or global runtime side effects.
- Before controlled, staging or live execution, readiness must be `ready_for_review` and `controlled_execution_allowed` must be true, or the exact blocker must be resolved through payload work, real backup artifacts and/or backup/rollback planning.
- Example-only rollback evidence may produce `ready_for_review`, but must keep `controlled_execution_allowed=false`.

Rollback plan checker:

- `scripts/sf4_wizard_rollback_plan.py`.
- Consumes readiness JSON and creates/checks backup and rollback plan artifacts under `source/output/wizard-rollback/*`.
- Empty templates must remain `rollback_plan_incomplete`.
- Filled plans can become `rollback_plan_ready`, but this still does not approve live execution.
- Pass `rollback_plan_ready` check reports back into `sf4_wizard_readiness.py --rollback-check` to distinguish missing rollback from review-ready example evidence.
- Real execution still requires explicit scope, real backup artifacts, ops/tester review and applicable federation gates.

Example:

```bash
python3 scripts/sf4_wizard_skeleton.py --code simai.example --name "SIMAI Example" --profile config --wrapper --force
python3 scripts/sf4_wizard_audit.py --site-root /Users/rim/Sites/sf4.test --master /absolute/path/to/source/output/wizard-skeleton/simai.example/master/simai.example --json source/output/wizard-skeleton/simai.example/audit.json
python3 scripts/sf4_wizard_readiness.py --audit source/output/wizard-skeleton/simai.example/audit.json --json source/output/wizard-readiness/simai.example.json --markdown source/output/wizard-readiness/simai.example.md
python3 scripts/sf4_wizard_rollback_plan.py --readiness source/output/wizard-readiness/simai.example.json --template-json source/output/wizard-rollback/simai.example/template.json --check-json source/output/wizard-rollback/simai.example/check-empty.json
```

Export builder example:

```bash
python3 scripts/sf4_wizard_export_inventory.py --site-root /Users/rim/Sites/university.test --solution-code simai.sf4university.export --site-dir /ru --iblock sf-ru-doc-common --win1251 --run-builder
python3 scripts/sf4_wizard_iblock_manifest.py --source /Users/rim/Sites/test.test/bitrix/modules/simai.sf4biblio/install/wizard/data --label simai.sf4biblio --base-manifest source/output/wizard-export-inventory/simai.sf4university.export/manifest.draft.json
python3 scripts/sf4_wizard_export_builder.py --manifest source/wizard/export-builder-example.json --force
python3 scripts/sf4_wizard_audit.py --site-root /Users/rim/Sites/university.test --master /absolute/path/to/source/output/wizard-export-builder/simai.example.export/master/simai.example.export --json source/output/wizard-export-builder/simai.example.export/audit.json
python3 scripts/sf4_wizard_readiness.py --audit source/output/wizard-export-builder/simai.example.export/audit.json --json source/output/wizard-export-builder/simai.example.export/readiness.json --markdown source/output/wizard-export-builder/simai.example.export/readiness.md
python3 scripts/sf4_wizard_rollback_plan.py --readiness source/output/wizard-export-builder/simai.example.export/readiness.json --template-json source/output/wizard-rollback/simai.example.export/rollback-plan.example.json --check-json source/output/wizard-rollback/simai.example.export/rollback-check.example.json --fill-demo
python3 scripts/sf4_wizard_readiness.py --audit source/output/wizard-export-builder/simai.example.export/audit.json --rollback-check source/output/wizard-rollback/simai.example.export/rollback-check.example.json --json source/output/wizard-rollback/simai.example.export/readiness-with-rollback.example.json --markdown source/output/wizard-rollback/simai.example.export/readiness-with-rollback.example.md
```

## Acceptance Scenarios

Before calling the specialist trained enough for practical universal master work, run the read-only acceptance package when local fixture paths are available:

```bash
python3 scripts/sf4_wizard_acceptance.py --manifest source/wizard/acceptance-fixtures.json --json source/output/wizard-acceptance/report.json
```

Acceptance package scope:

- complete runtime master with visuals and action chain:
  `/Users/rim/Sites/sf4.test/simai/wizard/master/simai.sveden`;
- missing config blocker:
  `/Users/rim/Sites/university.test/simai/wizard/master/simai.sf4university`;
- prebuilt module installer bridge:
  `/Users/rim/Sites/test.test/bitrix/modules/simai.sf4biblio`;
- second prebuilt bridge variant:
  `/Users/rim/Sites/test.test/bitrix/modules/simai.sf4med`;
- assembled module installer bridge:
  `/Users/rim/Sites/test.test/bitrix/modules/simai.sf4university`.

Minimum acceptance evidence:

- runner status is `success`;
- all scenarios are `success`;
- `simai.sveden` stays `ready` with 19 actions, no findings and visual asset resolution;
- missing university runtime master stays `blocked` with `missing_config` and `missing_master_config`;
- module bridge scenarios expose expected installer assembly signals;
- generated reports are stored under `source/output/wizard-acceptance/`.

If any scenario changes, update `source/wizard/acceptance-matrix.md` and `source/wizard/acceptance-fixtures.json` only after re-studying the underlying real source.

## Creation Playbook

For a new universal master:

1. Decide prebuilt vs assembled data shape.
2. Optionally generate a propose-only skeleton in `source/output` with `scripts/sf4_wizard_skeleton.py`.
3. Create wrapper wizard if the module must appear in Bitrix wizard list.
4. Create master `index.php`.
5. Create `.wizard.config.php`.
6. Prepare visual assets.
7. Prepare data payload.
8. Prepare action chain.
9. Verify action resolution and payload existence.
10. Define rollback per side effect.
11. Run only in controlled environment after gates.

## Modification Playbook

For an existing master:

1. Read current config and runtime state.
2. Identify affected stage/action/data key.
3. Preserve existing branch conditions.
4. Keep downstream `DATA_*` keys compatible.
5. Prefer master-local action override for solution-specific behavior.
6. Avoid editing global `/simai/wizard/action` unless framework-wide behavior is intended.
7. Re-run read-only audit.

## Graph Contract

When representing this specialist in Mirai Graph:

- raw source remains authoritative;
- graph object should point to this file and `wizard-actions.md`;
- graph relation should connect the specialist/capability to `skill.sf4.core`;
- graph relation should preserve existing `capability.sf4.wizard-actions` as broader parent/general capability;
- do not claim integration until graph contract gate and federation verification pass.

## Evidence Required In Responses

For wizard work, report:

- master path;
- config path;
- action chain;
- action resolution outcome;
- payload presence;
- side-effect classification;
- readiness status;
- rollback plan status when write actions exist;
- required backup/rollback if execution is requested;
- exact blocker if missing config/action/payload is found.

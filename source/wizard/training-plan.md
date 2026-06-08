# Universal Wizard Specialist Training Plan

## Goal

Train a dedicated SF4 Universal Wizard specialist that can create, modify, package, visualize, diagnose and safely execute universal master flows across SF4 solutions.

The specialist must understand both:

- old Bitrix `wizard_sol` solution installers;
- newer SF4 universal master wrappers and `/simai/wizard/master/<module>/data` payloads.

## Stage 1 - Corpus Review And Source Map

Goal: validate that the source files in this directory describe the real wizard runtime accurately.

Tasks:

- Review source index.
- Confirm runtime model against component source.
- Confirm `simai.sveden` chain against both real configs.
- Confirm `simai.sf4university` missing config interpretation.
- Review module wizard sources:
  - `simai.fund`;
  - `simai.educenter`;
  - `simai.school`;
  - `simai.sf4biblio`;
  - `simai.sf4med`;
  - `simai.sf4university`.
- Build source map for legacy `install/wizards` vs SF4 `install/wizard`.

Output:

- reviewed source corpus;
- list of corrections.
- `source/wizard/source-index.json` updated when new real-world sources are added.

## Stage 2 - Runtime And Entry Models

Goal: teach the specialist how a request enters and reaches the actual master runtime.

Topics:

- Bitrix `wizard_sol` class lifecycle.
- Wrapper `SelectSiteStep` redirect to `/simai/wizard/master/<module>/`.
- `master/<code>/index.php` parameters for `simai:sf.wizard`.
- Runtime storage in `SIMAI\Main\Configuration\Property`.
- `simai:sf.wizard` and `simai:sf.wizard.stage` division of responsibility.
- Action file fallback from master-local action to global `/simai/wizard/action`.

Acceptance:

- Specialist can explain why a wrapper wizard exists even when actual UI is universal master.
- Specialist can diagnose missing `master/<code>/.wizard.config.php`.

## Stage 3 - Master Creation

Goal: teach how to create a new universal master.

Topics:

- Directory contract:
  - `/simai/wizard/master/<module>/index.php`;
  - `/simai/wizard/master/<module>/.wizard.config.php`;
  - `/simai/wizard/master/<module>/data/*`;
  - optional `/simai/wizard/master/<module>/action/*`.
- Module wrapper contract:
  - `install/wizard/<module>/.description.php`;
  - `install/wizard/<module>/wizard.php`;
  - lang files;
  - images.
- Install bridge contract in `install/index.php`:
  - copy framework;
  - copy components;
  - copy wrapper wizard;
  - copy `/simai`;
  - copy payload to `/simai/wizard/master/<module>/data`;
  - unpack required zips;
  - register modules;
  - redirect to master.

Acceptance:

- Specialist can draft a new module wizard wrapper and master payload layout without executing live writes.

## Stage 4 - Wizard Config And Visual Design

Goal: teach appearance, navigation and UX of the universal master.

Topics:

- `.wizard.config.php` `description`.
- `logo`, `background`, `color`, `modifier`.
- Action titles and progress bar behavior.
- Difference between legacy Bitrix wizard visual assets and SF4 universal wizard visuals.
- How custom action output controls visible data per step.
- When to use `info`, `agreement`, `site.choice`, custom master-local actions.

Acceptance:

- Specialist can design a master appearance and identify which layer controls it.

## Stage 5 - Data Packaging

Goal: teach how to prepare files, dynamic data, config, iblocks and highload blocks for a master.

Topics:

- Public file payload:
  - raw copied files;
  - `public.zip`;
  - `site.ru.public.zip`;
  - root/site folders.
- Template payload:
  - `template.zip`;
  - `/bitrix/templates`;
  - `simai.data/template`.
- Component payload:
  - `components/simai.components.zip`;
  - `/bitrix/components/simai`.
- Config payload:
  - `config.zip`;
  - `.iblock.config.php`;
  - `.iblock.section.config.php`;
  - `.iblocktype.config.php`;
  - `.option.config.php`;
  - `.short.config.php`;
  - `urlrewrite.php`.
- PHP interface payload:
  - `dbconn.add.php`;
  - `init.add.php`.
- Module payload:
  - `data/module/*.zip`;
  - copied module sources under `install/bitrix/modules/*`.
- Legacy PHP-array data:
  - `types.php`;
  - `iblocks.php`;
  - `props.php`;
  - `sections.php`;
  - `elements.php`;
  - `fields.php`;
  - `forms.php`;
  - `seo.php`;
  - `highload.php`;
  - `highloadprops.php`;
  - `highloadelems.php`.
- New archive data:
  - `data/iblock/*.zip`;
  - highload content inside iblock export archives.

Acceptance:

- Specialist can choose old PHP-array format vs new archive format for a scenario.
- Specialist can specify exact files needed before an import action is allowed.

## Stage 6 - Per-Action Contracts

Goal: convert action inventory into detailed action contracts.

Priority actions:

1. `iblock.import.archive`
2. `iblock.import.archive.sveden`
3. `iblockconfig.import.data`
4. `site.choice.sveden`
5. `site.update.sveden`
6. `file.copy`
7. `replace.code`
8. `urlrewrite.add`
9. `data.import.file`
10. `option.import.data`
11. `iblock.export.archive`
12. `file.zip`
13. `file.unzip`

For each action capture:

- input data keys;
- output data keys;
- parameters;
- filesystem/database side effects;
- progress counters;
- AJAX files;
- required modules/extensions;
- idempotency notes;
- failure modes;
- safe test strategy.

Acceptance:

- Specialist can produce an action contract table for any wizard config.
- First contract table is captured in `source/wizard/action-contracts.md`.

## Stage 7 - Creation And Modification Playbooks

Goal: teach repeatable operations.

Playbooks:

- create a new master from an existing SF4 module package;
- add a new action stage to existing master;
- modify visual branding without changing action logic;
- add new public/template payload;
- add new config payload;
- add new iblock archive;
- add highload-aware archive;
- update `urlrewrite`;
- migrate legacy PHP-array data to archive payload;
- add master-local action override safely;
- repair missing data key or condition branch;
- debug stuck `WORK` stage.

Acceptance:

- Specialist can produce a step-by-step safe plan with rollback for each playbook.
- Master creation baseline is captured in `source/wizard/master-blueprint.md`.
- Packaging baseline is captured in `source/wizard/packaging-matrix.md`.
- Export/archive preparation is captured in `source/wizard/export-packaging-data.md`.

## Stage 8 - Specialist Draft

Goal: prepare a specialist source proposal.

Artifacts:

- specialist role definition;
- decision checklist;
- troubleshooting checklist;
- acceptance gates;
- examples from `sf4.test` and `university.test`.
- examples from `test.test` module install wizards.
- visual contract from `source/wizard/visual-contract.md`.
- read-only validator spec from `source/wizard/validator-spec.md`.

## Stage 9 - Owner Apply Plan

Goal: prepare controlled changes to canonical skill files.

Possible targets:

- `skills/sf4/SKILL.md` routing note;
- `skills/sf4/references/wizard-actions.md` expansion;
- new `skills/sf4/specialists/universal-wizard.md` if owner approves;
- graph capability/specialist proposal if federation integration is required.
- new validator/checklist artifacts for master packages.
- proposed source promotion path in `source/wizard/specialist-apply-plan.md`.

Required gates:

- owner approval;
- skill graph sync;
- federation verify;
- route check.

## Stage 10 - QA

Goal: verify the specialist can reason over real wizard tasks.

Test prompts:

- diagnose missing `.wizard.config.php`;
- trace `simai.sveden` install chain;
- explain why an action is skipped by condition;
- debug stage stuck in `WORK`;
- validate payload files before import;
- prepare safe rollback for `file.copy` plus iblock import.
- create a new master package plan for a module like `simai.sf4med`;
- explain how `install/index.php` prepares runtime master data;
- package a highload-aware iblock archive plan;
- modify wizard background/logo/colors/modifiers;
- convert legacy wizard service data into universal master data.

## Training Evidence Checklist

Before the specialist is considered ready, collect:

- runtime state diagram;
- master creation checklist;
- `.wizard.config.php` schema notes;
- action contract table;
- payload packaging matrix;
- visual design matrix;
- highload export/import notes;
- wrapper wizard vs universal master comparison;
- safe-write and rollback checklist;
- test prompts with expected answers.

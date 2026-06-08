# Universal Wizard Export Builder

`scripts/sf4_wizard_export_builder.py` creates a propose-only `wizard.export`-style SF4 universal master from a JSON manifest.

It is for packaging preparation, not for live execution.

## Safety Contract

The builder:

- writes only inside `source/output`;
- does not execute PHP;
- does not execute Bitrix;
- does not run wizard actions;
- does not copy files into a real site;
- does not create `/.last_version`;
- does not export iblocks/highload blocks;
- does not zip or delete generated runtime files.

The generated master may contain write actions, but those actions are not executed by the builder.

## Basic Usage

```bash
python3 scripts/sf4_wizard_export_builder.py \
  --manifest source/wizard/export-builder-example.json \
  --force
```

Generated package:

```text
source/output/wizard-export-builder/<solution_code>/
  README.md
  input-manifest.json
  builder-report.json
  master/<solution_code>/
    index.php
    .wizard.config.php
    image/
    temp/
```

## Manifest Contract

Required fields:

| Field | Meaning |
|---|---|
| `solution_code` | Generated master code and output folder name. |
| `solution_name` | Human-readable wizard name. |
| `source_site_root` | Source Bitrix/SF4 site root used later by audit and controlled execution. |
| `export.output_dir` | Site-relative output dir for generated package, for example `/.last_version/simai.example`. |

Optional fields:

| Field | Meaning |
|---|---|
| `modules` | Bitrix module codes copied from `/bitrix/modules/<code>`. |
| `copy` | Explicit site-relative file/directory copy rows. |
| `public_copy` | Public/root copy rows, kept as a separate `file.copy` stage. |
| `iblocks` | Explicit iblock code allowlist for `iblock.export.archive`. |
| `data_exports.site` | Enable `site.export.data`; default `true`. |
| `data_exports.mail` | Enable `mail.export.data`; default `false`. |
| `data_exports.mail_templates` | Enable `mail-templates.export.data`; default `false`. |
| `data_exports.usergroups` | User group code list for `usergroup.export.data`. |
| `data_exports.iblock_types` | Enable `iblocktype.export.data`; default `true`. |
| `data_exports.options` | Module option allowlist for `option.export.data`. |
| `data_files` | Override generated config file paths per `data_input_code`. |
| `php_interface_snippets` | Generated snippet rows for `file.create`. |
| `encoding.win1251` | Enable `file.encode.win1251`. |
| `archive.enabled` | Add final `file.zip` action. Keep disabled until review. |
| `cleanup.enabled` | Add `file.delete` cleanup action. Keep disabled until review. |

## Recommended Flow

1. Inventory the source solution manually or with `scripts/sf4_wizard_export_inventory.py`.
2. Create or review a manifest with explicit allowlists.
3. Generate a master proposal.
4. Run `sf4_wizard_audit.py` using the source site root as read-only action library.
5. Run `sf4_wizard_readiness.py`.
6. Create or check rollback plan for every write action.
7. Only then run in a disposable or explicitly approved source environment.

## Important Rules

- Do not enable mail export unless `mail.export.data` and `mail-templates.export.data` actions exist in the target action library or are supplied as reviewed master-local actions.
- Do not export all iblocks for productized packages. Use an explicit `iblocks` allowlist.
- Treat `data.export.file` outputs as generated files, not source payloads.
- Keep `archive.enabled` and `cleanup.enabled` false in review examples.
- Never execute a generated master on live/staging without ops gate, backup, rollback and stop conditions.

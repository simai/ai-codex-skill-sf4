# Universal Wizard Export Inventory Helper

`scripts/sf4_wizard_export_inventory.py` prepares a draft manifest for packaging an existing SF4/Bitrix project through the universal wizard export builder.

It is read-only for the inspected site.

## Safety Contract

The helper:

- reads a local `--site-root`;
- writes only under `source/output`;
- does not execute PHP or Bitrix;
- does not run wizard actions;
- does not create `/.last_version`;
- does not copy, zip, delete, import or export runtime data.

When `--run-builder` is used, it runs only the already safe proposal chain:

```text
inventory -> manifest.draft.json -> sf4_wizard_export_builder.py -> sf4_wizard_audit.py -> sf4_wizard_readiness.py
```

If readiness reports write actions, continue the safe proposal chain with:

```text
sf4_wizard_rollback_plan.py -> sf4_wizard_readiness.py --rollback-check
```

## Basic Usage

```bash
python3 scripts/sf4_wizard_export_inventory.py \
  --site-root /Users/rim/Sites/university.test \
  --solution-code simai.sf4university.export \
  --solution-name "SIMAI SF4 University Export" \
  --site-dir /ru \
  --iblock sf-ru-doc-common \
  --win1251 \
  --run-builder
```

Generated evidence:

```text
source/output/wizard-export-inventory/<solution_code>/
  inventory.json
  manifest.draft.json
  run-report.json
  audit.json
  readiness.json
  readiness.md
  builder/<solution_code>/
```

Rollback/readiness follow-up evidence is usually written separately under:

```text
source/output/wizard-rollback/<solution_code>/
  rollback-plan.example.json
  rollback-check.example.json
  readiness-with-rollback.example.json
```

## Inventory Signals

The helper detects:

- `bitrix/modules/simai.*`;
- `bitrix/components/simai`;
- `bitrix/templates/*`;
- public `--site-dir`;
- `/upload/medialibrary`;
- `/urlrewrite.php`;
- `/simai/wizard/action/*/action.php`;
- availability of export/copy/package actions:
  - `site.export.data`;
  - `mail.export.data`;
  - `mail-templates.export.data`;
  - `usergroup.export.data`;
  - `iblocktype.export.data`;
  - `option.export.data`;
  - `data.export.file`;
  - `iblock.export.archive`;
  - `file.copy`;
  - `file.create`;
  - `file.encode.win1251`;
  - `file.zip`.

## Manifest Draft Rules

- If `solution_code` exists as a module, it is included.
- If `solution_code` ends with `.export`, the helper also checks the same code without `.export`.
- Support modules are included only when present locally.
- Mail export is disabled unless requested with `--include-mail` and both mail actions exist.
- Iblock export uses only explicit `--iblock` allowlist values; an empty list is preserved as a review gap.
- Archive and cleanup remain disabled unless explicitly requested; cleanup remains disabled by design in generated examples.

## Review Rules

Inventory output is a draft, not execution approval.

Before running a generated master in any source environment:

1. Review `manifest.draft.json`.
2. Confirm module/template/public copy scope.
3. Confirm iblock allowlist.
4. Run audit/readiness.
5. Fill rollback plan for every write action.
6. Re-run readiness with rollback check evidence.
7. Use a disposable or explicitly approved source environment.

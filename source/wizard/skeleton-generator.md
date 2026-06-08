# Universal Wizard Skeleton Generator

`scripts/sf4_wizard_skeleton.py` creates propose-only universal master skeletons under `source/output/wizard-skeleton`.

It is a training and preparation tool, not a live installer.

## Safety Contract

The generator:

- writes only inside `source/output`;
- does not execute PHP;
- does not execute Bitrix;
- does not run wizard actions;
- does not import iblocks or highload blocks;
- does not copy files into `/simai`, `/bitrix` or public site roots.

The script refuses output directories outside `source/output`.

## Basic Usage

```bash
python3 scripts/sf4_wizard_skeleton.py \
  --code simai.example \
  --name "SIMAI Example" \
  --profile config \
  --wrapper \
  --force
```

Generated package:

```text
source/output/wizard-skeleton/simai.example/
  README.md
  manifest.json
  master/simai.example/
    index.php
    .wizard.config.php
    image/
    lang/ru/
    tmp/
    data/
      config/
      iblock/
      module/
      php_interface/
      root/
      site/
      template/
      components/
  module/install/wizard/simai.example/   # when --wrapper is used
```

## Profiles

| Profile | Action Chain | Purpose |
| --- | --- | --- |
| `minimal` | `site.choice.sveden`, `info` | Smallest valid master shell for visual/config iteration. |
| `config` | `site.choice.sveden`, `iblockconfig.import.data`, `urlrewrite.add`, `info` | Default package skeleton for config-aware masters. |
| `iblock` | `config` plus `iblocktype.import.data`, `iblock.import.archive` | Demonstrates archive packaging shape using a sample XML zip placeholder. |

## Audit Example

Use a real local SF4 site root only as a read-only action library:

```bash
python3 scripts/sf4_wizard_audit.py \
  --site-root /Users/rim/Sites/sf4.test \
  --master /Users/rim/Documents/GitHub/ai-codex-skill-sf4/source/output/wizard-skeleton/simai.example/master/simai.example \
  --json source/output/wizard-skeleton/simai.example/audit.json
```

Expected for generated examples:

- `status: ready`;
- all action codes resolve through the read-only action library site root;
- visual assets exist as placeholders;
- deterministic config payload paths exist.

Use an absolute `--master` path when `--site-root` points to a real action-library site. Relative master paths are intentionally resolved relative to `--site-root` by `sf4_wizard_audit.py`.

## Human Work Still Required

Before turning a skeleton into a real master:

- replace placeholder visual assets;
- fill real config/data payloads;
- export real iblock/HL archives where needed;
- choose exact action chain and conditions;
- define backup/rollback for every side effect;
- audit in a controlled environment;
- run only with explicit runtime scope and gates.

# Case: simai.sf4university

## Source Path

- `/Users/rim/Sites/university.test/simai/wizard/master/simai.sf4university`

## Evidence

The directory contains:

- `index.php`;
- large `data/site` payload;
- `data/bitrix` payload;
- `data/config/urlrewrite.php`;
- `data/iblock/*.zip` payloads.

Observed iblock archives:

- `sf-ru-banner-section.zip`
- `sf-ru-faq.zip`
- `sf-ru-news.zip`
- `sf-ru-video.zip`

No `.wizard.config.php` was found in the inspected master directory.

## Interpretation

This directory should be treated as a payload-rich master package with an incomplete or externally generated runtime scenario in the currently inspected filesystem state.

It is not enough to say "the master exists" because `index.php` points `WIZARD_CONFIG_FILE` to:

```text
<wizard_dir>/.wizard.config.php
```

Without that file, the universal wizard component will report a missing config file unless another installer step generates or copies it before runtime.

## Specialist Rule

When a master has payload but no `.wizard.config.php`:

1. Record the exact missing config.
2. Search module installer or packaging pipeline for generated config.
3. Do not claim the master is runnable until config provenance is found.
4. Use payload only as evidence of intended install content, not as action chain evidence.

## Training Value

This case is useful for teaching the specialist to distinguish:

- runnable master scenario;
- payload package;
- generated installer artifact;
- incomplete local snapshot;
- real blocker.

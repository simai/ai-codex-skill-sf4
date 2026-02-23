# E2E Validation: SF4 Type A/B/C Cases (`/ru`)

Validation date:

- 2026-02-23

Scope:

- Site root: `<project_root>`
- Site dir: `/ru`
- Cases:
  - Type A: `ru/worldskills-russia/index.php`
  - Type B: `ru/students/service/detail.php`
  - Type C: `ru/contacts/index.php`

## 1) Route Classification Check

Result:

- PASS: Type A page has no page-local component orchestration (`sf=0`, `bitrix=0`) and follows template/view/block route.
- PASS: Type B page is direct `simai:sf.grid` route (`sf=1`, includes `simai:sf.grid`).
- PASS: Type C page is component-heavy route (`sf=2`, `bitrix=2`; includes `simai:sf.iblock.list`, `simai:sf.feedback`, `bitrix:main.include`, `bitrix:map.yandex.view`).

## 2) Syntax Check (`php -l`)

Checked files:

- `ru/worldskills-russia/index.php`
- `ru/students/service/detail.php`
- `ru/students/service/.property.php`
- `ru/contacts/index.php`
- `local/templates/simai.framework/components/simai/sf.iblock.list/contacts/template.php`
- `local/templates/simai.framework/components/bitrix/map.yandex.view/contacts/template.php`
- `ru/simai.data/grid/view/main/top/default/template.php`
- `ru/simai.data/grid/block/main/page.title/template.php`
- all `ru/simai.data/grid/block/service-about/**/template.php`

Result:

- PASS: all listed files passed `php -l`.

## 3) Route/Structure Audit Baseline

Command:

- `python3 scripts/sf4_project_audit.py --site-root <project_root> --site-dir /ru --show-summary --link-report-json skills/sf4/references/artifacts/university-ru-link-report.json`

Result:

- PASS: critical SF4 core files and active `grid_view_*` bindings are valid.
- WARN: hygiene warnings in `grid/block` (archives/cache/manifests found).
- WARN: `view -> block` unresolved links exist in legacy/inactive variants.
  - summary: total `417`, ok `331`, missing `86`
  - hotspots: `home=71`, `homepage=14`, `header=1`

## 4) Frontend Baseline Audit

Markup inventory result:

- PASS: report generated (`university-ru-markup-inventory.json`).
- PASS: expected base classes detected (`sf-title`, `btn-primary`, utilities).

Interactive audit result:

- PASS: report generated (`university-ru-interactive-audit.json`).
- PASS: known markers present (`sf_modal_attr`, `aria_attr`, `sf_src_attr`).
- INFO: no `dropdown_toggle` and `inputmask_attr` markers found in scanned SF4 templates.

## 5) Backend Risk Baseline

Command:

- `python3 scripts/sf4_backend_risk_scan.py --site-root <project_root> --site-dir /ru --json-out skills/sf4/references/artifacts/university-ru-backend-risk.json`

Result:

- WARN: detected known risk patterns in baseline templates/config:
  - `iblock_siteid_concat=128`
  - `domcontentloaded=3`
  - `asset_addjs_addcss=11`
- PASS: `block_edit_without_position_relative=0`.

## 6) E2E Verdict For Skill Usage

Final status:

- PASS with WARNINGS.

Interpretation:

- Skill workflow is ready for real Type A/B/C modernization tasks.
- Existing WARN items are baseline project debt, not blocker for skill operation.
- For release tasks, run remediation flow for missing links and backend risk hotspots in controlled batches.

## 7) Skill Routing Consistency Check (`$sf4`)

Result:

- PASS: `simai-sf4` alias references in repository: `0`.
- PASS: skill key in metadata is `name: sf4`.
- PASS: UI metadata points to `SIMAI Framework 4` and usage examples call `$sf4`.


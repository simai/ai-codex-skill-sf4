# SF4 Scripts Catalog

Project scripts live in `skills/sf4/scripts/`; universal wizard scripts live in
the repository root `scripts/`. Add `--dry-run` / omit `--apply` to preview.

## Project Audit And Maps

- Audit project: `python3 scripts/sf4_project_audit.py --site-root <project_root> --site-dir <site_dir>`
- Export `view -> block` linkage: add `--link-report-json <path.json> --link-report-csv <path.csv>`
- Page route map with active views, key blocks, override hotspots:
  `python3 scripts/sf4_site_map.py --site-root <project_root> --site-dir <site_dir> [--json-out <path.json> --json]`
- Component templates and resolved source paths:
  `python3 scripts/sf4_component_template_map.py --site-root <project_root> --site-dir <site_dir> [--json-out <path.json>]`

## Scaffolding

- Block: `python3 scripts/create_sf4_block.py --site-root <project_root> --site-dir <site_dir> --section <section> --code <block_code> [--dry-run]`
- View: `python3 scripts/create_sf4_view.py --site-root <project_root> --site-dir <site_dir> --area <area> --code <view_code> [--dry-run]`
- Missing blocks from a link report:
  `python3 scripts/scaffold_missing_blocks.py --site-root <project_root> --site-dir <site_dir> --report-json <path.json> --limit 20 [--apply]`

## Frontend And Backend Scans

- Class inventory: `python3 scripts/sf4_markup_inventory.py --site-root <project_root> --site-dir <site_dir> --top 80`
  (lookup: `--class sf-form-control --class theme-dark`; export: `--json-out <path.json>`)
- Interactive markers and assets: `python3 scripts/sf4_interactive_audit.py --site-root <project_root> --site-dir <site_dir> --top 80`
  (details: `--marker sf_modal_attr --marker inputmask_attr`; export: `--json-out <path.json>`)
- Backend risks from `/ru/bx` guides: `python3 scripts/sf4_backend_risk_scan.py --site-root <project_root> --site-dir <site_dir> [--json-out <path.json>]`

## Universal Wizard (repository root `scripts/`)

- Read-only master/package audit: `python3 scripts/sf4_wizard_audit.py --master <master_path> --site-root <site_root> --json <report.json>`
- Propose-only skeleton under `source/output`: `python3 scripts/sf4_wizard_skeleton.py --code <wizard_code> --name "<name>" --profile config --wrapper`
- Propose-only `wizard.export`-style packaging master: `python3 scripts/sf4_wizard_export_builder.py --manifest <manifest.json> --force`
- Draft export manifest from a source site: `python3 scripts/sf4_wizard_export_inventory.py --site-root <site_root> --solution-code <code> --site-dir /ru --run-builder`
- Draft iblock/HL allowlist: `python3 scripts/sf4_wizard_iblock_manifest.py --source <wizard_data_or_legacy_iblock_data_dir> --label <label> --base-manifest <manifest.json>`
- Readiness board: `python3 scripts/sf4_wizard_readiness.py --audit <audit.json> --json <readiness.json> --markdown <readiness.md>`
- Rollback plan: `python3 scripts/sf4_wizard_rollback_plan.py --readiness <readiness.json> --template-json <plan.json> --check-json <check.json>`

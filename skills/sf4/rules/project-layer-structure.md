# Project Layer Structure

- Keep block metadata and params near block code: `.description.php`,
  `.parameters.php`, `lang/<lang>/`.
- Keep `grid_view_*` values aligned with real folders in
  `simai.data/grid/view/.../<code>/`.
- Keep row/column/area parameter naming consistent with SF4 grid patterns.
- Use area templates in `simai.data/template/area/.../template.php` to select
  the active view by property; compose pages from rows/columns/areas in view
  `template.php` files; add or override blocks under
  `simai.data/grid/block/<section>/<code>/`.
- Check file permissions for `simai.data` when changes do not persist.
- Do not commit archives, cache or vendor artifacts inside
  `simai.data/grid/block`.
- Keep secret-like values out of `.site.property.php` when possible; prefer
  environment-backed storage.
- Settings: schema in `simai.data/config/*.config.php`, values in
  `simai.data/.site.property.php` and section/page `/.property.php`.
  Precedence: site -> section -> page -> user -> optional global overrides
  (the latest merged level wins).
- Missing `view -> block` links: run the audit with `--link-report-json`, run
  `scaffold_missing_blocks.py` in dry-run first, apply in small `--limit`
  batches and re-run the audit after each batch.

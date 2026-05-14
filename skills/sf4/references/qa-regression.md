# SF4 QA and Regression

## Goal

Run predictable verification after SF4 changes and report evidence, risks, and residual gaps.

## Result Model

For each check record:

- Status: `PASS` / `FAIL` / `N-A` / `NEEDS RUN`
- Evidence: command output, URL/page, screenshot, or short log excerpt
- Risk: `Low` / `Medium` / `High`
- Recommendation: concrete fix or follow-up test

## Minimum Smoke For SF4 Tasks

1. Target page opens without PHP/Bitrix fatal errors.
2. Active `grid_view_*` property points to expected view folder.
3. Referenced blocks render from expected layer (`simai.data` or system fallback).
4. Changed settings are read with expected precedence (site/section/page/user).
5. Changed editor parameters and `lang` labels are visible where expected.
6. Cache is cleared and behavior is re-checked.

For portal/host-mode solution pages, this minimum smoke is not final
acceptance. Load `portal-runtime-source-of-truth.md` and also verify required
page-class blocks, meaningful content markers, current tenant/source
selection, host-mode include paths, and editor/admin context where applicable.

## Regression Minimum

Run focused regression around touched scope:

1. Adjacent layout areas (header/footer/sidebar/main) still render.
2. Existing property-driven variants still switch correctly.
3. Existing block params still map to template keys.
4. If iblock/HL logic changed: list/query/edit flow still works.
5. If wizard/update flow changed: install/update chain remains reproducible.
6. If portal/shared `simai.data` runtime is touched: sibling solution sentinel
   pages still render from their own source and do not pick up the changed
   solution's blocks, menus, banners, or root sections.

## Static Safety Checks

Suggested quick checks before runtime validation:

- `php -l <changed_file.php>` for each changed PHP file
- `rg -n "var_dump|print_r\\(|die\\(|exit\\(|TODO"` in touched directories
- Verify no accidental system-layer edits (`/simai`, `/bitrix/templates/simai.framework`, `/bitrix/components/simai`) unless explicitly requested
- Run `scripts/sf4_project_audit.py` and review hygiene warnings (duplicate keys, secret-like literals, archive/cache artifacts)

## Output Artifacts

Use templates from `references/artifacts/`:

- `regression-checklist.md` for compact release gating
- `qa-report.md` for expanded runs with risk/evidence model

## Exit Criteria

Task is ready to hand off when:

1. Smoke checks are `PASS` or have accepted, explicit exceptions.
2. Regression checks cover all touched risk areas.
3. Remaining gaps are listed as explicit follow-up items.

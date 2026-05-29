# sf4 Repo GrowGraph Migration

Дата: 2026-05-29

## Scope

Repo-local GrowGraph companion layer for `skill:sf4`.

This migration does not rewrite `skills/sf4/SKILL.md` and does not move SF4
domain knowledge out of the sf4 skill.

## Generated Artifacts

```text
graph/source/growgraph/seeds/sf4-repo-local-seed-20260529.json
graph/generated/seed-validation/sf4-repo-local-seed-validate-20260529/
graph/generated/seed-expansions/sf4-repo-local-seed-expand-20260529/
graph/generated/embryo-proposals/sf4-repo-local-embryo-proposals-20260529/
graph/generated/control-dashboards/sf4-repo-local-control-dashboard-20260529/
graph/generated/growgraph/semantic-preservation/sf4-repo-local-semantic-review-20260529/
graph/generated/growgraph/effectiveness-reports/sf4-repo-local-effectiveness-20260529/
graph/generated/readiness-scores/sf4-repo-local-score-20260529/
graph/federation/exports/sf4-repo-local-federation-export-20260529/
graph/generated/growgraph/integration-reviews/sf4-repo-local-integration-review-active-gate-20260529/
graph/generated/growgraph/adoption-reports/sf4-repo-local-adoption-gga9-active-gate-20260529/
```

## Result

```text
semantic preservation: pass_with_notes
effectiveness: improved
federation export: success
integration review: pass_with_notes
adoption: GGA9 federation_integrated
contract gate: success
canonical_write_allowed: false
```

## Boundary

This is `GGA9 federation_integrated` for the repo-local companion layer.
It is not `GGA10`; source-of-truth rewrites require a separate approved apply
plan.

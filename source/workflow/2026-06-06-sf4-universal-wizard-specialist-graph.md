# SF4 Universal Wizard Specialist And Graph Integration

## Goal

Create and train a dedicated SF4 Universal Wizard specialist from the reviewed `source/wizard` corpus, then integrate the specialist into canonical SF4 skill sources and Mirai Graph/federation routing according to the repo standards.

## Done When

- `skills/sf4/specialists/universal-wizard.md` exists and defines the specialist role, scope, source-of-truth hierarchy, runtime model, action contract discipline, packaging discipline, visual contract, audit workflow, escalation rules and acceptance gates.
- Canonical SF4 references point to the specialist without duplicating the entire staging corpus.
- The SF4 skill entrypoint routes wizard/master/package tasks to the specialist.
- Repo-local graph specs include a specialist/capability object or an equivalent accepted graph representation.
- Graph relations connect the specialist/capability to `skill.sf4.core` and the existing `capability.sf4.wizard-actions` without replacing raw skill sources.
- Graph index includes the new graph files.
- Verification gates are run and recorded:
  - preflight action gates;
  - `python3 scripts/mirai_graph_contract_gate.py`;
  - `scripts/skill-change-detect.sh` if available;
  - `scripts/skill-graph-sync.sh --skill sf4` if available and appropriate;
  - `scripts/federation-verify.sh --profile admin --no-write` or central fallback;
  - `scripts/federation-route-check.sh` or central fallback.
- `source/wizard` tracking decision remains explicit: staging corpus stays ignored unless separately approved.
- Kaizen sections are updated after each batch.

## Source Inputs

- `source/wizard/action-contracts.md`
- `source/wizard/packaging-matrix.md`
- `source/wizard/export-packaging-data.md`
- `source/wizard/master-blueprint.md`
- `source/wizard/visual-contract.md`
- `source/wizard/validator-spec.md`
- `source/wizard/specialist-apply-plan.md`
- `skills/sf4/SKILL.md`
- `skills/sf4/references/wizard-actions.md`
- `skills/sf4/references/system-layer-simai.md`
- `graph/specs/objects/capability-sf4-wizard-actions.json`
- `graph/specs/objects/skill-sf4-core.json`
- `graph/specs/index.json`

## Route And Gates

Federation route:

- primary: `graph`
- companions: `dev`, `teamlead`, `sf4`
- required gates: `graph_contract`, `learning_proposal`, `owner_approval`, `no_duplication`
- graph-only runtime: forbidden; raw SF4 skill sources remain source-of-truth for methodology.

Preflight evidence:

- `source/output/action-gates/action-gate-report-20260606092330.json`
- status: success
- blockers: none

Owner approval evidence:

- User request on 2026-06-06: "надо сделать специалиста и обучить его и все должно быть в графах в соответсвии со стандартами. можешь сформировать цель и сделать её батчами?"

## Workstreams

### A. Canonical Specialist

Create a dedicated specialist file under `skills/sf4/specialists/`.

Expected content:

- purpose and boundaries;
- source-of-truth hierarchy;
- universal master runtime model;
- action contract table discipline;
- packaging and export/import discipline;
- visual contract;
- read-only audit checklist;
- creation/modification playbooks;
- live/runtime escalation rules;
- required evidence.

### B. Canonical Reference Integration

Update minimal SF4 references:

- `skills/sf4/SKILL.md`: add pointer from wizard tasks to the specialist.
- `skills/sf4/references/wizard-actions.md`: add short specialist handoff section and avoid duplicating the entire corpus.

### C. Graph Integration

Add graph representation:

- object for `capability.sf4.universal-wizard-specialist` or specialist equivalent;
- relation from `skill.sf4.core` to the new capability;
- relation from new capability to existing `capability.sf4.wizard-actions`;
- source refs pointing to canonical specialist/reference files;
- index update.

### D. Verification And Sync

Run the repo gates and record evidence. If a sync script is missing or blocked, record the exact blocker and safe alternative.

### E. Kaizen

Update lessons learned, process improvements, skill/federation improvement candidates and follow-up proposals after each batch.

## Batches

### Batch 1 - Workflow And Current-State Inventory

Status: completed

Tasks:

- Create this workflow file.
- Confirm route/preflight evidence.
- Inventory current canonical skill files, specialist directory state and graph objects.
- Decide graph representation without duplication.

Acceptance:

- Workflow exists with goal, done-when, workstreams, batches, gates and next step.
- Current-state inventory is documented.

Evidence:

- This workflow file.
- Route evidence from `federation-route-resolve`: primary `graph`, companions `dev`, `teamlead`, `sf4`.
- Preflight evidence: `source/output/action-gates/action-gate-report-20260606092330.json`.
- Current inventory:
  - no previous `skills/sf4/specialists/`;
  - existing `capability.sf4.wizard-actions`;
  - existing `skill.sf4.core`.

### Batch 2 - Canonical Specialist Source

Status: completed

Tasks:

- Create `skills/sf4/specialists/universal-wizard.md`.
- Condense source corpus into operational specialist instructions.
- Keep `/simai`, `/bitrix/components/simai`, `/bitrix/templates/simai.framework` immutability and live safety boundaries explicit.

Acceptance:

- Specialist can answer create/modify/package/visualize/audit tasks from canonical source alone.
- Specialist references source corpus as evidence but does not depend on ignored files as the only source-of-truth.

Evidence:

- `skills/sf4/specialists/universal-wizard.md`

### Batch 3 - Skill Reference Wiring

Status: completed

Tasks:

- Update `skills/sf4/SKILL.md`.
- Update `skills/sf4/references/wizard-actions.md`.

Acceptance:

- Wizard tasks have a clear route to the specialist.
- Existing wizard reference remains concise and consistent.

Evidence:

- `skills/sf4/SKILL.md`
- `skills/sf4/references/wizard-actions.md`

### Batch 4 - Graph Specs

Status: completed

Tasks:

- Add graph object and relations.
- Update `graph/specs/index.json`.
- Preserve existing `capability.sf4.wizard-actions` as parent/general capability.

Acceptance:

- Graph can represent the specialist/capability and its relationship to SF4 core.
- No graph-only replacement of raw skill methodology.

Evidence:

- `graph/specs/objects/capability-sf4-universal-wizard-specialist.json`
- `graph/specs/relations/relation-skill-sf4-core-implements-capability-sf4-universal-wizard-specialist.json`
- `graph/specs/relations/relation-capability-sf4-universal-wizard-specialist-specializes-capability-sf4-wizard-actions.json`
- `graph/specs/index.json`

### Batch 5 - Verification Gates

Status: completed

Tasks:

- Run JSON validation for edited graph files.
- Run `python3 scripts/mirai_graph_contract_gate.py`.
- Run skill/federation sync/verify commands available in this repo or central control plane.
- Record blockers exactly.

Acceptance:

- Verification evidence is recorded.
- If graph sync/verify is blocked, workflow contains the exact blocker and next safe step.

Evidence:

- JSON validation for edited graph files: success.
- `python3 scripts/mirai_graph_contract_gate.py`: success, blockers none, `canonical_write_allowed=false`.
- `/Users/rim/Documents/GitHub/ai-codex/scripts/skill-change-detect.sh --repo /Users/rim/Documents/GitHub/ai-codex-skill-sf4 --skill sf4 --json`: status `changed`; detected `sf4.universal-wizard`; specialist promotion required.
- `/Users/rim/Documents/GitHub/ai-codex/scripts/skill-graph-sync.sh --repo /Users/rim/Documents/GitHub/ai-codex-skill-sf4 --skill sf4 --task "создать SF4 universal wizard specialist обучить на source/wizard встроить в Mirai Graph federation" --json`: success.
- Generated local graph evidence:
  - `graph/generated/mirai_graph/skill-source-changes/skill-graph-sync-sf4-20260606092808/skill-source-change-evidence.json`
  - `graph/generated/mirai_graph/skill-source-changes/skill-graph-sync-sf4-20260606092808/skill-graph-sync-report.json`
  - `graph/generated/mirai_graph/runtime-kit/skill-graph-sync-sf4-20260606092808-verify/runtime-kit-verify.json`
  - `graph/generated/mirai_graph/runtime-context/skill-graph-sync-sf4-20260606092808-context/context-pack.json`
- Generated central graph proposals:
  - `/Users/rim/Documents/GitHub/ai-codex-skill-graph/graph/generated/mirai_graph/federation-change/skill-graph-sync-sf4-20260606092808-federation-proposal/federation-change-proposal.json`
  - `/Users/rim/Documents/GitHub/ai-codex-skill-graph/graph/generated/mirai_graph/specialist-promotion/skill-graph-sync-sf4-20260606092808-specialist-sf4-universal-wizard/specialist-promotion-proposal.json`
- `/Users/rim/Documents/GitHub/ai-codex/scripts/federation-route-check.sh --profile admin --json`: success, 42/42 passed.
- `/Users/rim/Documents/GitHub/ai-codex/scripts/federation-verify.sh --profile admin --no-write`: first run partial due to missing sf4 sync/proposal; after `skill-graph-sync`, rerun status success, blockers none.
- Route smoke for "создать универсальный мастер SF4 с упаковкой инфоблоков highload и оформлением": primary `sf4`, companions `bitrix`, `tester`, confidence high, blockers none.
- Runtime context includes `capability.sf4.universal-wizard-specialist` and raw source refs.

Notes:

- `canonical_write_allowed=false` remains true for generated/proposal operations. That is expected for review/proposal layers and means generated evidence does not itself authorize uncontrolled central canonical registry writes.

### Batch 6 - Completion Audit And Kaizen

Status: completed

Tasks:

- Audit Done When item by item.
- Update Kaizen sections.
- Mark goal complete only if evidence proves completion.

Acceptance:

- No unverified requirement remains.

Evidence:

- `git diff --check`: success.
- Required files present:
  - `skills/sf4/specialists/universal-wizard.md`
  - `graph/specs/objects/capability-sf4-universal-wizard-specialist.json`
  - `graph/specs/relations/relation-skill-sf4-core-implements-capability-sf4-universal-wizard-specialist.json`
  - `graph/specs/relations/relation-capability-sf4-universal-wizard-specialist-specializes-capability-sf4-wizard-actions.json`
  - `graph/generated/mirai_graph/runtime-context/skill-graph-sync-sf4-20260606092808-context/context-pack.json`
- `rg` verification confirms specialist pointers in `SKILL.md`, `wizard-actions.md`, graph index, graph object and workflow.
- Current git state has expected modified/untracked files; `source/` remains ignored by design.

## Current-State Inventory

- `skills/sf4/specialists/` does not exist yet.
- Existing graph has `capability.sf4.wizard-actions` as a broad pilot capability.
- Existing graph has `skill.sf4.core`.
- Existing graph relation `skill.sf4.core -> capability.sf4.wizard-actions` uses `implements`.
- New graph work should refine or specialize the existing wizard capability, not replace it.
- `source/` remains ignored; staging corpus should stay local unless a separate tracking decision is approved.

## Next Step

Finish Batch 1, then implement Batch 2 by adding the canonical specialist file.

## Lessons Learned

- Dedicated wizard specialist must be represented in both raw skill source and graph context; graph alone is not enough.
- Existing broad wizard capability should be reused as parent/general capability to avoid duplication.
- `skill-change-detect` can still report `status=changed` after sync because raw working tree changes remain uncommitted; the meaningful closure evidence is sync/proposal generation plus federation verify success.
- Central graph proposals are written to `/Users/rim/Documents/GitHub/ai-codex-skill-graph`, while local runtime context/evidence is written under this repo's `graph/generated/mirai_graph`.

## Process Improvements

- For specialist creation, write the workflow before canonical raw source changes.
- Keep staging corpus and canonical condensed instructions separate.
- After adding a new specialist, immediately run `skill-graph-sync`; federation verify will otherwise report specialist promotion blockers.

## Skill/Federation Improvement Candidates

- Add a federation route fixture for "универсальный мастер", "universal master", "wizard packaging", "iblock archive export/import".
- Add future `sf4_wizard_audit.py` implementation once specialist source is accepted.
- Consider a canonical route scenario specifically for "создать универсальный мастер SF4 с упаковкой инфоблоков highload и оформлением" so the specialist capability is tested directly, not only through broad `sf4`.

## Follow-up Proposals

- Decide whether `source/wizard` should remain ignored or be promoted/partially unignored after canonical specialist integration.
- Decide whether to implement `scripts/sf4_wizard_audit.py` in a separate batch now that the specialist contract exists.

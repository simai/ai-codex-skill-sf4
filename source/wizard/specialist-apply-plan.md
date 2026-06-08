# Universal Wizard Specialist Apply Plan

This file describes how the staging corpus can be promoted into canonical SF4 skill sources after owner approval.

## Current Boundary

`source/wizard/*` is a staging corpus. It is ignored by the repository and should not be treated as canonical skill behavior until reviewed.

Canonical source writes are not allowed without owner-approved apply plan.

## Proposed Canonical Changes

### 1. Expand SF4 Wizard Reference

Target:

- `skills/sf4/references/wizard-actions.md`

Add:

- action contract table summary;
- long-running action patterns;
- packaging matrix summary;
- export/import archive notes;
- master creation checklist;
- validator checklist pointer.

Keep the detailed training corpus out of the reference unless it is reviewed and condensed.

### 2. Add Dedicated Specialist

Target:

- `skills/sf4/specialists/universal-wizard.md`

Purpose:

- separate role for creation, modification, packaging, visualization and audit of universal wizard masters;
- owned by `sf4`;
- companion boundaries:
  - `bitrix` for generic Bitrix module/marketplace rules;
  - `tester` for acceptance and smoke evidence;
  - `ops` for live/runtime/backup/rollback;
  - `docs` if large documentation publication is needed.

Suggested sections:

- role and scope;
- source-of-truth hierarchy;
- runtime model;
- action contract checklist;
- packaging checklist;
- visual contract checklist;
- export/import playbooks;
- read-only audit checklist;
- blockers and escalation.

### 3. Add Validator Script Proposal

Possible target:

- `scripts/sf4_wizard_audit.py`

Initial implementation scope:

- parse `.wizard.config.php` enough to inspect action entries;
- verify action resolution;
- verify deterministic payload paths;
- report side-effect risk;
- emit JSON.

Do not implement live execution or repair in the first version.

### 4. Update Skill Routing Note

Possible target:

- `skills/sf4/SKILL.md`

Minimal update only:

- add pointer from Wizard Actions section to the new specialist file;
- keep `SKILL.md` thin.

### 5. Graph/Federation Proposal

Possible targets:

- repo-local graph generated proposal or graph capability source, depending on current graph workflow;
- federation route fixtures if required by owner.

Intent:

- route "universal master", "wizard packaging", "iblock archive import/export", "master visual design" to `sf4` with `universal-wizard` specialist context.

Do not claim Mirai Graph integration until required gate passes:

```bash
python3 scripts/mirai_graph_contract_gate.py
```

## Required Gates Before Canonical Writes

1. Owner approval for source promotion.
2. Read current canonical files:
   - `skills/sf4/SKILL.md`;
   - `skills/sf4/references/wizard-actions.md`;
   - `skills/sf4/references/system-layer-simai.md`;
   - any existing `skills/sf4/specialists/*`.
3. Prepare exact patch plan.
4. Apply small patches.
5. Run:
   - `python3 scripts/mirai_graph_contract_gate.py`;
   - `scripts/skill-change-detect.sh` if available;
   - `scripts/skill-graph-sync.sh` if available and approved for the repo;
   - `scripts/federation-verify.sh` or central fallback;
   - `scripts/federation-route-check.sh` or central fallback.
6. Update workflow/evidence.

## Acceptance Criteria

- Specialist exists or canonical reference explicitly explains why a separate specialist is deferred.
- Wizard reference contains enough detail for:
  - master creation;
  - action modification;
  - data packaging;
  - iblock/HL archive export/import;
  - visual configuration;
  - read-only audit.
- No canonical source file duplicates bulky raw corpus unnecessarily.
- Route check sends universal wizard tasks to `sf4` or to `teamlead` with `sf4` as required owner fallback.
- All verification artifacts are recorded.

## Tracking Decision

`source/` is currently ignored by `.gitignore`.

Options:

1. Keep ignored:
   - good for private corpus and raw study notes;
   - bad for sharing specialist training material through the repo.
2. Add narrow `.gitignore` exception:
   - keep `/source/` ignored globally;
   - unignore `/source/wizard/**` if owner wants this corpus tracked.
3. Promote only condensed canonical files:
   - keep corpus ignored;
   - move reviewed knowledge into `skills/sf4/references` and `skills/sf4/specialists`.

Recommended default: keep `source/` ignored until the user approves what should become canonical. Then promote condensed content rather than tracking every study note.

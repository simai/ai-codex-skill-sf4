# SF4 Wizard Audit Validator

## Goal

Implement a read-only `scripts/sf4_wizard_audit.py` validator for SF4 universal wizard masters.

## Done When

- `scripts/sf4_wizard_audit.py` exists.
- The validator does not execute Bitrix, PHP wizard actions, DB writes, file copy/import actions or live mutations.
- It can inspect:
  - runtime master path;
  - standalone `.wizard.config.php`;
  - optional module root installer bridge.
- It reports:
  - master structure;
  - config shape;
  - action chain;
  - action resolution;
  - deterministic payload path checks;
  - zip readability checks;
  - inferred requirements;
  - side-effect/risk classification;
  - visual asset checks;
  - installer bridge signals.
- It emits JSON and readable summary.
- It is tested against real read-only examples:
  - `/Users/rim/Sites/sf4.test/simai/wizard/master/simai.sveden`;
  - `/Users/rim/Sites/test.test/bitrix/modules/simai.sf4biblio`;
  - `/Users/rim/Sites/test.test/bitrix/modules/simai.sf4med`;
  - missing-config case if useful.
- Workflow/evidence/Kaizen are updated.

## Route And Gates

Route:

- primary skill: `sf4`
- companions: `bitrix`, `tester`
- required gate: `platform_contract`
- process: `general_delivery`

Preflight evidence:

- `source/output/action-gates/action-gate-report-20260607120517.json`
- status: success
- blockers: none

## Workstreams

### A. Static Config Parser

Extract high-signal data from `.wizard.config.php` without executing PHP:

- description fields;
- action entries;
- action code/name/input/output;
- path-like parameter expressions;
- condition presence.

### B. Master Audit

Check:

- `index.php`;
- `.wizard.config.php`;
- `data/`;
- image assets;
- master-local action overrides.

### C. Action/Payload Audit

Check:

- master-local and global action resolution;
- missing action files;
- deterministic `source` path existence;
- archive readability;
- `DATA_INPUT_CODE` source chain;
- side-effect classification.

### D. Module Installer Bridge Audit

Check static signals in `install/index.php`:

- `CopyDirFiles`;
- `/simai/wizard/master`;
- `install/wizard/data`;
- `install/bitrix`, `install/ru/config`, `install/iblock`, `install/ru/php_interface`, `install/ru/root`, `install/ru/site`;
- `config.zip`, `medialibrary.zip`, `module/*.zip`;
- wrapper wizard copy;
- redirect to universal master.

### E. Verification

Run:

- `python3 -m py_compile scripts/sf4_wizard_audit.py`;
- real read-only audits;
- JSON validation of produced reports;
- `git diff --check`;
- applicable federation checks after raw script changes.

## Batches

### Batch 1 - Workflow And Inventory

Status: completed

Evidence:

- Current workflow file.
- Read `source/wizard/validator-spec.md`.
- Read `skills/sf4/specialists/universal-wizard.md`.
- Inspected existing script style under `skills/sf4/scripts/`.

### Batch 2 - Validator Implementation

Status: completed

Tasks:

- Add `scripts/sf4_wizard_audit.py`.
- Keep implementation read-only except optional JSON report output.

Evidence:

- `scripts/sf4_wizard_audit.py`
- `skills/sf4/SKILL.md` Scripts section points to the validator.
- `skills/sf4/specialists/universal-wizard.md` points to the implemented validator.
- `graph/specs/objects/capability-sf4-universal-wizard-specialist.json` includes the validator source ref.
- `source/wizard/validator-spec.md` now states the spec is implemented.

### Batch 3 - Real Source Verification

Status: completed

Tasks:

- Run validator against real masters/modules.
- Record reports under `source/output/wizard-audit/`.

Evidence:

- Runtime master audit:
  - command: `python3 scripts/sf4_wizard_audit.py --master /Users/rim/Sites/sf4.test/simai/wizard/master/simai.sveden --json source/output/wizard-audit/simai-sveden.json`
  - status: `ready`
  - actions: 19
  - missing actions: 0
  - missing payloads: 0
- Module bridge audits:
  - `source/output/wizard-audit/simai-sf4biblio-module.json`
  - `source/output/wizard-audit/simai-sf4med-module.json`
  - `source/output/wizard-audit/simai-sf4university-module.json`
- Missing config blocker audit:
  - `source/output/wizard-audit/simai-sf4university-missing-config.json`
  - status: `blocked`
  - finding codes: `missing_config`, `missing_master_config`

### Batch 4 - Final Gates And Kaizen

Status: completed

Tasks:

- Compile/check script.
- Run federation/skill checks as applicable.
- Update lessons and next steps.

Evidence:

- `python3 -m py_compile scripts/sf4_wizard_audit.py`: success.
- Real audits rerun successfully:
  - `simai-sveden.json`: status `ready`, actions `19`, missing actions `0`, missing payloads `0`.
  - `simai-sf4university-module.json`: status `ready`, installer bridge detects assembled `install/ru/*` payload signals.
  - `simai-sf4university-missing-config.json`: status `blocked`, expected missing config findings.
- JSON validation for `source/output/wizard-audit/*.json`: success.
- `git diff --check`: success.
- `/Users/rim/Documents/GitHub/ai-codex/scripts/skill-change-detect.sh --repo /Users/rim/Documents/GitHub/ai-codex-skill-sf4 --skill sf4 --json`: status `changed`; runtime script and specialist update detected; blockers none.
- `/Users/rim/Documents/GitHub/ai-codex/scripts/skill-graph-sync.sh --repo /Users/rim/Documents/GitHub/ai-codex-skill-sf4 --skill sf4 --task "реализовать read-only sf4_wizard_audit.py validator для SF4 universal wizard master" --json`: success.
- Generated graph evidence:
  - `graph/generated/mirai_graph/skill-source-changes/skill-graph-sync-sf4-20260607121255/skill-source-change-evidence.json`
  - `graph/generated/mirai_graph/skill-source-changes/skill-graph-sync-sf4-20260607121255/skill-graph-sync-report.json`
  - `graph/generated/mirai_graph/runtime-kit/skill-graph-sync-sf4-20260607121255-verify/runtime-kit-verify.json`
  - `graph/generated/mirai_graph/runtime-context/skill-graph-sync-sf4-20260607121255-context/context-pack.json`
- Central generated proposals:
  - `/Users/rim/Documents/GitHub/ai-codex-skill-graph/graph/generated/mirai_graph/federation-change/skill-graph-sync-sf4-20260607121255-federation-proposal/federation-change-proposal.json`
  - `/Users/rim/Documents/GitHub/ai-codex-skill-graph/graph/generated/mirai_graph/specialist-promotion/skill-graph-sync-sf4-20260607121255-specialist-sf4-universal-wizard/specialist-promotion-proposal.json`
- `/Users/rim/Documents/GitHub/ai-codex/scripts/federation-verify.sh --profile admin --no-write`: success, blockers none.
- `/Users/rim/Documents/GitHub/ai-codex/scripts/federation-route-check.sh --profile admin --json`: success, 64/64 passed.
- Route smoke for "проверить универсальный мастер SF4 через sf4_wizard_audit.py": primary `sf4`, companions `bitrix`, `tester`, confidence high.

Cleanup note:

- `python3 -m py_compile` created ignored `scripts/__pycache__/`.
- Cleanup command `rm -rf scripts/__pycache__` was blocked by SIMAI destructive safety hook because deletion lacks backup/approval. Left untouched; it is ignored and not part of deliverable.

## Lessons Learned

- Root `scripts/` currently contains Mirai runtime/gate scripts, while SF4 operational scripts mostly live under `skills/sf4/scripts/`; this validator is intentionally root-level because the agreed target path is `scripts/sf4_wizard_audit.py`.
- Static parsing must not strip `//...` line comments blindly because real configs can contain `https://...` strings.
- Static parser must preserve `#dir#`-style placeholders; they are runtime-dependent wizard values, not comments.
- Safety hooks can block cleanup of ignored generated files; do not bypass them. Record the ignored artifact and move on unless cleanup is required.

## Process Improvements

- Use static parsing for wizard configs first; live PHP include would require stubbing Bitrix/SF4 classes and increases risk.
- Include a missing-config fixture in validator checks because this is a known real-world wizard failure mode.

## Skill/Federation Improvement Candidates

- Add a future route/check fixture for read-only wizard audit tasks.

## Follow-up Proposals

- Add tests/fixtures for the static parser if the validator grows beyond current high-signal checks.
- Add explicit action-contract expansions for the next priority actions and reuse this validator output as evidence.

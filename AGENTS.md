# AGENTS.md

## Skill Routing

Работай на русском, если пользователь не переключился на другой язык.

Этот репозиторий содержит SIMAI skill. Domain skill остаётся владельцем своего
предметного смысла, source files, правил, references и acceptance gates.

`GrowGraph` используется как companion layer для структуры, связей,
adoption/readiness, semantic preservation, effectiveness и federation
contracts. Он не заменяет `SKILL.md`, `kernel/`, `rules/`, `activities/`,
`specialists/`, `knowledge-packs`, `references/` и `quality/`.

## GrowGraph Rules

- Не считать repo-local GrowGraph migration успешной только из-за валидного JSON.
- Не переписывать skill source files массово из generated artifacts.
- Generated candidates из `graph/generated/` не являются canonical truth.
- Domain ownership stays with the local skill; `$graph` owns graph structure and gates only.
- Canonical changes in `graph/specs/` require an apply plan, validation and a rollback path.
- If semantic preservation, effectiveness, federation export or integration review is missing, do not claim `GGA9`.

## Required Gate

Before claiming GrowGraph integration for this repository, run:

```bash
python3 scripts/growgraph_contract_gate.py
```

The GitHub workflow also runs this gate after ordinary repository checks.

## Current Repo-Local GrowGraph Scope

Current migration scope:

```text
skill:sf4
```

Canonical repo-local graph root:

```text
graph/
```

This repository is allowed to export a bounded federation contract after the
semantic and effectiveness gates pass.

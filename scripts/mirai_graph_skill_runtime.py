#!/usr/bin/env python3
"""Repo-local Mirai Graph Skill Runtime Kit wrapper."""

from __future__ import annotations

import os
import runpy
import sys
from pathlib import Path


def installed_kit_root() -> Path | None:
    marker = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))) / "simai-workspace" / "install.env"
    if not marker.is_file():
        return None
    for raw in marker.read_text(encoding="utf-8-sig").splitlines():
        key, separator, value = raw.partition("=")
        if separator and key.strip() == "KIT_ROOT":
            return Path(value.strip().strip("'\"")).expanduser()
    return None


def resolve_runtime() -> Path:
    explicit = os.environ.get("MIRAI_GRAPH_RUNTIME_KIT")
    repo = Path(__file__).resolve().parents[1]
    candidates = [Path(explicit).expanduser()] if explicit else []
    candidates.extend(
        [
            repo / "skills" / "graph" / "scripts" / "mirai_graph_skill_runtime.py",
            repo.parent / "ai-codex-skill-graph" / "skills" / "graph" / "scripts" / "mirai_graph_skill_runtime.py",
        ]
    )
    kit_root = installed_kit_root()
    if kit_root:
        candidates.append(
            kit_root.parent / "ai-codex-skill-graph" / "skills" / "graph" / "scripts" / "mirai_graph_skill_runtime.py"
        )
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    raise SystemExit("Mirai Graph runtime kit script not found in explicit, repository, sibling, or active runtime locations")


RUNTIME = resolve_runtime()
sys.argv = [str(RUNTIME), *sys.argv[1:]]
runpy.run_path(str(RUNTIME), run_name='__main__')

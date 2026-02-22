# SIMAI SF4 Skill

Skill for Codex to work with projects on SIMAI Framework 4 (SF4):
- audit SF4 project structure and links
- create and override blocks/views
- compose page grids from blocks
- work with config, properties, iblock/highloadblock flows
- remediate missing `view -> block` bindings

Repository layout:
- `SKILL.md`
- `agents/`
- `references/`
- `references/artifacts/`
- `scripts/`

Install target:
- macOS/Linux: `~/.codex/skills/simai-sf4`
- Windows: `%USERPROFILE%\.codex\skills\simai-sf4`

## 1) Install (macOS/Linux)

Copy:

```bash
SRC="/path/to/ai-codex-sf4skill"
DST="$HOME/.codex/skills/simai-sf4"
mkdir -p "$HOME/.codex/skills"
rm -rf "$DST"
cp -R "$SRC" "$DST"
```

Symlink (recommended for active development):

```bash
SRC="/path/to/ai-codex-sf4skill"
DST="$HOME/.codex/skills/simai-sf4"
mkdir -p "$HOME/.codex/skills"
rm -rf "$DST"
ln -s "$SRC" "$DST"
```

## 2) Install (Windows, PowerShell)

Copy:

```powershell
$src = "C:\path\to\ai-codex-sf4skill"
$dstRoot = "$env:USERPROFILE\.codex\skills"
$dst = "$dstRoot\simai-sf4"
New-Item -ItemType Directory -Force $dstRoot | Out-Null
if (Test-Path $dst) { Remove-Item -Recurse -Force $dst }
Copy-Item -Recurse -Force $src $dst
```

Symlink (recommended for active development, may require admin/developer mode):

```powershell
$src = "C:\path\to\ai-codex-sf4skill"
$dstRoot = "$env:USERPROFILE\.codex\skills"
$dst = "$dstRoot\simai-sf4"
New-Item -ItemType Directory -Force $dstRoot | Out-Null
if (Test-Path $dst) { Remove-Item -Recurse -Force $dst }
New-Item -ItemType SymbolicLink -Path $dst -Target $src
```

## 3) Restart Codex

After install/update, restart Codex so it reloads skills.

## 4) Verify install

Expected files:
- `~/.codex/skills/simai-sf4/SKILL.md`
- `~/.codex/skills/simai-sf4/references/`
- `~/.codex/skills/simai-sf4/scripts/`

Quick check:

```bash
python3 ~/.codex/skills/simai-sf4/scripts/sf4_project_audit.py --help
```

Windows:

```powershell
py "$env:USERPROFILE\.codex\skills\simai-sf4\scripts\sf4_project_audit.py" --help
```

## 5) How to use in prompts

Call explicitly:

```text
$simai-sf4 Audit project <project_root> for <site_dir>
$simai-sf4 Create block: section=home code=hero.banner
$simai-sf4 Create view: area=home code=modern
$simai-sf4 Build view->block report and remediate missing blocks in batches
```

## 6) Codex in VS Code

Yes, it works if VS Code Codex uses the same `CODEX_HOME`.

Important:
- For WSL/container/remote, install skill inside that environment too.
- If project policy uses skill whitelist in `AGENTS.md`, add `simai-sf4`.
- Restart Codex session in VS Code after install/update.

## 7) Typical SF4 flow

1. Run audit:
   `python3 scripts/sf4_project_audit.py --site-root <project_root> --site-dir <site_dir>`
2. Choose route (grid/block/view/config/data/wizard).
3. Change project layer only (`simai.data`) by default.
4. Validate syntax/runtime and clear cache.
5. For update/data tasks, prepare artifacts from `references/artifacts/`:
   - `migration-notes.md` (always)
   - `upgrade-notes.md`
   - `regression-checklist.md`
   - `qa-report.md` (for high-risk scope)

## 8) Update and rollback

Update:
- copy install: replace `~/.codex/skills/simai-sf4`
- symlink install: update repository files only

Rollback:
- remove `~/.codex/skills/simai-sf4`
- restart Codex

## 9) Troubleshooting

Skill not triggered:
- include `$simai-sf4` in prompt
- verify install in active environment
- restart Codex
- check skill whitelist in `AGENTS.md`

Scripts fail:
- verify Python 3
- verify `--site-root` and `--site-dir`
- verify write permissions for `simai.data` when using `--apply`

Unexpected project behavior:
- rerun audit with `--show-summary`
- export link report via `--link-report-json` and inspect missing references

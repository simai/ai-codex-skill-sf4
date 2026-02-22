#!/usr/bin/env python3
"""
Quick SF4 project audit.

Validate:
- simai.data discovery
- key config/template files
- grid_view_* mapping to existing view templates
- basic data hygiene checks in project layer
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


GRID_VIEW_PATHS = {
    "grid_view_header": ("grid", "view", "header"),
    "grid_view_footer": ("grid", "view", "footer"),
    "grid_view_home": ("grid", "view", "home"),
    "grid_view_sidebar_left": ("grid", "view", "sidebar", "left"),
    "grid_view_sidebar_right": ("grid", "view", "sidebar", "right"),
    "grid_view_main_top": ("grid", "view", "main", "top"),
    "grid_view_main_bottom": ("grid", "view", "main", "bottom"),
}

BLOCK_SECTION_PATTERN = re.compile(r"""['"]BLOCK_SECTION['"]\s*=>\s*['"]([^'"]+)['"]""")
AREA_TEMPLATE_PATTERN = re.compile(
    r"""['"]ROW_\d+_COL_\d+_AREA_\d+_TEMPLATE['"]\s*=>\s*['"]([^'"]+)['"]"""
)
PROPERTY_KEY_PATTERN = re.compile(r"""'([^']+)'\s*=>""")
PROPERTY_STRING_PATTERN = re.compile(r"""'([^']+)'\s*=>\s*'([^']*)'""")
SECRET_KEY_PATTERN = re.compile(
    r"""(secret|token|password|passwd|private[_-]?key|api[_-]?.*secret)""",
    re.IGNORECASE,
)

ARCHIVE_PATTERNS = ("*.zip", "*.tar", "*.tar.gz", "*.tgz", "*.rar", "*.7z")
MANIFEST_NAMES = (
    "composer.json",
    "package.json",
    "package-lock.json",
    "yarn.lock",
    "pnpm-lock.yaml",
)


@dataclass
class Check:
    key: str
    ok: bool
    detail: str
    required: bool


@dataclass
class LinkRecord:
    simai_data: str
    view_template: str
    block_section: str
    block_code: str
    project_template: str
    system_template: str
    project_exists: bool
    system_exists: bool
    status: str


def normalize_site_dir(raw: str) -> str:
    value = raw.strip()
    if not value:
        return "/"
    if not value.startswith("/"):
        value = "/" + value
    if value != "/":
        value = value.rstrip("/")
    return value


def walk_simai_data(root: Path) -> List[Path]:
    skip = {
        ".git",
        ".idea",
        ".vscode",
        "node_modules",
        "vendor",
        "upload",
        "tmp",
        "logs",
        "cache",
        "managed_cache",
        "stack_cache",
    }
    found: List[Path] = []
    for current, dirs, _ in os.walk(root, topdown=True):
        dirs[:] = [d for d in dirs if d not in skip]
        if os.path.basename(current) == "simai.data":
            found.append(Path(current))
            dirs[:] = []
    return sorted(set(found))


def is_packaged_copy(path: Path) -> bool:
    normalized = path.as_posix()
    package_markers = [
        "/bitrix/modules/",
        "/local/modules/",
        "/public_backup/",
        "/wizard/master/",
    ]
    return any(marker in normalized for marker in package_markers)


def parse_grid_views(site_property_file: Path) -> Dict[str, str]:
    text = site_property_file.read_text(encoding="utf-8", errors="ignore")
    pairs = re.findall(r"'(grid_view_[a-z_]+)'\s*=>\s*'([^']*)'", text)
    return {k: v for k, v in pairs}


def infer_block_section(view_template: Path, data_dir: Path) -> str:
    try:
        rel = view_template.relative_to(data_dir)
    except ValueError:
        return ""

    parts = rel.parts
    # Expected: grid/view/<area>/<code>/template.php
    if len(parts) < 5 or parts[0] != "grid" or parts[1] != "view":
        return ""

    area_root = parts[2]
    mapping = {
        "header": "header",
        "footer": "footer",
        "home": "home",
        "sidebar": "sidebar",
        "main": "main",
    }
    return mapping.get(area_root, "")


def parse_view_templates(view_template: Path, data_dir: Path) -> Tuple[str, List[str]]:
    text = view_template.read_text(encoding="utf-8", errors="ignore")

    section_match = BLOCK_SECTION_PATTERN.search(text)
    if section_match:
        block_section = section_match.group(1).strip()
    else:
        block_section = infer_block_section(view_template, data_dir)

    templates = sorted({m.strip() for m in AREA_TEMPLATE_PATTERN.findall(text) if m.strip()})
    return block_section, templates


def rel_from_root(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def sample_paths(paths: List[Path], root: Path, limit: int = 5) -> str:
    if not paths:
        return "-"
    return ", ".join(rel_from_root(p, root) for p in paths[:limit])


def required_paths(data_dir: Path) -> Iterable[Tuple[str, Path]]:
    return [
        ("site_property", data_dir / ".site.property.php"),
        ("site_config", data_dir / "config" / ".site.config.php"),
        ("structure_config", data_dir / "config" / ".structure.config.php"),
        ("template_entry", data_dir / "template" / "template.php"),
        ("template_property", data_dir / "template" / "property.php"),
        ("template_style", data_dir / "template" / "style.php"),
        ("template_js", data_dir / "template" / "js.php"),
        ("template_panel", data_dir / "template" / "panel.php"),
    ]


def recommended_paths(data_dir: Path) -> Iterable[Tuple[str, Path]]:
    return [
        ("iblock_config", data_dir / "config" / ".iblock.config.php"),
        ("iblock_section_config", data_dir / "config" / ".iblock.section.config.php"),
        ("view_header_selector", data_dir / "template" / "area" / "header" / "template.php"),
        ("view_footer_selector", data_dir / "template" / "area" / "footer" / "template.php"),
        ("view_main_top_selector", data_dir / "template" / "area" / "main" / "top" / "template.php"),
        (
            "view_main_bottom_selector",
            data_dir / "template" / "area" / "main" / "bottom" / "template.php",
        ),
    ]


def check_data_hygiene(data_dir: Path, root: Path) -> List[Check]:
    checks: List[Check] = []

    site_property = data_dir / ".site.property.php"
    if site_property.exists():
        text = site_property.read_text(encoding="utf-8", errors="ignore")

        key_hits: Dict[str, int] = {}
        for key in PROPERTY_KEY_PATTERN.findall(text):
            key_hits[key] = key_hits.get(key, 0) + 1
        duplicates = sorted((k, c) for k, c in key_hits.items() if c > 1)
        if duplicates:
            sample = ", ".join(f"{k}x{c}" for k, c in duplicates[:8])
            checks.append(
                Check(
                    key="site_property_duplicates",
                    ok=False,
                    detail=f"duplicate keys in .site.property.php: {sample}",
                    required=False,
                )
            )
        else:
            checks.append(
                Check(
                    key="site_property_duplicates",
                    ok=True,
                    detail="no duplicate keys detected in .site.property.php",
                    required=False,
                )
            )

        secret_like_non_empty: List[str] = []
        for key, value in PROPERTY_STRING_PATTERN.findall(text):
            if SECRET_KEY_PATTERN.search(key) and value.strip():
                if value.strip().lower() not in {"<secret>", "<redacted>", "***"}:
                    secret_like_non_empty.append(key)
        if secret_like_non_empty:
            unique_keys = sorted(set(secret_like_non_empty))
            sample = ", ".join(unique_keys[:8])
            checks.append(
                Check(
                    key="site_property_secret_like",
                    ok=False,
                    detail=(
                        "secret-like keys with non-empty literal values in .site.property.php: "
                        f"{sample}"
                    ),
                    required=False,
                )
            )
        else:
            checks.append(
                Check(
                    key="site_property_secret_like",
                    ok=True,
                    detail="no non-empty literal values detected for secret-like keys in .site.property.php",
                    required=False,
                )
            )

    block_root = data_dir / "grid" / "block"
    if block_root.exists():
        archives: List[Path] = []
        for pattern in ARCHIVE_PATTERNS:
            archives.extend(sorted(block_root.rglob(pattern)))
        cache_dirs = sorted([p for p in block_root.rglob("cache") if p.is_dir()])
        manifests: List[Path] = []
        for name in MANIFEST_NAMES:
            manifests.extend(sorted(block_root.rglob(name)))

        if archives or cache_dirs or manifests:
            details: List[str] = []
            if archives:
                details.append(
                    f"archives={len(archives)} sample: {sample_paths(archives, root)}"
                )
            if cache_dirs:
                details.append(
                    f"cache_dirs={len(cache_dirs)} sample: {sample_paths(cache_dirs, root)}"
                )
            if manifests:
                details.append(
                    f"manifests={len(manifests)} sample: {sample_paths(manifests, root)}"
                )
            checks.append(
                Check(
                    key="block_hygiene",
                    ok=False,
                    detail="block dir hygiene warnings: " + " | ".join(details),
                    required=False,
                )
            )
        else:
            checks.append(
                Check(
                    key="block_hygiene",
                    ok=True,
                    detail="no archives/cache dirs/vendor manifests detected under grid/block",
                    required=False,
                )
            )

    return checks


def check_view_block_links(data_dir: Path, root: Path) -> Tuple[List[Check], List[LinkRecord]]:
    checks: List[Check] = []
    records: List[LinkRecord] = []
    view_root = data_dir / "grid" / "view"
    project_block_root = data_dir / "grid" / "block"
    system_block_root = root / "simai" / "block"
    simai_data_rel = rel_from_root(data_dir, root)

    if not view_root.exists():
        checks.append(
            Check(
                key="view_block_links",
                ok=False,
                detail=f"view root missing ({view_root})",
                required=False,
            )
        )
        return checks, records

    views = sorted(view_root.glob("**/template.php"))
    checks.append(
        Check(
            key="view_template_count",
            ok=True,
            detail=f"view templates discovered: {len(views)}",
            required=False,
        )
    )

    missing: List[Tuple[str, str, str]] = []
    unresolved_section: List[str] = []

    for view_template in views:
        block_section, area_templates = parse_view_templates(view_template, data_dir)
        view_rel = rel_from_root(view_template, root)

        if not block_section:
            unresolved_section.append(view_rel)
            records.append(
                LinkRecord(
                    simai_data=simai_data_rel,
                    view_template=view_rel,
                    block_section="",
                    block_code="",
                    project_template="",
                    system_template="",
                    project_exists=False,
                    system_exists=False,
                    status="unknown_section",
                )
            )
            continue

        for code in area_templates:
            project_file = project_block_root / block_section / code / "template.php"
            system_file = system_block_root / block_section / code / "template.php"
            project_exists = project_file.exists()
            system_exists = system_file.exists()
            status = "ok" if (project_exists or system_exists) else "missing"
            records.append(
                LinkRecord(
                    simai_data=simai_data_rel,
                    view_template=view_rel,
                    block_section=block_section,
                    block_code=code,
                    project_template=rel_from_root(project_file, root),
                    system_template=rel_from_root(system_file, root),
                    project_exists=project_exists,
                    system_exists=system_exists,
                    status=status,
                )
            )
            if status == "missing":
                missing.append((view_rel, block_section, code))

    if unresolved_section:
        sample = ", ".join(unresolved_section[:5])
        checks.append(
            Check(
                key="view_block_section_detection",
                ok=False,
                detail=(
                    f"could not detect BLOCK_SECTION in {len(unresolved_section)} view files. "
                    f"Sample: {sample}"
                ),
                required=False,
            )
        )

    if missing:
        sample = "; ".join(
            f"{view} -> {section}/{code}" for view, section, code in missing[:10]
        )
        checks.append(
            Check(
                key="view_block_links",
                ok=False,
                detail=(
                    f"missing block templates for {len(missing)} area references. "
                    f"Sample: {sample}"
                ),
                required=False,
            )
        )
    else:
        checks.append(
            Check(
                key="view_block_links",
                ok=True,
                detail="all parsed area templates resolve to project or system block templates",
                required=False,
            )
        )

    return checks, records


def evaluate_data_dir(
    data_dir: Path, root: Path, check_links: bool
) -> Tuple[List[Check], int, List[LinkRecord]]:
    checks: List[Check] = []
    records: List[LinkRecord] = []
    hard_failures = 0

    for key, path in required_paths(data_dir):
        ok = path.exists()
        checks.append(
            Check(
                key=key,
                ok=ok,
                detail=f"{key}: {'found' if ok else 'missing'} ({rel_from_root(path, root)})",
                required=True,
            )
        )
        if not ok:
            hard_failures += 1

    for key, path in recommended_paths(data_dir):
        ok = path.exists()
        checks.append(
            Check(
                key=key,
                ok=ok,
                detail=f"{key}: {'found' if ok else 'missing'} ({rel_from_root(path, root)})",
                required=False,
            )
        )

    checks.extend(check_data_hygiene(data_dir, root))

    site_property = data_dir / ".site.property.php"
    if not site_property.exists():
        return checks, hard_failures, records

    view_values = parse_grid_views(site_property)
    if not view_values:
        checks.append(
            Check(
                key="grid_view_keys",
                ok=False,
                detail="No grid_view_* keys parsed from .site.property.php",
                required=False,
            )
        )

    for key, base_parts in GRID_VIEW_PATHS.items():
        value = view_values.get(key, "")
        if not value:
            checks.append(
                Check(
                    key=f"{key}_value",
                    ok=False,
                    detail=f"{key}: empty or missing in .site.property.php",
                    required=False,
                )
            )
            continue

        view_template = data_dir.joinpath(*base_parts, value, "template.php")
        ok = view_template.exists()
        checks.append(
            Check(
                key=f"{key}_template",
                ok=ok,
                detail=f"{key}='{value}' -> {'found' if ok else 'missing'} ({rel_from_root(view_template, root)})",
                required=False,
            )
        )

    if check_links:
        link_checks, link_records = check_view_block_links(data_dir, root)
        checks.extend(link_checks)
        records.extend(link_records)

    return checks, hard_failures, records


def select_data_dirs(root: Path, site_dir: str | None, include_packages: bool) -> List[Path]:
    if site_dir:
        normalized = normalize_site_dir(site_dir)
        candidate = root / normalized.lstrip("/") / "simai.data"
        return [candidate] if candidate.exists() else []
    paths = walk_simai_data(root)
    if include_packages:
        return paths
    return [p for p in paths if not is_packaged_copy(p)]


def summarize_links_by_simai_data(records: List[LinkRecord]) -> Dict[str, Dict[str, object]]:
    summary: Dict[str, Dict[str, object]] = {}
    for rec in records:
        bucket = summary.setdefault(
            rec.simai_data,
            {
                "total": 0,
                "ok": 0,
                "missing": 0,
                "unknown_section": 0,
                "missing_by_section": {},
            },
        )
        bucket["total"] = int(bucket["total"]) + 1
        if rec.status == "ok":
            bucket["ok"] = int(bucket["ok"]) + 1
        elif rec.status == "missing":
            bucket["missing"] = int(bucket["missing"]) + 1
            missing_by_section = bucket["missing_by_section"]
            if isinstance(missing_by_section, dict):
                missing_by_section[rec.block_section] = int(missing_by_section.get(rec.block_section, 0)) + 1
        elif rec.status == "unknown_section":
            bucket["unknown_section"] = int(bucket["unknown_section"]) + 1
    return summary


def format_missing_sections(missing_by_section: Dict[str, int], limit: int = 10) -> str:
    if not missing_by_section:
        return "-"
    ordered = sorted(missing_by_section.items(), key=lambda item: (-item[1], item[0]))
    return ", ".join(f"{section}:{count}" for section, count in ordered[:limit])


def print_human_report(
    root: Path,
    reports: List[Tuple[Path, List[Check]]],
    only_issues: bool,
    link_records: List[LinkRecord],
    show_summary: bool,
) -> None:
    print(f"SF4 audit root: {root}")
    summary_by_data = summarize_links_by_simai_data(link_records)
    for data_dir, checks in reports:
        print("")
        print(f"== simai.data: {data_dir}")
        for check in checks:
            level = "OK" if check.ok else ("FAIL" if check.required else "WARN")
            if only_issues and level == "OK":
                continue
            print(f"[{level}] {check.detail}")
        if show_summary:
            rel_key = rel_from_root(data_dir, root)
            summary = summary_by_data.get(rel_key)
            if summary:
                print(
                    "[SUMMARY] "
                    f"links total={summary['total']}, "
                    f"ok={summary['ok']}, "
                    f"missing={summary['missing']}, "
                    f"unknown_section={summary['unknown_section']}"
                )
                missing_by_section = summary["missing_by_section"]
                if isinstance(missing_by_section, dict):
                    print(
                        "[SUMMARY] "
                        f"missing_by_section: {format_missing_sections(missing_by_section)}"
                    )


def print_json_report(
    root: Path,
    reports: List[Tuple[Path, List[Check]]],
    link_records: List[LinkRecord],
) -> None:
    summary_by_data = summarize_links_by_simai_data(link_records)
    payload = {
        "root": str(root),
        "reports": [
            {
                "simai_data": str(data_dir),
                "checks": [
                    {
                        "key": c.key,
                        "ok": c.ok,
                        "required": c.required,
                        "detail": c.detail,
                    }
                    for c in checks
                ],
                "link_summary": summary_by_data.get(rel_from_root(data_dir, root), {}),
            }
            for data_dir, checks in reports
        ],
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def write_link_reports(
    json_path: str | None,
    csv_path: str | None,
    records: List[LinkRecord],
) -> None:
    if json_path:
        target_json = Path(json_path).expanduser().resolve()
        target_json.parent.mkdir(parents=True, exist_ok=True)
        payload = [
            {
                "simai_data": r.simai_data,
                "view_template": r.view_template,
                "block_section": r.block_section,
                "block_code": r.block_code,
                "project_template": r.project_template,
                "system_template": r.system_template,
                "project_exists": r.project_exists,
                "system_exists": r.system_exists,
                "status": r.status,
            }
            for r in records
        ]
        target_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"link report json: {target_json}")

    if csv_path:
        target_csv = Path(csv_path).expanduser().resolve()
        target_csv.parent.mkdir(parents=True, exist_ok=True)
        with target_csv.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=[
                    "simai_data",
                    "view_template",
                    "block_section",
                    "block_code",
                    "project_template",
                    "system_template",
                    "project_exists",
                    "system_exists",
                    "status",
                ],
            )
            writer.writeheader()
            for r in records:
                writer.writerow(
                    {
                        "simai_data": r.simai_data,
                        "view_template": r.view_template,
                        "block_section": r.block_section,
                        "block_code": r.block_code,
                        "project_template": r.project_template,
                        "system_template": r.system_template,
                        "project_exists": r.project_exists,
                        "system_exists": r.system_exists,
                        "status": r.status,
                    }
                )
        print(f"link report csv: {target_csv}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit SIMAI SF4 project structure.")
    parser.add_argument("--site-root", default=".", help="Project root to scan.")
    parser.add_argument(
        "--site-dir",
        default=None,
        help="Optional site dir (example: /ru). If set, audit only that site_dir/simai.data.",
    )
    parser.add_argument(
        "--include-packages",
        action="store_true",
        help="Include install/backup/module package copies of simai.data.",
    )
    parser.add_argument(
        "--no-view-block-links",
        action="store_true",
        help="Skip view->block linkage checks.",
    )
    parser.add_argument(
        "--only-issues",
        action="store_true",
        help="Print only FAIL/WARN checks in human-readable mode.",
    )
    parser.add_argument(
        "--show-summary",
        action="store_true",
        help="Print aggregated view->block summary in human-readable mode.",
    )
    parser.add_argument(
        "--link-report-json",
        default=None,
        help="Write full view->block linkage records to JSON file.",
    )
    parser.add_argument(
        "--link-report-csv",
        default=None,
        help="Write full view->block linkage records to CSV file.",
    )
    parser.add_argument("--json", action="store_true", help="Print JSON report.")
    args = parser.parse_args()

    root = Path(args.site_root).resolve()
    if not root.exists():
        print(f"Root does not exist: {root}", file=sys.stderr)
        return 2

    data_dirs = select_data_dirs(root, args.site_dir, args.include_packages)
    if not data_dirs:
        print("No simai.data directories found.", file=sys.stderr)
        return 2

    reports: List[Tuple[Path, List[Check]]] = []
    link_records_all: List[LinkRecord] = []
    hard_failures = 0
    for data_dir in data_dirs:
        checks, failures, link_records = evaluate_data_dir(
            data_dir,
            root,
            check_links=not args.no_view_block_links,
        )
        reports.append((data_dir, checks))
        link_records_all.extend(link_records)
        hard_failures += failures

    if args.json:
        print_json_report(root, reports, link_records_all)
    else:
        print_human_report(
            root,
            reports,
            only_issues=args.only_issues,
            link_records=link_records_all,
            show_summary=args.show_summary,
        )

    if args.link_report_json or args.link_report_csv:
        write_link_reports(args.link_report_json, args.link_report_csv, link_records_all)

    return 1 if hard_failures > 0 else 0


if __name__ == "__main__":
    raise SystemExit(main())

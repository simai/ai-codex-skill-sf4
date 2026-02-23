#!/usr/bin/env python3
"""
Scan SF4 project templates for interactive markup markers and asset usage.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Pattern, Set


ASSET_LOAD_PATTERN = re.compile(
    r"""(?:SIMAI\\Main\\Page\\)?Asset::getInstance\(\)->load\(\s*['"]([^'"]+)['"]\s*\)"""
)
ASSET_ADDJS_PATTERN = re.compile(
    r"""(?:SIMAI\\Main\\Page\\)?Asset::getInstance\(\)->addJs\(\s*['"]([^'"]+)['"]\s*\)"""
)
ASSET_ADDCSS_PATTERN = re.compile(
    r"""(?:SIMAI\\Main\\Page\\)?Asset::getInstance\(\)->addCss\(\s*['"]([^'"]+)['"]\s*\)"""
)

MARKER_PATTERNS: Dict[str, Pattern[str]] = {
    "sf_modal_attr": re.compile(r"\bsf-modal\b"),
    "sf_src_attr": re.compile(r"\bsf-src\b"),
    "dropdown_toggle": re.compile(r"""data-toggle\s*=\s*['"]dropdown['"]"""),
    "modal_toggle": re.compile(r"""data-toggle\s*=\s*['"]modal['"]"""),
    "tooltip_toggle": re.compile(r"""data-toggle\s*=\s*['"]tooltip['"]"""),
    "popover_toggle": re.compile(r"""data-toggle\s*=\s*['"]popover['"]"""),
    "inputmask_attr": re.compile(r"\bdata-inputmask(?:-[a-z-]+)?\s*="),
    "swiper_container": re.compile(r"\bswiper-container\b"),
    "swiper_init": re.compile(r"\bnew\s+Swiper\s*\("),
    "fancybox": re.compile(r"\bfancybox\b"),
    "inputmask_init": re.compile(r"\.inputmask\s*\("),
    "aria_attr": re.compile(r"\baria-[a-z-]+\s*="),
    "sr_only": re.compile(r"\bsr-only\b"),
    "tabindex": re.compile(r"\btabindex\s*="),
    "role_group": re.compile(r"""role\s*=\s*['"]group['"]"""),
    "include_component": re.compile(r"\$APPLICATION->IncludeComponent\s*\("),
}


def normalize_site_dir(raw: str) -> str:
    value = raw.strip()
    if not value:
        return "/"
    if not value.startswith("/"):
        value = "/" + value
    if value != "/":
        value = value.rstrip("/")
    return value


def rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def collect_files(data_dir: Path, include_all_php: bool) -> List[Path]:
    targets: Set[Path] = set()
    if include_all_php:
        for path in data_dir.rglob("*.php"):
            if path.is_file():
                targets.add(path)
    else:
        patterns = [
            "grid/block/**/template.php",
            "grid/view/**/template.php",
            "template/area/**/template.php",
        ]
        for pattern in patterns:
            for path in data_dir.glob(pattern):
                if path.is_file():
                    targets.add(path)
    return sorted(targets)


def print_counter(counter: Counter[str], title: str, top: int) -> None:
    print(f"\n{title}:")
    shown = 0
    for key, count in counter.most_common(top):
        shown += 1
        print(f"  {count:6d}  {key}")
    if shown == 0:
        print("  -")


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit SF4 interactive markup markers and assets.")
    parser.add_argument("--site-root", required=True, help="Project root path")
    parser.add_argument("--site-dir", required=True, help="Site dir, e.g. /ru")
    parser.add_argument(
        "--include-all-php",
        action="store_true",
        help="Scan all *.php files in simai.data (default: template.php targets only)",
    )
    parser.add_argument("--top", type=int, default=50, help="How many top entries to show (default: 50)")
    parser.add_argument(
        "--marker",
        dest="markers",
        action="append",
        default=[],
        help="Show detailed usage for marker key; can be repeated",
    )
    parser.add_argument(
        "--show-lines-limit",
        type=int,
        default=40,
        help="Max lines to print per --marker (default: 40)",
    )
    parser.add_argument("--json-out", default=None, help="Optional path for JSON report")
    args = parser.parse_args()

    site_root = Path(args.site_root).resolve()
    if not site_root.exists():
        print(f"Site root does not exist: {site_root}", file=sys.stderr)
        return 2

    site_dir = normalize_site_dir(args.site_dir)
    data_dir = site_root / site_dir.lstrip("/") / "simai.data"
    if not data_dir.exists():
        print(f"simai.data not found: {data_dir}", file=sys.stderr)
        return 2

    files = collect_files(data_dir, args.include_all_php)
    if not files:
        print("No files found for scan.", file=sys.stderr)
        return 1

    for marker in args.markers:
        if marker not in MARKER_PATTERNS:
            available = ", ".join(sorted(MARKER_PATTERNS.keys()))
            print(f"Unknown marker '{marker}'. Available: {available}", file=sys.stderr)
            return 2

    marker_counts: Counter[str] = Counter()
    marker_files: Dict[str, Set[str]] = defaultdict(set)
    marker_lines: Dict[str, List[str]] = defaultdict(list)

    asset_loads: Counter[str] = Counter()
    asset_addjs: Counter[str] = Counter()
    asset_addcss: Counter[str] = Counter()

    for file_path in files:
        text = file_path.read_text(encoding="utf-8", errors="ignore")
        rel_path = rel(file_path, site_root)

        for name in ASSET_LOAD_PATTERN.findall(text):
            asset_loads[name] += 1
        for path in ASSET_ADDJS_PATTERN.findall(text):
            asset_addjs[path] += 1
        for path in ASSET_ADDCSS_PATTERN.findall(text):
            asset_addcss[path] += 1

        for line_no, line in enumerate(text.splitlines(), start=1):
            for marker, pattern in MARKER_PATTERNS.items():
                matches = pattern.findall(line)
                if not matches:
                    continue
                marker_counts[marker] += len(matches)
                marker_files[marker].add(rel_path)
                if args.markers and marker in args.markers and len(marker_lines[marker]) < args.show_lines_limit:
                    snippet = line.strip()
                    if len(snippet) > 180:
                        snippet = snippet[:177] + "..."
                    marker_lines[marker].append(f"{rel_path}:{line_no}: {snippet}")

    print("SF4 Interactive Audit")
    print(f"Site root: {site_root}")
    print(f"Site dir: {site_dir}")
    print(f"simai.data: {data_dir}")
    print(f"Scanned files: {len(files)}")
    print(f"Marker keys: {len(MARKER_PATTERNS)}")

    print("\nInteractive markers:")
    shown = 0
    for marker, count in marker_counts.most_common(args.top):
        shown += 1
        file_count = len(marker_files.get(marker, set()))
        print(f"  {count:6d}  {marker}  (files: {file_count})")
    if shown == 0:
        print("  -")

    print_counter(asset_loads, "Asset::load(...)", args.top)
    print_counter(asset_addjs, "Asset::addJs(...)", args.top)
    print_counter(asset_addcss, "Asset::addCss(...)", args.top)

    if args.markers:
        for marker in args.markers:
            print(f"\nMarker details: {marker}")
            lines = marker_lines.get(marker, [])
            if not lines:
                print("  -")
                continue
            for item in lines:
                print(f"  {item}")

    if args.json_out:
        report = {
            "site_root": str(site_root),
            "site_dir": site_dir,
            "simai_data": str(data_dir),
            "scanned_files_count": len(files),
            "markers": [
                {
                    "marker": marker,
                    "count": marker_counts.get(marker, 0),
                    "files": len(marker_files.get(marker, set())),
                }
                for marker in sorted(MARKER_PATTERNS.keys())
            ],
            "asset_load": [{"name": name, "count": cnt} for name, cnt in asset_loads.most_common()],
            "asset_addjs": [{"path": path, "count": cnt} for path, cnt in asset_addjs.most_common()],
            "asset_addcss": [{"path": path, "count": cnt} for path, cnt in asset_addcss.most_common()],
            "marker_lines": {k: v for k, v in marker_lines.items()},
        }
        out_path = Path(args.json_out).resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\n[OK] JSON report written: {out_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""
Scan SF4 project PHP files for common backend integration risks.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Pattern, Set


CHECK_PATTERNS: Dict[str, Pattern[str]] = {
    "domcontentloaded": re.compile(r"DOMContentLoaded"),
    "block_edit_overlay": re.compile(r"Block\\Edit::add[A-Za-z]+Area\s*\("),
    "position_relative": re.compile(r"\bposition-relative\b"),
    "iblock_siteid_concat": re.compile(
        r"""IBLOCK_(?:TYPE|CODE)\s*['"]?\s*=>[^\n\r]*SITE_ID|sf[_-]\s*['"]?\s*\.\s*SITE_ID""",
        re.IGNORECASE,
    ),
    "asset_addjs_addcss": re.compile(r"Asset::getInstance\(\)->(?:addJs|addCss)\s*\("),
    "asset_load": re.compile(r"(?:SIMAI\\Main\\Page\\)?Asset::getInstance\(\)->load\s*\("),
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
            "grid/block/**/*.php",
            "grid/view/**/*.php",
            "template/**/*.php",
            "config/**/*.php",
            ".site.property.php",
            ".site.config.php",
            ".structure.config.php",
        ]
        for pattern in patterns:
            for path in data_dir.glob(pattern):
                if path.is_file():
                    targets.add(path)
    return sorted(targets)


def add_line(
    bucket: Dict[str, List[str]],
    key: str,
    item: str,
    limit: int,
) -> None:
    if len(bucket[key]) < limit:
        bucket[key].append(item)


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan SF4 project for backend integration risks.")
    parser.add_argument("--site-root", required=True, help="Project root path")
    parser.add_argument("--site-dir", required=True, help="Site dir, e.g. /ru")
    parser.add_argument(
        "--include-all-php",
        action="store_true",
        help="Scan all *.php files under simai.data (default: high-signal subsets)",
    )
    parser.add_argument(
        "--show-lines-limit",
        type=int,
        default=40,
        help="Max findings lines to print per check (default: 40)",
    )
    parser.add_argument("--json-out", default=None, help="Optional JSON output path")
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

    files = collect_files(data_dir, include_all_php=args.include_all_php)
    if not files:
        print("No files found for scan.", file=sys.stderr)
        return 1

    check_lines: Dict[str, List[str]] = defaultdict(list)
    check_files: Dict[str, Set[str]] = defaultdict(set)
    check_counts: Dict[str, int] = defaultdict(int)

    for file_path in files:
        text = file_path.read_text(encoding="utf-8", errors="ignore")
        rel_path = rel(file_path, site_root)
        has_block_edit = False
        has_position_relative = False

        if CHECK_PATTERNS["block_edit_overlay"].search(text):
            has_block_edit = True
            check_files["block_edit_overlay"].add(rel_path)
            check_counts["block_edit_overlay"] += len(
                CHECK_PATTERNS["block_edit_overlay"].findall(text)
            )

        if CHECK_PATTERNS["position_relative"].search(text):
            has_position_relative = True
            check_files["position_relative"].add(rel_path)
            check_counts["position_relative"] += len(
                CHECK_PATTERNS["position_relative"].findall(text)
            )

        if has_block_edit and not has_position_relative:
            check_files["block_edit_without_position_relative"].add(rel_path)
            check_counts["block_edit_without_position_relative"] += 1
            add_line(
                check_lines,
                "block_edit_without_position_relative",
                f"{rel_path}: contains Block\\Edit::add*Area but no position-relative marker",
                args.show_lines_limit,
            )

        for line_no, line in enumerate(text.splitlines(), start=1):
            for key in ("domcontentloaded", "iblock_siteid_concat", "asset_addjs_addcss", "asset_load"):
                pattern = CHECK_PATTERNS[key]
                matches = pattern.findall(line)
                if not matches:
                    continue
                check_counts[key] += len(matches)
                check_files[key].add(rel_path)
                snippet = line.strip()
                if len(snippet) > 180:
                    snippet = snippet[:177] + "..."
                add_line(
                    check_lines,
                    key,
                    f"{rel_path}:{line_no}: {snippet}",
                    args.show_lines_limit,
                )

    print("SF4 Backend Risk Scan")
    print(f"Site root: {site_root}")
    print(f"Site dir: {site_dir}")
    print(f"simai.data: {data_dir}")
    print(f"Scanned files: {len(files)}")

    ordered_checks = [
        "iblock_siteid_concat",
        "domcontentloaded",
        "block_edit_without_position_relative",
        "asset_addjs_addcss",
        "asset_load",
    ]

    print("\nSummary:")
    for key in ordered_checks:
        count = check_counts.get(key, 0)
        files_count = len(check_files.get(key, set()))
        print(f"  {key:36s}  count={count:4d}  files={files_count:3d}")

    print("\nDetails:")
    for key in ordered_checks:
        print(f"\n{key}:")
        lines = check_lines.get(key, [])
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
            "checks": [
                {
                    "check": key,
                    "count": check_counts.get(key, 0),
                    "files": len(check_files.get(key, set())),
                    "lines": check_lines.get(key, []),
                }
                for key in ordered_checks
            ],
        }
        out_path = Path(args.json_out).resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\n[OK] JSON report written: {out_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

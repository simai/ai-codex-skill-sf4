#!/usr/bin/env python3
"""
Scan SF4 templates and summarize CSS class usage.

Primary purpose:
- quickly find existing class patterns in project layer before markup refactoring.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Set, Tuple


CLASS_ATTR_PATTERN = re.compile(r"""class\s*=\s*(['"])(.*?)\1""", re.IGNORECASE | re.DOTALL)
TOKEN_SPLIT_PATTERN = re.compile(r"\s+")
VALID_CLASS_PATTERN = re.compile(r"^[A-Za-z0-9_-]+(?::[A-Za-z0-9_-]+)?$")

UTILITY_PREFIXES = (
    "m-",
    "mx-",
    "my-",
    "mt-",
    "mb-",
    "ml-",
    "mr-",
    "p-",
    "px-",
    "py-",
    "pt-",
    "pb-",
    "pl-",
    "pr-",
    "w-",
    "h-",
    "d-",
    "align-",
    "justify-",
    "text-",
    "bg-",
    "border-",
    "rounded",
    "shadow",
    "position-",
    "z-",
)


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


def class_group(token: str) -> str:
    if token.startswith("sf-"):
        return "sf"
    if token.startswith("t-"):
        return "typography"
    if token.startswith("theme-"):
        return "theme"
    if token.startswith("c-"):
        return "color"
    if token == "row" or token.startswith("col-") or token in {"container", "container-fluid"}:
        return "grid"
    if token.startswith(UTILITY_PREFIXES):
        return "utility"
    return "other"


def extract_tokens(text: str) -> Tuple[List[str], int, int]:
    tokens: List[str] = []
    class_attr_count = 0
    skipped_dynamic = 0

    for _, raw in CLASS_ATTR_PATTERN.findall(text):
        class_attr_count += 1
        for token in TOKEN_SPLIT_PATTERN.split(raw.strip()):
            token = token.strip()
            if not token:
                continue
            if not VALID_CLASS_PATTERN.fullmatch(token):
                skipped_dynamic += 1
                continue
            tokens.append(token)

    return tokens, class_attr_count, skipped_dynamic


def print_top(
    counter: Counter[str],
    title: str,
    top: int,
    min_count: int,
    with_files: Dict[str, Set[str]] | None = None,
) -> None:
    print(f"\n{title}:")
    shown = 0
    for cls, cnt in counter.most_common():
        if cnt < min_count:
            continue
        shown += 1
        if with_files is None:
            print(f"  {cnt:6d}  {cls}")
        else:
            file_cnt = len(with_files.get(cls, set()))
            print(f"  {cnt:6d}  {cls}  (files: {file_cnt})")
        if shown >= top:
            break
    if shown == 0:
        print("  -")


def main() -> int:
    parser = argparse.ArgumentParser(description="Inventory CSS classes used in SF4 project templates.")
    parser.add_argument("--site-root", required=True, help="Project root path")
    parser.add_argument("--site-dir", required=True, help="Site dir, e.g. /ru")
    parser.add_argument(
        "--include-all-php",
        action="store_true",
        help="Scan all *.php files in simai.data (default: template.php targets only)",
    )
    parser.add_argument("--top", type=int, default=60, help="How many top classes to print (default: 60)")
    parser.add_argument(
        "--min-count",
        type=int,
        default=1,
        help="Show classes with count >= min-count (default: 1)",
    )
    parser.add_argument(
        "--class",
        dest="classes",
        action="append",
        default=[],
        help="Inspect specific class usage; can be passed multiple times",
    )
    parser.add_argument(
        "--show-files-limit",
        type=int,
        default=30,
        help="Limit listed files per --class (default: 30)",
    )
    parser.add_argument(
        "--json-out",
        default=None,
        help="Optional path to write machine-readable JSON report",
    )
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
        print("No target files found for scan.", file=sys.stderr)
        return 1

    class_counter: Counter[str] = Counter()
    group_counter: Counter[str] = Counter()
    class_to_files: Dict[str, Set[str]] = defaultdict(set)
    total_class_attrs = 0
    skipped_dynamic_tokens = 0

    for path in files:
        text = path.read_text(encoding="utf-8", errors="ignore")
        tokens, attr_count, skipped_dynamic = extract_tokens(text)
        total_class_attrs += attr_count
        skipped_dynamic_tokens += skipped_dynamic

        rel_path = rel(path, site_root)
        for token in tokens:
            class_counter[token] += 1
            group_counter[class_group(token)] += 1
            class_to_files[token].add(rel_path)

    total_tokens = sum(class_counter.values())
    unique_classes = len(class_counter)

    print("SF4 Markup Inventory")
    print(f"Site root: {site_root}")
    print(f"Site dir: {site_dir}")
    print(f"simai.data: {data_dir}")
    print(f"Scanned files: {len(files)}")
    print(f"Class attributes found: {total_class_attrs}")
    print(f"Class tokens (valid): {total_tokens}")
    print(f"Unique classes: {unique_classes}")
    print(f"Skipped dynamic/invalid tokens: {skipped_dynamic_tokens}")

    print_top(class_counter, "Top classes", args.top, args.min_count, with_files=class_to_files)
    print_top(group_counter, "Class groups", 20, 1)

    if args.classes:
        for token in args.classes:
            print(f"\nClass lookup: {token}")
            count = class_counter.get(token, 0)
            file_list = sorted(class_to_files.get(token, set()))
            print(f"  occurrences: {count}")
            print(f"  files: {len(file_list)}")
            for item in file_list[: args.show_files_limit]:
                print(f"    - {item}")
            if len(file_list) > args.show_files_limit:
                print(f"    ... and {len(file_list) - args.show_files_limit} more")

    if args.json_out:
        report = {
            "site_root": str(site_root),
            "site_dir": site_dir,
            "simai_data": str(data_dir),
            "scanned_files": [rel(p, site_root) for p in files],
            "metrics": {
                "file_count": len(files),
                "class_attribute_count": total_class_attrs,
                "class_token_count": total_tokens,
                "unique_class_count": unique_classes,
                "skipped_dynamic_tokens": skipped_dynamic_tokens,
            },
            "top_classes": [
                {"class": cls, "count": cnt, "files": len(class_to_files.get(cls, set()))}
                for cls, cnt in class_counter.most_common(args.top)
                if cnt >= args.min_count
            ],
            "group_counts": [{"group": g, "count": c} for g, c in group_counter.most_common()],
            "class_lookup": {
                token: sorted(class_to_files.get(token, set())) for token in args.classes
            },
        }
        out_path = Path(args.json_out).resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\n[OK] JSON report written: {out_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

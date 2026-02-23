#!/usr/bin/env python3
"""
Map component usage in site pages and resolve where templates are actually loaded from.

Primary purpose:
- for component-heavy SF4 pages, quickly locate the correct template file to edit.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple


INCLUDE_COMPONENT_RE = re.compile(
    r"""IncludeComponent\s*\(\s*(?P<q>['\"])(?P<component>[^'\"]+)(?P=q)\s*,\s*(?:(?P<tq>['\"])(?P<template>[^'\"]*)(?P=tq)|(?P<template_expr>[^,\)\n]+))""",
    re.S,
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


def strip_php_comments(text: str) -> str:
    out: List[str] = []
    i = 0
    n = len(text)
    in_single = False
    in_double = False

    while i < n:
        ch = text[i]
        nxt = text[i + 1] if i + 1 < n else ""

        if in_single:
            out.append(ch)
            if ch == "\\" and i + 1 < n:
                out.append(text[i + 1])
                i += 2
                continue
            if ch == "'":
                in_single = False
            i += 1
            continue

        if in_double:
            out.append(ch)
            if ch == "\\" and i + 1 < n:
                out.append(text[i + 1])
                i += 2
                continue
            if ch == '"':
                in_double = False
            i += 1
            continue

        if ch == "'":
            in_single = True
            out.append(ch)
            i += 1
            continue

        if ch == '"':
            in_double = True
            out.append(ch)
            i += 1
            continue

        if ch == "/" and nxt == "*":
            i += 2
            while i < n:
                if text[i] == "*" and (i + 1) < n and text[i + 1] == "/":
                    i += 2
                    break
                if text[i] == "\n":
                    out.append("\n")
                i += 1
            continue

        if (ch == "/" and nxt == "/") or ch == "#":
            i += 2 if ch == "/" else 1
            while i < n and text[i] != "\n":
                i += 1
            continue

        out.append(ch)
        i += 1

    return "".join(out)


def collect_files(site_root: Path, site_dir: str, include_all_php: bool) -> List[Path]:
    site_dir_path = site_root / site_dir.lstrip("/") if site_dir != "/" else site_root
    if not site_dir_path.exists():
        return []

    files: List[Path] = []

    if include_all_php:
        for path in sorted(site_dir_path.rglob("*.php")):
            if path.is_file():
                files.append(path)
        return files

    # Default: page-level PHP files under site dir, excluding simai.data internals.
    simai_data = site_dir_path / "simai.data"
    for path in sorted(site_dir_path.rglob("*.php")):
        if not path.is_file():
            continue
        if simai_data in path.parents:
            continue
        files.append(path)

    return files


def parse_template_literal(raw_template: str) -> str:
    value = raw_template.strip()
    if value == "":
        return ".default"
    return value


def template_candidates(
    site_root: Path,
    vendor: str,
    component_name: str,
    template_name: str,
) -> List[Tuple[str, Path]]:
    local_override = (
        site_root
        / "local"
        / "templates"
        / "simai.framework"
        / "components"
        / vendor
        / component_name
        / template_name
        / "template.php"
    )
    local_component = (
        site_root
        / "local"
        / "components"
        / vendor
        / component_name
        / "templates"
        / template_name
        / "template.php"
    )
    bitrix_component = (
        site_root
        / "bitrix"
        / "components"
        / vendor
        / component_name
        / "templates"
        / template_name
        / "template.php"
    )

    return [
        ("local_override", local_override),
        ("local_component_source", local_component),
        ("bitrix_component_source", bitrix_component),
    ]


def resolve_template(
    site_root: Path,
    component: str,
    template: str,
    template_is_dynamic: bool,
) -> Tuple[str, Optional[str], Optional[str]]:
    if template_is_dynamic:
        return "dynamic_template", None, None

    if ":" not in component:
        return "unknown_component_format", None, None

    vendor, component_name = component.split(":", 1)

    for source_type, path in template_candidates(site_root, vendor, component_name, template):
        if path.exists():
            return source_type, rel(path, site_root), None

    fallback_path: Optional[str] = None
    for _, candidate in template_candidates(site_root, vendor, component_name, ".default"):
        if candidate.exists():
            fallback_path = rel(candidate, site_root)
            break

    if fallback_path:
        return "unresolved_with_default_fallback", None, fallback_path

    return "unresolved", None, None


def build_report(site_root: Path, site_dir: str, include_all_php: bool) -> Dict[str, object]:
    files = collect_files(site_root, site_dir, include_all_php=include_all_php)
    if not files:
        raise FileNotFoundError("No PHP files found for scan")

    records: List[Dict[str, object]] = []

    component_counter: Counter[str] = Counter()
    component_template_counter: Counter[str] = Counter()
    resolve_counter: Counter[str] = Counter()
    unresolved_counter: Counter[str] = Counter()

    pages_with_components = 0

    for path in files:
        text = path.read_text(encoding="utf-8", errors="ignore")
        text = strip_php_comments(text)

        matches = list(INCLUDE_COMPONENT_RE.finditer(text))
        if not matches:
            continue

        pages_with_components += 1
        page_rel = rel(path, site_root)

        for match in matches:
            component = match.group("component").strip()
            template_literal = match.group("template")
            template_expr = match.group("template_expr")

            template_is_dynamic = template_literal is None
            template_expr_clean = ""
            if template_is_dynamic and template_expr is not None:
                template_expr_clean = re.sub(r"\s+", " ", template_expr.strip())[:120]

            template = parse_template_literal(template_literal if template_literal is not None else "")

            source_type, resolved_template_path, fallback_template_path = resolve_template(
                site_root=site_root,
                component=component,
                template=template,
                template_is_dynamic=template_is_dynamic,
            )

            rec = {
                "page": page_rel,
                "component": component,
                "template": template,
                "template_is_dynamic": template_is_dynamic,
                "template_expr": template_expr_clean,
                "resolved_source": source_type,
                "resolved_template_path": resolved_template_path,
                "fallback_template_path": fallback_template_path,
            }
            records.append(rec)

            component_counter[component] += 1
            component_template_counter[f"{component}::{template}"] += 1
            resolve_counter[source_type] += 1

            if source_type in {
                "unresolved",
                "unresolved_with_default_fallback",
                "dynamic_template",
            }:
                unresolved_counter[f"{component}::{template}"] += 1

    return {
        "site_root": str(site_root),
        "site_dir": site_dir,
        "scan_mode": "all_php" if include_all_php else "page_php_excluding_simai_data",
        "scanned_files_count": len(files),
        "pages_with_components_count": pages_with_components,
        "records_count": len(records),
        "records": records,
        "summary": {
            "component_counts": dict(component_counter.most_common()),
            "component_template_counts": dict(component_template_counter.most_common()),
            "resolved_source_counts": dict(resolve_counter.most_common()),
            "unresolved_component_templates": dict(unresolved_counter.most_common()),
        },
    }


def print_human(report: Dict[str, object], top: int, component_filters: List[str]) -> None:
    print("SF4 Component Template Map")
    print(f"Site root: {report['site_root']}")
    print(f"Site dir: {report['site_dir']}")
    print(f"Scan mode: {report['scan_mode']}")
    print(f"Scanned files: {report['scanned_files_count']}")
    print(f"Pages with components: {report['pages_with_components_count']}")
    print(f"IncludeComponent records: {report['records_count']}")

    comp_counts: Dict[str, int] = report["summary"]["component_counts"]
    source_counts: Dict[str, int] = report["summary"]["resolved_source_counts"]

    print("\nTop components:")
    shown = 0
    for comp, cnt in comp_counts.items():
        print(f"  {cnt:5d}  {comp}")
        shown += 1
        if shown >= top:
            break
    if shown == 0:
        print("  -")

    print("\nResolved source types:")
    if source_counts:
        for src, cnt in source_counts.items():
            print(f"  {cnt:5d}  {src}")
    else:
        print("  -")

    unresolved = report["summary"]["unresolved_component_templates"]
    print("\nTop unresolved/dynamic component templates:")
    if unresolved:
        shown = 0
        for key, cnt in unresolved.items():
            print(f"  {cnt:5d}  {key}")
            shown += 1
            if shown >= top:
                break
    else:
        print("  -")

    if component_filters:
        print("\nComponent details:")
        records: List[Dict[str, object]] = report["records"]
        for comp in component_filters:
            print(f"\n  {comp}")
            filtered = [r for r in records if r["component"] == comp]
            print(f"    records: {len(filtered)}")
            combos: Counter[str] = Counter(f"{r['template']} ({r['resolved_source']})" for r in filtered)
            for combo, cnt in combos.most_common(top):
                print(f"      {cnt:4d}  {combo}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Map component usage and template resolution for SF4 component-heavy pages."
    )
    parser.add_argument("--site-root", required=True, help="Project root path")
    parser.add_argument("--site-dir", required=True, help="Site dir, e.g. /ru")
    parser.add_argument(
        "--include-all-php",
        action="store_true",
        help="Scan all PHP files under site dir (default scans page PHP excluding simai.data)",
    )
    parser.add_argument("--top", type=int, default=40, help="How many top entries to show")
    parser.add_argument(
        "--component",
        dest="components",
        action="append",
        default=[],
        help="Show details for selected component; can be repeated",
    )
    parser.add_argument("--json", action="store_true", help="Print JSON to stdout")
    parser.add_argument("--json-out", default=None, help="Write JSON report to file")
    args = parser.parse_args()

    site_root = Path(args.site_root).resolve()
    if not site_root.exists():
        print(f"Site root does not exist: {site_root}", file=sys.stderr)
        return 2

    site_dir = normalize_site_dir(args.site_dir)

    try:
        report = build_report(site_root=site_root, site_dir=site_dir, include_all_php=args.include_all_php)
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print_human(report, top=args.top, component_filters=args.components)

    if args.json_out:
        out = Path(args.json_out).resolve()
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\n[OK] JSON report written: {out}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

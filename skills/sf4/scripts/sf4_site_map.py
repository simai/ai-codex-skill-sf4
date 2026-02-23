#!/usr/bin/env python3
"""
Build a practical SF4 site map:
- active grid views
- key blocks from active views
- .property.php layout/view overrides
- top-level page component signals
- direct simai:sf.grid pages outside simai.data
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Dict, List


GRID_VIEW_KEYS = [
    "grid_view_header",
    "grid_view_footer",
    "grid_view_home",
    "grid_view_main_top",
    "grid_view_main_bottom",
    "grid_view_sidebar_left",
    "grid_view_sidebar_right",
]

GRID_VIEW_TO_PATH = {
    "grid_view_header": ("grid", "view", "header"),
    "grid_view_footer": ("grid", "view", "footer"),
    "grid_view_home": ("grid", "view", "home"),
    "grid_view_main_top": ("grid", "view", "main", "top"),
    "grid_view_main_bottom": ("grid", "view", "main", "bottom"),
    "grid_view_sidebar_left": ("grid", "view", "sidebar", "left"),
    "grid_view_sidebar_right": ("grid", "view", "sidebar", "right"),
}

OVERRIDE_KEYS = [
    "grid_view_header",
    "grid_view_footer",
    "grid_view_home",
    "grid_view_main_top",
    "grid_view_main_bottom",
    "grid_view_sidebar_left",
    "grid_view_sidebar_right",
    "sidebar_show",
    "show_title",
    "show_breadcrumb",
    "layout_sidebar_type",
]

PROPERTY_PAIR_RE = re.compile(r"""['"]([a-zA-Z0-9_\\-]+)['"]\s*=>\s*['"]([^'"]*)['"]""")
BLOCK_SECTION_RE = re.compile(r"""['"]BLOCK_SECTION['"]\s*=>\s*['"]([^'"]+)['"]""")
ROW_AREA_TEMPLATE_RE = re.compile(
    r"""['"]ROW_[^'"]*_AREA_[0-9]+_TEMPLATE['"]\s*=>\s*['"]([^'"]+)['"]"""
)
INCLUDE_COMPONENT_RE = re.compile(r"""IncludeComponent\s*\(\s*["']([^"']+)["']""", re.S)


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


def parse_php_string_map(path: Path) -> Dict[str, str]:
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8", errors="ignore")
    text = strip_php_comments(text)
    out: Dict[str, str] = {}
    for key, val in PROPERTY_PAIR_RE.findall(text):
        out[key] = val
    return out


def parse_active_views(site_property_file: Path) -> Dict[str, str]:
    pairs = parse_php_string_map(site_property_file)
    out: Dict[str, str] = {}
    for key in GRID_VIEW_KEYS:
        value = pairs.get(key)
        if value:
            out[key] = value
    return out


def build_active_view_templates(
    simai_data_dir: Path, active_views: Dict[str, str], site_root: Path
) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for key in GRID_VIEW_KEYS:
        code = active_views.get(key)
        if not code:
            continue
        view_path = simai_data_dir.joinpath(*GRID_VIEW_TO_PATH[key], code, "template.php")
        entry: Dict[str, object] = {
            "property": key,
            "code": code,
            "template_path": rel(view_path, site_root),
            "exists": view_path.exists(),
            "block_section": "",
            "key_blocks": [],
            "key_blocks_count": 0,
        }
        if view_path.exists():
            text = view_path.read_text(encoding="utf-8", errors="ignore")
            section_match = BLOCK_SECTION_RE.search(text)
            if section_match:
                entry["block_section"] = section_match.group(1).strip()
            blocks = sorted({x.strip() for x in ROW_AREA_TEMPLATE_RE.findall(text) if x.strip()})
            entry["key_blocks"] = blocks
            entry["key_blocks_count"] = len(blocks)
        rows.append(entry)
    return rows


def collect_property_overrides(site_dir_path: Path, site_root: Path) -> List[Dict[str, object]]:
    results: List[Dict[str, object]] = []
    for prop in sorted(site_dir_path.rglob(".property.php")):
        pairs = parse_php_string_map(prop)
        filtered = {k: pairs[k] for k in OVERRIDE_KEYS if k in pairs}
        if not filtered:
            continue
        results.append(
            {
                "file": rel(prop, site_root),
                "values": filtered,
            }
        )
    return results


def extract_components(path: Path) -> List[str]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    text = strip_php_comments(text)
    return [x.strip() for x in INCLUDE_COMPONENT_RE.findall(text) if x.strip()]


def collect_top_level_index_components(site_dir_path: Path, site_root: Path) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    index_paths: List[Path] = []

    root_index = site_dir_path / "index.php"
    if root_index.exists():
        index_paths.append(root_index)

    for child in sorted(site_dir_path.iterdir()):
        if not child.is_dir():
            continue
        index_file = child / "index.php"
        if index_file.exists():
            index_paths.append(index_file)

    for index_path in index_paths:
        components = extract_components(index_path)
        sf_components = [x for x in components if x.startswith("simai:sf.")]
        bitrix_components = [x for x in components if x.startswith("bitrix:")]
        rows.append(
            {
                "file": rel(index_path, site_root),
                "components": components,
                "sf_components": sf_components,
                "bitrix_components": bitrix_components,
            }
        )
    return rows


def collect_direct_sf_grid_pages(site_dir_path: Path, simai_data_dir: Path, site_root: Path) -> List[str]:
    pages: List[str] = []
    for php_file in sorted(site_dir_path.rglob("*.php")):
        if simai_data_dir in php_file.parents:
            continue
        components = extract_components(php_file)
        if "simai:sf.grid" in components:
            pages.append(rel(php_file, site_root))
    return pages


def build_component_counters(top_level_rows: List[Dict[str, object]]) -> Dict[str, Dict[str, int]]:
    sf_counter: Counter[str] = Counter()
    bx_counter: Counter[str] = Counter()

    for row in top_level_rows:
        for comp in row.get("sf_components", []):
            sf_counter[comp] += 1
        for comp in row.get("bitrix_components", []):
            bx_counter[comp] += 1

    return {
        "sf": dict(sf_counter.most_common()),
        "bitrix": dict(bx_counter.most_common()),
    }


def build_report(site_root: Path, site_dir: str) -> Dict[str, object]:
    site_dir_rel = site_dir.lstrip("/")
    site_dir_path = site_root / site_dir_rel if site_dir_rel else site_root
    simai_data_dir = site_dir_path / "simai.data"
    site_property_file = simai_data_dir / ".site.property.php"

    if not site_dir_path.exists():
        raise FileNotFoundError(f"site dir does not exist: {site_dir_path}")
    if not simai_data_dir.exists():
        raise FileNotFoundError(f"simai.data not found: {simai_data_dir}")
    if not site_property_file.exists():
        raise FileNotFoundError(f".site.property.php not found: {site_property_file}")

    active_views = parse_active_views(site_property_file)
    active_view_templates = build_active_view_templates(simai_data_dir, active_views, site_root)
    property_overrides = collect_property_overrides(site_dir_path, site_root)
    top_level_indexes = collect_top_level_index_components(site_dir_path, site_root)
    direct_sf_grid_pages = collect_direct_sf_grid_pages(site_dir_path, simai_data_dir, site_root)
    component_counters = build_component_counters(top_level_indexes)

    return {
        "site_root": str(site_root),
        "site_dir": site_dir,
        "simai_data": rel(simai_data_dir, site_root),
        "active_views": active_views,
        "active_view_templates": active_view_templates,
        "property_overrides": property_overrides,
        "top_level_indexes": top_level_indexes,
        "top_level_component_counters": component_counters,
        "direct_sf_grid_pages": direct_sf_grid_pages,
        "stats": {
            "top_level_indexes_count": len(top_level_indexes),
            "property_overrides_count": len(property_overrides),
            "direct_sf_grid_pages_count": len(direct_sf_grid_pages),
        },
    }


def print_human(report: Dict[str, object]) -> None:
    print("SF4 Site Map")
    print(f"Site root: {report['site_root']}")
    print(f"Site dir: {report['site_dir']}")
    print(f"simai.data: {report['simai_data']}")
    print()

    print("Active grid views:")
    active_views = report["active_views"]
    for key in GRID_VIEW_KEYS:
        value = active_views.get(key)
        if value:
            print(f"  {key}: {value}")
    print()

    print("Active view templates and key blocks:")
    for row in report["active_view_templates"]:
        status = "OK" if row["exists"] else "MISSING"
        section = row["block_section"] if row["block_section"] else "-"
        print(
            f"  [{status}] {row['property']}={row['code']} section={section} "
            f"blocks={row['key_blocks_count']} file={row['template_path']}"
        )
    print()

    print("Top-level component usage (index.php at site root and first-level sections):")
    sf_counter = report["top_level_component_counters"]["sf"]
    bx_counter = report["top_level_component_counters"]["bitrix"]
    if sf_counter:
        print("  simai:sf.*")
        for comp, cnt in sf_counter.items():
            print(f"    {cnt:>3}  {comp}")
    else:
        print("  simai:sf.* : none")
    if bx_counter:
        print("  bitrix:*")
        for comp, cnt in bx_counter.items():
            print(f"    {cnt:>3}  {comp}")
    else:
        print("  bitrix:* : none")
    print()

    print("Property override files (subset with layout/view keys):")
    print(f"  count: {report['stats']['property_overrides_count']}")
    for item in report["property_overrides"][:20]:
        keys = ", ".join(f"{k}={v}" for k, v in item["values"].items())
        print(f"  - {item['file']}: {keys}")
    if report["stats"]["property_overrides_count"] > 20:
        print("  ...")
    print()

    print("Direct simai:sf.grid pages outside simai.data:")
    if report["direct_sf_grid_pages"]:
        for path in report["direct_sf_grid_pages"]:
            print(f"  - {path}")
    else:
        print("  - none")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build SF4 site map with page/view/block signals.")
    parser.add_argument("--site-root", required=True, help="Project root path")
    parser.add_argument("--site-dir", required=True, help="Site dir, e.g. /ru")
    parser.add_argument("--json-out", help="Optional path for JSON report")
    parser.add_argument("--json", action="store_true", help="Print JSON report to stdout")
    return parser


def main(argv: List[str]) -> int:
    args = build_parser().parse_args(argv)
    site_root = Path(args.site_root).resolve()
    site_dir = normalize_site_dir(args.site_dir)

    try:
        report = build_report(site_root=site_root, site_dir=site_dir)
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print_human(report)

    if args.json_out:
        out = Path(args.json_out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

#!/usr/bin/env python3
"""
Create an SF4 view scaffold in simai.data/grid/view.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


AREA_TO_BLOCK_SECTION = {
    "header": "header",
    "footer": "footer",
    "home": "home",
    "sidebar/left": "sidebar",
    "sidebar/right": "sidebar",
    "main/top": "main",
    "main/bottom": "main",
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


def validate_area(area: str) -> str:
    value = area.strip().lower().rstrip("/")
    if value not in AREA_TO_BLOCK_SECTION:
        allowed = ", ".join(sorted(AREA_TO_BLOCK_SECTION.keys()))
        raise ValueError(f"Unsupported area '{value}'. Allowed: {allowed}")
    return value


def validate_code(code: str) -> str:
    value = code.strip()
    if not re.fullmatch(r"[A-Za-z0-9._-]+", value):
        raise ValueError("View code must match [A-Za-z0-9._-]+")
    return value


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def write_file(path: Path, content: str, dry_run: bool, force: bool) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"File exists: {path}")
    if dry_run:
        print(f"[DRY-RUN] write {path}")
        return
    ensure_parent(path)
    path.write_text(content, encoding="utf-8")
    print(f"[OK] wrote {path}")


def build_view_template(block_section: str, area_template: str) -> str:
    return f"""<?
if(!defined("B_PROLOG_INCLUDED") || B_PROLOG_INCLUDED!==true)die();

$APPLICATION->IncludeComponent(
\t"simai:sf.grid",
\t".default",
\tarray(
\t\t"COMPONENT_TEMPLATE" => ".default",
\t\t"BLOCK_SECTION" => "{block_section}",
\t\t"EXPERT_MODE" => "Y",
\t\t"ROW_COUNT" => "1",
\t\t"ROW_ORDER" => "0",
\t\t"ROW_0_NAME" => "Row 0",
\t\t"ROW_0_ACTIVE" => "Y",
\t\t"ROW_0_USE_CONTAINER" => "Y",
\t\t"ROW_0_USE_CONDITION" => "N",
\t\t"ROW_0_COL_COUNT" => "1",
\t\t"ROW_0_COL_0_AREA_COUNT" => "1",
\t\t"ROW_0_COL_0_AREA_0_TEMPLATE" => "{area_template}",
\t\t"ROW_0_COL_0_AREA_0_MODIFIER" => "",
\t\t"ANIMATE_MODE" => "N",
\t\t"USE_BACKGROUND" => "N",
\t\t"COMPOSITE_FRAME_MODE" => "A",
\t\t"COMPOSITE_FRAME_TYPE" => "AUTO",
\t),
\tfalse
);
?>
"""


def build_description_php() -> str:
    return """<?
if (!defined("B_PROLOG_INCLUDED") || B_PROLOG_INCLUDED!==true) die();

use Bitrix\\Main\\Localization\\Loc;
Loc::loadMessages(__FILE__);

$nameTemplate = strtoupper(basename(__DIR__));

return array(
\t"NAME" => Loc::getMessage("SF_GRID__" . $nameTemplate . "__NAME"),
\t"DESCRIPTION" => Loc::getMessage("SF_GRID__" . $nameTemplate . "__DESCRIPTION"),
\t"SORT" => 100,
\t"VERSION" => "1.0.0",
);
?>
"""


def build_lang_description(msg_key: str, name: str, description: str) -> str:
    return (
        "<?\n"
        f'$MESS["SF_GRID__{msg_key}__NAME"] = "{name}";\n'
        f'$MESS["SF_GRID__{msg_key}__DESCRIPTION"] = "{description}";\n'
        "?>\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Create SF4 view scaffold.")
    parser.add_argument("--site-root", required=True, help="Project root, e.g. /var/www/site")
    parser.add_argument("--site-dir", required=True, help="Site dir, e.g. /ru")
    parser.add_argument(
        "--area",
        required=True,
        help="View area: header, footer, home, sidebar/left, sidebar/right, main/top, main/bottom",
    )
    parser.add_argument("--code", required=True, help="View code, e.g. default, 010, promo")
    parser.add_argument(
        "--area-template",
        default="empty",
        help="Default block code for ROW_0_COL_0_AREA_0_TEMPLATE (default: empty)",
    )
    parser.add_argument("--name", default=None, help="View display name")
    parser.add_argument("--description", default=None, help="View description")
    parser.add_argument("--lang", default="ru", help="Language folder name, default: ru")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without writing")
    args = parser.parse_args()

    try:
        area = validate_area(args.area)
        code = validate_code(args.code)
    except ValueError as exc:
        print(f"Validation error: {exc}", file=sys.stderr)
        return 2

    site_root = Path(args.site_root).resolve()
    if not site_root.exists():
        print(f"Site root does not exist: {site_root}", file=sys.stderr)
        return 2

    site_dir = normalize_site_dir(args.site_dir)
    data_dir = site_root / site_dir.lstrip("/") / "simai.data"
    view_dir = data_dir / "grid" / "view" / area / code
    lang_dir = view_dir / "lang" / args.lang

    block_section = AREA_TO_BLOCK_SECTION[area]
    msg_key = code.upper()
    view_name = args.name or f"{area}:{code}"
    view_description = args.description or f"SF4 view scaffold for {area}/{code}"

    files = {
        view_dir / "template.php": build_view_template(block_section, args.area_template),
        view_dir / ".description.php": build_description_php(),
        lang_dir / ".description.php": build_lang_description(msg_key, view_name, view_description),
    }

    print(f"Target view dir: {view_dir}")
    if not data_dir.exists():
        print(f"Warning: simai.data dir not found yet: {data_dir}")
    if args.dry_run:
        print("[DRY-RUN] no files will be written")

    try:
        for path, content in files.items():
            write_file(path, content, dry_run=args.dry_run, force=args.force)
    except FileExistsError as exc:
        print(str(exc), file=sys.stderr)
        print("Use --force to overwrite existing files.", file=sys.stderr)
        return 1

    if args.dry_run:
        print("[DRY-RUN] completed")
    else:
        print("[OK] view scaffold created")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())


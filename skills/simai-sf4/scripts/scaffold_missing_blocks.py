#!/usr/bin/env python3
"""
Scaffold missing SF4 blocks from view->block linkage report JSON.

Default mode is dry-run. Use --apply to write files.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple


def normalize_site_dir(raw: str) -> str:
    value = raw.strip()
    if not value:
        return "/"
    if not value.startswith("/"):
        value = "/" + value
    if value != "/":
        value = value.rstrip("/")
    return value


def valid_section(value: str) -> bool:
    return bool(re.fullmatch(r"[a-z0-9_-]+", value))


def valid_code(value: str) -> bool:
    return bool(re.fullmatch(r"[a-z0-9._-]+", value))


def build_template_php() -> str:
    return """<?
if(!defined("B_PROLOG_INCLUDED") || B_PROLOG_INCLUDED!==true)die();

$nameTemplate = strtoupper(basename(__DIR__));
?>

<div class="<?=htmlspecialcharsbx($arBlockProperty[$nameTemplate . "__WRAP_MODIFIER"])?>">
\t<?=htmlspecialcharsBack($arBlockProperty[$nameTemplate . "__TEXT"])?>
</div>
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


def build_parameters_php() -> str:
    return """<?
use Bitrix\\Main\\Localization\\Loc;
Loc::loadMessages(__FILE__);

$nameTemplate = strtoupper(basename(__DIR__));

return array(
\t$nameTemplate . "__TEXT" => array(
\t\t"NAME" => Loc::getMessage("SF_GRID__" . $nameTemplate . "__TEXT"),
\t\t"TYPE" => "STRING",
\t\t"DEFAULT" => "",
\t),
\t$nameTemplate . "__WRAP_MODIFIER" => array(
\t\t"NAME" => Loc::getMessage("SF_GRID__" . $nameTemplate . "__WRAP_MODIFIER"),
\t\t"TYPE" => "STRING",
\t\t"DEFAULT" => "",
\t),
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


def build_lang_parameters(msg_key: str) -> str:
    return (
        "<?\n"
        f'$MESS["SF_GRID__{msg_key}__TEXT"] = "Text";\n'
        f'$MESS["SF_GRID__{msg_key}__WRAP_MODIFIER"] = "Wrap modifier";\n'
        "?>\n"
    )


def write_file(path: Path, content: str, apply: bool, force: bool) -> Tuple[bool, str]:
    if path.exists() and not force:
        return False, f"skip exists: {path}"
    if not apply:
        return True, f"dry-run write: {path}"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True, f"wrote: {path}"


def load_report(path: Path) -> List[Dict[str, object]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("Expected JSON array of linkage records.")
    return data


def main() -> int:
    parser = argparse.ArgumentParser(description="Scaffold missing SF4 blocks from linkage report.")
    parser.add_argument("--site-root", required=True, help="Project root, e.g. /var/www/site")
    parser.add_argument("--site-dir", required=True, help="Site dir, e.g. /ru")
    parser.add_argument("--report-json", required=True, help="Path to linkage report JSON from sf4_project_audit.py")
    parser.add_argument("--lang", default="ru", help="Language folder for lang files")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    parser.add_argument("--limit", type=int, default=0, help="Limit number of unique blocks (0 means no limit)")
    parser.add_argument("--apply", action="store_true", help="Write files. Without this flag script runs in dry-run mode.")
    args = parser.parse_args()

    site_root = Path(args.site_root).resolve()
    if not site_root.exists():
        print(f"Site root does not exist: {site_root}", file=sys.stderr)
        return 2

    report_json = Path(args.report_json).resolve()
    if not report_json.exists():
        print(f"Report JSON not found: {report_json}", file=sys.stderr)
        return 2

    site_dir = normalize_site_dir(args.site_dir)
    simai_data_key = f"{site_dir.lstrip('/')}/simai.data"
    data_dir = site_root / site_dir.lstrip("/") / "simai.data"

    try:
        records = load_report(report_json)
    except Exception as exc:  # noqa: BLE001
        print(f"Failed to load report: {exc}", file=sys.stderr)
        return 2

    missing_pairs: Set[Tuple[str, str]] = set()
    invalid_pairs: List[Tuple[str, str]] = []
    for item in records:
        if not isinstance(item, dict):
            continue
        if item.get("simai_data") != simai_data_key:
            continue
        if item.get("status") != "missing":
            continue
        section = str(item.get("block_section", "")).strip()
        code = str(item.get("block_code", "")).strip()
        if not section or not code:
            continue
        if not valid_section(section) or not valid_code(code):
            invalid_pairs.append((section, code))
            continue
        missing_pairs.add((section, code))

    pairs = sorted(missing_pairs)
    if args.limit > 0:
        pairs = pairs[: args.limit]

    print(f"Target simai.data: {data_dir}")
    print(f"Missing unique blocks: {len(missing_pairs)}")
    if args.limit > 0:
        print(f"Applying limit: {args.limit}, selected: {len(pairs)}")
    if invalid_pairs:
        print(f"Invalid section/code pairs skipped: {len(invalid_pairs)}")
    if not args.apply:
        print("Mode: dry-run (no files will be written). Use --apply to write.")

    created_count = 0
    skipped_count = 0
    for section, code in pairs:
        block_dir = data_dir / "grid" / "block" / section / code
        lang_dir = block_dir / "lang" / args.lang
        msg_key = code.upper()
        files = {
            block_dir / "template.php": build_template_php(),
            block_dir / ".description.php": build_description_php(),
            block_dir / ".parameters.php": build_parameters_php(),
            lang_dir / ".description.php": build_lang_description(
                msg_key,
                code,
                f"Autogenerated scaffold for missing block {section}/{code}",
            ),
            lang_dir / ".parameters.php": build_lang_parameters(msg_key),
        }
        print(f"\n== block {section}/{code}")
        for path, content in files.items():
            ok, msg = write_file(path, content, apply=args.apply, force=args.force)
            print(msg)
            if ok:
                created_count += 1
            else:
                skipped_count += 1

    print(
        "\nSummary: "
        f"selected_blocks={len(pairs)}, "
        f"file_ops_ok={created_count}, "
        f"file_ops_skipped={skipped_count}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


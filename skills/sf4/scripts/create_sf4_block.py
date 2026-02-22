#!/usr/bin/env python3
"""
Create an SF4 block scaffold in simai.data.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def normalize_site_dir(raw: str) -> str:
    value = raw.strip()
    if not value:
        return "/"
    if not value.startswith("/"):
        value = "/" + value
    if value != "/":
        value = value.rstrip("/")
    return value


def validate_code(value: str) -> str:
    # SF4 block codes often contain dots, lowercase letters, digits, underscores, hyphens.
    if not re.fullmatch(r"[a-z0-9._-]+", value):
        raise ValueError("Block code must match [a-z0-9._-]+")
    return value


def validate_section(value: str) -> str:
    if not re.fullmatch(r"[a-z0-9_-]+", value):
        raise ValueError("Section must match [a-z0-9_-]+")
    return value


def to_msg_key(code: str) -> str:
    return code.upper()


def to_prefix(code: str) -> str:
    return code.upper()


def ensure_parent(path: Path, dry_run: bool) -> None:
    if dry_run:
        return
    path.parent.mkdir(parents=True, exist_ok=True)


def write_file(path: Path, content: str, dry_run: bool, force: bool) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"File exists: {path}")
    if dry_run:
        print(f"[DRY-RUN] write {path}")
        return
    ensure_parent(path, dry_run=False)
    path.write_text(content, encoding="utf-8")
    print(f"[OK] wrote {path}")


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


def main() -> int:
    parser = argparse.ArgumentParser(description="Create SF4 block scaffold.")
    parser.add_argument("--site-root", required=True, help="Project root, e.g. /var/www/site")
    parser.add_argument("--site-dir", required=True, help="Site dir, e.g. /ru")
    parser.add_argument("--section", required=True, help="Block section, e.g. header")
    parser.add_argument("--code", required=True, help="Block code, e.g. custom.button")
    parser.add_argument("--name", default=None, help="Block display name for lang file")
    parser.add_argument("--description", default=None, help="Block description for lang file")
    parser.add_argument("--lang", default="ru", help="Language folder name, default: ru")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without writing")
    args = parser.parse_args()

    try:
        section = validate_section(args.section.strip())
        code = validate_code(args.code.strip())
    except ValueError as exc:
        print(f"Validation error: {exc}", file=sys.stderr)
        return 2

    site_root = Path(args.site_root).resolve()
    if not site_root.exists():
        print(f"Site root does not exist: {site_root}", file=sys.stderr)
        return 2

    site_dir = normalize_site_dir(args.site_dir)
    data_dir = site_root / site_dir.lstrip("/") / "simai.data"
    block_dir = data_dir / "grid" / "block" / section / code
    lang_dir = block_dir / "lang" / args.lang

    block_name = args.name or code
    block_description = args.description or f"SF4 block scaffold for {code}"
    msg_key = to_msg_key(code)

    files = {
        block_dir / "template.php": build_template_php(),
        block_dir / ".description.php": build_description_php(),
        block_dir / ".parameters.php": build_parameters_php(),
        lang_dir / ".description.php": build_lang_description(msg_key, block_name, block_description),
        lang_dir / ".parameters.php": build_lang_parameters(msg_key),
    }

    print(f"Target block dir: {block_dir}")
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
        print("[OK] block scaffold created")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())


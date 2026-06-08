#!/usr/bin/env python3
"""
Propose-only generator for SF4 universal wizard master skeletons.

The generator writes candidate files into source/output by default. It is
deliberately not a live installer: it does not touch /Users/rim/Sites, /simai,
/bitrix, public site roots, Bitrix DB or wizard runtime state.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path
from typing import Any, Dict, List


SCHEMA_VERSION = "1.0.0"
PNG_1X1 = bytes.fromhex(
    "89504e470d0a1a0a0000000d4948445200000001000000010806000000"
    "1f15c4890000000a49444154789c6360000002000100ffff0300000600"
    "057bfabf0000000049454e44ae426082"
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def slug_code(value: str) -> str:
    value = value.strip()
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", value):
        raise ValueError("code must contain only letters, digits, dot, underscore or hyphen")
    return value


def php_string(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def ensure_safe_output(path: Path, root: Path) -> Path:
    resolved = path.expanduser().resolve()
    allowed = (root / "source" / "output").resolve()
    if allowed not in [resolved, *resolved.parents]:
        raise ValueError(f"output_dir must be inside {allowed}")
    return resolved


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_bytes(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)


def mkdirs(paths: List[Path]) -> None:
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)


def build_actions(profile: str, name: str) -> str:
    actions: List[str] = [
        """
        array(
            "name" => Loc::getMessage("SITE_CHOICE"),
            "code" => "site.choice.sveden",
            "data_output_code" => "site_config",
            "parameter" => array(),
        )""".strip()
    ]

    if profile in {"config", "iblock"}:
        actions.extend(
            [
                """
        array(
            "name" => Loc::getMessage("CREATE_IBLOCKCONFIG"),
            "code" => "iblockconfig.import.data",
            "autocomplete" => "Y",
            "data_input_code" => "site_config",
            "parameter" => array(
                "site" => array(
                    "array" => "site_config",
                    "key" => "site",
                ),
                "file" => array(
                    "iblock" => array(
                        "config" => Wizard::getLocal(__DIR__) . "/data/config/.iblock.config.php",
                        "lang" => Wizard::getLocal(__DIR__) . "/data/config/lang/ru/.iblock.config.php",
                    ),
                    "iblocksection" => array(
                        "config" => Wizard::getLocal(__DIR__) . "/data/config/.iblock.section.config.php",
                        "lang" => Wizard::getLocal(__DIR__) . "/data/config/lang/ru/.iblock.section.config.php",
                    ),
                    "tmp" => Wizard::getLocal(__DIR__) . "/tmp/",
                ),
            ),
        )""".strip(),
                """
        array(
            "name" => Loc::getMessage("ADD_URLREWRITE"),
            "code" => "urlrewrite.add",
            "autocomplete" => "Y",
            "data_input_code" => "site_config",
            "parameter" => array(
                "source" => Wizard::getLocal(__DIR__) . "/data/config/urlrewrite.php",
            ),
        )""".strip(),
            ]
        )

    if profile == "iblock":
        actions.extend(
            [
                """
        array(
            "name" => Loc::getMessage("CREATE_IBLOCK_TYPE"),
            "code" => "iblocktype.import.data",
            "autocomplete" => "Y",
            "data_input_code" => "site_config",
            "parameter" => array(
                "source" => Wizard::getLocal(__DIR__) . "/data/config/.iblocktype.config.php",
            ),
        )""".strip(),
                """
        array(
            "name" => Loc::getMessage("IMPORT_IBLOCK_ARCHIVE"),
            "code" => "iblock.import.archive",
            "autocomplete" => "Y",
            "data_input_code" => "site_config",
            "parameter" => array(
                array(
                    "source" => Wizard::getLocal(__DIR__) . "/data/iblock/sample.zip",
                    "destination" => "sf_ru_map_data",
                    "site" => array(
                        "array" => "site_config",
                        "key" => "site",
                    ),
                    "name" => """ + php_string(name + " sample archive") + """,
                ),
            ),
        )""".strip(),
            ]
        )

    actions.append(
        """
        array(
            "name" => Loc::getMessage("FINISH"),
            "code" => "info",
            "autocomplete" => "Y",
            "parameter" => array(
                "message" => Loc::getMessage("FINISH_MESSAGE"),
            ),
        )""".strip()
    )
    return ",\n\n        ".join(actions)


def render_config(code: str, storage_code: str, name: str, profile: str) -> str:
    actions = build_actions(profile, name)
    return f"""<?
\\Bitrix\\Main\\Loader::includeSharewareModule("simai.framework");

use Bitrix\\Main\\Localization\\Loc;
use SIMAI\\Wizard;

Loc::loadMessages(__FILE__);

return array(
    "description" => array(
        "name" => Loc::getMessage("WIZARD_SOLUTION"),
        "code" => "{storage_code}",
        "stage_renew" => "Y",
        "logo" => Wizard::getLocal(__DIR__) . "/image/logo.png",
        "author" => "SIMAI",
        "copyright" => "© SIMAI",
        "background" => array(
            "color" => "#134A5B",
            "image" => Wizard::getLocal(__DIR__) . "/image/wizard_bg.jpg",
            "position" => "bottom",
            "repeat" => "no-repeat",
            "size" => "cover",
            "attachment" => "fixed",
        ),
        "color" => array(
            "primary" => "#F34E3F",
            "secondary" => "#134A5B",
        ),
        "modifier" => array(
            "page_body" => "theme-dark bg-theme-50 p-md-5 py-4 py-lg-6",
            "wizard_wrap" => "r-2 w-80 wr-md-7 mx-auto",
            "wizard_area" => "p-4 bg-white theme-light",
            "wizard_nav" => "p-4 bg-white",
            "wizard_copyright" => "p-2 t-center t--1 c-text-secondary l-inherit l-underline",
        ),
    ),
    "action" => array(
        {actions}
    ),
);
"""


def render_index() -> str:
    return """<?
if (!defined("B_PROLOG_INCLUDED") || B_PROLOG_INCLUDED !== true) {
    require($_SERVER["DOCUMENT_ROOT"] . "/bitrix/header.php");
}

define("WIZARD_DIR", __DIR__);
define("WIZARD_TEMP_DIR", __DIR__ . "/tmp");
define("WIZARD_CONFIG_FILE", __DIR__ . "/.wizard.config.php");

$APPLICATION->IncludeComponent(
    "simai:sf.wizard",
    "",
    array(
        "WIZARD_DIR" => WIZARD_DIR,
        "WIZARD_TEMP_DIR" => WIZARD_TEMP_DIR,
        "WIZARD_CONFIG_FILE" => WIZARD_CONFIG_FILE,
        "AJAX_TIME_STEP" => 5,
        "AJAX_TIME_INTERVAL" => 500,
        "AJAX_MODE" => "Y",
        "CACHE_TYPE" => "N",
    )
);

require($_SERVER["DOCUMENT_ROOT"] . "/bitrix/footer.php");
"""


def render_lang(name: str) -> str:
    return f"""<?
$MESS["WIZARD_SOLUTION"] = {php_string(name)};
$MESS["SITE_CHOICE"] = "Выбор сайта";
$MESS["CREATE_IBLOCKCONFIG"] = "Подготовка конфигурации инфоблоков";
$MESS["ADD_URLREWRITE"] = "Подготовка правил URL";
$MESS["CREATE_IBLOCK_TYPE"] = "Подготовка типов инфоблоков";
$MESS["IMPORT_IBLOCK_ARCHIVE"] = "Подготовка архива инфоблока";
$MESS["FINISH"] = "Завершение";
$MESS["FINISH_MESSAGE"] = "Skeleton мастера подготовлен. Перед live запуском требуется аудит, backup и rollback.";
"""


def render_wrapper_wizard(code: str) -> str:
    return f"""<?
if (!defined("B_PROLOG_INCLUDED") || B_PROLOG_INCLUDED !== true) {{
    die();
}}

class SelectSiteStep extends CWizardStep
{{
    public function InitStep()
    {{
        $wizard =& $this->GetWizard();
        $wizard->solutionName = "{code}";
        LocalRedirect("/simai/wizard/master/{code}/");
    }}
}}
"""


def render_wrapper_description(code: str, name: str) -> str:
    return f"""<?
if (!defined("B_PROLOG_INCLUDED") || B_PROLOG_INCLUDED !== true) {{
    die();
}}

$arWizardDescription = array(
    "NAME" => {php_string(name)},
    "DESCRIPTION" => "SF4 universal wizard wrapper for {code}",
    "VERSION" => "1.0.0",
    "START_TYPE" => "WINDOW",
    "WIZARD_TYPE" => "INSTALL",
);
"""


def create_sample_zip(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("sample.xml", "<?xml version=\"1.0\" encoding=\"UTF-8\"?><items></items>")


def generate(args: argparse.Namespace) -> Dict[str, Any]:
    root = repo_root()
    code = slug_code(args.code)
    storage_code = args.storage_code or code.replace(".", "_").replace("-", "_")
    name = args.name or code
    output_root = ensure_safe_output(Path(args.output_dir), root)
    package_root = output_root / code
    master = package_root / "master" / code

    if package_root.exists() and not args.force:
        raise FileExistsError(f"{package_root} already exists; pass --force to replace files in this proposal")

    mkdirs(
        [
            master / "image",
            master / "tmp",
            master / "data" / "bitrix" / "templates",
            master / "data" / "config" / "lang" / "ru",
            master / "data" / "iblock",
            master / "data" / "module",
            master / "data" / "php_interface",
            master / "data" / "root",
            master / "data" / "site",
            master / "data" / "template",
            master / "data" / "components",
            master / "lang" / "ru",
        ]
    )

    write_text(master / "index.php", render_index())
    write_text(master / ".wizard.config.php", render_config(code, storage_code, name, args.profile))
    write_text(master / "lang" / "ru" / ".wizard.config.php", render_lang(name))
    write_text(master / "data" / "config" / ".iblock.config.php", "<?\nreturn array();\n")
    write_text(master / "data" / "config" / ".iblock.section.config.php", "<?\nreturn array();\n")
    write_text(master / "data" / "config" / ".iblocktype.config.php", "<?\nreturn array();\n")
    write_text(master / "data" / "config" / "urlrewrite.php", "<?\nreturn array();\n")
    write_text(master / "data" / "config" / "lang" / "ru" / ".iblock.config.php", "<?\n$MESS = array();\n")
    write_text(master / "data" / "config" / "lang" / "ru" / ".iblock.section.config.php", "<?\n$MESS = array();\n")
    write_bytes(master / "image" / "logo.png", PNG_1X1)
    write_bytes(master / "image" / "wizard_bg.jpg", PNG_1X1)
    if args.profile == "iblock":
        create_sample_zip(master / "data" / "iblock" / "sample.zip")

    wrapper_root = None
    if args.wrapper:
        wrapper_root = package_root / "module" / "install" / "wizard" / code
        mkdirs([wrapper_root / "lang" / "ru", wrapper_root / "images"])
        write_text(wrapper_root / "wizard.php", render_wrapper_wizard(code))
        write_text(wrapper_root / ".description.php", render_wrapper_description(code, name))
        write_text(wrapper_root / "lang" / "ru" / ".description.php", render_lang(name))
        write_text(wrapper_root / "lang" / "ru" / "wizard.php", render_lang(name))
        write_bytes(wrapper_root / "images" / "wizard.png", PNG_1X1)

    readme = f"""# {name}

Generated SF4 universal wizard skeleton proposal.

This package is not installed and not executable in live/runtime by itself.
Review `.wizard.config.php`, fill real payload data, define backup/rollback and
run `sf4_wizard_audit.py` before any controlled environment execution.

Master proposal:

```text
{master}
```
"""
    write_text(package_root / "README.md", readme)

    manifest: Dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "operation_id": "sf4.wizard.skeleton",
        "mode": {
            "propose_only": True,
            "read_only_runtime": True,
            "writes": "source_output_only",
            "executes_php": False,
            "executes_wizard_actions": False,
        },
        "code": code,
        "storage_code": storage_code,
        "name": name,
        "profile": args.profile,
        "package_root": str(package_root),
        "master": str(master),
        "config": str(master / ".wizard.config.php"),
        "wrapper": str(wrapper_root) if wrapper_root else None,
        "audit_hint": {
            "command": [
                "python3",
                "scripts/sf4_wizard_audit.py",
                "--site-root",
                args.audit_site_root,
                "--master",
                str(master),
                "--json",
                f"source/output/wizard-skeleton/{code}/audit.json",
            ]
        },
        "next_required_human_work": [
            "replace placeholder visual assets",
            "fill real config/data payloads",
            "choose exact action chain and branch conditions",
            "define backup/rollback per side effect",
            "audit in controlled environment before execution",
        ],
    }
    write_text(package_root / "manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2))
    return manifest


def main() -> int:
    root = repo_root()
    parser = argparse.ArgumentParser(description="Generate a propose-only SF4 universal wizard skeleton.")
    parser.add_argument("--code", required=True, help="Wizard/module code, for example simai.example")
    parser.add_argument("--name", help="Human-readable wizard name")
    parser.add_argument("--storage-code", help="description.code storage key. Defaults to code with dots/hyphens as underscores.")
    parser.add_argument(
        "--profile",
        choices=["minimal", "config", "iblock"],
        default="config",
        help="Generated action-chain profile.",
    )
    parser.add_argument(
        "--output-dir",
        default=str(root / "source" / "output" / "wizard-skeleton"),
        help="Output directory. Must be inside source/output.",
    )
    parser.add_argument("--audit-site-root", default="/Users/rim/Sites/sf4.test", help="Read-only action library site root for audit hints.")
    parser.add_argument("--wrapper", action="store_true", help="Also generate Bitrix wrapper wizard skeleton.")
    parser.add_argument("--force", action="store_true", help="Allow overwriting files in an existing proposal directory.")
    parser.add_argument("--json", dest="json_only", action="store_true", help="Print machine-readable manifest only.")
    args = parser.parse_args()

    try:
        manifest = generate(args)
    except Exception as exc:  # noqa: BLE001 - CLI should report exact failure.
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.json_only:
        print(json.dumps(manifest, ensure_ascii=False, indent=2))
    else:
        print("SF4 Wizard Skeleton")
        print(f"Package: {manifest['package_root']}")
        print(f"Master: {manifest['master']}")
        print(f"Config: {manifest['config']}")
        print("Mode: propose-only, source/output writes only")
    return 0


if __name__ == "__main__":
    sys.exit(main())

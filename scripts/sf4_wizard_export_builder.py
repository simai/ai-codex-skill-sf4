#!/usr/bin/env python3
"""
Propose-only builder for SF4 universal wizard export/package masters.

The builder takes a JSON manifest and generates a `wizard.export`-style master
under source/output. It does not execute PHP, Bitrix, wizard actions, iblock
exports, file copy actions or archive cleanup.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional


SCHEMA_VERSION = "1.0.0"
PNG_1X1 = bytes.fromhex(
    "89504e470d0a1a0a0000000d4948445200000001000000010806000000"
    "1f15c4890000000a49444154789c6360000002000100ffff0300000600"
    "057bfabf0000000049454e44ae426082"
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_manifest(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def slug_code(value: str) -> str:
    value = value.strip()
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", value):
        raise ValueError("solution_code must contain only letters, digits, dot, underscore or hyphen")
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


def rel_site_path(path: str) -> str:
    if not path.startswith("/"):
        raise ValueError(f"site-relative path must start with /: {path}")
    if ".." in Path(path).parts:
        raise ValueError(f"site-relative path must not contain '..': {path}")
    return path


def php_array_rows(rows: Iterable[str]) -> str:
    rows = list(rows)
    if not rows:
        return ""
    return ",\n".join(rows)


def action_row(name: str, code: str, body: str = "") -> str:
    body = body.rstrip()
    if body:
        body = "\n" + body
    return f"""        array(
            "name" => {php_string(name)},
            "code" => {php_string(code)},{body}
        )"""


def list_item(value: str) -> str:
    return "                    " + php_string(value)


def render_file_copy_action(name: str, items: List[Dict[str, str]]) -> Optional[str]:
    if not items:
        return None
    rows = []
    for item in items:
        source = rel_site_path(item["source"])
        destination = rel_site_path(item["destination"])
        item_name = item.get("name") or source
        rows.append(
            f"""                array(
                    "source" => {php_string(source)},
                    "destination" => {php_string(destination)},
                    "name" => {php_string(item_name)},
                )"""
        )
    body = f"""
            "parameter" => array(
{php_array_rows(rows)}
            ),"""
    return action_row(name, "file.copy", body)


def render_export_data_action(
    name: str,
    code: str,
    output_code: str,
    parameter: Optional[Dict[str, Any]] = None,
    autocomplete: bool = False,
) -> str:
    parameter = parameter or {}
    lines = [
        f'            "data_output_code" => {php_string(output_code)},',
    ]
    if autocomplete:
        lines.append('            "autocomplete" => "Y",')
    lines.append("            \"parameter\" => " + php_value(parameter, 3) + ",")
    return action_row(name, code, "\n" + "\n".join(lines))


def render_data_file_action(name: str, input_code: str, file_path: str, autocomplete: bool = False) -> str:
    lines = [
        f'            "data_input_code" => {php_string(input_code)},',
    ]
    if autocomplete:
        lines.append('            "autocomplete" => "Y",')
    lines.append(
        f"""            "parameter" => array(
                "file" => {php_string(rel_site_path(file_path))},
            ),"""
    )
    return action_row(name, "data.export.file", "\n" + "\n".join(lines))


def render_iblock_export_action(iblocks: List[str], destination: str) -> Optional[str]:
    if not iblocks:
        return None
    iblock_rows = ",\n".join(list_item(code) for code in iblocks)
    body = f"""
            "data_output_code" => "iblock_pack",
            "parameter" => array(
                "iblock" => array(
{iblock_rows}
                ),
                "destination" => {php_string(rel_site_path(destination))},
            ),"""
    return action_row("Запаковка инфоблоков", "iblock.export.archive", body)


def render_file_create_action(snippets: List[Dict[str, str]]) -> Optional[str]:
    if not snippets:
        return None
    rows = []
    for item in snippets:
        directory = rel_site_path(item["dir"])
        filename = item["filename"]
        text = item.get("text", "")
        rows.append(
            f"""                array(
                    "dir" => {php_string(directory)},
                    "filename" => {php_string(filename)},
                    "text" => {php_string(text)},
                )"""
        )
    body = f"""
            "parameter" => array(
{php_array_rows(rows)}
            ),"""
    return action_row("Создаём файлы php_interface", "file.create", body)


def render_encode_action(paths: List[str]) -> Optional[str]:
    if not paths:
        return None
    rows = ",\n".join(list_item(rel_site_path(path)) for path in paths)
    body = f"""
            "parameter" => array(
{rows}
            ),"""
    return action_row("Меняем кодировку у языковых файлов", "file.encode.win1251", body)


def render_zip_action(source: str, destination: str) -> str:
    body = f"""
            "parameter" => array(
                array(
                    "source" => {php_string(rel_site_path(source))},
                    "destination" => {php_string(rel_site_path(destination))},
                    "name" => "Архивирование экспортного пакета",
                ),
            ),"""
    return action_row("Архивируем экспортный пакет", "file.zip", body)


def render_delete_action(paths: List[str]) -> Optional[str]:
    if not paths:
        return None
    rows = ",\n".join(list_item(rel_site_path(path)) for path in paths)
    body = f"""
            "parameter" => array(
{rows}
            ),"""
    return action_row("Удаляем временные файлы", "file.delete", body)


def php_value(value: Any, indent: int = 0) -> str:
    pad = "    " * indent
    child = "    " * (indent + 1)
    if isinstance(value, str):
        return php_string(value)
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    if value is None:
        return "null"
    if isinstance(value, list):
        if not value:
            return "array()"
        rows = [child + php_value(item, indent + 1) for item in value]
        return "array(\n" + ",\n".join(rows) + "\n" + pad + ")"
    if isinstance(value, dict):
        if not value:
            return "array()"
        rows = [
            child + php_string(str(key)) + " => " + php_value(item, indent + 1)
            for key, item in value.items()
        ]
        return "array(\n" + ",\n".join(rows) + "\n" + pad + ")"
    raise TypeError(f"Unsupported PHP value type: {type(value)!r}")


def render_index() -> str:
    return """<?php
require($_SERVER["DOCUMENT_ROOT"] . "/bitrix/modules/main/include/prolog_before.php");

\\Bitrix\\Main\\Loader::includeSharewareModule("simai.framework");

use SIMAI\\Wizard;

$dirWizard = Wizard::getLocal(__DIR__);

$APPLICATION->IncludeComponent(
    "simai:sf.wizard",
    ".default",
    array(
        "COMPONENT_TEMPLATE" => ".default",
        "WIZARD_DIR" => $dirWizard,
        "WIZARD_TEMP_DIR" => $dirWizard . "/temp",
        "WIZARD_CONFIG_FILE" => $dirWizard . "/.wizard.config.php",
        "AJAX_TIME_STEP" => 5,
        "AJAX_TIME_INTERVAL" => 2,
        "AJAX_MODE" => "Y",
        "AJAX_OPTION_JUMP" => "N",
        "AJAX_OPTION_STYLE" => "N",
        "AJAX_OPTION_HISTORY" => "N",
        "AJAX_OPTION_ADDITIONAL" => "",
        "COMPOSITE_FRAME_MODE" => "N",
        "COMPOSITE_FRAME_TYPE" => "AUTO",
        "CACHE_TYPE" => "N",
    ),
    false
);
"""


def render_config(manifest: Dict[str, Any], actions: List[str]) -> str:
    description = manifest.get("description") or {}
    name = description.get("name") or manifest["solution_name"]
    storage_code = description.get("storage_code") or manifest["solution_code"].replace(".", "_").replace("-", "_")
    primary = description.get("primary_color", "#E53935")
    secondary = description.get("secondary_color", "#2196F3")
    background = description.get("background_color", "#263238")
    action_block = ",\n\n".join(actions)
    return f"""<?php
\\Bitrix\\Main\\Loader::includeSharewareModule("simai.framework");
\\Bitrix\\Main\\Loader::includeSharewareModule("iblock");

use SIMAI\\Wizard;

return array(
    "description" => array(
        "name" => {php_string(name)},
        "code" => {php_string(storage_code)},
        "stage_renew" => "Y",
        "logo" => Wizard::getLocal(__DIR__) . "/image/logo.png",
        "copyright" => "© SIMAI",
        "background" => array(
            "color" => {php_string(background)},
            "image" => Wizard::getLocal(__DIR__) . "/image/wizard_bg.jpg",
            "position" => "bottom",
            "repeat" => "no-repeat",
            "size" => "cover",
            "attachment" => "fixed",
        ),
        "color" => array(
            "primary" => {php_string(primary)},
            "secondary" => {php_string(secondary)},
        ),
        "modifier" => array(
            "page_body" => "theme-light bg-theme-50 p-md-5 py-4 py-lg-6",
            "wizard_wrap" => "r-2 w-80 wr-md-7 mx-auto",
            "wizard_area" => "p-4 bg-white",
            "wizard_nav" => "p-4 bg-white",
            "wizard_copyright" => "p-2 t-center t--1 c-white l-inherit l-underline",
        ),
    ),
    "action" => array(
{action_block}
    ),
);
"""


def normalize_copy_items(manifest: Dict[str, Any]) -> List[Dict[str, str]]:
    output_dir = manifest["export"]["output_dir"].rstrip("/")
    items: List[Dict[str, str]] = []
    for section in manifest.get("copy", []):
        source = rel_site_path(section["source"])
        destination = rel_site_path(section["destination"])
        items.append(
            {
                "source": source,
                "destination": destination,
                "name": section.get("name") or source,
            }
        )
    for module in manifest.get("modules", []):
        module = slug_code(module)
        items.append(
            {
                "source": f"/bitrix/modules/{module}",
                "destination": f"{output_dir}/install/bitrix/modules/{module}",
                "name": f"Копирование модуля {module}",
            }
        )
    return items


def build_actions(manifest: Dict[str, Any]) -> List[str]:
    export = manifest["export"]
    output_dir = rel_site_path(export["output_dir"].rstrip("/"))
    actions: List[Optional[str]] = []

    actions.append(render_file_copy_action("Копируем файлы решения", normalize_copy_items(manifest)))

    data_exports = manifest.get("data_exports", {})
    if data_exports.get("site", True):
        actions.append(render_export_data_action("Получаем данные настроек сайтов", "site.export.data", "site"))
    if data_exports.get("mail", False):
        actions.append(render_export_data_action("Получаем данные почтовых событий", "mail.export.data", "mail", autocomplete=True))
    if data_exports.get("mail_templates", False):
        actions.append(
            render_export_data_action(
                "Получаем данные почтовых шаблонов",
                "mail-templates.export.data",
                "mail-templates",
                autocomplete=True,
            )
        )
    if data_exports.get("usergroups"):
        actions.append(
            render_export_data_action(
                "Получаем настройки групп пользователей",
                "usergroup.export.data",
                "usergroup",
                {"code": data_exports["usergroups"]},
            )
        )
    if data_exports.get("iblock_types", True):
        actions.append(render_export_data_action("Получаем данные типов инфоблоков", "iblocktype.export.data", "iblocktype"))
    if data_exports.get("options"):
        actions.append(render_export_data_action("Получаем настройки модулей", "option.export.data", "option", data_exports["options"]))

    public_copy = manifest.get("public_copy", [])
    actions.append(render_file_copy_action("Копируем файлы публичной части", public_copy))

    iblocks = manifest.get("iblocks", [])
    actions.append(render_iblock_export_action(iblocks, f"{output_dir}/install/iblock"))

    data_files = manifest.get("data_files", {})
    default_data_files = {
        "site": f"{output_dir}/install/ru/config/.site.config.php",
        "usergroup": f"{output_dir}/install/ru/config/.usergroup.config.php",
        "option": f"{output_dir}/install/ru/config/.option.config.php",
        "iblocktype": f"{output_dir}/install/ru/config/.iblocktype.config.php",
    }
    if data_exports.get("mail", False):
        default_data_files["mail"] = f"{output_dir}/install/ru/config/mail.config.php"
    if data_exports.get("mail_templates", False):
        default_data_files["mail-templates"] = f"{output_dir}/install/ru/config/mail-templates.config.php"
    for input_code, file_path in {**default_data_files, **data_files}.items():
        if should_emit_data_file(input_code, data_exports):
            actions.append(render_data_file_action(f"Записываем данные {input_code} в файл", input_code, file_path))

    actions.append(render_file_create_action(manifest.get("php_interface_snippets", [])))
    if manifest.get("encoding", {}).get("win1251", False):
        actions.append(render_encode_action(manifest.get("encoding", {}).get("paths", [output_dir + "/"])))

    archive = manifest.get("archive", {})
    if archive.get("enabled", False):
        actions.append(render_zip_action(archive.get("source", output_dir), archive.get("destination", output_dir + ".zip")))
    cleanup = manifest.get("cleanup", {})
    if cleanup.get("enabled", False):
        actions.append(render_delete_action(cleanup.get("paths", [output_dir + "/"])))

    actions.append(action_row("Завершение упаковки", "info", '\n            "parameter" => array(\n                "text" => "Упаковка решения успешно подготовлена",\n            ),'))
    return [item for item in actions if item]


def should_emit_data_file(input_code: str, data_exports: Dict[str, Any]) -> bool:
    if input_code == "site":
        return bool(data_exports.get("site", True))
    if input_code == "mail":
        return bool(data_exports.get("mail", False))
    if input_code == "mail-templates":
        return bool(data_exports.get("mail_templates", False))
    if input_code == "usergroup":
        return bool(data_exports.get("usergroups"))
    if input_code == "option":
        return bool(data_exports.get("options"))
    if input_code == "iblocktype":
        return bool(data_exports.get("iblock_types", True))
    return True


def validate_manifest(manifest: Dict[str, Any]) -> None:
    required = ["solution_code", "solution_name", "source_site_root", "export"]
    for key in required:
        if key not in manifest:
            raise ValueError(f"manifest missing required key: {key}")
    slug_code(manifest["solution_code"])
    export = manifest["export"]
    if "output_dir" not in export:
        raise ValueError("manifest.export.output_dir is required")
    rel_site_path(export["output_dir"])
    if manifest.get("archive", {}).get("enabled") and manifest.get("cleanup", {}).get("enabled"):
        raise ValueError("archive and cleanup can both be present, but do not enable cleanup in generated review examples")


def generate(args: argparse.Namespace) -> Dict[str, Any]:
    root = repo_root()
    manifest_path = Path(args.manifest).expanduser().resolve()
    manifest = load_manifest(manifest_path)
    validate_manifest(manifest)

    code = slug_code(manifest["solution_code"])
    output_root = ensure_safe_output(Path(args.output_dir or root / "source" / "output" / "wizard-export-builder"), root)
    package_root = output_root / code
    master = package_root / "master" / code

    if package_root.exists() and not args.force:
        raise FileExistsError(f"{package_root} already exists; pass --force to overwrite proposal files")

    for directory in (master / "image", master / "temp", master / "data", master / "lang" / "ru"):
        directory.mkdir(parents=True, exist_ok=True)

    actions = build_actions(manifest)
    write_text(master / "index.php", render_index())
    write_text(master / ".wizard.config.php", render_config(manifest, actions))
    write_bytes(master / "image" / "logo.png", PNG_1X1)
    write_bytes(master / "image" / "wizard_bg.jpg", PNG_1X1)
    write_text(package_root / "input-manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2))

    readme = f"""# {manifest['solution_name']}

Generated SF4 universal export master proposal.

This package is a controlled proposal only. It does not contain exported data
and was not executed. Review `.wizard.config.php`, run audit/readiness, then
use only in a disposable or explicitly approved source environment.

Source site root expected by manifest:

```text
{manifest['source_site_root']}
```

Generated master:

```text
{master}
```
"""
    write_text(package_root / "README.md", readme)

    result: Dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "operation_id": "sf4.wizard.export_builder",
        "mode": {
            "propose_only": True,
            "writes": "source_output_only",
            "executes_php": False,
            "executes_bitrix": False,
            "executes_wizard_actions": False,
            "exports_data": False,
        },
        "solution_code": code,
        "solution_name": manifest["solution_name"],
        "source_site_root": manifest["source_site_root"],
        "package_root": str(package_root),
        "master": str(master),
        "config": str(master / ".wizard.config.php"),
        "action_count": len(actions),
        "audit_hint": {
            "command": [
                "python3",
                "scripts/sf4_wizard_audit.py",
                "--site-root",
                manifest["source_site_root"],
                "--master",
                str(master),
                "--json",
                f"source/output/wizard-export-builder/{code}/audit.json",
            ]
        },
        "readiness_hint": {
            "command": [
                "python3",
                "scripts/sf4_wizard_readiness.py",
                "--audit",
                f"source/output/wizard-export-builder/{code}/audit.json",
                "--label",
                code,
                "--json",
                f"source/output/wizard-export-builder/{code}/readiness.json",
            ]
        },
        "stop_conditions": [
            "do not run generated master on live/staging without explicit scope",
            "do not enable cleanup until generated export tree is verified",
            "do not use broad iblock export for product packages without allowlist review",
            "stop if audit/readiness reports are stale or blocked",
        ],
    }
    write_text(package_root / "builder-report.json", json.dumps(result, ensure_ascii=False, indent=2))
    return result


def main() -> int:
    root = repo_root()
    parser = argparse.ArgumentParser(description="Generate a propose-only SF4 universal export master.")
    parser.add_argument("--manifest", required=True, help="JSON export manifest")
    parser.add_argument(
        "--output-dir",
        default=str(root / "source" / "output" / "wizard-export-builder"),
        help="Output directory. Must be inside source/output.",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite proposal files")
    parser.add_argument("--json", dest="json_only", action="store_true", help="Print machine-readable report only")
    args = parser.parse_args()

    try:
        report = generate(args)
    except Exception as exc:  # noqa: BLE001 - CLI should report exact failure.
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.json_only:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print("SF4 Wizard Export Builder")
        print(f"Package: {report['package_root']}")
        print(f"Master: {report['master']}")
        print(f"Config: {report['config']}")
        print("Mode: propose-only, source/output writes only")
    return 0


if __name__ == "__main__":
    sys.exit(main())

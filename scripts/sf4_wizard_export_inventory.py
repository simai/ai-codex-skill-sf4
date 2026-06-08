#!/usr/bin/env python3
"""
Read-only source-site inventory helper for SF4 wizard export packaging.

The helper inspects a local Bitrix/SF4 site tree, drafts a manifest for
sf4_wizard_export_builder.py and can run the safe proposal chain:
inventory -> builder -> audit -> readiness.

It never executes Bitrix, PHP runtime, wizard actions, iblock export/import,
file copy actions or writes into the inspected site root.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional


SCHEMA_VERSION = "1.0.0"


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def slug_code(value: str) -> str:
    value = value.strip()
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", value):
        raise ValueError("solution-code must contain only letters, digits, dot, underscore or hyphen")
    return value


def safe_site_dir(value: str) -> str:
    if not value.startswith("/"):
        raise ValueError("--site-dir must start with /")
    if ".." in Path(value).parts:
        raise ValueError("--site-dir must not contain '..'")
    return value.rstrip("/") or "/"


def ensure_safe_output(path: Path, root: Path) -> Path:
    resolved = path.expanduser().resolve()
    allowed = (root / "source" / "output").resolve()
    if allowed not in [resolved, *resolved.parents]:
        raise ValueError(f"output dir must be inside {allowed}")
    return resolved


def rel_exists(site_root: Path, rel: str) -> bool:
    return (site_root / rel.lstrip("/")).exists()


def list_dirs(path: Path) -> List[str]:
    if not path.exists() or not path.is_dir():
        return []
    return sorted(item.name for item in path.iterdir() if item.is_dir())


def available_actions(site_root: Path) -> List[str]:
    action_root = site_root / "simai" / "wizard" / "action"
    actions = []
    for action_file in action_root.glob("*/action.php"):
        actions.append(action_file.parent.name)
    return sorted(actions)


def pick_modules(site_root: Path, solution_code: str, explicit: Optional[List[str]]) -> List[str]:
    modules = list_dirs(site_root / "bitrix" / "modules")
    simai_modules = [item for item in modules if item.startswith("simai.")]
    if explicit:
        return [item for item in explicit if item in modules]
    preferred = []
    solution_candidates = [solution_code]
    if solution_code.endswith(".export"):
        solution_candidates.append(solution_code[: -len(".export")])
    for candidate in solution_candidates:
        if candidate in simai_modules and candidate not in preferred:
            preferred.append(candidate)
    support_priority = [
        "simai.framework",
        "simai.backup",
        "simai.property",
        "simai.property4iblock",
        "simai.bxeditor",
        "simai.filebackup",
    ]
    preferred.extend(item for item in support_priority if item in simai_modules and item not in preferred)
    return preferred


def pick_templates(site_root: Path, explicit: Optional[List[str]]) -> List[str]:
    templates = list_dirs(site_root / "bitrix" / "templates")
    if explicit:
        return [item for item in explicit if item in templates]
    preferred = [item for item in ("simai.framework", ".default") if item in templates]
    if preferred:
        return preferred
    return templates[:3]


def build_copy_rows(site_root: Path, output_dir: str, templates: List[str]) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    if rel_exists(site_root, "/bitrix/components/simai"):
        rows.append(
            {
                "source": "/bitrix/components/simai",
                "destination": f"{output_dir}/install/bitrix/components/simai",
                "name": "Копирование компонентов SIMAI",
            }
        )
    for template in templates:
        rows.append(
            {
                "source": f"/bitrix/templates/{template}",
                "destination": f"{output_dir}/install/bitrix/templates/{template}",
                "name": f"Копирование шаблона {template}",
            }
        )
    if rel_exists(site_root, "/upload/medialibrary"):
        rows.append(
            {
                "source": "/upload/medialibrary",
                "destination": f"{output_dir}/install/ru/root/upload/medialibrary",
                "name": "Копирование медиабиблиотеки",
            }
        )
    return rows


def build_public_copy(site_root: Path, site_dir: str, output_dir: str) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    if site_dir != "/" and rel_exists(site_root, site_dir):
        rows.append(
            {
                "source": site_dir,
                "destination": f"{output_dir}/install/ru/site",
                "name": "Копирование публичных файлов",
            }
        )
    if rel_exists(site_root, "/urlrewrite.php"):
        rows.append(
            {
                "source": "/urlrewrite.php",
                "destination": f"{output_dir}/install/ru/config/urlrewrite.php",
                "name": "Копирование urlrewrite",
            }
        )
    return rows


def default_options(actions: List[str]) -> Dict[str, List[str]]:
    if "option.export.data" not in actions:
        return {}
    return {
        "main": [
            "email_from",
            "site_name",
            "auth_components_template",
            "map_top_menu_type",
            "map_left_menu_type",
        ],
        "fileman": ["menutypes"],
    }


def build_manifest(args: argparse.Namespace, inventory: Dict[str, Any]) -> Dict[str, Any]:
    site_root = Path(args.site_root).expanduser().resolve()
    solution_code = slug_code(args.solution_code)
    site_dir = safe_site_dir(args.site_dir)
    output_dir = args.export_dir or f"/.last_version/{solution_code}"
    if not output_dir.startswith("/"):
        raise ValueError("--export-dir must be site-relative and start with /")

    modules = pick_modules(site_root, solution_code, args.modules)
    templates = pick_templates(site_root, args.templates)
    actions = inventory["wizard_actions"]
    mail_actions_available = "mail.export.data" in actions and "mail-templates.export.data" in actions

    iblocks = args.iblock or []
    data_exports: Dict[str, Any] = {
        "site": "site.export.data" in actions,
        "mail": bool(args.include_mail and "mail.export.data" in actions),
        "mail_templates": bool(args.include_mail and "mail-templates.export.data" in actions),
        "usergroups": args.usergroup if "usergroup.export.data" in actions else [],
        "iblock_types": "iblocktype.export.data" in actions,
        "options": default_options(actions),
    }

    manifest: Dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "solution_code": solution_code,
        "solution_name": args.solution_name or solution_code,
        "source_site_root": str(site_root),
        "description": {
            "name": args.wizard_name or f"Мастер упаковки {solution_code}",
            "storage_code": solution_code.replace(".", "_").replace("-", "_"),
            "primary_color": "#E53935",
            "secondary_color": "#2196F3",
            "background_color": "#263238",
        },
        "export": {
            "output_dir": output_dir.rstrip("/"),
        },
        "modules": modules,
        "copy": build_copy_rows(site_root, output_dir.rstrip("/"), templates),
        "public_copy": build_public_copy(site_root, site_dir, output_dir.rstrip("/")),
        "data_exports": data_exports,
        "iblocks": iblocks,
        "php_interface_snippets": [
            {
                "dir": f"{output_dir.rstrip('/')}/install/ru/php_interface",
                "filename": "dbconn.add.php",
                "text": f'define("SF_SOLUTION","{solution_code}");',
            }
        ],
        "encoding": {
            "win1251": bool(args.win1251),
            "paths": [output_dir.rstrip("/") + "/"],
        },
        "archive": {
            "enabled": bool(args.enable_zip),
            "source": output_dir.rstrip("/"),
            "destination": output_dir.rstrip("/") + ".zip",
        },
        "cleanup": {
            "enabled": False,
            "paths": [output_dir.rstrip("/") + "/"],
        },
    }

    manifest["_inventory_notes"] = {
        "generated_by": "sf4_wizard_export_inventory.py",
        "mail_actions_available": mail_actions_available,
        "mail_requested": bool(args.include_mail),
        "mail_enabled": bool(data_exports["mail"] and data_exports["mail_templates"]),
        "iblock_allowlist_source": "cli" if iblocks else "empty_requires_review",
        "templates_detected": templates,
        "modules_detected": modules,
    }
    return manifest


def inspect_site(args: argparse.Namespace) -> Dict[str, Any]:
    site_root = Path(args.site_root).expanduser().resolve()
    if not site_root.exists():
        raise FileNotFoundError(f"site root not found: {site_root}")
    if not site_root.is_dir():
        raise NotADirectoryError(f"site root is not a directory: {site_root}")

    site_dir = safe_site_dir(args.site_dir)
    modules = list_dirs(site_root / "bitrix" / "modules")
    simai_modules = [item for item in modules if item.startswith("simai.")]
    templates = list_dirs(site_root / "bitrix" / "templates")
    components = list_dirs(site_root / "bitrix" / "components" / "simai")
    actions = available_actions(site_root)
    return {
        "schema_version": SCHEMA_VERSION,
        "operation_id": "sf4.wizard.export_inventory",
        "mode": {
            "read_only": True,
            "writes": "source_output_only",
            "executes_php": False,
            "executes_bitrix": False,
            "executes_wizard_actions": False,
        },
        "site_root": str(site_root),
        "site_dir": site_dir,
        "exists": {
            "bitrix_modules": (site_root / "bitrix" / "modules").is_dir(),
            "simai_components": (site_root / "bitrix" / "components" / "simai").is_dir(),
            "templates": (site_root / "bitrix" / "templates").is_dir(),
            "site_dir": rel_exists(site_root, site_dir),
            "media_library": rel_exists(site_root, "/upload/medialibrary"),
            "urlrewrite": rel_exists(site_root, "/urlrewrite.php"),
            "wizard_actions": (site_root / "simai" / "wizard" / "action").is_dir(),
        },
        "simai_modules": simai_modules,
        "simai_components": components,
        "templates": templates,
        "wizard_actions": actions,
        "action_capabilities": {
            "site_export": "site.export.data" in actions,
            "mail_export": "mail.export.data" in actions,
            "mail_templates_export": "mail-templates.export.data" in actions,
            "usergroup_export": "usergroup.export.data" in actions,
            "iblocktype_export": "iblocktype.export.data" in actions,
            "option_export": "option.export.data" in actions,
            "data_export_file": "data.export.file" in actions,
            "iblock_export_archive": "iblock.export.archive" in actions,
            "file_copy": "file.copy" in actions,
            "file_create": "file.create" in actions,
            "file_encode_win1251": "file.encode.win1251" in actions,
            "file_zip": "file.zip" in actions,
        },
    }


def run_command(command: List[str], cwd: Path) -> Dict[str, Any]:
    proc = subprocess.run(command, cwd=str(cwd), text=True, capture_output=True, check=False)
    return {
        "command": command,
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
    }


def write_json(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def generate(args: argparse.Namespace) -> Dict[str, Any]:
    root = repo_root()
    solution_code = slug_code(args.solution_code)
    output_root = ensure_safe_output(Path(args.output_dir or root / "source" / "output" / "wizard-export-inventory"), root)
    package_root = output_root / solution_code
    package_root.mkdir(parents=True, exist_ok=True)

    inventory = inspect_site(args)
    manifest = build_manifest(args, inventory)
    inventory_path = package_root / "inventory.json"
    manifest_path = package_root / "manifest.draft.json"
    write_json(inventory_path, inventory)
    write_json(manifest_path, manifest)

    report: Dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "operation_id": "sf4.wizard.export_inventory.run",
        "mode": inventory["mode"],
        "solution_code": solution_code,
        "package_root": str(package_root),
        "inventory": str(inventory_path),
        "manifest": str(manifest_path),
        "builder_report": None,
        "audit_report": None,
        "readiness_report": None,
        "commands": [],
        "status": "inventory_ready",
    }

    if args.run_builder:
        builder_cmd = [
            sys.executable,
            "scripts/sf4_wizard_export_builder.py",
            "--manifest",
            str(manifest_path),
            "--output-dir",
            str(root / "source" / "output" / "wizard-export-inventory" / solution_code / "builder"),
            "--force",
            "--json",
        ]
        builder_result = run_command(builder_cmd, root)
        report["commands"].append(builder_result)
        if builder_result["returncode"] != 0:
            report["status"] = "builder_failed"
            write_json(package_root / "run-report.json", report)
            return report

        builder_package = package_root / "builder" / solution_code
        builder_report = builder_package / "builder-report.json"
        master = builder_package / "master" / solution_code
        audit_path = package_root / "audit.json"
        readiness_path = package_root / "readiness.json"
        readiness_md = package_root / "readiness.md"
        report["builder_report"] = str(builder_report)

        audit_cmd = [
            sys.executable,
            "scripts/sf4_wizard_audit.py",
            "--site-root",
            str(Path(args.site_root).expanduser().resolve()),
            "--master",
            str(master),
            "--json",
            str(audit_path),
        ]
        audit_result = run_command(audit_cmd, root)
        report["commands"].append(audit_result)
        report["audit_report"] = str(audit_path)

        readiness_cmd = [
            sys.executable,
            "scripts/sf4_wizard_readiness.py",
            "--audit",
            str(audit_path),
            "--label",
            solution_code,
            "--json",
            str(readiness_path),
            "--markdown",
            str(readiness_md),
        ]
        readiness_result = run_command(readiness_cmd, root)
        report["commands"].append(readiness_result)
        report["readiness_report"] = str(readiness_path)

        report["status"] = "chain_complete" if audit_result["returncode"] in (0, 1) and readiness_result["returncode"] in (0, 1) else "chain_attention"

    write_json(package_root / "run-report.json", report)
    return report


def main() -> int:
    root = repo_root()
    parser = argparse.ArgumentParser(description="Read-only inventory helper for SF4 wizard export packaging.")
    parser.add_argument("--site-root", required=True, help="Local Bitrix/SF4 source site root")
    parser.add_argument("--solution-code", required=True, help="Solution/master code")
    parser.add_argument("--solution-name", help="Human-readable solution name")
    parser.add_argument("--wizard-name", help="Wizard display name")
    parser.add_argument("--site-dir", default="/ru", help="Public site dir, default /ru")
    parser.add_argument("--export-dir", help="Site-relative output dir, default /.last_version/<solution-code>")
    parser.add_argument("--module", dest="modules", action="append", help="Explicit module allowlist item")
    parser.add_argument("--template", dest="templates", action="append", help="Explicit template allowlist item")
    parser.add_argument("--iblock", action="append", help="Iblock code allowlist item; repeatable")
    parser.add_argument("--usergroup", action="append", default=["user_editor"], help="User group code allowlist item")
    parser.add_argument("--include-mail", action="store_true", help="Enable mail export only if actions exist")
    parser.add_argument("--win1251", action="store_true", help="Enable file.encode.win1251 stage")
    parser.add_argument("--enable-zip", action="store_true", help="Add final file.zip action; still not executed")
    parser.add_argument("--run-builder", action="store_true", help="Run builder, audit and readiness proposal chain")
    parser.add_argument(
        "--output-dir",
        default=str(root / "source" / "output" / "wizard-export-inventory"),
        help="Output directory. Must be inside source/output.",
    )
    parser.add_argument("--json", dest="json_only", action="store_true", help="Print JSON report only")
    args = parser.parse_args()

    try:
        report = generate(args)
    except Exception as exc:  # noqa: BLE001 - CLI should report exact failure.
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.json_only:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print("SF4 Wizard Export Inventory")
        print(f"Status: {report['status']}")
        print(f"Package: {report['package_root']}")
        print(f"Manifest: {report['manifest']}")
    return 0 if report["status"] in {"inventory_ready", "chain_complete"} else 1


if __name__ == "__main__":
    sys.exit(main())

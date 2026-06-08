#!/usr/bin/env python3
"""
Read-only audit for SF4 universal wizard masters.

The script deliberately does not execute Bitrix, wizard actions, PHP imports,
database writes or filesystem-changing wizard operations. It statically reads
wizard config/source files and reports high-signal structural and payload risks.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


SCHEMA_VERSION = "1.0.0"

RISK_BY_ACTION = {
    "agreement": "read_only",
    "dir.choice": "read_only",
    "info": "read_only",
    "install.check": "read_only",
    "language.choice": "read_only",
    "site.choice": "read_only",
    "site.choice.install": "read_only",
    "site.choice.sveden": "read_only",
    "translate.check": "read_only",
    "iblock.export.archive": "read_only",
    "site.export.data": "read_only",
    "mail.export.data": "read_only",
    "mail-templates.export.data": "read_only",
    "usergroup.export.data": "read_only",
    "iblocktype.export.data": "read_only",
    "option.export.data": "read_only",
    "shortlink.export.data": "read_only",
    "file.copy": "filesystem_write",
    "file.create": "filesystem_write",
    "data.export.file": "filesystem_write",
    "file.delete": "filesystem_write",
    "file.encode.win1251": "filesystem_write",
    "file.rename": "filesystem_write",
    "file.unzip": "filesystem_write",
    "file.zip": "filesystem_write",
    "replace.code": "filesystem_write",
    "restore.names": "filesystem_write",
    "cut.names": "filesystem_write",
    "dir.make": "filesystem_write",
    "data.add.config": "db_write",
    "data.add.property": "db_write",
    "data.import.file": "db_write",
    "iblock.import.archive": "db_write",
    "iblock.import.archive.sveden": "db_write",
    "iblock.translate": "db_write",
    "iblockconfig.import.data": "filesystem_write",
    "iblocksection.import.data": "db_write",
    "iblocktype.import.data": "db_write",
    "option.import.data": "db_write",
    "prepare.urlrewrite": "filesystem_write",
    "shortlink.import.data": "db_write",
    "site.create": "db_write",
    "site.import.data": "db_write",
    "site.translate": "db_write",
    "site.update": "db_write",
    "site.update.sveden": "db_write",
    "urlrewrite.add": "db_write",
    "usergroup.import.data": "db_write",
}

REQUIREMENTS_BY_ACTION = {
    "file.copy": ["admin", "simai.framework"],
    "file.rename": ["admin", "simai.framework"],
    "file.unzip": ["admin", "simai.framework", "ZipArchive"],
    "file.zip": ["admin", "simai.framework", "ZipArchive"],
    "replace.code": ["admin", "simai.framework"],
    "iblock.import.archive": ["admin", "simai.framework", "iblock", "XMLReader", "ZipArchive"],
    "iblock.import.archive.sveden": [
        "admin",
        "simai.framework",
        "iblock",
        "XMLReader",
        "ZipArchive",
    ],
    "iblock.export.archive": ["admin", "simai.framework", "iblock", "XMLReader", "ZipArchive"],
    "site.export.data": ["admin", "simai.framework"],
    "mail.export.data": ["admin", "simai.framework"],
    "mail-templates.export.data": ["admin", "simai.framework"],
    "usergroup.export.data": ["admin", "simai.framework"],
    "iblocktype.export.data": ["admin", "simai.framework", "iblock"],
    "option.export.data": ["admin", "simai.framework"],
    "shortlink.export.data": ["admin", "simai.framework"],
    "data.export.file": ["admin", "simai.framework"],
    "iblockconfig.import.data": ["admin", "simai.framework", "iblock"],
    "iblocktype.import.data": ["admin", "simai.framework", "iblock"],
    "option.import.data": ["admin", "simai.framework"],
    "urlrewrite.add": ["admin", "simai.framework"],
    "site.update": ["admin", "simai.framework"],
    "site.update.sveden": ["admin", "simai.framework"],
}

PATH_KEYS = {
    "source",
    "destination",
    "config",
    "lang",
    "tmp",
    "file",
    "logo",
    "image",
}

OUTPUT_FILE_ACTIONS = {
    "data.export.file",
    "file.create",
    "file.zip",
}


@dataclass
class Finding:
    severity: str
    code: str
    message: str
    path: Optional[str] = None
    action: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        item = {
            "severity": self.severity,
            "code": self.code,
            "message": self.message,
        }
        if self.path:
            item["path"] = self.path
        if self.action:
            item["action"] = self.action
        return item


def add_finding(
    findings: List[Finding],
    severity: str,
    code: str,
    message: str,
    path: Optional[Path | str] = None,
    action: Optional[str] = None,
) -> None:
    findings.append(
        Finding(
            severity=severity,
            code=code,
            message=message,
            path=str(path) if path is not None else None,
            action=action,
        )
    )


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def strip_comments(text: str) -> str:
    return re.sub(r"/\*.*?\*/", "", text, flags=re.S)


def find_matching(text: str, open_index: int, opener: str = "(", closer: str = ")") -> int:
    depth = 0
    quote: Optional[str] = None
    escape = False
    for idx in range(open_index, len(text)):
        ch = text[idx]
        if quote:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == quote:
                quote = None
            continue
        if ch in ("'", '"'):
            quote = ch
            continue
        if ch == opener:
            depth += 1
        elif ch == closer:
            depth -= 1
            if depth == 0:
                return idx
    return -1


def extract_named_array(text: str, key: str) -> Optional[str]:
    pattern = re.compile(rf"""['"]{re.escape(key)}['"]\s*=>\s*array\s*\(""", re.I)
    match = pattern.search(text)
    if not match:
        return None
    open_index = text.find("(", match.end() - 1)
    close_index = find_matching(text, open_index)
    if close_index == -1:
        return None
    return text[open_index + 1 : close_index]


def iter_top_level_arrays(block: str) -> Iterable[str]:
    idx = 0
    while idx < len(block):
        match = re.search(r"\barray\s*\(", block[idx:], flags=re.I)
        if not match:
            break
        start = idx + match.start()
        open_index = block.find("(", start)
        if nesting_depth(block, start) != 0:
            idx = open_index + 1
            continue
        close_index = find_matching(block, open_index)
        if close_index == -1:
            break
        yield block[open_index + 1 : close_index]
        idx = close_index + 1


def nesting_depth(text: str, position: int) -> int:
    depth = 0
    quote: Optional[str] = None
    escape = False
    idx = 0
    while idx < position:
        ch = text[idx]
        if quote:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == quote:
                quote = None
            idx += 1
            continue
        if ch in ("'", '"'):
            quote = ch
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        idx += 1
    return depth


def split_top_level_arrays(block: str) -> List[str]:
    """Return array(...) items declared directly inside a PHP array block."""
    items: List[str] = []
    idx = 0
    while idx < len(block):
        match = re.search(r"\barray\s*\(", block[idx:], flags=re.I)
        if not match:
            break
        start = idx + match.start()
        open_index = block.find("(", start)
        depth_before = nesting_depth(block, start)
        close_index = find_matching(block, open_index)
        if close_index == -1:
            break
        if depth_before == 0:
            items.append(block[open_index + 1 : close_index])
        idx = close_index + 1
    return items


def extract_scalar(block: str, key: str) -> Optional[str]:
    patterns = [
        rf"""['"]{re.escape(key)}['"]\s*=>\s*['"]([^'"]*)['"]""",
        rf"""{re.escape(key)}\s*=>\s*['"]([^'"]*)['"]""",
    ]
    for pattern in patterns:
        match = re.search(pattern, block, flags=re.I)
        if match:
            return match.group(1)
    return None


def extract_expression(block: str, key: str) -> Optional[str]:
    pattern = re.compile(rf"""['"]{re.escape(key)}['"]\s*=>\s*([^,\n\r]+(?:\.[^,\n\r]+)*)""", re.I)
    match = pattern.search(block)
    if match:
        return match.group(1).strip()
    return None


def extract_path_expressions(block: str) -> List[Dict[str, str]]:
    results: List[Dict[str, str]] = []
    pattern = re.compile(
        r"""['"](?P<key>source|destination|config|lang|tmp|file|logo|image)['"]\s*=>\s*(?P<expr>[^,\n\r]+(?:\.[^,\n\r]+)*)""",
        re.I,
    )
    for match in pattern.finditer(block):
        results.append({"key": match.group("key").lower(), "expr": match.group("expr").strip()})
    return results


def normalize_site_root(path: Optional[str], master: Optional[Path], config: Optional[Path]) -> Path:
    if path:
        return Path(path).expanduser().resolve()
    for candidate in (master, config):
        if candidate:
            parts = candidate.resolve().parts
            needle = ("simai", "wizard", "master")
            for idx in range(0, len(parts) - len(needle) + 1):
                if parts[idx : idx + len(needle)] == needle:
                    return Path(*parts[:idx]).resolve()
    return Path.cwd().resolve()


def resolve_master(raw: Optional[str], site_root: Path) -> Optional[Path]:
    if not raw:
        return None
    path = Path(raw).expanduser()
    if path.is_absolute():
        return path.resolve()
    return (site_root / raw.lstrip("/")).resolve()


def resolve_config(raw: Optional[str], master: Optional[Path], site_root: Path) -> Optional[Path]:
    if raw:
        path = Path(raw).expanduser()
        if path.is_absolute():
            return path.resolve()
        return (site_root / raw.lstrip("/")).resolve()
    if master:
        return (master / ".wizard.config.php").resolve()
    return None


def expression_to_path(expr: str, config_dir: Path, site_root: Path) -> Tuple[Optional[Path], str]:
    if "#" in expr:
        return None, "runtime_placeholder"

    expr = expr.strip()
    strings = re.findall(r"""['"]([^'"]*)['"]""", expr)
    if not strings:
        return None, "unresolved_expression"

    if "Wizard::getLocal(__DIR__)" in expr or "__DIR__" in expr:
        suffix = "".join(strings)
        return (config_dir / suffix.lstrip("/")).resolve(), "deterministic"

    value = "".join(strings)
    if "#" in value:
        return None, "runtime_placeholder"
    if value.startswith("/"):
        return (site_root / value.lstrip("/")).resolve(), "deterministic"
    return (config_dir / value).resolve(), "deterministic"


def inspect_zip(path: Path) -> Dict[str, Any]:
    result: Dict[str, Any] = {
        "path": str(path),
        "is_zip": False,
        "can_open": False,
        "xml_entries": [],
        "entries_count": 0,
    }
    if path.suffix.lower() != ".zip":
        return result
    result["is_zip"] = True
    try:
        with zipfile.ZipFile(path) as zf:
            names = zf.namelist()
            result["can_open"] = True
            result["entries_count"] = len(names)
            result["xml_entries"] = [name for name in names if name.lower().endswith(".xml")][:20]
    except Exception as exc:  # noqa: BLE001 - report arbitrary zip failures.
        result["error"] = str(exc)
    return result


def classify_risk(action_code: str) -> str:
    return RISK_BY_ACTION.get(action_code, "unknown")


def requirements_for(action_code: str) -> List[str]:
    return REQUIREMENTS_BY_ACTION.get(action_code, ["admin", "simai.framework"])


def detect_installer_bridge(module_root: Optional[Path], findings: List[Finding]) -> Dict[str, Any]:
    if not module_root:
        return {"provided": False}
    module_root = module_root.resolve()
    install_index = module_root / "install" / "index.php"
    result: Dict[str, Any] = {
        "provided": True,
        "module_root": str(module_root),
        "install_index": str(install_index),
        "install_index_exists": install_index.exists(),
        "signals": {},
    }
    if not install_index.exists():
        add_finding(findings, "warning", "missing_install_index", "Module install/index.php not found", install_index)
        return result

    text = read_text(install_index)
    signal_patterns = {
        "copy_dir_files": r"CopyDirFiles\s*\(",
        "runtime_master_data": r"/simai/wizard/master/.+?/data|/simai/wizard/master/",
        "install_wizard_data": r"install/wizard/data",
        "install_bitrix": r"install/bitrix",
        "install_ru_config": r"install/ru/config",
        "install_iblock": r"install/iblock",
        "install_php_interface": r"install/ru/php_interface",
        "install_ru_root": r"install/ru/root",
        "install_ru_site": r"install/ru/site",
        "config_zip": r"config\.zip",
        "medialibrary_zip": r"medialibrary\.zip",
        "module_zip": r"data/module|module/.+?\.zip",
        "wrapper_wizard_copy": r"/bitrix/wizards/simai/",
        "master_redirect": r"LocalRedirect\s*\(.+?/simai/wizard/master/",
    }
    result["signals"] = {
        key: bool(re.search(pattern, text, flags=re.I | re.S))
        for key, pattern in signal_patterns.items()
    }
    if not result["signals"]["runtime_master_data"]:
        add_finding(
            findings,
            "warning",
            "installer_no_runtime_master_signal",
            "install/index.php does not clearly assemble /simai/wizard/master data",
            install_index,
        )
    return result


def parse_actions(config_text: str) -> List[Dict[str, Any]]:
    actions_block = extract_named_array(config_text, "action")
    if actions_block is None:
        return []
    actions: List[Dict[str, Any]] = []
    for idx, item in enumerate(split_top_level_arrays(actions_block), start=1):
        code = extract_scalar(item, "code") or ""
        action = {
            "index": idx,
            "code": code,
            "name": extract_scalar(item, "name"),
            "data_input_code": extract_scalar(item, "data_input_code"),
            "data_output_code": extract_scalar(item, "data_output_code"),
            "autocomplete": extract_scalar(item, "autocomplete"),
            "has_condition": bool(re.search(r"""['"]condition['"]\s*=>\s*array\s*\(""", item, re.I)),
            "path_expressions": extract_path_expressions(item),
            "raw_snippet_length": len(item),
        }
        actions.append(action)
    return actions


def parse_description(config_text: str) -> Dict[str, Any]:
    block = extract_named_array(config_text, "description") or ""
    background = extract_named_array(block, "background") or ""
    color = extract_named_array(block, "color") or ""
    modifier = extract_named_array(block, "modifier") or ""
    return {
        "name": extract_scalar(block, "name"),
        "code": extract_scalar(block, "code"),
        "stage_renew": extract_scalar(block, "stage_renew"),
        "logo_expr": extract_expression(block, "logo"),
        "background_image_expr": extract_expression(background, "image"),
        "background_color": extract_scalar(background, "color"),
        "primary_color": extract_scalar(color, "primary"),
        "secondary_color": extract_scalar(color, "secondary"),
        "modifier_keys": sorted(set(re.findall(r"""['"]([^'"]+)['"]\s*=>""", modifier))),
        "exists": bool(block),
    }


def action_resolution(
    action_code: str,
    master: Optional[Path],
    site_root: Path,
) -> Dict[str, Any]:
    local = master / "action" / action_code / "action.php" if master else None
    global_path = site_root / "simai" / "wizard" / "action" / action_code / "action.php"
    resolved = None
    source = None
    if local and local.exists():
        resolved = local
        source = "master-local"
    elif global_path.exists():
        resolved = global_path
        source = "global"
    return {
        "local": str(local) if local else None,
        "global": str(global_path),
        "resolved": str(resolved) if resolved else None,
        "source": source,
    }


def audit(args: argparse.Namespace) -> Dict[str, Any]:
    findings: List[Finding] = []
    initial_master = Path(args.master).expanduser().resolve() if args.master else None
    initial_config = Path(args.config).expanduser().resolve() if args.config else None
    site_root = normalize_site_root(args.site_root, initial_master, initial_config)
    master = resolve_master(args.master, site_root)
    config = resolve_config(args.config, master, site_root)
    module_root = Path(args.module_root).expanduser().resolve() if args.module_root else None

    result: Dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "operation_id": "sf4.wizard.audit",
        "site_root": str(site_root),
        "master": str(master) if master else None,
        "config": str(config) if config else None,
        "module_root": str(module_root) if module_root else None,
        "mode": {
            "read_only": True,
            "executes_php": False,
            "executes_wizard_actions": False,
            "writes": "json_report_only" if args.json else "none",
            "strict_live": bool(args.strict_live),
        },
        "master_checks": {},
        "description": {},
        "actions": [],
        "installer_bridge": {},
        "findings": [],
        "summary": {},
        "status": "ready",
    }

    if not master and not config and not module_root:
        add_finding(findings, "error", "missing_target", "Provide --master or --config")
    if master:
        result["master_checks"] = {
            "index_exists": (master / "index.php").exists(),
            "config_exists": (master / ".wizard.config.php").exists(),
            "data_exists": (master / "data").exists(),
            "image_dir_exists": (master / "image").exists(),
            "action_dir_exists": (master / "action").exists(),
        }
        if not (master / "index.php").exists():
            add_finding(findings, "error", "missing_master_index", "Master index.php not found", master / "index.php")
        if not (master / ".wizard.config.php").exists() and not args.config:
            add_finding(
                findings,
                "error",
                "missing_master_config",
                "Master .wizard.config.php not found",
                master / ".wizard.config.php",
            )
        if not (master / "data").exists():
            add_finding(findings, "warning", "missing_master_data", "Master data/ directory not found", master / "data")

    config_text = ""
    if config and config.exists():
        config_text = strip_comments(read_text(config))
    elif config:
        add_finding(findings, "error", "missing_config", "Wizard config file not found", config)

    if config_text:
        description = parse_description(config_text)
        result["description"] = description
        config_dir = config.parent
        if not description.get("exists"):
            add_finding(findings, "error", "missing_description", "Config has no description array", config)
        if not description.get("code"):
            add_finding(findings, "error", "missing_description_code", "description.code is missing", config)

        for key in ("logo_expr", "background_image_expr"):
            expr = description.get(key)
            if not expr:
                continue
            resolved, mode = expression_to_path(expr, config_dir, site_root)
            description[key.replace("_expr", "_path")] = str(resolved) if resolved else None
            description[key.replace("_expr", "_resolution")] = mode
            if resolved and not resolved.exists():
                add_finding(
                    findings,
                    "warning",
                    "missing_visual_asset",
                    f"{key} does not resolve to an existing file",
                    resolved,
                )

        actions = parse_actions(config_text)
        if not actions:
            add_finding(findings, "error", "missing_actions", "Config has no action array or no parseable actions", config)

        produced_outputs: set[str] = set()
        for action in actions:
            code = action["code"]
            if not code:
                add_finding(findings, "error", "missing_action_code", "Action entry has no code", config)
                continue

            if action.get("data_input_code") and action["data_input_code"] not in produced_outputs:
                # Common external/site-choice inputs are allowed but should stay visible.
                if action["data_input_code"] not in {"site_config"}:
                    add_finding(
                        findings,
                        "warning",
                        "unresolved_data_input",
                        f"DATA_INPUT_CODE '{action['data_input_code']}' has no earlier DATA_OUTPUT_CODE",
                        action=code,
                    )

            if action.get("data_output_code"):
                produced_outputs.add(action["data_output_code"])

            resolution = action_resolution(code, master, site_root)
            if not resolution["resolved"]:
                add_finding(
                    findings,
                    "error",
                    "missing_action_file",
                    f"Action '{code}' does not resolve to master-local or global action.php",
                    action=code,
                )

            path_checks = []
            for item in action["path_expressions"]:
                resolved, mode = expression_to_path(item["expr"], config_dir, site_root)
                check: Dict[str, Any] = {
                    "key": item["key"],
                    "expr": item["expr"],
                    "resolution": mode,
                    "path": str(resolved) if resolved else None,
                    "exists": resolved.exists() if resolved else None,
                }
                input_path_keys = {"source", "config", "lang", "file"}
                if action["code"] in OUTPUT_FILE_ACTIONS:
                    input_path_keys.discard("file")
                if resolved and item["key"] in input_path_keys and not resolved.exists():
                    add_finding(
                        findings,
                        "error",
                        "missing_payload",
                        f"Payload path for {item['key']} does not exist",
                        resolved,
                        action=code,
                    )
                if resolved and resolved.suffix.lower() == ".zip":
                    zip_info = inspect_zip(resolved)
                    check["zip"] = zip_info
                    if not zip_info.get("can_open"):
                        add_finding(findings, "error", "invalid_zip", "Zip payload cannot be opened", resolved, code)
                    elif not zip_info.get("xml_entries") and code.startswith("iblock."):
                        add_finding(
                            findings,
                            "warning",
                            "zip_without_xml",
                            "Iblock archive zip has no XML entries in the sampled listing",
                            resolved,
                            code,
                        )
                path_checks.append(check)

            action["resolution"] = resolution
            action["risk"] = classify_risk(code)
            action["requirements"] = requirements_for(code)
            action["path_checks"] = path_checks
            action.pop("raw_snippet_length", None)
            result["actions"].append(action)

    result["installer_bridge"] = detect_installer_bridge(module_root, findings)

    severity_order = {"error": 3, "warning": 2, "info": 1}
    errors = sum(1 for item in findings if item.severity == "error")
    warnings = sum(1 for item in findings if item.severity == "warning")
    high_risk = sum(
        1
        for action in result["actions"]
        if action.get("risk") in {"db_write", "global_runtime_write", "filesystem_write"}
    )
    missing_actions = sum(1 for item in findings if item.code == "missing_action_file")
    missing_payloads = sum(1 for item in findings if item.code == "missing_payload")
    result["summary"] = {
        "actions": len(result["actions"]),
        "findings": len(findings),
        "errors": errors,
        "warnings": warnings,
        "missing_actions": missing_actions,
        "missing_payloads": missing_payloads,
        "high_risk_side_effects": high_risk,
    }
    if errors:
        result["status"] = "blocked"
    elif warnings:
        result["status"] = "warning"
    else:
        result["status"] = "ready"
    result["findings"] = [
        item.to_dict()
        for item in sorted(findings, key=lambda x: (-severity_order.get(x.severity, 0), x.code, x.message))
    ]
    return result


def print_summary(report: Dict[str, Any]) -> None:
    print("SF4 Wizard Audit")
    print(f"Status: {report['status']}")
    print(f"Site root: {report['site_root']}")
    print(f"Master: {report.get('master') or '-'}")
    print(f"Config: {report.get('config') or '-'}")
    summary = report["summary"]
    print(
        "Summary: "
        f"actions={summary['actions']} "
        f"errors={summary['errors']} "
        f"warnings={summary['warnings']} "
        f"missing_actions={summary['missing_actions']} "
        f"missing_payloads={summary['missing_payloads']} "
        f"high_risk={summary['high_risk_side_effects']}"
    )
    if report["findings"]:
        print("\nFindings:")
        for item in report["findings"][:80]:
            path = f" path={item['path']}" if item.get("path") else ""
            action = f" action={item['action']}" if item.get("action") else ""
            print(f"- [{item['severity']}] {item['code']}: {item['message']}{action}{path}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only audit for SF4 universal wizard masters.")
    parser.add_argument("--site-root", help="Bitrix/SF4 site root. Inferred from --master when omitted.")
    parser.add_argument("--master", help="Runtime master path, absolute or relative to site root.")
    parser.add_argument("--config", help="Standalone .wizard.config.php path.")
    parser.add_argument("--module-root", help="Optional Bitrix module root for install/index.php bridge audit.")
    parser.add_argument("--strict-live", action="store_true", help="Reserve stricter live checks for future use.")
    parser.add_argument("--json", dest="json", help="Optional JSON report output path.")
    parser.add_argument("--json-out", dest="json", help="Alias for --json.")
    parser.add_argument("--quiet", action="store_true", help="Do not print human summary.")
    args = parser.parse_args()

    report = audit(args)

    if args.json:
        out_path = Path(args.json).expanduser().resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    if not args.quiet:
        print_summary(report)

    return 2 if report["status"] == "blocked" else 0


if __name__ == "__main__":
    sys.exit(main())

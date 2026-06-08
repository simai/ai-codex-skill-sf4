#!/usr/bin/env python3
"""
Read-only iblock/HL manifest assistant for SF4 universal wizard packaging.

The assistant inspects local archive/config/legacy data structures and proposes
explicit manifest entries for review. It never executes PHP, Bitrix, wizard
actions, imports, exports or writes outside source/output.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional


SCHEMA_VERSION = "1.0.0"
LEGACY_FILES = {
    "types.php",
    "iblocks.php",
    "props.php",
    "sections.php",
    "elements.php",
    "fields.php",
    "forms.php",
    "seo.php",
    "highload.php",
    "highloadprops.php",
    "highloadelems.php",
}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def ensure_source_output(path: Path) -> Path:
    root = repo_root()
    resolved = path.expanduser().resolve()
    allowed = (root / "source" / "output").resolve()
    if allowed not in [resolved, *resolved.parents]:
        raise ValueError(f"output path must be inside {allowed}")
    return resolved


def safe_slug(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9_.-]+", "-", value.strip())
    return value.strip("-") or "iblock-manifest"


def rel(path: Path, base: Path) -> str:
    try:
        return str(path.resolve().relative_to(base.resolve()))
    except ValueError:
        return str(path.resolve())


def read_text_lossy(path: Path) -> str:
    for encoding in ("utf-8", "cp1251", "latin-1"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_bytes().decode("utf-8", errors="replace")


def zip_members(path: Path, limit: int = 30) -> Dict[str, Any]:
    if not zipfile.is_zipfile(path):
        return {
            "valid_zip": False,
            "member_count": 0,
            "sample_members": [],
            "has_export_xml": False,
            "has_highload_hint": False,
        }
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
    lowered = [name.lower() for name in names]
    return {
        "valid_zip": True,
        "member_count": len(names),
        "sample_members": names[:limit],
        "has_export_xml": any(name.endswith("export.xml") for name in lowered),
        "has_highload_hint": any("highload" in name or "hlblock" in name or "hlbd" in name for name in lowered),
    }


def discover_archives(source: Path) -> List[Dict[str, Any]]:
    archives: List[Dict[str, Any]] = []
    for path in sorted(source.rglob("*.zip")):
        parts = {part.lower() for part in path.parts}
        parent_names = {part.lower() for part in path.parent.parts}
        filename_code = path.stem
        kind = "other_zip"
        if "iblock" in parent_names or "iblock" in parts:
            kind = "iblock_archive"
        elif "highload" in parent_names or "highload" in parts or "hl" in filename_code.lower():
            kind = "highload_archive"
        elif filename_code.startswith("sf-") or filename_code.startswith("form-"):
            kind = "iblock_archive_candidate"
        info = zip_members(path)
        if info["has_highload_hint"]:
            kind = "highload_archive"
        archives.append(
            {
                "kind": kind,
                "code": filename_code,
                "path": str(path.resolve()),
                "relative_path": rel(path, source),
                "valid_zip": info["valid_zip"],
                "member_count": info["member_count"],
                "sample_members": info["sample_members"],
                "has_export_xml": info["has_export_xml"],
                "has_highload_hint": info["has_highload_hint"],
            }
        )
    return archives


def extract_legacy_iblocks(text: str) -> List[Dict[str, Any]]:
    items: List[Dict[str, Any]] = []
    for block in re.finditer(r"Array\s*\((.*?)\)\s*,", text, flags=re.S):
        body = block.group(1)
        code_match = re.search(r'"CODE"\s*=>\s*"([^"]+)"', body)
        type_match = re.search(r'"IBLOCK_TYPE_ID"\s*=>\s*"([^"]+)"', body)
        name_match = re.search(r'"NAME"\s*=>\s*"([^"]+)"', body)
        if not code_match:
            continue
        items.append(
            {
                "code": code_match.group(1),
                "iblock_type": type_match.group(1) if type_match else None,
                "name": name_match.group(1) if name_match else None,
            }
        )
    return dedupe_by_key(items, "code")


def extract_legacy_highload(text: str) -> List[Dict[str, Any]]:
    items: List[Dict[str, Any]] = []
    for block in re.finditer(r"array\s*\((.*?)\)", text, flags=re.S | re.I):
        body = block.group(1)
        name_match = re.search(r"['\"]NAME['\"]\s*=>\s*['\"]([^'\"]+)['\"]", body)
        table_match = re.search(r"['\"]TABLE_NAME['\"]\s*=>\s*['\"]([^'\"]+)['\"]", body)
        if not name_match and not table_match:
            continue
        items.append(
            {
                "name": name_match.group(1) if name_match else None,
                "table_name": table_match.group(1) if table_match else None,
            }
        )
    key = "table_name" if any(item.get("table_name") for item in items) else "name"
    return dedupe_by_key(items, key)


def extract_config_codes(text: str) -> List[str]:
    # SF4 .iblock.config.php usually maps iblock codes as top-level quoted keys.
    candidates: List[str] = []
    for match in re.finditer(r'^([ \t]*)["\']([A-Za-z0-9_.-]+)["\'][ \t]*=>[ \t]*array\s*\(', text, flags=re.M):
        indent, code = match.groups()
        # Keep only shallow keys. Nested sections/properties in SF4 config files
        # are not iblock codes and would make the allowlist noisy.
        if indent.count("\t") > 1:
            continue
        if "\t" not in indent and len(indent) > 4:
            continue
        if code != code.lower():
            continue
        candidates.append(code)
    ignored = {
        "main",
        "preview",
        "detail",
        "additional",
        "section",
        "property",
        "name",
    }
    return sorted({item for item in candidates if item.lower() not in ignored})


def discover_legacy_data(source: Path) -> List[Dict[str, Any]]:
    found: List[Dict[str, Any]] = []
    for path in sorted(source.rglob("*.php")):
        if path.name not in LEGACY_FILES and not path.name.endswith(".config.php"):
            continue
        text = read_text_lossy(path)
        entry: Dict[str, Any] = {
            "path": str(path.resolve()),
            "relative_path": rel(path, source),
            "filename": path.name,
            "iblocks": [],
            "highload": [],
            "config_codes": [],
        }
        if path.name == "iblocks.php":
            entry["iblocks"] = extract_legacy_iblocks(text)
        elif path.name == "highload.php":
            entry["highload"] = extract_legacy_highload(text)
        elif path.name.endswith(".config.php"):
            entry["config_codes"] = extract_config_codes(text)
        else:
            entry["signal"] = "legacy_support_file"
        if entry["iblocks"] or entry["highload"] or entry["config_codes"] or entry.get("signal"):
            found.append(entry)
    return found


def dedupe_by_key(items: Iterable[Dict[str, Any]], key: str) -> List[Dict[str, Any]]:
    seen = set()
    result = []
    for item in items:
        value = item.get(key)
        if not value or value in seen:
            continue
        seen.add(value)
        result.append(item)
    return result


def build_manifest_entries(archives: List[Dict[str, Any]], legacy: List[Dict[str, Any]]) -> Dict[str, Any]:
    archive_iblocks = [
        item
        for item in archives
        if item["kind"] in {"iblock_archive", "iblock_archive_candidate"} and item["valid_zip"]
    ]
    legacy_iblocks: List[Dict[str, Any]] = []
    highload: List[Dict[str, Any]] = []
    config_codes: List[str] = []
    for item in legacy:
        legacy_iblocks.extend(item.get("iblocks") or [])
        highload.extend(item.get("highload") or [])
        config_codes.extend(item.get("config_codes") or [])

    iblock_codes = sorted(
        {
            *[item["code"] for item in archive_iblocks],
            *[item["code"] for item in legacy_iblocks],
        }
    )
    config_only = sorted(set(config_codes) - set(iblock_codes))
    return {
        "iblocks": iblock_codes,
        "iblock_entries": [
            {
                "code": item["code"],
                "source": "archive",
                "archive": item["relative_path"],
                "has_export_xml": item["has_export_xml"],
            }
            for item in archive_iblocks
        ]
        + [
            {
                "code": item["code"],
                "source": "legacy_php_array",
                "iblock_type": item.get("iblock_type"),
                "name": item.get("name"),
            }
            for item in legacy_iblocks
        ],
        "highload_entries": dedupe_by_key(highload, "table_name"),
        "config_only_codes": config_only,
        "review_notes": [
            "iblocks is an explicit allowlist draft for sf4_wizard_export_builder.py",
            "config_only_codes are not added to iblocks automatically; confirm matching real iblock codes first",
            "highload_entries require a dedicated export/import action path or iblock archive support confirmation",
        ],
    }


def markdown_report(report: Dict[str, Any]) -> str:
    draft = report["manifest_draft"]
    lines = [
        f"# SF4 Wizard Iblock Manifest: {report['label']}",
        "",
        f"- source: `{report['source']}`",
        f"- iblock_count: `{len(draft['iblocks'])}`",
        f"- highload_count: `{len(draft['highload_entries'])}`",
        f"- config_only_count: `{len(draft['config_only_codes'])}`",
        "",
        "## Iblocks",
        "",
    ]
    for code in draft["iblocks"]:
        lines.append(f"- `{code}`")
    if not draft["iblocks"]:
        lines.append("- none")
    lines.extend(["", "## Highload", ""])
    for item in draft["highload_entries"]:
        label = item.get("table_name") or item.get("name")
        lines.append(f"- `{label}`")
    if not draft["highload_entries"]:
        lines.append("- none")
    lines.extend(["", "## Review Notes", ""])
    for note in draft["review_notes"]:
        lines.append(f"- {note}")
    lines.append("")
    return "\n".join(lines)


def build_report(source: Path, label: str, base_manifest: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    archives = discover_archives(source)
    legacy = discover_legacy_data(source)
    draft = build_manifest_entries(archives, legacy)
    builder_patch = {
        "iblocks": draft["iblocks"],
        "_iblock_manifest_notes": {
            "generated_by": "sf4_wizard_iblock_manifest.py",
            "source": str(source.resolve()),
            "highload_entries_detected": len(draft["highload_entries"]),
            "config_only_codes_detected": len(draft["config_only_codes"]),
        },
    }
    merged_manifest = None
    if base_manifest is not None:
        merged_manifest = json.loads(json.dumps(base_manifest))
        merged_manifest["iblocks"] = draft["iblocks"]
        merged_manifest["_iblock_manifest_notes"] = builder_patch["_iblock_manifest_notes"]
    return {
        "schema_version": SCHEMA_VERSION,
        "operation_id": "sf4.wizard.iblock_manifest",
        "label": label,
        "source": str(source.resolve()),
        "mode": {
            "read_only": True,
            "executes_php": False,
            "executes_bitrix": False,
            "executes_wizard_actions": False,
            "writes": "source_output_only",
        },
        "summary": {
            "archives": len(archives),
            "valid_archives": sum(1 for item in archives if item["valid_zip"]),
            "iblock_archives": sum(1 for item in archives if item["kind"] in {"iblock_archive", "iblock_archive_candidate"}),
            "legacy_files": len(legacy),
            "iblocks": len(draft["iblocks"]),
            "highload": len(draft["highload_entries"]),
            "config_only_codes": len(draft["config_only_codes"]),
        },
        "archives": archives,
        "legacy_data": legacy,
        "manifest_draft": draft,
        "builder_manifest_patch": builder_patch,
        "merged_manifest_draft": merged_manifest,
        "stop_conditions": [
            "do not execute PHP files while inspecting legacy data",
            "do not treat config-only codes as export allowlist without human review",
            "do not treat highload hints as covered unless the selected action path supports them",
            "re-run export builder audit/readiness after applying the draft allowlist",
        ],
    }


def main() -> int:
    root = repo_root()
    parser = argparse.ArgumentParser(description="Create read-only iblock/HL manifest draft for SF4 wizard packaging.")
    parser.add_argument("--source", required=True, help="Source folder to inspect.")
    parser.add_argument("--label", help="Report label. Defaults to source folder name.")
    parser.add_argument("--base-manifest", help="Optional export builder manifest to patch in output only.")
    parser.add_argument(
        "--output-dir",
        help="Output directory. Defaults to source/output/wizard-iblock-manifest/<label>.",
    )
    parser.add_argument("--json", dest="json_only", action="store_true", help="Print JSON report only.")
    args = parser.parse_args()

    try:
        source = Path(args.source).expanduser().resolve()
        if not source.exists() or not source.is_dir():
            raise ValueError(f"source directory does not exist: {source}")
        label = safe_slug(args.label or source.name)
        output_dir = ensure_source_output(
            Path(args.output_dir).expanduser()
            if args.output_dir
            else root / "source" / "output" / "wizard-iblock-manifest" / label
        )
        base_manifest = load_json(Path(args.base_manifest).expanduser().resolve()) if args.base_manifest else None
        report = build_report(source, label, base_manifest)
        write_json(output_dir / "iblock-manifest.report.json", report)
        write_json(output_dir / "iblock-manifest.draft.json", report["manifest_draft"])
        write_json(output_dir / "builder-manifest.patch.json", report["builder_manifest_patch"])
        if report["merged_manifest_draft"] is not None:
            write_json(output_dir / "builder-manifest.merged.draft.json", report["merged_manifest_draft"])
        write_text(output_dir / "iblock-manifest.report.md", markdown_report(report))
    except Exception as exc:  # noqa: BLE001 - CLI reports exact failure.
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.json_only:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print("SF4 Wizard Iblock Manifest Assistant")
        print(f"Source: {report['source']}")
        print(f"Iblocks: {report['summary']['iblocks']}")
        print(f"Highload: {report['summary']['highload']}")
        print(f"Output: {output_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

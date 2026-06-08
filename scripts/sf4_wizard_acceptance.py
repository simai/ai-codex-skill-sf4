#!/usr/bin/env python3
"""
Read-only acceptance runner for the SF4 universal wizard specialist.

The runner executes sf4_wizard_audit.py against real local wizard/module
fixtures, then compares stable expected invariants. It never executes Bitrix,
wizard actions, PHP imports, database writes or runtime file operations.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional


SCHEMA_VERSION = "1.0.0"


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def nested_get(data: Dict[str, Any], path: List[str]) -> Any:
    current: Any = data
    for key in path:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current


def compare_mapping(
    label: str,
    expected: Dict[str, Any],
    actual: Dict[str, Any],
    path_prefix: Optional[List[str]] = None,
) -> List[str]:
    failures: List[str] = []
    path_prefix = path_prefix or []
    for key, value in expected.items():
        actual_value = nested_get(actual, path_prefix + [key])
        if actual_value != value:
            dotted = ".".join([label] + path_prefix + [key])
            failures.append(f"{dotted}: expected {value!r}, got {actual_value!r}")
    return failures


def action_codes(report: Dict[str, Any]) -> List[str]:
    return [item.get("code") for item in report.get("actions", [])]


def finding_codes(report: Dict[str, Any]) -> List[str]:
    return sorted(item.get("code") for item in report.get("findings", []))


def build_audit_command(repo_root: Path, scenario: Dict[str, Any], report_path: Path) -> List[str]:
    args = scenario.get("audit_args", {})
    command = [
        sys.executable,
        str(repo_root / "scripts" / "sf4_wizard_audit.py"),
        "--json",
        str(report_path),
        "--quiet",
    ]
    if args.get("site_root"):
        command.extend(["--site-root", args["site_root"]])
    if args.get("master"):
        command.extend(["--master", args["master"]])
    if args.get("config"):
        command.extend(["--config", args["config"]])
    if args.get("module_root"):
        command.extend(["--module-root", args["module_root"]])
    return command


def evaluate_scenario(
    repo_root: Path,
    scenario: Dict[str, Any],
    output_dir: Path,
) -> Dict[str, Any]:
    scenario_id = scenario["id"]
    audit_dir = output_dir / "audit"
    audit_dir.mkdir(parents=True, exist_ok=True)
    audit_report = audit_dir / f"{scenario_id}.json"
    command = build_audit_command(repo_root, scenario, audit_report)

    process = subprocess.run(command, cwd=repo_root, text=True, capture_output=True, check=False)
    report = load_json(audit_report) if audit_report.exists() else {}
    expected = scenario.get("expected", {})
    failures: List[str] = []

    if process.returncode != expected.get("exit_code", 0):
        failures.append(f"exit_code: expected {expected.get('exit_code', 0)}, got {process.returncode}")

    if expected.get("status") is not None and report.get("status") != expected["status"]:
        failures.append(f"status: expected {expected['status']!r}, got {report.get('status')!r}")

    if expected.get("summary"):
        failures.extend(compare_mapping("summary", expected["summary"], report, ["summary"]))

    if expected.get("master_checks"):
        failures.extend(compare_mapping("master_checks", expected["master_checks"], report, ["master_checks"]))

    if expected.get("description"):
        failures.extend(compare_mapping("description", expected["description"], report, ["description"]))

    if expected.get("installer_bridge_signals"):
        failures.extend(
            compare_mapping(
                "installer_bridge_signals",
                expected["installer_bridge_signals"],
                report,
                ["installer_bridge", "signals"],
            )
        )

    expected_findings = sorted(expected.get("finding_codes", []))
    actual_findings = finding_codes(report)
    if actual_findings != expected_findings:
        failures.append(f"finding_codes: expected {expected_findings!r}, got {actual_findings!r}")

    for code in expected.get("action_codes_contains", []):
        if code not in action_codes(report):
            failures.append(f"action_codes_contains: missing {code!r}")

    return {
        "id": scenario_id,
        "status": "success" if not failures else "failed",
        "audit_report": str(audit_report),
        "command": command,
        "exit_code": process.returncode,
        "failures": failures,
        "stderr": process.stderr.strip(),
    }


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description="Run SF4 wizard specialist acceptance scenarios.")
    parser.add_argument(
        "--manifest",
        default=str(repo_root / "source" / "wizard" / "acceptance-fixtures.json"),
        help="Acceptance fixture manifest.",
    )
    parser.add_argument(
        "--json",
        dest="json_report",
        default=str(repo_root / "source" / "output" / "wizard-acceptance" / "report.json"),
        help="Combined acceptance report output.",
    )
    parser.add_argument("--quiet", action="store_true", help="Do not print human summary.")
    args = parser.parse_args()

    manifest_path = Path(args.manifest).expanduser().resolve()
    output_path = Path(args.json_report).expanduser().resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    manifest = load_json(manifest_path)
    results = [
        evaluate_scenario(repo_root, scenario, output_path.parent)
        for scenario in manifest.get("scenarios", [])
    ]
    failures = [item for item in results if item["status"] != "success"]
    combined = {
        "schema_version": SCHEMA_VERSION,
        "operation_id": "sf4.wizard.acceptance",
        "manifest": str(manifest_path),
        "mode": {
            "read_only": True,
            "executes_php": False,
            "executes_wizard_actions": False,
            "writes": "json_reports_only",
        },
        "summary": {
            "scenarios": len(results),
            "success": len(results) - len(failures),
            "failed": len(failures),
        },
        "status": "success" if not failures else "failed",
        "results": results,
    }
    output_path.write_text(json.dumps(combined, ensure_ascii=False, indent=2), encoding="utf-8")

    if not args.quiet:
        print("SF4 Wizard Acceptance")
        print(f"Status: {combined['status']}")
        print(
            "Summary: "
            f"scenarios={combined['summary']['scenarios']} "
            f"success={combined['summary']['success']} "
            f"failed={combined['summary']['failed']}"
        )
        for item in results:
            print(f"- {item['id']}: {item['status']}")
            for failure in item["failures"]:
                print(f"  - {failure}")

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())

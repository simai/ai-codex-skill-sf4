#!/usr/bin/env python3
"""
Readiness review board for SF4 universal wizard audit reports.

This script consumes JSON produced by sf4_wizard_audit.py and emits a
human-oriented readiness decision. It does not inspect Bitrix runtime, execute
PHP, run wizard actions, import archives, write live files or mutate DB state.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List


SCHEMA_VERSION = "1.0.0"
WRITE_RISKS = {"filesystem_write", "db_write", "global_runtime_write"}


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def unique_sorted(items: Iterable[str]) -> List[str]:
    return sorted({item for item in items if item})


def action_summary(report: Dict[str, Any]) -> Dict[str, Any]:
    actions = report.get("actions", [])
    by_risk: Dict[str, List[str]] = {}
    requirements: List[str] = []
    write_actions: List[Dict[str, Any]] = []
    for action in actions:
        risk = action.get("risk") or "unknown"
        code = action.get("code") or "<missing>"
        by_risk.setdefault(risk, []).append(code)
        requirements.extend(action.get("requirements") or [])
        if risk in WRITE_RISKS:
            write_actions.append(
                {
                    "index": action.get("index"),
                    "code": code,
                    "risk": risk,
                    "requirements": action.get("requirements") or [],
                }
            )
    return {
        "total": len(actions),
        "by_risk": {risk: sorted(codes) for risk, codes in sorted(by_risk.items())},
        "requirements": unique_sorted(requirements),
        "write_actions": write_actions,
    }


def finding_codes(report: Dict[str, Any]) -> List[str]:
    return unique_sorted(item.get("code") for item in report.get("findings", []))


def payload_gaps(report: Dict[str, Any]) -> List[Dict[str, Any]]:
    return [
        {
            "severity": item.get("severity"),
            "code": item.get("code"),
            "message": item.get("message"),
            "path": item.get("path"),
            "action": item.get("action"),
        }
        for item in report.get("findings", [])
        if item.get("code") in {"missing_payload", "invalid_zip", "zip_without_xml"}
    ]


def blockers(report: Dict[str, Any]) -> List[Dict[str, Any]]:
    return [
        {
            "severity": item.get("severity"),
            "code": item.get("code"),
            "message": item.get("message"),
            "path": item.get("path"),
            "action": item.get("action"),
        }
        for item in report.get("findings", [])
        if item.get("severity") == "error"
    ]


def backup_rollback_required(write_actions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    requirements: List[Dict[str, Any]] = []
    for action in write_actions:
        code = action["code"]
        risk = action["risk"]
        if risk == "filesystem_write":
            scope = "filesystem"
            backup = "destination file/directory inventory and backup before action"
            rollback = "restore backup or remove copied/generated paths by inventory"
        elif risk == "db_write":
            scope = "database"
            backup = "DB backup or exact export of affected Bitrix entities/options before action"
            rollback = "restore DB backup or run reviewed cleanup/delete script for created entities"
        else:
            scope = "global_runtime"
            backup = "runtime tree inventory plus DB/config backup before global write"
            rollback = "restore runtime tree and DB/config state from backup"
        requirements.append(
            {
                "action": code,
                "risk": risk,
                "scope": scope,
                "backup_required": backup,
                "rollback_required": rollback,
            }
        )
    return requirements


def rollback_ready(rollback_check: Dict[str, Any] | None) -> bool:
    if not rollback_check:
        return False
    return rollback_check.get("plan_status") == "rollback_plan_ready"


def decide_status(
    report: Dict[str, Any],
    action_info: Dict[str, Any],
    gaps: List[Dict[str, Any]],
    rollback_check: Dict[str, Any] | None = None,
) -> str:
    summary = report.get("summary") or {}
    if report.get("status") == "blocked" or summary.get("errors", 0) > 0:
        return "blocked"
    if gaps or summary.get("missing_payloads", 0) > 0:
        return "needs_payload"
    if action_info["write_actions"] and not rollback_ready(rollback_check):
        return "needs_rollback_plan"
    return "ready_for_review"


def stop_conditions(status: str, report: Dict[str, Any], action_info: Dict[str, Any]) -> List[str]:
    conditions = [
        "stop if audit JSON is stale relative to master/config files",
        "stop if live target, site root, user permissions or backup path are not explicit",
    ]
    if status == "blocked":
        conditions.append("stop until all audit error findings are resolved")
    if action_info["write_actions"]:
        conditions.extend(
            [
                "stop before controlled execution until backup and rollback evidence exists",
                "stop if write action destination scope is broader than approved target",
            ]
        )
    if any(item.get("risk") == "db_write" for item in action_info["write_actions"]):
        conditions.append("stop before DB import unless DB backup and cleanup strategy are reviewed")
    if report.get("summary", {}).get("missing_payloads", 0):
        conditions.append("stop until every deterministic payload path exists and archives open")
    return conditions


def next_actions(status: str, has_write_actions: bool = False, rollback_check: Dict[str, Any] | None = None) -> List[str]:
    if status == "blocked":
        return [
            "fix missing config/action/payload blockers",
            "re-run sf4_wizard_audit.py",
            "re-run sf4_wizard_readiness.py",
        ]
    if status == "needs_payload":
        return [
            "prepare missing payload files or archives",
            "validate zip/XML payloads",
            "re-run audit and readiness",
        ]
    if status == "needs_rollback_plan":
        return [
            "write backup and rollback plan for every write action",
            "define controlled environment and stop conditions",
            "ask ops/tester gatekeepers before live or staging execution",
        ]
    actions = ["review action chain and visual contract"]
    if has_write_actions and rollback_ready(rollback_check):
        actions.extend(
            [
                "replace example-only rollback evidence with real backup artifacts before execution",
                "ask ops/tester gatekeepers before live or staging execution",
            ]
        )
    else:
        actions.append("prepare controlled execution plan if runtime execution is requested")
    return actions


def rollback_summary(rollback_check_path: Path | None, rollback_check: Dict[str, Any] | None) -> Dict[str, Any]:
    if not rollback_check:
        return {
            "provided": False,
            "path": None,
            "plan_status": None,
            "execution_approval": False,
            "evidence_mode": None,
            "summary": {},
        }
    return {
        "provided": True,
        "path": str(rollback_check_path) if rollback_check_path else None,
        "plan_status": rollback_check.get("plan_status"),
        "execution_approval": bool(rollback_check.get("execution_approval")),
        "evidence_mode": rollback_check.get("evidence_mode"),
        "summary": rollback_check.get("summary") or {},
    }


def controlled_execution_allowed(status: str, action_info: Dict[str, Any], rollback_check: Dict[str, Any] | None) -> bool:
    if status != "ready_for_review":
        return False
    if not action_info["write_actions"]:
        return True
    return rollback_ready(rollback_check) and bool(rollback_check.get("execution_approval"))


def build_report(
    audit_path: Path,
    audit: Dict[str, Any],
    label: str,
    rollback_check_path: Path | None = None,
    rollback_check: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    action_info = action_summary(audit)
    gaps = payload_gaps(audit)
    error_blockers = blockers(audit)
    status = decide_status(audit, action_info, gaps, rollback_check)
    rollback_info = rollback_summary(rollback_check_path, rollback_check)
    return {
        "schema_version": SCHEMA_VERSION,
        "operation_id": "sf4.wizard.readiness",
        "label": label,
        "audit_report": str(audit_path),
        "mode": {
            "read_only": True,
            "executes_php": False,
            "executes_wizard_actions": False,
            "writes": "json_or_markdown_report_only",
        },
        "readiness_status": status,
        "controlled_execution_allowed": controlled_execution_allowed(status, action_info, rollback_check),
        "rollback_plan": rollback_info,
        "audit_status": audit.get("status"),
        "master": audit.get("master"),
        "config": audit.get("config"),
        "module_root": audit.get("module_root"),
        "summary": audit.get("summary") or {},
        "finding_codes": finding_codes(audit),
        "blockers": error_blockers,
        "payload_gaps": gaps,
        "side_effects": action_info,
        "backup_rollback_required": backup_rollback_required(action_info["write_actions"]),
        "stop_conditions": stop_conditions(status, audit, action_info),
        "next_actions": next_actions(status, bool(action_info["write_actions"]), rollback_check),
    }


def markdown(report: Dict[str, Any]) -> str:
    lines = [
        f"# Wizard Readiness: {report['label']}",
        "",
        f"- readiness_status: `{report['readiness_status']}`",
        f"- controlled_execution_allowed: `{str(report['controlled_execution_allowed']).lower()}`",
        f"- audit_status: `{report.get('audit_status')}`",
        f"- master: `{report.get('master') or '-'}`",
        f"- config: `{report.get('config') or '-'}`",
        "",
        "## Summary",
        "",
    ]
    for key, value in sorted((report.get("summary") or {}).items()):
        lines.append(f"- {key}: `{value}`")
    lines.extend(["", "## Findings", ""])
    if report["finding_codes"]:
        for code in report["finding_codes"]:
            lines.append(f"- `{code}`")
    else:
        lines.append("- none")
    lines.extend(["", "## Side Effects", ""])
    by_risk = report["side_effects"].get("by_risk") or {}
    if by_risk:
        for risk, codes in by_risk.items():
            lines.append(f"- {risk}: {', '.join('`' + code + '`' for code in codes)}")
    else:
        lines.append("- none")
    lines.extend(["", "## Backup And Rollback Required", ""])
    if report["backup_rollback_required"]:
        for item in report["backup_rollback_required"]:
            lines.append(f"- `{item['action']}` ({item['risk']}): {item['backup_required']}; rollback: {item['rollback_required']}")
    else:
        lines.append("- none")
    lines.extend(["", "## Rollback Plan Evidence", ""])
    rollback_info = report.get("rollback_plan") or {}
    if rollback_info.get("provided"):
        lines.append(f"- plan_status: `{rollback_info.get('plan_status')}`")
        lines.append(f"- execution_approval: `{str(bool(rollback_info.get('execution_approval'))).lower()}`")
        lines.append(f"- evidence_mode: `{rollback_info.get('evidence_mode')}`")
        for key, value in sorted((rollback_info.get("summary") or {}).items()):
            lines.append(f"- {key}: `{value}`")
    else:
        lines.append("- none")
    lines.extend(["", "## Stop Conditions", ""])
    for item in report["stop_conditions"]:
        lines.append(f"- {item}")
    lines.extend(["", "## Next Actions", ""])
    for item in report["next_actions"]:
        lines.append(f"- {item}")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Create SF4 wizard readiness report from audit JSON.")
    parser.add_argument("--audit", required=True, help="Path to sf4_wizard_audit.py JSON report.")
    parser.add_argument("--label", help="Human-readable label. Defaults to audit filename stem.")
    parser.add_argument("--rollback-check", help="Optional sf4_wizard_rollback_plan.py check JSON.")
    parser.add_argument("--json", dest="json_out", help="Optional readiness JSON output path.")
    parser.add_argument("--markdown", dest="markdown_out", help="Optional readiness Markdown output path.")
    parser.add_argument("--quiet", action="store_true", help="Do not print summary.")
    args = parser.parse_args()

    audit_path = Path(args.audit).expanduser().resolve()
    audit = load_json(audit_path)
    rollback_check_path = Path(args.rollback_check).expanduser().resolve() if args.rollback_check else None
    rollback_check = load_json(rollback_check_path) if rollback_check_path else None
    label = args.label or audit_path.stem
    report = build_report(audit_path, audit, label, rollback_check_path, rollback_check)

    if args.json_out:
        path = Path(args.json_out).expanduser().resolve()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    if args.markdown_out:
        path = Path(args.markdown_out).expanduser().resolve()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(markdown(report), encoding="utf-8")

    if not args.quiet:
        print("SF4 Wizard Readiness")
        print(f"Status: {report['readiness_status']}")
        print(f"Controlled execution allowed: {str(report['controlled_execution_allowed']).lower()}")
        print(f"Audit: {audit_path}")
    return 2 if report["readiness_status"] == "blocked" else 0


if __name__ == "__main__":
    sys.exit(main())

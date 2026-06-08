#!/usr/bin/env python3
"""
Rollback plan template/checker for SF4 universal wizard readiness reports.

The script creates and validates human-filled backup/rollback plans. It never
creates backups, runs rollback commands, executes Bitrix/PHP/wizard actions,
imports data or touches live/runtime project paths.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List


SCHEMA_VERSION = "1.0.0"
REQUIRED_FIELDS = [
    "target_scope",
    "backup_artifact",
    "backup_method",
    "rollback_artifact",
    "rollback_method",
    "verification_method",
    "owner",
    "stop_condition",
]


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def slug(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9_.-]+", "-", value.strip())
    return value.strip("-") or "item"


def action_items(readiness: Dict[str, Any]) -> List[Dict[str, Any]]:
    required = readiness.get("backup_rollback_required") or []
    write_actions = readiness.get("side_effects", {}).get("write_actions") or []
    items: List[Dict[str, Any]] = []
    for idx, item in enumerate(required, start=1):
        action = item.get("action") or "unknown"
        matching_action = write_actions[idx - 1] if idx - 1 < len(write_actions) else {}
        action_index = matching_action.get("index") or idx
        risk = item.get("risk") or matching_action.get("risk") or "unknown"
        scope = item.get("scope") or risk
        items.append(
            {
                "id": f"{action_index:02d}-{slug(action)}-{scope}",
                "action": action,
                "action_index": action_index,
                "risk": risk,
                "scope": scope,
                "required_backup": item.get("backup_required"),
                "required_rollback": item.get("rollback_required"),
                "target_scope": "",
                "backup_artifact": "",
                "backup_method": "",
                "rollback_artifact": "",
                "rollback_method": "",
                "verification_method": "",
                "owner": "",
                "stop_condition": "",
                "notes": "",
                "status": "template",
            }
        )
    return items


def build_template(readiness_path: Path, readiness: Dict[str, Any], label: str) -> Dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "operation_id": "sf4.wizard.rollback_plan",
        "label": label,
        "mode": {
            "read_only": True,
            "creates_backups": False,
            "executes_rollback": False,
            "executes_wizard_actions": False,
            "writes": "plan_json_or_markdown_only",
        },
        "readiness_report": str(readiness_path),
        "readiness_status": readiness.get("readiness_status"),
        "controlled_execution_allowed_by_readiness": readiness.get("controlled_execution_allowed"),
        "master": readiness.get("master"),
        "config": readiness.get("config"),
        "plan_status": "rollback_plan_missing" if action_items(readiness) else "rollback_plan_not_required",
        "evidence_mode": "template",
        "items": action_items(readiness),
        "review": {
            "ops_reviewer": "",
            "tester_reviewer": "",
            "approved_scope": "",
            "review_date": "",
            "approval_note": "",
        },
    }


def fill_demo(plan: Dict[str, Any]) -> Dict[str, Any]:
    filled = json.loads(json.dumps(plan))
    filled["evidence_mode"] = "example_only_not_execution_evidence"
    filled["plan_status"] = "rollback_plan_ready"
    for item in filled.get("items", []):
        item["target_scope"] = f"Example target scope for {item['action']} action #{item['action_index']}"
        item["backup_artifact"] = f"source/output/wizard-rollback/example/{item['id']}/backup-evidence.txt"
        item["backup_method"] = f"Documented example backup method for {item['scope']}"
        item["rollback_artifact"] = f"source/output/wizard-rollback/example/{item['id']}/rollback-plan.txt"
        item["rollback_method"] = f"Documented example rollback method for {item['scope']}"
        item["verification_method"] = "Re-run audit/readiness and compare expected status after rollback"
        item["owner"] = "example-owner"
        item["stop_condition"] = "Stop on any missing backup artifact, wider-than-approved scope or failed verification"
        item["notes"] = "Example-only filled item; not real runtime approval."
        item["status"] = "ready"
    filled["review"] = {
        "ops_reviewer": "example-ops",
        "tester_reviewer": "example-tester",
        "approved_scope": "example-only scope, not live execution approval",
        "review_date": "2026-06-07",
        "approval_note": "Example-only plan used to prove checker behavior.",
    }
    return filled


def missing_fields(item: Dict[str, Any]) -> List[str]:
    return [field for field in REQUIRED_FIELDS if not str(item.get(field, "")).strip()]


def check_plan(plan_path: Path, plan: Dict[str, Any]) -> Dict[str, Any]:
    items = plan.get("items") or []
    item_results = []
    missing_count = 0
    for item in items:
        missing = missing_fields(item)
        missing_count += len(missing)
        item_results.append(
            {
                "id": item.get("id"),
                "action": item.get("action"),
                "risk": item.get("risk"),
                "status": "ready" if not missing else "incomplete",
                "missing_fields": missing,
            }
        )

    review = plan.get("review") or {}
    review_missing = [
        field
        for field in ["ops_reviewer", "tester_reviewer", "approved_scope", "review_date", "approval_note"]
        if not str(review.get(field, "")).strip()
    ]

    if not items:
        status = "rollback_plan_not_required"
    elif missing_count or review_missing:
        status = "rollback_plan_incomplete"
    else:
        status = "rollback_plan_ready"

    return {
        "schema_version": SCHEMA_VERSION,
        "operation_id": "sf4.wizard.rollback_plan.check",
        "plan": str(plan_path),
        "label": plan.get("label"),
        "plan_status": status,
        "execution_approval": False,
        "evidence_mode": plan.get("evidence_mode"),
        "summary": {
            "items": len(items),
            "ready_items": sum(1 for item in item_results if item["status"] == "ready"),
            "incomplete_items": sum(1 for item in item_results if item["status"] != "ready"),
            "missing_field_count": missing_count,
            "review_missing_count": len(review_missing),
        },
        "review_missing_fields": review_missing,
        "items": item_results,
        "stop_conditions": [
            "This checker does not approve live execution.",
            "Real backup artifacts must exist and be reviewed by ops/tester before controlled execution.",
            "If target scope changes, regenerate readiness and rollback plan.",
        ],
    }


def markdown_check(report: Dict[str, Any]) -> str:
    lines = [
        f"# Wizard Rollback Plan Check: {report.get('label') or '-'}",
        "",
        f"- plan_status: `{report['plan_status']}`",
        f"- execution_approval: `{str(report['execution_approval']).lower()}`",
        f"- evidence_mode: `{report.get('evidence_mode')}`",
        "",
        "## Summary",
        "",
    ]
    for key, value in sorted(report["summary"].items()):
        lines.append(f"- {key}: `{value}`")
    lines.extend(["", "## Review Missing Fields", ""])
    if report["review_missing_fields"]:
        for field in report["review_missing_fields"]:
            lines.append(f"- `{field}`")
    else:
        lines.append("- none")
    lines.extend(["", "## Items", ""])
    for item in report["items"]:
        missing = ", ".join(f"`{field}`" for field in item["missing_fields"]) or "none"
        lines.append(f"- `{item['id']}` {item['action']} ({item['risk']}): {item['status']}; missing: {missing}")
    lines.extend(["", "## Stop Conditions", ""])
    for condition in report["stop_conditions"]:
        lines.append(f"- {condition}")
    lines.append("")
    return "\n".join(lines)


def markdown_template(plan: Dict[str, Any]) -> str:
    lines = [
        f"# Wizard Rollback Plan Template: {plan.get('label') or '-'}",
        "",
        f"- readiness_status: `{plan.get('readiness_status')}`",
        f"- evidence_mode: `{plan.get('evidence_mode')}`",
        f"- master: `{plan.get('master') or '-'}`",
        "",
        "## Items",
        "",
    ]
    for item in plan.get("items", []):
        lines.extend(
            [
                f"### {item['id']}",
                "",
                f"- action: `{item['action']}`",
                f"- risk: `{item['risk']}`",
                f"- required_backup: {item.get('required_backup')}",
                f"- required_rollback: {item.get('required_rollback')}",
                "- target_scope:",
                "- backup_artifact:",
                "- backup_method:",
                "- rollback_artifact:",
                "- rollback_method:",
                "- verification_method:",
                "- owner:",
                "- stop_condition:",
                "",
            ]
        )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate or check SF4 wizard rollback plans.")
    parser.add_argument("--readiness", help="Readiness JSON to generate a rollback plan template from.")
    parser.add_argument("--plan", help="Rollback plan JSON to check.")
    parser.add_argument("--label", help="Human-readable label.")
    parser.add_argument("--template-json", help="Output rollback plan template JSON.")
    parser.add_argument("--template-markdown", help="Output rollback plan template Markdown.")
    parser.add_argument("--check-json", help="Output rollback plan check JSON.")
    parser.add_argument("--check-markdown", help="Output rollback plan check Markdown.")
    parser.add_argument("--fill-demo", action="store_true", help="Fill generated template with example-only evidence.")
    parser.add_argument("--quiet", action="store_true", help="Do not print summary.")
    args = parser.parse_args()

    generated_plan: Dict[str, Any] | None = None
    if args.readiness:
        readiness_path = Path(args.readiness).expanduser().resolve()
        readiness = load_json(readiness_path)
        generated_plan = build_template(readiness_path, readiness, args.label or readiness.get("label") or readiness_path.stem)
        if args.fill_demo:
            generated_plan = fill_demo(generated_plan)
        if args.template_json:
            write_json(Path(args.template_json).expanduser().resolve(), generated_plan)
        if args.template_markdown:
            path = Path(args.template_markdown).expanduser().resolve()
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(markdown_template(generated_plan), encoding="utf-8")

    check_source_path: Path | None = None
    check_payload: Dict[str, Any] | None = None
    if args.plan:
        check_source_path = Path(args.plan).expanduser().resolve()
        check_payload = load_json(check_source_path)
    elif generated_plan is not None:
        check_source_path = Path(args.template_json).expanduser().resolve() if args.template_json else Path("<generated>")
        check_payload = generated_plan

    check_report: Dict[str, Any] | None = None
    if check_payload is not None and check_source_path is not None:
        check_report = check_plan(check_source_path, check_payload)
        if args.check_json:
            write_json(Path(args.check_json).expanduser().resolve(), check_report)
        if args.check_markdown:
            path = Path(args.check_markdown).expanduser().resolve()
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(markdown_check(check_report), encoding="utf-8")

    if not args.quiet:
        if generated_plan is not None:
            print("SF4 Wizard Rollback Plan")
            print(f"Template status: {generated_plan['plan_status']}")
            print(f"Items: {len(generated_plan.get('items', []))}")
        if check_report is not None:
            print(f"Check status: {check_report['plan_status']}")

    if check_report and check_report["plan_status"] == "rollback_plan_incomplete":
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

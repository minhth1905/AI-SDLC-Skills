#!/usr/bin/env python3
"""AI-SDLC v0.2: dependency-free local state, evidence gates and resume."""
import argparse
import datetime as dt
import json
import os
from pathlib import Path
import re
import sys
import subprocess
from verify_runner import fingerprint

ROOT = Path.cwd()
BASE = ROOT / "docs" / "ai-sdlc"
PHASES = ("new", "planned", "approved", "building", "verifying", "reviewing", "ready_for_human_review", "blocked", "needs_human_review")
NEXT = {
    "new": {"planned", "blocked"},
    "planned": {"approved", "building", "blocked"},
    "approved": {"building", "blocked"},
    "building": {"verifying", "blocked"},
    "verifying": {"reviewing", "building", "blocked"},
    "reviewing": {"ready_for_human_review", "building", "needs_human_review", "blocked"},
    "blocked": {"planned", "building", "verifying"},
    "needs_human_review": {"reviewing", "building"},
    "ready_for_human_review": set(),
}

def now():
    return dt.datetime.now(dt.timezone.utc).isoformat()

def task_dir(task):
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,79}", task) or task in (".", ".."):
        raise ValueError("Invalid task ID")
    return BASE / task

def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))

def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)

def state(task):
    return read_json(task_dir(task) / "state.json")

def evidence_gate(task):
    path = task_dir(task) / "evidence.json"
    if not path.is_file():
        return False, "Missing evidence.json"
    try:
        data = read_json(path)
        checks = data["checks"]
        criteria = data["acceptance_criteria"]
        if data.get("task_id") != task or not isinstance(checks, list) or not checks:
            return False, "Evidence needs matching task_id and nonempty checks"
        if not isinstance(criteria, list) or not criteria:
            return False, "Acceptance criteria evidence is required"
        current_fingerprint, _ = fingerprint()
        for check in checks:
            if check.get("required", True):
                if check.get("source") != "verify_runner" or check.get("worktree_fingerprint") != current_fingerprint or check.get("worktree_changed_during_check"):
                    return False, "Required check lacks current runner provenance: " + str(check.get("name"))
                if check.get("status") != "passed" or check.get("exit_code") != 0 or not check.get("command"):
                    return False, "Required check missing successful command evidence: " + str(check.get("name"))
        for item in criteria:
            if item.get("status") != "passed" or not item.get("evidence"):
                return False, "Acceptance criterion lacks passing evidence"
        if data.get("status") != "passed":
            return False, "Evidence status is not passed"
        return True, "Evidence gate passed"
    except (ValueError, KeyError, TypeError, OSError, subprocess.CalledProcessError) as exc:
        return False, "Invalid evidence: " + str(exc)

def cmd_init(args):
    folder = task_dir(args.task)
    if (folder / "state.json").exists():
        raise ValueError("Task already initialized")
    folder.mkdir(parents=True, exist_ok=True)
    write_json(folder / "state.json", {"task_id": args.task, "tier": args.tier, "phase": "new", "approved": False, "review_cycles": 0, "updated_at": now()})
    print("Initialized", folder)

def cmd_transition(args):
    data = state(args.task)
    old, new = data["phase"], args.phase
    if new not in NEXT.get(old, set()):
        raise ValueError("Invalid transition: " + old + " -> " + new)
    if new == "approved":
        if not args.human_approved:
            raise ValueError("Approval must be explicitly confirmed by a human")
        data["approved"] = True
    if new == "building" and data["tier"] in ("T2", "T3") and not data.get("approved"):
        raise ValueError("T2/T3 require human approval before build")
    if new == "ready_for_human_review":
        ok, reason = evidence_gate(args.task)
        if not ok:
            raise ValueError(reason)
        if not (task_dir(args.task) / "review.md").is_file():
            raise ValueError("Missing review.md")
    if old == "reviewing" and new == "building":
        if data.get("review_cycles", 0) >= 2:
            raise ValueError("Automatic review/fix budget exhausted; request human review")
        data["review_cycles"] = data.get("review_cycles", 0) + 1
    data["phase"] = new
    data["updated_at"] = now()
    write_json(task_dir(args.task) / "state.json", data)
    print(old, "->", new)

def cmd_gate(args):
    ok, reason = evidence_gate(args.task)
    print(reason)
    return 0 if ok else 1

def cmd_resume(args):
    data = state(args.task)
    folder = task_dir(args.task)
    print("Task:", args.task, "Tier:", data["tier"], "Phase:", data["phase"])
    print("Approved:", data.get("approved"), "Review cycles:", data.get("review_cycles", 0))
    for name in ("plan.md", "design.md", "progress.md", "evidence.json", "qa-report.md", "review.md"):
        if (folder / name).exists():
            print("Artifact:", folder / name)
    print("Next: inspect artifacts and continue from the recorded phase; never assume work was verified.")

def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    init = sub.add_parser("init")
    init.add_argument("task")
    init.add_argument("--tier", choices=("T1", "T2", "T3"), required=True)
    tr = sub.add_parser("transition")
    tr.add_argument("task")
    tr.add_argument("phase", choices=PHASES)
    tr.add_argument("--human-approved", action="store_true")
    for name in ("gate", "resume"):
        sub.add_parser(name).add_argument("task")
    args = parser.parse_args()
    try:
        if args.cmd == "init": cmd_init(args)
        elif args.cmd == "transition": cmd_transition(args)
        elif args.cmd == "resume": cmd_resume(args)
        else: return cmd_gate(args)
    except (ValueError, FileNotFoundError, KeyError) as exc:
        print("ERROR:", exc, file=sys.stderr)
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Run a verification command and append provenance to a task's evidence.json."""
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

BASE = Path.cwd() / "docs" / "ai-sdlc"
def fingerprint():
    """Hash tracked/untracked worktree contents without storing sensitive content."""
    proc = subprocess.run(["git", "ls-files", "-co", "--exclude-standard", "-z"], capture_output=True, check=True)
    digest = hashlib.sha256()
    for raw in sorted(set(filter(None, proc.stdout.split(b"\0")))):
        rel = os.fsdecode(raw)
        path = Path(rel)
        if path.is_symlink() or not path.is_file() or rel.startswith("docs/ai-sdlc/"):
            continue
        digest.update(raw + b"\0")
        digest.update(hashlib.sha256(path.read_bytes()).digest())
    head = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()
    digest.update(head.encode())
    return digest.hexdigest(), head

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("task")
    parser.add_argument("--name", required=True)
    parser.add_argument("--", dest="unused", action="store_true", help=argparse.SUPPRESS)
    args, command = parser.parse_known_args()
    if command and command[0] == "--":
        command = command[1:]
    if not command or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,79}", args.task):
        parser.error("provide a valid task and command after --")
    folder = BASE / args.task
    if not (folder / "state.json").is_file():
        parser.error("task must be initialized first")
    before, head = fingerprint()
    started = dt.datetime.now(dt.timezone.utc).isoformat()
    # Do not persist stdout/stderr: it may contain secrets. Inherit terminal output.
    try:
        completed = subprocess.run(command, check=False)
        exit_code = completed.returncode
    except OSError as exc:
        print("Cannot execute verification command:", exc, file=sys.stderr)
        exit_code = 127
    after, _ = fingerprint()
    path = folder / "evidence.json"
    data = json.loads(path.read_text()) if path.exists() else {
        "task_id": args.task, "status": "not_verified", "checks": [], "acceptance_criteria": []
    }
    if data.get("task_id") != args.task or not isinstance(data.get("checks"), list):
        parser.error("invalid existing evidence.json")
    entry = {
        "name": args.name, "command": command, "status": "passed" if exit_code == 0 and before == after else "failed",
        "exit_code": exit_code, "required": True, "observed_at": started,
        "source": "verify_runner", "head": head, "worktree_fingerprint": before,
        "worktree_changed_during_check": before != after
    }
    data["checks"] = [c for c in data["checks"] if c.get("name") != args.name] + [entry]
    data["status"] = "not_verified"  # Gate requires separate explicit acceptance mapping and status.
    temp = path.with_suffix(".json.tmp")
    temp.write_text(json.dumps(data, indent=2) + "\n")
    temp.replace(path)
    print("Recorded", args.name, "exit", exit_code, "worktree changed", before != after)
    return exit_code if exit_code else (1 if before != after else 0)

if __name__ == "__main__":
    sys.exit(main())

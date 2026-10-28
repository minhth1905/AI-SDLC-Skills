#!/usr/bin/env python3
"""Git-local task knowledge capture. Standard library only; never commits or pushes."""
import argparse
import datetime as dt
import json
import os
from pathlib import Path
import re
import subprocess
import sys

ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,79}\Z")
SECRET = re.compile(r"(?i)(-----BEGIN .*PRIVATE KEY-----|(?:api[_-]?key|access[_-]?token|secret[_-]?key|password)\s*[:=]\s*[^\s<]{8,}|gh[pousr]_[A-Za-z0-9_]{20,})")

def fail(message):
    raise ValueError(message)

def read(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return fail(f"Cannot read {path}: {exc}")

def text(value, label, required=False):
    if not isinstance(value, str) or len(value) > 8000 or (required and not value.strip()):
        fail("Invalid field: " + label)
    if SECRET.search(value):
        fail("Possible secret in " + label)
    return value.strip().replace("<", "&lt;").replace(">", "&gt;")

def entries(value, label):
    if not isinstance(value, list) or len(value) > 80:
        fail("Expected list for " + label)
    return [text(v, label, True).replace("\n", " ") for v in value]

def bullets(items):
    return "\n".join("- " + item for item in items) if items else "- None recorded"

def capture(root, task, manifest, dry_run=False):
    if not ID.fullmatch(task) or task in (".", ".."):
        fail("Invalid task ID")
    folder = root / "docs" / "ai-sdlc" / task
    state = read(folder / "state.json")
    ev = read(folder / "evidence.json")
    if state.get("task_id") != task or state.get("phase") != "ready_for_human_review":
        fail("Task is not ready_for_human_review")
    if ev.get("task_id") != task or ev.get("status") != "passed":
        fail("Evidence gate failed")
    checks, criteria = ev.get("checks"), ev.get("acceptance_criteria")
    if not isinstance(checks, list) or not checks or not isinstance(criteria, list) or not criteria:
        fail("Missing verification evidence")
    for c in checks:
        if not isinstance(c, dict):
            fail("Invalid check")
        if c.get("required", True) and (c.get("status") != "passed" or c.get("exit_code") != 0 or not c.get("command")):
            fail("Required check not passed")
    for c in criteria:
        if not isinstance(c, dict) or c.get("status") != "passed" or not c.get("evidence"):
            fail("Acceptance criterion lacks evidence")
    if not (folder / "review.md").is_file():
        fail("Missing review.md")
    m = read(manifest)
    if m.get("task_id") != task:
        fail("Manifest task ID mismatch")
    title = text(m.get("title"), "title", True)
    summary = text(m.get("summary"), "summary", True)
    rationale = text(m.get("rationale", ""), "rationale")
    changed = entries(m.get("changed_files", []), "changed_files")
    if len(set(changed)) != len(changed):
        fail("Duplicate changed_files entries")
    decisions = entries(m.get("decisions", []), "decisions")
    risks = entries(m.get("remaining_risks", []), "remaining_risks")
    followups = entries(m.get("followups", []), "followups")
    for p in changed:
        if p.startswith(("/", "~")) or ".." in Path(p).parts or "\\" in p:
            fail("Unsafe repository-relative file path")
    # Check reported implementation paths against the worktree and Git history.
    for p in changed:
        tracked = subprocess.run(["git", "ls-files", "--error-unmatch", "--", p], cwd=root, capture_output=True)
        existing = (root / p).is_file()
        if not tracked.returncode == 0 and not existing:
            fail("Changed file not found in repository: " + p)
    proc = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, text=True, capture_output=True)
    if proc.returncode:
        fail("Cannot resolve git HEAD")
    header = f"# {title} ({task})\n\n"
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    check_lines = [text(f"{c.get('name', 'check')}: {c.get('status')} (exit {c.get('exit_code', 'n/a')}) — {c.get('command', 'not run')}", "check") for c in checks]
    criteria_lines = [text(f"{c.get('id', c.get('name', 'criterion'))}: {c.get('evidence')}", "criterion") for c in criteria]
    implementation = header + f"Captured: {stamp}\n\nGit HEAD: `{proc.stdout.strip()}` (not proof implementation is committed)\n\n## Outcome\n{summary}\n\n## Changed files (reported)\n{bullets(changed)}\n\n## Checks (local evidence; review provenance separately)\n{bullets(check_lines)}\n\n## Acceptance criteria\n{bullets(criteria_lines)}\n"
    decision_doc = header + "## Decisions\n" + (rationale + "\n\n" if rationale else "") + bullets(decisions) + "\n\n## Risks\n" + bullets(risks) + "\n"
    handoff = header + f"## Status\nReady for human PR review; **not merged or released**.\n\n## Outcome\n{summary}\n\n## Next actions\n{bullets(followups)}\n\n## Risks\n{bullets(risks)}\n\n## Read next\n- [Plan](plan.md)\n- [Decisions](decisions.md)\n- [Implementation](implementation.md)\n- [Evidence](evidence.json)\n- [Review](review.md)\n"
    index = root / "docs" / "ai-sdlc" / "index.md"
    existing = index.read_text(encoding="utf-8") if index.exists() else "# AI-SDLC Task Knowledge Index\n\nHuman-reviewed task handoffs.\n"
    lines = [line for line in existing.splitlines() if not line.startswith(f"- [{task}](")]
    lines.append(f"- [{task}]({task}/handoff.md) — {title}")
    outputs = {folder / "implementation.md": implementation, folder / "decisions.md": decision_doc, folder / "handoff.md": handoff, index: "\n".join(lines).rstrip() + "\n"}
    if not dry_run:
        for path, value in outputs.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            tmp = path.with_name(path.name + f".{os.getpid()}.tmp")
            try:
                tmp.write_text(value, encoding="utf-8")
                tmp.replace(path)
            finally:
                if tmp.exists():
                    tmp.unlink()
    return [str(p.relative_to(root)) for p in outputs]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("task")
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    proc = subprocess.run(["git", "rev-parse", "--show-toplevel"], text=True, capture_output=True)
    if proc.returncode:
        print("ERROR: Run inside a Git repository", file=sys.stderr)
        return 1
    try:
        for path in capture(Path(proc.stdout.strip()).resolve(), args.task, args.manifest, args.dry_run):
            print(path)
    except ValueError as exc:
        print("ERROR:", exc, file=sys.stderr)
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())

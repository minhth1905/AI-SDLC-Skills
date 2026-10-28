#!/usr/bin/env python3
"""Claude Code Stop hook: block claiming completion when active task lacks evidence."""
import json
from pathlib import Path
import re
import sys

def main():
    try:
        payload = json.load(sys.stdin)
    except (ValueError, OSError):
        return 0
    active = Path(".ai-sdlc-active")
    if not active.exists() or payload.get("stop_hook_active"):
        return 0
    task = active.read_text(encoding="utf-8").strip()
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,79}", task):
        return 0
    folder = Path("docs/ai-sdlc") / task
    state_path = folder / "state.json"
    if not state_path.exists():
        return 0
    try:
        state = json.loads(state_path.read_text(encoding="utf-8"))
    except ValueError:
        return 0
    # Stop is allowed for human approval, blockers and planning.
    if state.get("phase") != "ready_for_human_review":
        return 0
    from subprocess import run
    result = run([sys.executable, str(Path(__file__).resolve().parents[1] / "scripts/sdlc.py"), "gate", task], capture_output=True, text=True)
    if result.returncode:
        print(json.dumps({"decision": "block", "reason": "AI-SDLC evidence gate failed: " + result.stdout.strip()}))
    return 0

if __name__ == "__main__":
    sys.exit(main())

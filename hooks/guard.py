#!/usr/bin/env python3
"""Claude Code PreToolUse/Stop hooks. Opt-in: only active with .ai-sdlc-active task ID."""
import json
from pathlib import Path
import re
import sys

def deny(message):
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny", "permissionDecisionReason": message}}))
    return 0

def main():
    try:
        payload = json.load(sys.stdin)
    except (ValueError, OSError):
        return 0
    active = Path(".ai-sdlc-active")
    if not active.exists():
        return 0  # do not interfere with unrelated sessions
    task = active.read_text(encoding="utf-8").strip()
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,79}", task):
        return deny("Invalid active AI-SDLC task ID")
    name = payload.get("tool_name", "")
    inp = payload.get("tool_input") or {}
    if name == "Bash":
        cmd = str(inp.get("command", ""))
        # This is defense-in-depth, not a shell sandbox.
        forbidden = [
            r"(?i)(^|[;&|\s])(?:printenv|env)(?:\s|$)",
            r"(?i)(^|[;&|\s])(?:rm\s+-rf|sudo\s+rm|git\s+push\s+--force)(?:\s|$)",
            r"(?i)(?:cat|head|tail|less|more)\s+[^\n]*?(?:\.env\b|\.pem\b|\.key\b)",
        ]
        if any(re.search(pattern, cmd) for pattern in forbidden):
            return deny("AI-SDLC guard: command requires manual approval")
    if name in ("Read", "Edit", "Write", "MultiEdit"):
        paths = [str(inp.get(k, "")) for k in ("file_path", "path")]
        for path in paths:
            parts = Path(path).parts
            if any(p == ".env" or p.startswith(".env.") or p.endswith((".pem", ".key")) for p in parts):
                return deny("AI-SDLC guard: secret-like file access blocked")
    return 0

if __name__ == "__main__":
    sys.exit(main())

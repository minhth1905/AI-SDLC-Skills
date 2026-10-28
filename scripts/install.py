#!/usr/bin/env python3
"""Install AI-SDLC workflow into a target Git repository. Standard library only."""
import argparse
from pathlib import Path
import shutil
import subprocess
import sys

SKILLS = ("sdlc-orchestrate", "sdlc-spec", "sdlc-plan", "sdlc-build", "sdlc-verify", "sdlc-review", "sdlc-capture")
SCRIPTS = ("sdlc.py", "context_store.py")
HOOKS = ("guard.py", "stop.py")

def install(source, target, force=False):
    source, target = Path(source).resolve(), Path(target).resolve()
    if not (source / ".claude/commands/sdlc.md").is_file():
        raise ValueError("Run installer from the AI-SDLC-Skills repository")
    if subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=target, capture_output=True).returncode:
        raise ValueError("Target must be inside a Git repository")
    paths = [(source / name, target / ".claude/skills" / name) for name in SKILLS]
    paths += [(source / "scripts" / name, target / ".claude/ai-sdlc/scripts" / name) for name in SCRIPTS]
    paths += [(source / "hooks" / name, target / ".claude/ai-sdlc/hooks" / name) for name in HOOKS]
    paths.append((source / ".claude/commands/sdlc.md", target / ".claude/commands/sdlc.md"))
    for src, dst in paths:
        if not src.exists():
            raise ValueError("Missing source: " + str(src))
        if dst.exists() and not force:
            raise ValueError("Already exists (use --force to overwrite): " + str(dst))
    for src, dst in paths:
        dst.parent.mkdir(parents=True, exist_ok=True)
        if src.is_dir():
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)
    return [str(dst.relative_to(target)) for _, dst in paths]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", default=".", help="Target Git project root")
    parser.add_argument("--force", action="store_true", help="Overwrite previously installed AI-SDLC files")
    args = parser.parse_args()
    try:
        for path in install(Path(__file__).resolve().parents[1], args.target, args.force):
            print("Installed:", path)
    except (ValueError, OSError) as exc:
        print("ERROR:", exc, file=sys.stderr)
        return 1
    print("Next: open Claude Code in target project and run /sdlc <TICKET-ID> <description>")
    print("Optional Claude hooks are NOT enabled by this installer.")
    return 0

if __name__ == "__main__":
    sys.exit(main())

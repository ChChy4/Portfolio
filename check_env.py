"""Check that the software required for this project is installed.

Run with:  py check_env.py
Exits with code 1 if any required tool is missing.
"""

import shutil
import subprocess
import sys

# (command, version args, required?)
TOOLS = [
    ("git", ["--version"], True),
    ("gh", ["--version"], True),
    ("py", ["--version"], True),
    ("pip", ["--version"], True),
    ("claude", ["--version"], True),
    ("node", ["--version"], False),
    ("npm", ["--version"], False),
    ("code", ["--version"], False),
]


def version_of(cmd, args):
    path = shutil.which(cmd)
    if not path:
        return None
    try:
        out = subprocess.run(
            [path, *args], capture_output=True, text=True, timeout=30
        ).stdout.strip()
        return out.splitlines()[0] if out else "(installed, no version output)"
    except Exception as exc:  # noqa: BLE001
        return f"(installed, version check failed: {exc})"


def gh_logged_in():
    if not shutil.which("gh"):
        return False
    result = subprocess.run(
        [shutil.which("gh"), "auth", "status"], capture_output=True, text=True
    )
    return result.returncode == 0


def main():
    missing_required = []
    print(f"{'Tool':<8} {'Status':<9} Version")
    print("-" * 60)
    for cmd, args, required in TOOLS:
        version = version_of(cmd, args)
        if version:
            status = "OK"
        else:
            status = "MISSING" if required else "optional"
            if required:
                missing_required.append(cmd)
        print(f"{cmd:<8} {status:<9} {version or '-'}")

    print("-" * 60)
    print(f"GitHub CLI logged in: {'yes' if gh_logged_in() else 'NO - run: gh auth login'}")

    if missing_required:
        print(f"\nMissing required tools: {', '.join(missing_required)}")
        sys.exit(1)
    print("\nAll required tools are installed.")


if __name__ == "__main__":
    main()

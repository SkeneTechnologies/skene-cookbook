#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2024-2026 Skene Technologies

"""
Documentation and link validation for E2E and pre-flight.
Checks that required docs exist and optionally validates markdown links.
"""

import argparse
import subprocess
import sys
from pathlib import Path

REQUIRED_DOCS = [
    "README.md",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "SECURITY_POLICY.md",
    "CHANGELOG.md",
    "LICENSE",
    "LICENSES.txt",
    "docs/SKILL_CHAINS.md",
    "docs/PLAYBOOKS.md",
    "docs/directory.md",
]

# Key docs to run link check on (markdown-link-check)
LINK_CHECK_FILES = [
    "README.md",
    "CONTRIBUTING.md",
    "docs/PLAYBOOKS.md",
]


def main():
    parser = argparse.ArgumentParser(description="Validate documentation and optional links")
    parser.add_argument(
        "--links",
        action="store_true",
        help="Run markdown link check on key docs (requires npx markdown-link-check)",
    )
    parser.add_argument(
        "--base",
        default=".",
        help="Repository root path (default: current directory)",
    )
    args = parser.parse_args()
    base = Path(args.base)

    errors = 0
    for rel in REQUIRED_DOCS:
        path = base / rel
        if not path.exists():
            print(f"❌ Missing required doc: {rel}")
            errors += 1
        else:
            print(f"✅ {rel}")

    if errors > 0:
        print(f"\n❌ {errors} required document(s) missing.")
        sys.exit(1)

    if args.links:
        print("\n🔗 Checking markdown links...")
        for rel in LINK_CHECK_FILES:
            path = base / rel
            if not path.exists():
                continue
            try:
                # Treat 403 as alive (e.g. npm package pages often return 403 for bots)
                result = subprocess.run(
                    [
                        "npx",
                        "--yes",
                        "markdown-link-check",
                        "--alive",
                        "200,403",
                        str(path),
                    ],
                    cwd=base,
                    capture_output=True,
                    text=True,
                    timeout=60,
                )
                if result.returncode != 0:
                    print(f"❌ Link check failed: {rel}")
                    if result.stdout:
                        print(result.stdout)
                    if result.stderr:
                        print(result.stderr, file=sys.stderr)
                    errors += 1
                else:
                    print(f"✅ Links OK: {rel}")
            except (FileNotFoundError, subprocess.TimeoutExpired) as e:
                print(f"⚠️  Link check skipped for {rel}: {e}")
                break

        if errors > 0:
            sys.exit(1)

    print("\n✅ Documentation validation complete.")
    sys.exit(0)


if __name__ == "__main__":
    main()

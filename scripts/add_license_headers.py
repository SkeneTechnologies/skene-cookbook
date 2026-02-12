#!/usr/bin/env python3
"""
Script to add SPDX license headers to Python and JavaScript source files.
"""

import os
import sys
from pathlib import Path

PYTHON_HEADER = """# SPDX-License-Identifier: MIT
# Copyright (c) 2024-2026 Skene Technologies

"""

JAVASCRIPT_HEADER = """// SPDX-License-Identifier: MIT
// Copyright (c) 2024-2026 Skene Technologies

"""


def has_spdx_header(content: str) -> bool:
    """Check if file already has SPDX header."""
    return "SPDX-License-Identifier" in content[:500]


def add_header_to_python_file(filepath: Path) -> bool:
    """Add SPDX header to Python file if not present."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        if has_spdx_header(content):
            print(f"  ✓ Already has header: {filepath}")
            return False

        # Check if file starts with shebang
        if content.startswith("#!"):
            # Preserve shebang, add header after
            lines = content.split("\n", 1)
            shebang = lines[0] + "\n"
            rest = lines[1] if len(lines) > 1 else ""
            new_content = shebang + PYTHON_HEADER + rest
        else:
            new_content = PYTHON_HEADER + content

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)

        print(f"  ✅ Added header: {filepath}")
        return True

    except Exception as e:
        print(f"  ❌ Error processing {filepath}: {e}")
        return False


def add_header_to_javascript_file(filepath: Path) -> bool:
    """Add SPDX header to JavaScript file if not present."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        if has_spdx_header(content):
            print(f"  ✓ Already has header: {filepath}")
            return False

        # Check if file starts with shebang
        if content.startswith("#!"):
            # Preserve shebang, add header after
            lines = content.split("\n", 1)
            shebang = lines[0] + "\n"
            rest = lines[1] if len(lines) > 1 else ""
            new_content = shebang + JAVASCRIPT_HEADER + rest
        else:
            new_content = JAVASCRIPT_HEADER + content

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)

        print(f"  ✅ Added header: {filepath}")
        return True

    except Exception as e:
        print(f"  ❌ Error processing {filepath}: {e}")
        return False


def main():
    """Main function to add headers to all source files."""
    repo_root = Path(__file__).parent.parent
    os.chdir(repo_root)

    print("🔍 Adding SPDX license headers to source files...\n")

    python_files = []
    javascript_files = []

    # Find Python files
    for pattern in ["scripts/*.py", "eval_harness/**/*.py"]:
        python_files.extend(repo_root.glob(pattern))

    # Find JavaScript files
    javascript_files.extend(repo_root.glob("bin/*.js"))

    # Filter out __pycache__ and this script itself
    python_files = [
        f
        for f in python_files
        if "__pycache__" not in str(f) and f.name != "add_license_headers.py"
    ]

    print(f"📝 Found {len(python_files)} Python files")
    print(f"📝 Found {len(javascript_files)} JavaScript files\n")

    # Process Python files
    print("Python files:")
    python_updated = sum(add_header_to_python_file(f) for f in python_files)

    print(f"\nJavaScript files:")
    js_updated = sum(add_header_to_javascript_file(f) for f in javascript_files)

    print(f"\n✨ Summary:")
    print(f"  - Python: {python_updated}/{len(python_files)} files updated")
    print(f"  - JavaScript: {js_updated}/{len(javascript_files)} files updated")
    print(f"  - Total: {python_updated + js_updated} files updated")


if __name__ == "__main__":
    main()

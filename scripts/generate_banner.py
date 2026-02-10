#!/usr/bin/env python3
"""
ASCII Banner Generator for Skills Directory
"""

import pyfiglet

def generate_banner(text="SKILL-LOOM", font="slant"):
    """Generate ASCII art banner"""
    banner = pyfiglet.figlet_format(text, font=font)
    return banner

def generate_readme_header():
    """Generate full README header with banner"""
    banner = generate_banner()

    header = f"""```
{banner}```

<p align="center">
  <strong>808+ AI Skills for Claude and Cursor • Production Ready</strong>
</p>

<p align="center">
  <a href="https://github.com/yourusername/skene-cookbook/actions">
    <img src="https://github.com/yourusername/skene-cookbook/workflows/Lint%20&%20Build%20Documentation/badge.svg" alt="Build Status">
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License: MIT">
  </a>
  <a href="docs/directory.md">
    <img src="https://img.shields.io/badge/skills-808-brightgreen.svg" alt="Skills: 808">
  </a>
  <a href="reports/security_analysis.md">
    <img src="https://img.shields.io/badge/security-100%25-success.svg" alt="Security: 100%">
  </a>
  <a href="SECURITY_POLICY.md">
    <img src="https://img.shields.io/badge/critical_risk-0-success.svg" alt="Critical Risk: 0">
  </a>
</p>

<p align="center">
  <a href="#install">Install</a> •
  <a href="#features">Features</a> •
  <a href="docs/directory.md">Browse Skills</a> •
  <a href="skill-loom-cli.py">CLI Tool</a> •
  <a href="ARCHITECTURE.md">Architecture</a>
</p>

---
"""
    return header

if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == '--readme':
        print(generate_readme_header())
    else:
        print(generate_banner())

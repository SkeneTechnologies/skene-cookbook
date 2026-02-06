# Security Skills

**Total Skills:** 18

## Risk Distribution

| Risk Level | Count |
|------------|-------|
| 🔴 Critical | 16 |
| 🔵 Medium | 1 |
| 🟢 Low | 1 |

---

## Skills

| # | Skill ID | Risk | Job to be Done |
|---|----------|------|----------------|
| 1 | `security/dwarf-expert` | 🔴 Critical | Provides expertise for analyzing DWARF debug files and understanding the DWARF debug format/standard (v3-v5). Triggers when understanding DWARF information, interacting with DWARF files, answering DWARF-related questions, or working with code that parses DWARF data. |
| 2 | `security/ask-questions-if-underspecified` | 🔴 Critical | Clarify requirements before implementing. Use when serious doubts arise. |
| 3 | `security/audit-context-building` | 🔴 Critical | Enables ultra-granular, line-by-line code analysis to build deep architectural context before vulnerability or bug finding. |
| 4 | `security/claude-in-chrome-troubleshooting` | 🔵 Medium | Diagnose and fix Claude in Chrome MCP extension connectivity issues. Use when mcp__claude-in-chrome__* tools fail, return "Browser extension is not connected", or behave erratically. |
| 5 | `security/entry-point-analyzer` | 🔴 Critical | Analyzes smart contract codebases to identify state-changing entry points for security auditing. Detects externally callable functions that modify state, categorizes them by access level (public, admin, role-restricted, contract-only), and generates structured audit reports. Excludes view/pure/read-only functions. Use when auditing smart contracts (Solidity, Vyper, Solana/Rust, Move, TON, CosmWasm) or when asked to find entry points, audit flows, external functions, access control patterns, or privileged operations. |
| 6 | `security/semgrep-rule-creator` | 🔴 Critical | Creates custom Semgrep rules for detecting security vulnerabilities, bug patterns, and code patterns. Use when writing Semgrep rules or building custom static analysis detections. |
| 7 | `security/constant-time-analysis` | 🔴 Critical | Detects timing side-channel vulnerabilities in cryptographic code. Use when implementing or reviewing crypto code, encountering division on secrets, secret-dependent branches, or constant-time programming questions in C, C++, Go, Rust, Swift, Java, Kotlin, C#, PHP, JavaScript, TypeScript, Python, or Ruby. |
| 8 | `security/property-based-testing` | 🔴 Critical | Provides guidance for property-based testing across multiple languages and smart contracts. Use when writing tests, reviewing code with serialization/validation/parsing patterns, designing features, or when property-based testing would provide stronger coverage than example-based tests. |
| 9 | `security/differential-review` | 🔴 Critical | Performs security-focused differential review of code changes (PRs, commits, diffs). Adapts analysis depth to codebase size, uses git history for context, and generates comprehensive security reports. |
| 10 | `security/insecure-defaults` | 🔴 Critical | "Detects fail-open insecure defaults (hardcoded secrets, weak auth, permissive security) that allow apps to run insecurely in production. Use when auditing security, reviewing config management, or analyzing environment variable handling." |
| 11 | `security/variant-analysis` | 🔴 Critical | Find similar vulnerabilities and bugs across codebases using pattern-based analysis. Use when hunting bug variants, building CodeQL/Semgrep queries, analyzing security vulnerabilities, or performing systematic code audits after finding an initial issue. |
| 12 | `security/firebase-apk-scanner` | 🔴 Critical | Scans Android APKs for Firebase security misconfigurations including open databases, storage buckets, authentication issues, and exposed cloud functions. Use when analyzing APK files for Firebase vulnerabilities, performing mobile app security audits, or testing Firebase endpoint security. For authorized security research only. |
| 13 | `security/fix-review` | 🔴 Critical | Verifies that git commits address security audit findings without introducing bugs. Use when reviewing fix branches, validating remediation commits, or checking if specific findings have been addressed. |
| 14 | `security/spec-to-code-compliance` | 🔴 Critical | Verifies code implements exactly what documentation specifies for blockchain audits. Use when comparing code against whitepapers, finding gaps between specs and implementation, or performing compliance checks for protocol implementations. |
| 15 | `security/sharp-edges` | 🔴 Critical | "Identifies error-prone APIs, dangerous configurations, and footgun designs that enable security mistakes. Use when reviewing API designs, configuration schemas, cryptographic library ergonomics, or evaluating whether code follows 'secure by default' and 'pit of success' principles. Triggers: footgun, misuse-resistant, secure defaults, API usability, dangerous configuration." |
| 16 | `security/modern-python` | 🔴 Critical | Configures Python projects with modern tooling (uv, ruff, ty). Use when creating projects, writing standalone scripts, or migrating from pip/Poetry/mypy/black. |
| 17 | `security/semgrep-rule-variant-creator` | 🔴 Critical | Creates language variants of existing Semgrep rules. Use when porting a Semgrep rule to specified target languages. Takes an existing rule and target languages as input, produces independent rule+test directories for each language. |
| 18 | `cursor_rules/clerk` | 🟢 Low | This guide establishes definitive best practices for integrating Clerk, focusing on robust security, efficient session management, and secure token handling in line with modern OAuth 2.0 (RFC 9700) and JWT (RFC 8725) standards. |

---

[← Back to Directory](../directory.md)


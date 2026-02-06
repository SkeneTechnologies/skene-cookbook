#!/usr/bin/env python3
"""
Documentation Generator for Skills Directory
Generates GitHub-optimized markdown documentation with Mermaid diagrams
"""

import json
import yaml
from pathlib import Path
from datetime import datetime
from collections import defaultdict


class DocsGenerator:
    """Generate comprehensive documentation"""

    def __init__(self, base_path="."):
        self.base_path = Path(base_path)
        self.registry_path = self.base_path / "registry" / "job_functions" / "index.json"
        self.skills_path = self.base_path / "skills-library"
        self.docs_path = self.base_path / "docs"
        self.job_functions = {}

        # Create docs directory
        self.docs_path.mkdir(exist_ok=True)
        (self.docs_path / "functions").mkdir(exist_ok=True)

        self.load_registry()

    def load_registry(self):
        """Load job function registry"""
        with open(self.registry_path, 'r') as f:
            self.job_functions = json.load(f)

    def generate_all(self):
        """Generate all documentation"""
        print("📚 Generating Documentation Suite...")
        print()

        self.generate_directory()
        self.generate_function_docs()
        self.generate_mermaid_tree()
        self.update_readme()

        print("\n✅ Documentation generation complete!")

    def generate_directory(self):
        """Generate searchable directory of all skills"""
        print("  📄 Generating docs/directory.md...")

        output_path = self.docs_path / "directory.md"

        with open(output_path, 'w') as f:
            f.write("# Skills Directory - Complete Catalog\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d')}\n\n")

            # Summary stats
            total_skills = sum(len(skills) for skills in self.job_functions.values())
            f.write("## Overview\n\n")
            f.write(f"- **Total Skills:** {total_skills}\n")
            f.write(f"- **Job Functions:** {len(self.job_functions)}\n")
            f.write(f"- **Status:** Production Ready\n\n")

            # Risk distribution
            risk_counts = {'Critical': 0, 'High': 0, 'Medium': 0, 'Low': 0}
            for skills in self.job_functions.values():
                for skill in skills:
                    risk_counts[skill['risk_level']] += 1

            f.write("## Security Status\n\n")
            f.write("| Risk Level | Count | Percentage |\n")
            f.write("|------------|-------|------------|\n")
            for risk in ['Critical', 'High', 'Medium', 'Low']:
                count = risk_counts[risk]
                pct = (count / total_skills * 100) if total_skills else 0
                emoji = {'Critical': '🔴', 'High': '🟡', 'Medium': '🔵', 'Low': '🟢'}[risk]
                f.write(f"| {emoji} {risk} | {count} | {pct:.1f}% |\n")

            f.write("\n---\n\n")

            # Table of contents by job function
            f.write("## Quick Navigation\n\n")
            for func in sorted(self.job_functions.keys()):
                count = len(self.job_functions[func])
                f.write(f"- [{func.replace('_', ' ').title()}](functions/{func}.md) ({count} skills)\n")

            f.write("\n---\n\n")

            # Complete table
            f.write("## Complete Skills Directory\n\n")
            f.write("| Skill ID | Job Function | Risk | Description |\n")
            f.write("|----------|--------------|------|-------------|\n")

            # Flatten all skills
            all_skills = []
            for func, skills in self.job_functions.items():
                for skill in skills:
                    all_skills.append({**skill, 'function': func})

            # Sort by skill_id
            all_skills.sort(key=lambda x: x['skill_id'])

            for skill in all_skills:
                func = skill['function'].replace('_', ' ').title()
                risk_emoji = {'Critical': '🔴', 'High': '🟡', 'Medium': '🔵', 'Low': '🟢'}[skill['risk_level']]
                jtbd = skill['jtbd'][:60] + "..." if len(skill['jtbd']) > 60 else skill['jtbd']

                f.write(f"| `{skill['skill_id']}` | {func} | {risk_emoji} {skill['risk_level']} | {jtbd} |\n")

            # Search tips
            f.write("\n---\n\n")
            f.write("## Search Tips\n\n")
            f.write("- **By Function:** Use the Quick Navigation links above\n")
            f.write("- **By Keyword:** Use Ctrl+F (Cmd+F on Mac) to search this page\n")
            f.write("- **By Risk:** Filter by emoji: 🔴 🟡 🔵 🟢\n")
            f.write("- **CLI Tool:** Run `python3 skill-loom-cli.py` for interactive search\n\n")

        print(f"     ✓ Created {output_path}")

    def generate_function_docs(self):
        """Generate individual docs for each job function"""
        print("  📁 Generating function-specific docs...")

        for func, skills in self.job_functions.items():
            output_path = self.docs_path / "functions" / f"{func}.md"

            with open(output_path, 'w') as f:
                title = func.replace('_', ' ').title()
                f.write(f"# {title} Skills\n\n")
                f.write(f"**Total Skills:** {len(skills)}\n\n")

                # Risk breakdown
                risk_counts = defaultdict(int)
                for skill in skills:
                    risk_counts[skill['risk_level']] += 1

                f.write("## Risk Distribution\n\n")
                f.write("| Risk Level | Count |\n")
                f.write("|------------|-------|\n")
                for risk in ['Critical', 'High', 'Medium', 'Low']:
                    if risk in risk_counts:
                        emoji = {'Critical': '🔴', 'High': '🟡', 'Medium': '🔵', 'Low': '🟢'}[risk]
                        f.write(f"| {emoji} {risk} | {risk_counts[risk]} |\n")

                f.write("\n---\n\n")

                # Skills table
                f.write("## Skills\n\n")
                f.write("| # | Skill ID | Risk | Job to be Done |\n")
                f.write("|---|----------|------|----------------|\n")

                for i, skill in enumerate(skills, 1):
                    risk_emoji = {'Critical': '🔴', 'High': '🟡', 'Medium': '🔵', 'Low': '🟢'}[skill['risk_level']]
                    jtbd = skill['jtbd'].replace('|', '\\|')  # Escape pipes
                    f.write(f"| {i} | `{skill['skill_id']}` | {risk_emoji} {skill['risk_level']} | {jtbd} |\n")

                # Back link
                f.write("\n---\n\n")
                f.write("[← Back to Directory](../directory.md)\n\n")

            print(f"     ✓ Created {output_path}")

    def generate_mermaid_tree(self):
        """Generate Mermaid.js skill tree visualization"""
        print("  🌳 Generating Mermaid skill tree...")

        output_path = self.docs_path / "skill-tree.md"

        with open(output_path, 'w') as f:
            f.write("# Skills Directory - Visual Tree\n\n")
            f.write("Interactive visualization of the skills directory structure.\n\n")

            f.write("```mermaid\ngraph TD\n")
            f.write("    Root[Skills Directory<br/>808 Skills]\n\n")

            # Top level: Job Functions
            for func in sorted(self.job_functions.keys()):
                func_id = func
                func_label = func.replace('_', ' ').title()
                count = len(self.job_functions[func])

                # Determine color based on dominant risk
                risk_counts = defaultdict(int)
                for skill in self.job_functions[func]:
                    risk_counts[skill['risk_level']] += 1

                if risk_counts['Critical'] > 0:
                    color = "fill:#ffcccc"
                elif risk_counts['High'] > count * 0.5:
                    color = "fill:#fff4cc"
                elif risk_counts['Low'] > count * 0.5:
                    color = "fill:#ccffcc"
                else:
                    color = "fill:#cce5ff"

                f.write(f"    Root --> {func_id}[{func_label}<br/>{count} skills]\n")
                f.write(f"    style {func_id} {color}\n")

            # Add legend
            f.write("\n    style Root fill:#e0e0e0,stroke:#333,stroke-width:3px\n")

            f.write("```\n\n")

            # Add interactive legend
            f.write("## Color Legend\n\n")
            f.write("- 🔴 **Red:** Contains Critical risk skills\n")
            f.write("- 🟡 **Yellow:** Primarily High risk skills\n")
            f.write("- 🔵 **Blue:** Mixed risk levels\n")
            f.write("- 🟢 **Green:** Primarily Low risk skills\n\n")

            # Add workflow visualization
            f.write("## Example Workflow Chain\n\n")
            f.write("```mermaid\ngraph LR\n")
            f.write("    A[Partner Onboard] -->|Success| B[Setup Integration]\n")
            f.write("    B -->|Success| C[Health Check]\n")
            f.write("    B -->|Failure| D[Manual Setup]\n")
            f.write("    C -->|Parallel| E[Revenue Tracking]\n")
            f.write("    C -->|Parallel| F[Co-Sell Enable]\n")
            f.write("    E --> G[Complete]\n")
            f.write("    F --> G\n")
            f.write("    D --> G\n\n")
            f.write("    style A fill:#ccffcc\n")
            f.write("    style B fill:#cce5ff\n")
            f.write("    style C fill:#cce5ff\n")
            f.write("    style D fill:#fff4cc\n")
            f.write("    style E fill:#cce5ff\n")
            f.write("    style F fill:#cce5ff\n")
            f.write("    style G fill:#ccffcc\n")
            f.write("```\n\n")

            f.write("---\n\n")
            f.write("[← Back to Directory](directory.md)\n\n")

        print(f"     ✓ Created {output_path}")

    def update_readme(self):
        """Update main README with documentation links"""
        print("  📝 Updating README.md...")

        readme_path = self.base_path / "README.md"

        # Read existing README
        with open(readme_path, 'r') as f:
            readme_content = f.read()

        # Add documentation section if not exists
        if "## Documentation" not in readme_content:
            # Insert before "## License" or at end
            if "## License" in readme_content:
                parts = readme_content.split("## License")
                new_section = "\n## Documentation\n\n"
                new_section += "- 📚 [Complete Skills Directory](docs/directory.md)\n"
                new_section += "- 🌳 [Visual Skill Tree](docs/skill-tree.md)\n"
                new_section += "- 📋 [Browse by Job Function](docs/functions/)\n"
                new_section += "- 🖥️  [Interactive CLI](skill-loom-cli.py) - Run `python3 skill-loom-cli.py`\n"
                new_section += "- 🏗️  [Architecture Guide](ARCHITECTURE.md)\n"
                new_section += "- 🔒 [Security Policy](SECURITY_POLICY.md)\n\n"

                readme_content = parts[0] + new_section + "## License" + parts[1]
            else:
                readme_content += "\n## Documentation\n\n"
                readme_content += "- 📚 [Complete Skills Directory](docs/directory.md)\n"
                readme_content += "- 🌳 [Visual Skill Tree](docs/skill-tree.md)\n"
                readme_content += "- 📋 [Browse by Job Function](docs/functions/)\n"
                readme_content += "- 🖥️  [Interactive CLI](skill-loom-cli.py) - Run `python3 skill-loom-cli.py`\n"
                readme_content += "- 🏗️  [Architecture Guide](ARCHITECTURE.md)\n"
                readme_content += "- 🔒 [Security Policy](SECURITY_POLICY.md)\n\n"

            with open(readme_path, 'w') as f:
                f.write(readme_content)

            print(f"     ✓ Updated {readme_path}")


def main():
    generator = DocsGenerator()
    generator.generate_all()


if __name__ == '__main__':
    main()

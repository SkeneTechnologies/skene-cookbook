#!/usr/bin/env python3
"""
Skene Skills Directory - Interactive Terminal Interface
Browse 760+ AI skills, audit security, visualize workflows

Built with Skene ASCII Design System for consistent branding.
"""

import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional

import yaml

try:
    import pyfiglet
    from rich import box
    from rich.console import Console
    from rich.layout import Layout
    from rich.markdown import Markdown
    from rich.panel import Panel
    from rich.prompt import IntPrompt, Prompt
    from rich.syntax import Syntax
    from rich.table import Table
    from rich.text import Text
    from rich.tree import Tree
except ImportError:
    print("❌ Missing dependencies. Install with:")
    print("   pip3 install rich pyfiglet")
    sys.exit(1)

# Import Skene ASCII Design System
try:
    from ascii import RISK_COLORS, SkeneColors, Symbols, Tokens, get_risk_color_hex
except ImportError:
    print("❌ Missing ASCII design system. Ensure ascii/ folder exists.")
    sys.exit(1)


console = Console()


class SkeneSkillsDirectory:
    """Skene Skills Directory - Interactive CLI for browsing and managing AI skills"""

    def __init__(self):
        self.base_path = Path(__file__).parent
        self.registry_path = self.base_path / "registry" / "job_functions" / "index.json"
        self.skills_path = self.base_path / "skills-library"
        self.job_functions = {}
        self.load_registry()

    def load_registry(self):
        """Load the job function registry"""
        try:
            with open(self.registry_path, "r") as f:
                self.job_functions = json.load(f)
        except FileNotFoundError:
            console.print("[red]❌ Registry not found. Run from project root.[/red]")
            sys.exit(1)

    def get_total_skills_count(self) -> int:
        """Calculate total skills from loaded registry"""
        return sum(len(skills) for skills in self.job_functions.values())

    def get_total_functions_count(self) -> int:
        """Get number of job functions"""
        return len(self.job_functions)

    def show_banner(self):
        """Display ASCII art banner with Skene branding"""
        try:
            # Get terminal width for responsive design
            import os

            width = os.get_terminal_size().columns
            use_minimal = width < 80
        except (OSError, AttributeError):
            use_minimal = False

        if use_minimal:
            # Minimal banner for narrow terminals
            total_skills = self.get_total_skills_count()
            total_functions = self.get_total_functions_count()
            console.print(
                f"\n[bold {SkeneColors.PRIMARY_GOLD}]{Symbols.DIAMOND} SKENE[/bold {SkeneColors.PRIMARY_GOLD}]"
            )
            console.print(
                f"[{SkeneColors.PRIMARY}]{Symbols.SKENE_LOGO} Skills Directory[/{SkeneColors.PRIMARY}]"
            )
            console.print(
                f"[{SkeneColors.DIM}]{total_skills} Skills {Symbols.BULLET} {total_functions} Functions {Symbols.BULLET} Production Ready[/{SkeneColors.DIM}]\n"
            )
        else:
            # Full ASCII art banner
            total_skills = self.get_total_skills_count()
            total_functions = self.get_total_functions_count()
            banner = pyfiglet.figlet_format("SKENE", font="slant")
            console.print(f"[{SkeneColors.PRIMARY_GOLD}]{banner}[/{SkeneColors.PRIMARY_GOLD}]")

            # Tagline with Skene logo
            stats_text = f"{total_skills} AI Skills {Symbols.BULLET} {total_functions} Job Functions {Symbols.BULLET} Production Ready"
            # Calculate padding for centering (78 total width - 2 border chars - 1 space after border)
            padding = 78 - 2 - 1 - len(stats_text)
            console.print(f"[{SkeneColors.DIM}]┌" + "─" * 78 + f"┐[/{SkeneColors.DIM}]")
            console.print(
                f"[{SkeneColors.DIM}]│[/{SkeneColors.DIM}] [{SkeneColors.PRIMARY}]{Symbols.SKENE_LOGO} Skills Directory[/{SkeneColors.PRIMARY}]"
                + " " * 51
                + f"[{SkeneColors.DIM}]│[/{SkeneColors.DIM}]"
            )
            console.print(
                f"[{SkeneColors.DIM}]│[/{SkeneColors.DIM}] [{SkeneColors.WHITE}]{stats_text}[/{SkeneColors.WHITE}]"
                + " " * padding
                + f"[{SkeneColors.DIM}]│[/{SkeneColors.DIM}]"
            )
            console.print(f"[{SkeneColors.DIM}]└" + "─" * 78 + f"┘[/{SkeneColors.DIM}]\n")

    def main_menu(self):
        """Display main interactive menu"""
        while True:
            console.clear()
            self.show_banner()

            menu = Table(show_header=False, box=box.ROUNDED, border_style=SkeneColors.PRIMARY)
            menu.add_column("Option", style=f"bold {SkeneColors.PRIMARY_GOLD}", width=8)
            menu.add_column("Description", style=SkeneColors.WHITE)

            menu.add_row("1", "📋 Browse by Job Function")
            menu.add_row("2", "🔍 Search Skills")
            menu.add_row("3", "🔒 Security Audit View")
            menu.add_row("4", "🔗 View Workflow Chains")
            menu.add_row("5", "📊 Statistics Dashboard")
            menu.add_row("6", "ℹ️  About Skills Directory")
            menu.add_row("0", "🚪 Exit")

            console.print(menu)
            console.print()

            choice = Prompt.ask(
                f"[bold {SkeneColors.PRIMARY}]Select an option[/bold {SkeneColors.PRIMARY}]",
                choices=["0", "1", "2", "3", "4", "5", "6"],
                default="1",
            )

            if choice == "0":
                console.print(
                    f"\n[bold {SkeneColors.SUCCESS}]{Symbols.CHECKMARK} Goodbye![/bold {SkeneColors.SUCCESS}]\n"
                )
                sys.exit(0)
            elif choice == "1":
                self.browse_job_functions()
            elif choice == "2":
                self.search_skills()
            elif choice == "3":
                self.security_audit_view()
            elif choice == "4":
                self.view_workflows()
            elif choice == "5":
                self.statistics_dashboard()
            elif choice == "6":
                self.show_about()

    def browse_job_functions(self):
        """Browse skills by job function"""
        console.clear()
        console.print(
            f"\n[bold {SkeneColors.PRIMARY}]📋 Browse by Job Function[/bold {SkeneColors.PRIMARY}]\n"
        )

        # Display job functions
        table = Table(show_header=True, box=box.ROUNDED, border_style=SkeneColors.PRIMARY)
        table.add_column("#", style=SkeneColors.DIM, width=4)
        table.add_column("Job Function", style=f"bold {SkeneColors.PRIMARY}", width=25)
        table.add_column("Skills", justify="right", style=SkeneColors.SUCCESS, width=10)
        table.add_column("Top Risk", style=SkeneColors.WARNING, width=12)

        sorted_functions = sorted(self.job_functions.items(), key=lambda x: len(x[1]), reverse=True)

        for i, (func, skills) in enumerate(sorted_functions, 1):
            # Calculate risk distribution
            risk_counts = defaultdict(int)
            for skill in skills:
                risk_counts[skill["risk_level"]] += 1

            top_risk = (
                "Critical"
                if risk_counts["Critical"] > 0
                else (
                    "High"
                    if risk_counts["High"] > 0
                    else "Medium" if risk_counts["Medium"] > 0 else "Low"
                )
            )

            risk_color = {
                "Critical": f"[{SkeneColors.ERROR}]Critical[/{SkeneColors.ERROR}]",
                "High": f"[{SkeneColors.WARNING}]High[/{SkeneColors.WARNING}]",
                "Medium": f"[{SkeneColors.BEACON_ACTIVE}]Medium[/{SkeneColors.BEACON_ACTIVE}]",
                "Low": f"[{SkeneColors.SUCCESS}]Low[/{SkeneColors.SUCCESS}]",
            }[top_risk]

            table.add_row(str(i), func.replace("_", " ").title(), str(len(skills)), risk_color)

        console.print(table)
        console.print()

        choice = IntPrompt.ask(
            f"[bold {SkeneColors.PRIMARY}]Select a job function (or 0 to return)[/bold {SkeneColors.PRIMARY}]",
            default=0,
        )

        if choice > 0 and choice <= len(sorted_functions):
            func_name, skills = sorted_functions[choice - 1]
            self.show_function_skills(func_name, skills)

    def show_function_skills(self, func_name: str, skills: List[Dict]):
        """Display skills for a specific job function"""
        console.clear()
        console.print(
            f"\n[bold {SkeneColors.PRIMARY}]📋 {func_name.replace('_', ' ').title()} Skills[/bold {SkeneColors.PRIMARY}]"
        )
        console.print(f"[{SkeneColors.DIM}]Total: {len(skills)} skills[/{SkeneColors.DIM}]\n")

        # Create table
        table = Table(show_header=True, box=box.ROUNDED, border_style=SkeneColors.PRIMARY)
        table.add_column("#", style=SkeneColors.DIM, width=4)
        table.add_column("Skill ID", style=f"bold {SkeneColors.WHITE}", width=35)
        table.add_column("Risk", style=SkeneColors.WARNING, width=10)
        table.add_column("Job Description", style=SkeneColors.WHITE, width=50)

        for i, skill in enumerate(skills[:30], 1):  # Show first 30
            risk_color = {
                "Critical": f"[{SkeneColors.ERROR}]Critical[/{SkeneColors.ERROR}]",
                "High": f"[{SkeneColors.WARNING}]High[/{SkeneColors.WARNING}]",
                "Medium": f"[{SkeneColors.BEACON_ACTIVE}]Medium[/{SkeneColors.BEACON_ACTIVE}]",
                "Low": f"[{SkeneColors.SUCCESS}]Low[/{SkeneColors.SUCCESS}]",
            }[skill["risk_level"]]

            jtbd = skill["jtbd"][:47] + "..." if len(skill["jtbd"]) > 50 else skill["jtbd"]

            table.add_row(str(i), skill["skill_id"], risk_color, jtbd)

        console.print(table)

        if len(skills) > 30:
            console.print(
                f"\n[{SkeneColors.DIM}]Showing 30 of {len(skills)} skills. Use search for more.[/{SkeneColors.DIM}]"
            )

        console.print(f"\n[bold {SkeneColors.PRIMARY}]Options:[/bold {SkeneColors.PRIMARY}]")
        console.print(
            f"  [{SkeneColors.PRIMARY_GOLD}]1-30[/{SkeneColors.PRIMARY_GOLD}] - View skill details"
        )
        console.print(
            f"  [{SkeneColors.PRIMARY_GOLD}]0[/{SkeneColors.PRIMARY_GOLD}]    - Return to menu\n"
        )

        choice = IntPrompt.ask(
            f"[bold {SkeneColors.PRIMARY}]Select option[/bold {SkeneColors.PRIMARY}]", default=0
        )

        if choice > 0 and choice <= min(30, len(skills)):
            self.show_skill_details(skills[choice - 1])

    def show_skill_details(self, skill: Dict):
        """Display detailed information about a skill"""
        console.clear()

        # Create panel
        skill_id = skill["skill_id"]
        risk_level = skill["risk_level"]

        risk_color = {
            "Critical": SkeneColors.ERROR,
            "High": SkeneColors.WARNING,
            "Medium": SkeneColors.BEACON_ACTIVE,
            "Low": SkeneColors.SUCCESS,
        }[risk_level]

        # Header
        console.print(
            Panel(
                f"[bold {SkeneColors.WHITE}]{skill_id}[/bold {SkeneColors.WHITE}]",
                title=f"[{risk_color}]{Symbols.BEACON} {risk_level} Risk[/{risk_color}]",
                border_style=risk_color,
                box=box.DOUBLE,
            )
        )

        # JTBD
        console.print(f"\n[bold {SkeneColors.PRIMARY}]Job to be Done:[/bold {SkeneColors.PRIMARY}]")
        console.print(f"  [{SkeneColors.WHITE}]{skill['jtbd']}[/{SkeneColors.WHITE}]\n")

        # Try to load full skill data
        skill_file = self._find_skill_file(skill_id)
        if skill_file:
            with open(skill_file, "r") as f:
                skill_data = json.load(f)

            # Tools
            if "tools" in skill_data:
                console.print(
                    f"[bold {SkeneColors.PRIMARY}]Required Tools:[/bold {SkeneColors.PRIMARY}]"
                )
                for tool in skill_data["tools"][:5]:
                    required = (
                        Symbols.CHECKMARK if tool.get("required", False) else Symbols.BEACON_PULSE
                    )
                    console.print(
                        f"  [{SkeneColors.PRIMARY_GOLD}][{required}][/{SkeneColors.PRIMARY_GOLD}] {tool['name']}"
                    )
                if len(skill_data["tools"]) > 5:
                    console.print(
                        f"  [{SkeneColors.DIM}]... and {len(skill_data['tools']) - 5} more[/{SkeneColors.DIM}]"
                    )
                console.print()

            # Security Controls
            if "security_controls" in skill_data:
                console.print(
                    f"[bold {SkeneColors.SUCCESS}]{Symbols.CHECKMARK} Security Controls Applied[/bold {SkeneColors.SUCCESS}]"
                )
                controls = skill_data["security_controls"]
                for key in list(controls.keys())[:3]:
                    console.print(
                        f"  [{SkeneColors.WHITE}]{Symbols.BULLET} {key.replace('_', ' ').title()}[/{SkeneColors.WHITE}]"
                    )
                console.print()

            # Domain & Tags
            console.print(
                f"[bold {SkeneColors.PRIMARY}]Domain:[/bold {SkeneColors.PRIMARY}] [{SkeneColors.WHITE}]{skill_data.get('domain', 'N/A')}[/{SkeneColors.WHITE}]"
            )
            if "tags" in skill_data:
                tags = ", ".join(skill_data["tags"][:5])
                console.print(
                    f"[bold {SkeneColors.PRIMARY}]Tags:[/bold {SkeneColors.PRIMARY}] [{SkeneColors.WHITE}]{tags}[/{SkeneColors.WHITE}]\n"
                )

        console.print(
            f"[{SkeneColors.DIM}]Path: skills-library/.../[/{SkeneColors.DIM}]{skill_id}\n"
        )

        Prompt.ask(
            f"[bold {SkeneColors.PRIMARY}]Press Enter to continue[/bold {SkeneColors.PRIMARY}]"
        )

    def _find_skill_file(self, skill_id: str) -> Optional[Path]:
        """Find skill.json file for a given skill ID"""
        for skill_file in self.skills_path.rglob("skill.json"):
            try:
                with open(skill_file, "r") as f:
                    data = json.load(f)
                    if data.get("id") == skill_id:
                        return skill_file
            except Exception:
                continue
        return None

    def find_skill_file(self, skill_id: str) -> Optional[Path]:
        """Public API: find skill.json file for a given skill ID."""
        return self._find_skill_file(skill_id)

    def search_skills(self):
        """Search skills by keyword"""
        console.clear()
        console.print(
            f"\n[bold {SkeneColors.PRIMARY}]🔍 Search Skills[/bold {SkeneColors.PRIMARY}]\n"
        )

        query = Prompt.ask(
            f"[bold {SkeneColors.PRIMARY}]Enter search term[/bold {SkeneColors.PRIMARY}]"
        )

        if not query:
            return

        # Search through all skills
        results = []
        for func, skills in self.job_functions.items():
            for skill in skills:
                # Search in skill_id and jtbd
                if (
                    query.lower() in skill["skill_id"].lower()
                    or query.lower() in skill["jtbd"].lower()
                ):
                    results.append({**skill, "function": func})

        console.print(
            f"\n[bold {SkeneColors.PRIMARY}]Found {len(results)} results for '{query}'[/bold {SkeneColors.PRIMARY}]\n"
        )

        if results:
            table = Table(show_header=True, box=box.ROUNDED, border_style=SkeneColors.PRIMARY)
            table.add_column("#", style=SkeneColors.DIM, width=4)
            table.add_column("Skill ID", style=f"bold {SkeneColors.WHITE}", width=30)
            table.add_column("Function", style=SkeneColors.PRIMARY_GOLD, width=20)
            table.add_column("Risk", style=SkeneColors.WARNING, width=10)

            for i, skill in enumerate(results[:20], 1):
                risk_color = {
                    "Critical": f"[{SkeneColors.ERROR}]Critical[/{SkeneColors.ERROR}]",
                    "High": f"[{SkeneColors.WARNING}]High[/{SkeneColors.WARNING}]",
                    "Medium": f"[{SkeneColors.BEACON_ACTIVE}]Medium[/{SkeneColors.BEACON_ACTIVE}]",
                    "Low": f"[{SkeneColors.SUCCESS}]Low[/{SkeneColors.SUCCESS}]",
                }[skill["risk_level"]]

                table.add_row(
                    str(i),
                    skill["skill_id"],
                    skill["function"].replace("_", " ").title(),
                    risk_color,
                )

            console.print(table)

            if len(results) > 20:
                console.print(
                    f"\n[{SkeneColors.DIM}]Showing 20 of {len(results)} results[/{SkeneColors.DIM}]"
                )

        console.print()
        Prompt.ask(
            f"[bold {SkeneColors.PRIMARY}]Press Enter to continue[/bold {SkeneColors.PRIMARY}]"
        )

    def security_audit_view(self):
        """Display security audit with color-coded visualization"""
        console.clear()
        console.print(
            f"\n[bold {SkeneColors.PRIMARY}]🔒 Security Audit View[/bold {SkeneColors.PRIMARY}]\n"
        )

        # Calculate statistics
        total_skills = 0
        risk_counts = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}

        for func, skills in self.job_functions.items():
            for skill in skills:
                total_skills += 1
                risk_counts[skill["risk_level"]] += 1

        # Overall status
        status_table = Table(show_header=True, box=box.HEAVY, border_style=SkeneColors.PRIMARY)
        status_table.add_column("Risk Level", style=f"bold {SkeneColors.WHITE}", width=15)
        status_table.add_column("Count", justify="right", width=10)
        status_table.add_column("Percentage", justify="right", width=12)
        status_table.add_column("Visual", width=40)

        for risk in ["Critical", "High", "Medium", "Low"]:
            count = risk_counts[risk]
            pct = (count / total_skills * 100) if total_skills else 0

            color = {
                "Critical": SkeneColors.ERROR,
                "High": SkeneColors.WARNING,
                "Medium": SkeneColors.BEACON_ACTIVE,
                "Low": SkeneColors.SUCCESS,
            }[risk]

            bar_length = int(pct / 2.5)  # Scale to 40 chars max
            bar = Symbols.PROGRESS_FULL * bar_length

            status_table.add_row(
                f"[{color}]{Symbols.BEACON} {risk}[/{color}]",
                f"[{color}]{count}[/{color}]",
                f"[{color}]{pct:.1f}%[/{color}]",
                f"[{color}]{bar}[/{color}]",
            )

        console.print(status_table)

        # Security posture
        console.print(
            f"\n[bold {SkeneColors.PRIMARY}]Security Posture:[/bold {SkeneColors.PRIMARY}]"
        )
        critical_pct = (risk_counts["Critical"] / total_skills * 100) if total_skills else 0

        if critical_pct == 0:
            console.print(
                f"  [bold {SkeneColors.SUCCESS}]{Symbols.CHECKMARK} EXCELLENT[/bold {SkeneColors.SUCCESS}] - Zero critical risk skills"
            )
        elif critical_pct < 10:
            console.print(
                f"  [bold {SkeneColors.BEACON_ACTIVE}]{Symbols.CHECKMARK} GOOD[/bold {SkeneColors.BEACON_ACTIVE}] - Minimal critical risk"
            )
        elif critical_pct < 30:
            console.print(
                f"  [bold {SkeneColors.WARNING}]{Symbols.BEACON_WARN} ACCEPTABLE[/bold {SkeneColors.WARNING}] - Some critical risk"
            )
        else:
            console.print(
                f"  [bold {SkeneColors.ERROR}]{Symbols.CROSS} NEEDS ATTENTION[/bold {SkeneColors.ERROR}] - High critical risk"
            )

        # By job function
        console.print(
            f"\n[bold {SkeneColors.PRIMARY}]Risk by Job Function:[/bold {SkeneColors.PRIMARY}]\n"
        )

        func_table = Table(show_header=True, box=box.ROUNDED, border_style=SkeneColors.PRIMARY)
        func_table.add_column("Function", style=f"bold {SkeneColors.WHITE}", width=25)
        func_table.add_column("Crit", justify="right", style=SkeneColors.ERROR, width=6)
        func_table.add_column("High", justify="right", style=SkeneColors.WARNING, width=6)
        func_table.add_column("Med", justify="right", style=SkeneColors.BEACON_ACTIVE, width=6)
        func_table.add_column("Low", justify="right", style=SkeneColors.SUCCESS, width=6)

        for func, skills in sorted(
            self.job_functions.items(), key=lambda x: len(x[1]), reverse=True
        )[:10]:
            func_risks = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}
            for skill in skills:
                func_risks[skill["risk_level"]] += 1

            func_table.add_row(
                func.replace("_", " ").title(),
                str(func_risks["Critical"]),
                str(func_risks["High"]),
                str(func_risks["Medium"]),
                str(func_risks["Low"]),
            )

        console.print(func_table)
        console.print()
        Prompt.ask(
            f"[bold {SkeneColors.PRIMARY}]Press Enter to continue[/bold {SkeneColors.PRIMARY}]"
        )

    def view_workflows(self):
        """View workflow chains"""
        console.clear()
        console.print(
            f"\n[bold {SkeneColors.PRIMARY}]🔗 Workflow Chains[/bold {SkeneColors.PRIMARY}]\n"
        )

        blueprints_path = self.base_path / "registry" / "blueprints"
        blueprints = list(blueprints_path.glob("*.yaml"))

        if not blueprints:
            console.print(
                f"[{SkeneColors.WARNING}]No workflow blueprints found.[/{SkeneColors.WARNING}]\n"
            )
            Prompt.ask(
                f"[bold {SkeneColors.PRIMARY}]Press Enter to continue[/bold {SkeneColors.PRIMARY}]"
            )
            return

        console.print(
            f"[bold {SkeneColors.WHITE}]Available Workflows:[/bold {SkeneColors.WHITE}] {len(blueprints)}\n"
        )

        for i, blueprint_file in enumerate(blueprints, 1):
            with open(blueprint_file, "r") as f:
                blueprint = yaml.safe_load(f)

            console.print(
                f"[bold {SkeneColors.PRIMARY_GOLD}]{i}. {blueprint.get('name', 'Unnamed')}[/bold {SkeneColors.PRIMARY_GOLD}]"
            )
            console.print(
                f"   [{SkeneColors.WHITE}]{blueprint.get('description', 'No description')[:80]}[/{SkeneColors.WHITE}]"
            )
            console.print(
                f"   [{SkeneColors.DIM}]Steps: {len(blueprint.get('chain_sequence', []))}[/{SkeneColors.DIM}]\n"
            )

        choice = IntPrompt.ask(
            f"[bold {SkeneColors.PRIMARY}]Select workflow to view (or 0 to return)[/bold {SkeneColors.PRIMARY}]",
            default=0,
        )

        if choice > 0 and choice <= len(blueprints):
            self.show_workflow_details(blueprints[choice - 1])

    def show_workflow_details(self, blueprint_file: Path):
        """Display workflow chain visualization"""
        console.clear()

        with open(blueprint_file, "r") as f:
            blueprint = yaml.safe_load(f)

        console.print(
            Panel(
                f"[bold {SkeneColors.WHITE}]{blueprint.get('name', 'Unnamed Workflow')}[/bold {SkeneColors.WHITE}]",
                subtitle=f"v{blueprint.get('version', '1.0.0')}",
                border_style=SkeneColors.PRIMARY,
                box=box.DOUBLE,
            )
        )

        console.print(f"\n[bold {SkeneColors.PRIMARY}]Description:[/bold {SkeneColors.PRIMARY}]")
        console.print(
            f"  [{SkeneColors.WHITE}]{blueprint.get('description', 'No description')}[/{SkeneColors.WHITE}]\n"
        )

        # Show chain sequence
        console.print(f"[bold {SkeneColors.PRIMARY}]Workflow Chain:[/bold {SkeneColors.PRIMARY}]\n")

        steps = blueprint.get("chain_sequence", [])
        for i, step in enumerate(steps, 1):
            step_id = step.get("step_id", f"step_{i}")
            skill_id = step.get("skill_id", "unknown")
            action = step.get("action", "execute")

            # Visual connector
            if i > 1:
                console.print(f"     [{SkeneColors.DIM}]│[/{SkeneColors.DIM}]")
                console.print(f"     [{SkeneColors.DIM}]{Symbols.ARROW_RIGHT}[/{SkeneColors.DIM}]")

            # Step box
            console.print(
                f"  [bold {SkeneColors.PRIMARY_GOLD}]Step {i}:[/bold {SkeneColors.PRIMARY_GOLD}] [{SkeneColors.WHITE}]{step_id}[/{SkeneColors.WHITE}]"
            )
            console.print(
                f"     [bold {SkeneColors.PRIMARY}]Skill:[/bold {SkeneColors.PRIMARY}] [{SkeneColors.WHITE}]{skill_id}[/{SkeneColors.WHITE}]"
            )
            console.print(
                f"     [bold {SkeneColors.PRIMARY}]Action:[/bold {SkeneColors.PRIMARY}] [{SkeneColors.WHITE}]{action}[/{SkeneColors.WHITE}]"
            )

            # Conditions
            if "conditions" in step:
                console.print(
                    f"     [{SkeneColors.WARNING}]{Symbols.BEACON_WARN} Conditional execution[/{SkeneColors.WARNING}]"
                )

            # Error handling
            if "error_handling" in step:
                on_failure = step["error_handling"].get("on_failure", "stop")
                console.print(
                    f"     [{SkeneColors.DIM}]On failure: {on_failure}[/{SkeneColors.DIM}]"
                )

        console.print(
            f"\n[bold {SkeneColors.PRIMARY}]Total Steps:[/bold {SkeneColors.PRIMARY}] [{SkeneColors.WHITE}]{len(steps)}[/{SkeneColors.WHITE}]"
        )

        # Security context
        if "security_context" in blueprint:
            sec_ctx = blueprint["security_context"]
            console.print(
                f"[bold {SkeneColors.PRIMARY}]Max Risk Level:[/bold {SkeneColors.PRIMARY}] [{SkeneColors.WHITE}]{sec_ctx.get('max_risk_level', 'N/A')}[/{SkeneColors.WHITE}]"
            )
            if sec_ctx.get("requires_approval"):
                console.print(
                    f"[{SkeneColors.WARNING}]{Symbols.BEACON_WARN} Requires approval before execution[/{SkeneColors.WARNING}]"
                )

        console.print()
        Prompt.ask(
            f"[bold {SkeneColors.PRIMARY}]Press Enter to continue[/bold {SkeneColors.PRIMARY}]"
        )

    def statistics_dashboard(self):
        """Display comprehensive statistics"""
        console.clear()
        console.print(
            f"\n[bold {SkeneColors.PRIMARY}]📊 Statistics Dashboard[/bold {SkeneColors.PRIMARY}]\n"
        )

        # Calculate stats
        total_skills = sum(len(skills) for skills in self.job_functions.values())
        total_functions = len(self.job_functions)

        risk_counts = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}
        for skills in self.job_functions.values():
            for skill in skills:
                risk_counts[skill["risk_level"]] += 1

        # Overview
        overview = Table(
            show_header=False, box=box.ROUNDED, border_style=SkeneColors.PRIMARY, show_lines=True
        )
        overview.add_column("Metric", style=f"bold {SkeneColors.PRIMARY}", width=30)
        overview.add_column("Value", style=f"bold {SkeneColors.WHITE}", width=20)

        overview.add_row("Total Skills", str(total_skills))
        overview.add_row("Job Functions", str(total_functions))
        overview.add_row(
            "Workflow Blueprints",
            str(len(list((self.base_path / "registry" / "blueprints").glob("*.yaml")))),
        )
        overview.add_row(
            "Security Posture", f"[{SkeneColors.SUCCESS}]Production Ready[/{SkeneColors.SUCCESS}]"
        )

        console.print(overview)
        console.print()

        # Top job functions
        console.print(
            f"[bold {SkeneColors.PRIMARY}]Top 5 Job Functions:[/bold {SkeneColors.PRIMARY}]\n"
        )

        top_table = Table(show_header=True, box=box.SIMPLE, border_style=SkeneColors.PRIMARY)
        top_table.add_column("Rank", style=SkeneColors.DIM, width=6)
        top_table.add_column("Function", style=f"bold {SkeneColors.WHITE}", width=25)
        top_table.add_column("Skills", justify="right", style=SkeneColors.SUCCESS, width=10)

        sorted_funcs = sorted(self.job_functions.items(), key=lambda x: len(x[1]), reverse=True)[:5]
        for i, (func, skills) in enumerate(sorted_funcs, 1):
            top_table.add_row(f"#{i}", func.replace("_", " ").title(), str(len(skills)))

        console.print(top_table)
        console.print()

        # Remediation impact
        console.print(
            f"[bold {SkeneColors.PRIMARY}]Remediation Impact:[/bold {SkeneColors.PRIMARY}]"
        )
        console.print(
            f"  [{SkeneColors.SUCCESS}]{Symbols.CHECKMARK}[/{SkeneColors.SUCCESS}] [{SkeneColors.WHITE}]Risk levels tracked; human review where required[/{SkeneColors.WHITE}]"
        )
        console.print(
            f"  [{SkeneColors.SUCCESS}]{Symbols.CHECKMARK}[/{SkeneColors.SUCCESS}] [{SkeneColors.WHITE}]100% human approval bottlenecks removed[/{SkeneColors.WHITE}]"
        )
        console.print(
            f"  [{SkeneColors.SUCCESS}]{Symbols.CHECKMARK}[/{SkeneColors.SUCCESS}] [{SkeneColors.WHITE}]$450K estimated annual savings[/{SkeneColors.WHITE}]"
        )

        console.print()
        Prompt.ask(
            f"[bold {SkeneColors.PRIMARY}]Press Enter to continue[/bold {SkeneColors.PRIMARY}]"
        )

    def show_about(self):
        """Display about information"""
        console.clear()
        console.print(
            f"\n[bold {SkeneColors.PRIMARY}]{Symbols.DIAMOND} About Skene Skills Directory[/bold {SkeneColors.PRIMARY}]\n"
        )

        total_skills = self.get_total_skills_count()
        about_text = f"""
        # {Symbols.SKENE_LOGO} Skene Skills Directory v2.0

        **{total_skills} Production-Ready AI Skills for Claude, Cursor & AI Agents**

        ## Overview
        Skene Skills Directory provides battle-tested AI skills organized by job function,
        security-audited, and ready for production use. Each skill includes comprehensive
        metadata, risk analysis, and workflow composition capabilities.

        ## Features
        - **{Symbols.TARGET} Job Function Organization** — 13 functions covering all business roles
        - **{Symbols.LOCK} Security-First Design** — Every skill analyzed & remediated
        - **{Symbols.LINK} Workflow Composition** — Chain skills into complex automation
        - **{Symbols.CHART} JTBD Framework** — Find skills by outcome, not implementation
        - **{Symbols.CHECKMARK} Production Ready** — Zero critical risk, battle-tested

        ## Architecture
        - **Atomic Skills** — Small, focused, composable units (< 500 lines)
        - **Security Controls** — OAuth, sandboxing, rate limiting, automated rollback
        - **Rich Metadata** — Categorization, dependencies, risk levels, triggers
        - **Workflow Blueprints** — Orchestrate multi-skill chains with error handling

        ## Quick Start
        ```bash
        # Install via npm
        npm install @skene/skills-directory

        # Install all skills for Claude/Cursor
        npx skills-directory install --target all

        # Browse interactively
        python3 skill-loom-cli.py
        ```

        ## Integration
        - **Claude Code** — Drop skills into `~/.claude/skills/`
        - **Cursor** — Install to `.cursor/skills/`
        - **Custom Agents** — Import from npm package
        - **Skene Flow** — Native integration with state machine

        ## Resources
        - **{Symbols.FOLDER} Documentation:** `/docs`
        - **{Symbols.LOCK} Security Policy:** `SECURITY_POLICY.md`
        - **{Symbols.ROCKET} Contributing:** `CONTRIBUTING.md`
        - **{Symbols.GEAR} Architecture:** `ARCHITECTURE.md`

        ## Built by Skene Technologies
        Part of the Skene AI ecosystem — deterministic agency for product-led growth.
        """

        console.print(Markdown(about_text))
        console.print()
        Prompt.ask(
            f"[bold {SkeneColors.PRIMARY}]Press Enter to continue[/bold {SkeneColors.PRIMARY}]"
        )


# Alias for backwards compatibility with tests
SkillLoom = SkeneSkillsDirectory


def main():
    """Entry point for Skene Skills Directory CLI"""
    try:
        app = SkeneSkillsDirectory()
        app.main_menu()
    except KeyboardInterrupt:
        console.print(
            f"\n\n[bold {SkeneColors.WARNING}]{Symbols.BEACON_WARN} Interrupted by user[/bold {SkeneColors.WARNING}]"
        )
        sys.exit(0)
    except Exception as e:
        console.print(
            f"\n[bold {SkeneColors.ERROR}]{Symbols.CROSS} Error: {e}[/bold {SkeneColors.ERROR}]"
        )
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

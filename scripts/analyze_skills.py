#!/usr/bin/env python3
"""
Skill Analyzer - Automated security analysis and categorization tool
Parses raw skills, assigns security risk levels, and generates enriched metadata
"""

import json
import yaml
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
import argparse


# Security risk keywords and their weights
SECURITY_KEYWORDS = {
    'Critical': [
        'delete', 'remove', 'drop', 'truncate', 'destroy',
        'financial', 'payment', 'credit_card', 'bank_account',
        'password', 'secret', 'credential', 'api_key',
        'execute', 'eval', 'system', 'shell', 'command'
    ],
    'High': [
        'write', 'update', 'modify', 'change', 'alter',
        'access', 'authenticate', 'authorize', 'permission',
        'pii', 'personal', 'sensitive', 'confidential',
        'external_api', 'third_party', 'webhook'
    ],
    'Medium': [
        'read', 'fetch', 'get', 'retrieve', 'query',
        'email', 'notification', 'alert', 'message',
        'analytics', 'track', 'log', 'monitor'
    ],
    'Low': [
        'list', 'search', 'filter', 'sort', 'format',
        'calculate', 'compute', 'aggregate', 'summarize',
        'display', 'show', 'view', 'preview'
    ]
}


# Job function mappings based on domain and description keywords
JOB_FUNCTION_MAPPINGS = {
    'engineering': ['development', 'api', 'integration', 'technical', 'code', 'deploy', 'devops'],
    'marketing': ['campaign', 'content', 'seo', 'brand', 'social', 'advertising', 'promotion'],
    'sales': ['deal', 'pipeline', 'forecast', 'quota', 'opportunity', 'crm', 'revenue'],
    'customer_success': ['health', 'churn', 'retention', 'onboarding', 'support', 'satisfaction', 'nps'],
    'product': ['roadmap', 'feature', 'release', 'backlog', 'user_story', 'sprint'],
    'finance': ['invoice', 'billing', 'payment', 'revenue', 'arr', 'mrr', 'financial', 'budget'],
    'legal': ['compliance', 'contract', 'terms', 'privacy', 'gdpr', 'regulation'],
    'hr': ['hiring', 'recruiting', 'employee', 'performance', 'onboard'],
    'operations': ['workflow', 'process', 'automation', 'efficiency', 'ops'],
    'executive': ['strategy', 'executive', 'board', 'vision', 'objectives', 'kpi'],
    'security': ['security', 'threat', 'vulnerability', 'audit', 'access_control'],
    'data': ['analytics', 'data', 'report', 'dashboard', 'metrics', 'insight'],
    'design': ['design', 'ui', 'ux', 'prototype', 'wireframe', 'mockup']
}


@dataclass
class SkillAnalysis:
    """Result of skill analysis"""
    skill_id: str
    security_risk_level: str
    security_requirements: Dict
    job_function: str
    jtbd: Dict
    risk_factors: List[str]
    composability_hints: List[str]


class SkillAnalyzer:
    """Analyzes skills for security, categorization, and workflow composition"""

    def __init__(self, skills_library_path: str = "skills-library"):
        self.skills_library_path = Path(skills_library_path)
        self.analyzed_skills = []

    def analyze_skill_file(self, skill_json_path: Path) -> Optional[SkillAnalysis]:
        """Analyze a single skill.json file"""
        try:
            with open(skill_json_path, 'r') as f:
                skill_data = json.load(f)

            # Read instructions if available
            instructions_path = skill_json_path.parent / "instructions.md"
            instructions = ""
            if instructions_path.exists():
                with open(instructions_path, 'r') as f:
                    instructions = f.read().lower()

            # Combine text for analysis
            analysis_text = f"{skill_data.get('name', '')} {skill_data.get('description', '')} {instructions}".lower()

            # Determine security risk level
            risk_level, risk_factors = self._calculate_risk_level(analysis_text, skill_data)

            # Determine job function
            job_function = self._determine_job_function(skill_data.get('domain', ''), analysis_text)

            # Extract JTBD
            jtbd = self._extract_jtbd(skill_data)

            # Determine security requirements
            security_reqs = self._determine_security_requirements(risk_level, risk_factors, skill_data)

            # Analyze composability
            composability = self._analyze_composability(skill_data)

            return SkillAnalysis(
                skill_id=skill_data.get('id'),
                security_risk_level=risk_level,
                security_requirements=security_reqs,
                job_function=job_function,
                jtbd=jtbd,
                risk_factors=risk_factors,
                composability_hints=composability
            )

        except Exception as e:
            print(f"Error analyzing {skill_json_path}: {e}", file=sys.stderr)
            return None

    def _calculate_risk_level(self, text: str, skill_data: Dict) -> Tuple[str, List[str]]:
        """Calculate security risk level based on keywords and tool requirements"""
        risk_scores = {'Critical': 0, 'High': 0, 'Medium': 0, 'Low': 0}
        risk_factors = []

        # Analyze text for keywords
        for level, keywords in SECURITY_KEYWORDS.items():
            for keyword in keywords:
                if keyword in text:
                    risk_scores[level] += 1
                    risk_factors.append(keyword)

        # Analyze tools for risky operations
        tools = skill_data.get('tools', [])
        for tool in tools:
            tool_name = tool.get('name', '').lower()
            if any(risky in tool_name for risky in ['delete', 'write', 'update', 'execute', 'admin']):
                risk_scores['High'] += 2
                risk_factors.append(f"risky_tool: {tool.get('name')}")

        # Check for external API calls
        if any('api' in tool.get('name', '').lower() for tool in tools):
            risk_scores['Medium'] += 1
            risk_factors.append('external_api_calls')

        # Determine final risk level
        if risk_scores['Critical'] > 0:
            return 'Critical', risk_factors
        elif risk_scores['High'] >= 2:
            return 'High', risk_factors
        elif risk_scores['High'] > 0 or risk_scores['Medium'] >= 3:
            return 'Medium', risk_factors
        else:
            return 'Low', risk_factors

    def _determine_job_function(self, domain: str, text: str) -> str:
        """Determine primary job function based on domain and content"""
        scores = {func: 0 for func in JOB_FUNCTION_MAPPINGS.keys()}

        # Check domain directly
        if domain.lower() in scores:
            scores[domain.lower()] += 5

        # Check keywords
        for func, keywords in JOB_FUNCTION_MAPPINGS.items():
            for keyword in keywords:
                if keyword in text:
                    scores[func] += 1

        # Return highest scoring function
        max_func = max(scores.items(), key=lambda x: x[1])
        return max_func[0] if max_func[1] > 0 else 'operations'

    def _extract_jtbd(self, skill_data: Dict) -> Dict:
        """Extract Jobs to be Done framework from skill data"""
        description = skill_data.get('description', '')

        # Simple heuristic extraction
        return {
            'job': description,
            'context': f"When working in {skill_data.get('domain', 'general')} domain",
            'outcome': f"Successfully execute {skill_data.get('name', 'task')}"
        }

    def _determine_security_requirements(self, risk_level: str, risk_factors: List[str], skill_data: Dict) -> Dict:
        """Determine security requirements based on risk analysis"""
        reqs = {
            'sandboxing_required': risk_level in ['High', 'Critical'],
            'human_in_loop_required': risk_level == 'Critical',
            'audit_logging': risk_level in ['Medium', 'High', 'Critical'],
            'data_access_scope': [],
            'risk_factors': risk_factors
        }

        # Determine data access scope
        text = f"{skill_data.get('name', '')} {skill_data.get('description', '')}".lower()
        if any(keyword in text for keyword in ['pii', 'personal', 'user_data']):
            reqs['data_access_scope'].append('pii')
        if any(keyword in text for keyword in ['financial', 'payment', 'revenue']):
            reqs['data_access_scope'].append('financial')
        if any(keyword in text for keyword in ['internal', 'confidential']):
            reqs['data_access_scope'].append('confidential')
        if not reqs['data_access_scope']:
            reqs['data_access_scope'].append('internal')

        return reqs

    def _analyze_composability(self, skill_data: Dict) -> List[str]:
        """Analyze how this skill can be composed with others"""
        hints = []

        # Check exit states
        exit_states = skill_data.get('exitStates', [])
        for state in exit_states:
            if state != 'idle':
                hints.append(f"can_chain_to: {state}")

        # Check if skill has clear output schema
        if skill_data.get('outputSchema'):
            hints.append('has_structured_output')

        return hints

    def analyze_all_skills(self) -> List[SkillAnalysis]:
        """Analyze all skills in the library"""
        skill_files = list(self.skills_library_path.rglob("skill.json"))
        print(f"Found {len(skill_files)} skills to analyze...")

        results = []
        for skill_file in skill_files:
            analysis = self.analyze_skill_file(skill_file)
            if analysis:
                results.append(analysis)

        self.analyzed_skills = results
        return results

    def generate_metadata_yaml(self, analysis: SkillAnalysis, output_path: Path):
        """Generate metadata.yaml file for a skill"""
        metadata = {
            'security': {
                'risk_level': analysis.security_risk_level,
                'requirements': analysis.security_requirements
            },
            'categorization': {
                'job_function': analysis.job_function,
                'jtbd': analysis.jtbd
            },
            'composability': {
                'hints': analysis.composability_hints
            }
        }

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            yaml.dump(metadata, f, default_flow_style=False, sort_keys=False)

    def generate_security_report(self, output_path: str = "reports/security_analysis.md"):
        """Generate a comprehensive security analysis report"""
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        risk_distribution = {'Critical': 0, 'High': 0, 'Medium': 0, 'Low': 0}
        for analysis in self.analyzed_skills:
            risk_distribution[analysis.security_risk_level] += 1

        with open(output_path, 'w') as f:
            f.write("# Security Analysis Report\n\n")
            f.write(f"**Total Skills Analyzed:** {len(self.analyzed_skills)}\n\n")
            f.write("## Risk Distribution\n\n")
            for level, count in risk_distribution.items():
                percentage = (count / len(self.analyzed_skills) * 100) if self.analyzed_skills else 0
                f.write(f"- **{level}:** {count} ({percentage:.1f}%)\n")

            f.write("\n## Critical Risk Skills\n\n")
            critical_skills = [s for s in self.analyzed_skills if s.security_risk_level == 'Critical']
            for skill in critical_skills:
                f.write(f"### {skill.skill_id}\n")
                f.write(f"- **Risk Factors:** {', '.join(skill.risk_factors)}\n")
                f.write(f"- **Human-in-loop:** {skill.security_requirements['human_in_loop_required']}\n\n")

    def generate_job_function_index(self, output_path: str = "registry/job_functions/index.json"):
        """Generate index of skills by job function"""
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        index = {}
        for analysis in self.analyzed_skills:
            func = analysis.job_function
            if func not in index:
                index[func] = []
            index[func].append({
                'skill_id': analysis.skill_id,
                'risk_level': analysis.security_risk_level,
                'jtbd': analysis.jtbd['job']
            })

        with open(output_path, 'w') as f:
            json.dump(index, f, indent=2)


def main():
    parser = argparse.ArgumentParser(description='Analyze skills for security and categorization')
    parser.add_argument('--skills-path', default='skills-library', help='Path to skills library')
    parser.add_argument('--action', choices=['analyze', 'report', 'metadata'], default='analyze',
                       help='Action to perform')
    parser.add_argument('--output', help='Output path for reports')

    args = parser.parse_args()

    analyzer = SkillAnalyzer(args.skills_path)

    if args.action == 'analyze':
        print("🔍 Analyzing all skills...")
        results = analyzer.analyze_all_skills()
        print(f"✅ Analyzed {len(results)} skills")

        # Generate default reports
        print("📊 Generating security report...")
        analyzer.generate_security_report()

        print("📋 Generating job function index...")
        analyzer.generate_job_function_index()

        print("\n✨ Analysis complete!")
        print("- Security report: reports/security_analysis.md")
        print("- Job function index: registry/job_functions/index.json")

    elif args.action == 'report':
        results = analyzer.analyze_all_skills()
        output = args.output or 'reports/security_analysis.md'
        analyzer.generate_security_report(output)
        print(f"Report generated: {output}")

    elif args.action == 'metadata':
        print("Generating metadata.yaml files for all skills...")
        results = analyzer.analyze_all_skills()
        for analysis in results:
            # Find the skill directory
            skill_files = list(Path(args.skills_path).rglob("skill.json"))
            for skill_file in skill_files:
                with open(skill_file, 'r') as f:
                    data = json.load(f)
                if data.get('id') == analysis.skill_id:
                    metadata_path = skill_file.parent / "metadata.yaml"
                    analyzer.generate_metadata_yaml(analysis, metadata_path)
                    print(f"Generated: {metadata_path}")
                    break


if __name__ == '__main__':
    main()

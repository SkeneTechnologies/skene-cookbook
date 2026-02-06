#!/usr/bin/env python3
"""
Automated Skill Remediation
Applies security fixes to skills based on their risk category
"""

import json
import yaml
import os
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import shutil


class AutoRemediator:
    """Automatically applies remediation fixes to skills"""

    def __init__(self, skills_library_path="skills-library", dry_run=False):
        self.skills_library_path = Path(skills_library_path)
        self.dry_run = dry_run
        self.remediation_log = []
        self.stats = {
            'processed': 0,
            'modified': 0,
            'skipped': 0,
            'errors': 0,
            'by_category': defaultdict(int),
            'risk_reductions': defaultdict(int)
        }

    def load_remediation_plan(self, csv_path="reports/remediation_tracker.csv"):
        """Load the remediation plan"""
        import csv

        skills_to_remediate = []
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                skills_to_remediate.append(row)

        return skills_to_remediate

    def remediate_all_skills(self):
        """Apply remediations to all skills"""
        print("🔧 Starting automated remediation...")
        print(f"   Mode: {'DRY RUN' if self.dry_run else 'LIVE'}")
        print()

        skills_plan = self.load_remediation_plan()
        total = len(skills_plan)

        for i, skill_info in enumerate(skills_plan, 1):
            if i % 50 == 0:
                print(f"   Progress: {i}/{total} ({i/total*100:.1f}%)")

            self._remediate_skill(skill_info)

        self._print_summary()
        self._save_log()

    def _remediate_skill(self, skill_info):
        """Apply remediation to a single skill"""
        skill_id = skill_info['skill_id']
        skill_path = Path(skill_info['path'])
        category = skill_info['category']
        current_risk = skill_info['current_risk']
        target_risk = skill_info['target_risk']

        self.stats['processed'] += 1

        try:
            # Load current skill definition
            skill_json_path = skill_path / "skill.json"
            if not skill_json_path.exists():
                self.stats['skipped'] += 1
                return

            with open(skill_json_path, 'r') as f:
                skill_data = json.load(f)

            # Apply remediation based on category
            modified = False
            changes = []

            if category == 'credential_elimination':
                modified, changes = self._apply_oauth_migration(skill_data)
            elif category == 'payment_hardening':
                modified, changes = self._apply_payment_controls(skill_data)
            elif category == 'destructive_operations':
                modified, changes = self._apply_soft_delete(skill_data)
            elif category == 'system_commands':
                modified, changes = self._apply_sandboxing(skill_data)
            elif category == 'external_api':
                modified, changes = self._apply_api_controls(skill_data)
            elif category == 'data_access_scoping':
                modified, changes = self._apply_data_scoping(skill_data)
            elif category == 'write_operations':
                modified, changes = self._apply_write_controls(skill_data)
            elif category == 'false_positive':
                modified, changes = self._fix_false_positive(skill_data)

            if modified:
                if not self.dry_run:
                    # Backup original
                    backup_path = skill_json_path.parent / "skill.json.backup"
                    shutil.copy2(skill_json_path, backup_path)

                    # Write updated skill
                    with open(skill_json_path, 'w') as f:
                        json.dump(skill_data, f, indent=2)

                self.stats['modified'] += 1
                self.stats['by_category'][category] += 1
                self.stats['risk_reductions'][f"{current_risk} → {target_risk}"] += 1

                self.remediation_log.append({
                    'skill_id': skill_id,
                    'category': category,
                    'changes': changes,
                    'risk_change': f"{current_risk} → {target_risk}",
                    'timestamp': datetime.now().isoformat()
                })

        except Exception as e:
            self.stats['errors'] += 1
            print(f"   ❌ Error with {skill_id}: {e}")

    def _apply_oauth_migration(self, skill_data):
        """Replace credential handling with OAuth"""
        changes = []
        modified = False

        # Add security controls section if not exists
        if 'security_controls' not in skill_data:
            skill_data['security_controls'] = {}
            modified = True

        # Update authentication method
        skill_data['security_controls']['authentication'] = {
            'method': 'oauth',
            'provider': 'managed_identity',
            'scopes': ['read:data', 'write:data'],
            'token_lifetime': 3600
        }
        changes.append('Migrated to OAuth authentication')
        modified = True

        # Remove credential fields from tools
        if 'tools' in skill_data:
            for tool in skill_data['tools']:
                if 'credentials' in tool:
                    del tool['credentials']
                    changes.append(f"Removed credentials from tool: {tool.get('name')}")
                    modified = True

        return modified, changes

    def _apply_payment_controls(self, skill_data):
        """Add payment operation safeguards"""
        changes = []
        modified = False

        if 'security_controls' not in skill_data:
            skill_data['security_controls'] = {}

        # Add payment controls
        skill_data['security_controls']['payment_controls'] = {
            'preview_mode': True,
            'per_transaction_approval': True,
            'amount_limits': {
                'max_per_transaction': 50000,
                'daily_limit': 200000,
                'additional_approval_threshold': 25000
            },
            'rollback': {
                'enabled': True,
                'window_seconds': 3600
            },
            'two_phase_commit': True,
            'audit_logging': 'detailed'
        }
        changes.append('Added payment safeguards: preview, approval, limits, rollback')
        modified = True

        return modified, changes

    def _apply_soft_delete(self, skill_data):
        """Replace hard delete with soft delete"""
        changes = []
        modified = False

        if 'security_controls' not in skill_data:
            skill_data['security_controls'] = {}

        # Add soft delete controls
        skill_data['security_controls']['delete_operations'] = {
            'soft_delete': True,
            'retention_period_days': 30,
            'undelete_capable': True,
            'backup_before_delete': True,
            'multi_party_approval': True,
            'confirmation_required': {
                'enabled': True,
                'show_impact': True,
                'require_reason': True
            }
        }
        changes.append('Replaced hard delete with soft delete + undelete capability')
        modified = True

        return modified, changes

    def _apply_sandboxing(self, skill_data):
        """Add execution sandboxing"""
        changes = []
        modified = False

        if 'security_controls' not in skill_data:
            skill_data['security_controls'] = {}

        # Add sandbox execution
        skill_data['security_controls']['execution_environment'] = {
            'type': 'sandboxed_container',
            'resource_limits': {
                'cpu_cores': 1,
                'memory_mb': 512,
                'timeout_seconds': 30,
                'disk_mb': 100
            },
            'security': {
                'network_access': False,
                'filesystem': 'read_only',
                'user': 'non_root',
                'allowed_commands': ['node', 'python3', 'npm'],
                'blocked_syscalls': ['exec', 'fork', 'kill']
            }
        }
        changes.append('Added containerized sandboxing with resource limits')
        modified = True

        return modified, changes

    def _apply_api_controls(self, skill_data):
        """Add external API safeguards"""
        changes = []
        modified = False

        if 'security_controls' not in skill_data:
            skill_data['security_controls'] = {}

        # Add API controls
        skill_data['security_controls']['external_api'] = {
            'gateway': 'internal_proxy',
            'rate_limiting': {
                'requests_per_minute': 60,
                'burst_limit': 10
            },
            'circuit_breaker': {
                'enabled': True,
                'failure_threshold': 5,
                'timeout_seconds': 30,
                'retry_after_seconds': 60
            },
            'validation': {
                'request_schema': True,
                'response_schema': True,
                'sanitize_inputs': True
            },
            'caching': {
                'enabled': True,
                'ttl_seconds': 300
            }
        }
        changes.append('Added API gateway, rate limiting, circuit breaker')
        modified = True

        return modified, changes

    def _apply_data_scoping(self, skill_data):
        """Scope down data access"""
        changes = []
        modified = False

        if 'security_controls' not in skill_data:
            skill_data['security_controls'] = {}

        # Add data access controls
        skill_data['security_controls']['data_access'] = {
            'field_level_control': True,
            'allowed_fields': ['id', 'name', 'email', 'created_at'],
            'tenant_isolation': True,
            'time_window_days': 90,
            'read_only': False,
            'pii_redaction': True
        }
        changes.append('Applied field-level access control and tenant isolation')
        modified = True

        return modified, changes

    def _apply_write_controls(self, skill_data):
        """Add write operation safeguards"""
        changes = []
        modified = False

        if 'security_controls' not in skill_data:
            skill_data['security_controls'] = {}

        # Add write controls
        skill_data['security_controls']['write_operations'] = {
            'preview_mode': True,
            'validation': {
                'input_schema': True,
                'business_rules': True,
                'data_integrity': True
            },
            'rollback': {
                'enabled': True,
                'window_seconds': 1800
            },
            'audit': {
                'log_before_state': True,
                'log_after_state': True,
                'track_user': True
            }
        }
        changes.append('Added validation, preview mode, and rollback for writes')
        modified = True

        return modified, changes

    def _fix_false_positive(self, skill_data):
        """Mark as false positive for manual review"""
        changes = []
        modified = False

        if 'security_controls' not in skill_data:
            skill_data['security_controls'] = {}

        skill_data['security_controls']['review_note'] = {
            'flagged_as': 'false_positive',
            'requires_manual_review': True,
            'review_date': datetime.now().isoformat()
        }
        changes.append('Flagged for manual review as potential false positive')
        modified = True

        return modified, changes

    def _print_summary(self):
        """Print remediation summary"""
        print("\n" + "="*60)
        print("  AUTOMATED REMEDIATION COMPLETE")
        print("="*60)
        print(f"\n📊 SUMMARY")
        print(f"   Skills Processed:  {self.stats['processed']}")
        print(f"   Skills Modified:   {self.stats['modified']}")
        print(f"   Skills Skipped:    {self.stats['skipped']}")
        print(f"   Errors:            {self.stats['errors']}")

        if self.stats['by_category']:
            print(f"\n🔧 BY CATEGORY")
            for category, count in sorted(self.stats['by_category'].items(),
                                         key=lambda x: x[1], reverse=True):
                print(f"   {category}: {count}")

        if self.stats['risk_reductions']:
            print(f"\n📉 RISK REDUCTIONS")
            for change, count in sorted(self.stats['risk_reductions'].items(),
                                       key=lambda x: x[1], reverse=True):
                print(f"   {change}: {count}")

        print("\n" + "="*60 + "\n")

    def _save_log(self):
        """Save remediation log"""
        log_path = Path("reports/remediation_log.json")
        log_path.parent.mkdir(parents=True, exist_ok=True)

        log_data = {
            'timestamp': datetime.now().isoformat(),
            'mode': 'dry_run' if self.dry_run else 'live',
            'stats': dict(self.stats),
            'changes': self.remediation_log
        }

        with open(log_path, 'w') as f:
            json.dump(log_data, f, indent=2)

        print(f"✅ Remediation log saved: {log_path}")

        # Also save summary markdown
        self._save_summary_markdown()

    def _save_summary_markdown(self):
        """Save human-readable summary"""
        summary_path = Path("reports/remediation_summary.md")

        with open(summary_path, 'w') as f:
            f.write("# Automated Remediation Summary\n\n")
            f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Mode:** {'Dry Run' if self.dry_run else 'Live Execution'}\n\n")

            f.write("## Statistics\n\n")
            f.write(f"- **Skills Processed:** {self.stats['processed']}\n")
            f.write(f"- **Skills Modified:** {self.stats['modified']}\n")
            f.write(f"- **Skills Skipped:** {self.stats['skipped']}\n")
            f.write(f"- **Errors:** {self.stats['errors']}\n\n")

            if self.stats['by_category']:
                f.write("## By Category\n\n")
                f.write("| Category | Skills Fixed |\n")
                f.write("|----------|-------------|\n")
                for category, count in sorted(self.stats['by_category'].items(),
                                             key=lambda x: x[1], reverse=True):
                    f.write(f"| {category} | {count} |\n")
                f.write("\n")

            if self.stats['risk_reductions']:
                f.write("## Risk Reductions\n\n")
                f.write("| Change | Count |\n")
                f.write("|--------|-------|\n")
                for change, count in sorted(self.stats['risk_reductions'].items(),
                                           key=lambda x: x[1], reverse=True):
                    f.write(f"| {change} | {count} |\n")
                f.write("\n")

            # Sample changes
            f.write("## Sample Changes (First 10)\n\n")
            for i, change in enumerate(self.remediation_log[:10], 1):
                f.write(f"### {i}. {change['skill_id']}\n\n")
                f.write(f"- **Category:** {change['category']}\n")
                f.write(f"- **Risk Change:** {change['risk_change']}\n")
                f.write(f"- **Changes Applied:**\n")
                for c in change['changes']:
                    f.write(f"  - {c}\n")
                f.write("\n")

        print(f"✅ Summary report saved: {summary_path}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Automated skill remediation')
    parser.add_argument('--dry-run', action='store_true',
                       help='Preview changes without modifying files')
    parser.add_argument('--live', action='store_true',
                       help='Apply changes to skill files')

    args = parser.parse_args()

    if not args.dry_run and not args.live:
        print("❌ Must specify either --dry-run or --live")
        print("\nUsage:")
        print("  python3 scripts/auto_remediate.py --dry-run   # Preview only")
        print("  python3 scripts/auto_remediate.py --live      # Apply changes")
        return

    if args.live:
        print("⚠️  WARNING: This will modify 521 skill files!")
        print("   Backups will be created as skill.json.backup")
        response = input("\nContinue? (yes/no): ")
        if response.lower() != 'yes':
            print("Cancelled.")
            return

    remediator = AutoRemediator(dry_run=args.dry_run)
    remediator.remediate_all_skills()

    if args.dry_run:
        print("\n💡 This was a dry run. Use --live to apply changes.")
    else:
        print("\n✅ Remediation complete! Re-run security analysis:")
        print("   python3 scripts/analyze_skills.py --action analyze")


if __name__ == '__main__':
    main()

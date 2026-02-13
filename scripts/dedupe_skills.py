#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2024-2026 Skene Technologies

"""
Semantic Deduplication Engine for Skills Directory
Uses sentence transformers to identify duplicate and similar skills
"""

import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import yaml

try:
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity
except ImportError:
    print("❌ Missing dependencies. Install with:")
    print("   pip3 install sentence-transformers scikit-learn")
    exit(1)


class SkillDeduplicator:
    """Semantic deduplication engine for skills"""

    def __init__(self, similarity_threshold=0.88, base_path="."):
        self.base_path = Path(base_path)
        self.similarity_threshold = similarity_threshold
        self.skills_path = self.base_path / "skills-library"

        print("🔄 Loading semantic model (this may take a moment)...")
        self.model = SentenceTransformer("all-MiniLM-L6-v2")  # Lightweight, fast

        self.skills = []
        self.embeddings = None
        self.duplicates = []
        self.similar_pairs = []
        self.incomplete = []
        self.unique_verified = []

    def load_all_skills(self):
        """Load all skills from the library"""
        print("\n📥 Loading skills from library...")

        skill_files = list(self.skills_path.rglob("skill.json"))
        print(f"   Found {len(skill_files)} skill files")

        for skill_file in skill_files:
            try:
                with open(skill_file, "r") as f:
                    skill_data = json.load(f)

                # Load metadata if available
                metadata_file = skill_file.parent / "metadata.yaml"
                metadata = {}
                if metadata_file.exists():
                    with open(metadata_file, "r") as f:
                        metadata = yaml.safe_load(f)

                # Combine skill data
                skill_record = {
                    "file_path": str(skill_file),
                    "skill_id": skill_data.get("id"),
                    "name": skill_data.get("name", ""),
                    "description": skill_data.get("description", ""),
                    "domain": skill_data.get("domain", ""),
                    "tools": skill_data.get("tools", []),
                    "inputSchema": skill_data.get("inputSchema"),
                    "outputSchema": skill_data.get("outputSchema"),
                    "tags": skill_data.get("tags", []),
                    "metadata": metadata,
                }

                self.skills.append(skill_record)

            except Exception as e:
                print(f"   ⚠️  Error loading {skill_file}: {e}")

        print(f"   ✅ Loaded {len(self.skills)} skills successfully")

    def generate_embeddings(self):
        """Generate semantic embeddings for all skills"""
        print("\n🧠 Generating semantic embeddings...")

        # Combine description and name for better matching
        texts = []
        for skill in self.skills:
            text = f"{skill['name']} {skill['description']}"
            texts.append(text)

        # Generate embeddings
        self.embeddings = self.model.encode(texts, show_progress_bar=True)
        print(f"   ✅ Generated {len(self.embeddings)} embeddings")

    def find_duplicates(self):
        """Find duplicate and similar skills using cosine similarity"""
        print(f"\n🔍 Finding duplicates (threshold: {self.similarity_threshold})...")

        # Calculate similarity matrix
        similarity_matrix = cosine_similarity(self.embeddings)

        # Find pairs above threshold
        seen_pairs = set()
        duplicate_groups = defaultdict(list)

        for i in range(len(self.skills)):
            for j in range(i + 1, len(self.skills)):
                similarity = similarity_matrix[i][j]

                if similarity >= self.similarity_threshold:
                    pair_key = tuple(sorted([i, j]))
                    if pair_key not in seen_pairs:
                        seen_pairs.add(pair_key)

                        # High similarity = duplicate
                        if similarity >= 0.95:
                            duplicate_groups[i].append((j, similarity))
                        # Medium-high similarity = similar/merge candidate
                        elif similarity >= self.similarity_threshold:
                            self.similar_pairs.append(
                                {
                                    "skill1": self.skills[i],
                                    "skill2": self.skills[j],
                                    "similarity": float(similarity),
                                    "recommendation": "merge" if similarity > 0.92 else "review",
                                }
                            )

        # Process duplicate groups
        for primary_idx, duplicates in duplicate_groups.items():
            group = {
                "primary": self.skills[primary_idx],
                "duplicates": [
                    {"skill": self.skills[dup_idx], "similarity": float(sim)}
                    for dup_idx, sim in duplicates
                ],
                "recommendation": "delete_duplicates",
            }
            self.duplicates.append(group)

        print(f"   🔴 Found {len(self.duplicates)} duplicate groups")
        print(f"   🟡 Found {len(self.similar_pairs)} similar pairs for review")

    def validate_completeness(self):
        """Validate skills for completeness"""
        print("\n✅ Validating skill completeness...")

        required_fields = ["id", "name", "description"]
        recommended_fields = ["inputSchema", "outputSchema", "domain"]

        for skill in self.skills:
            issues = []

            # Check required fields
            for field in required_fields:
                if not skill.get(field):
                    issues.append(f"Missing required field: {field}")

            # Check recommended fields
            missing_recommended = []
            for field in recommended_fields:
                if not skill.get(field):
                    missing_recommended.append(field)

            if missing_recommended:
                issues.append(f"Missing recommended: {', '.join(missing_recommended)}")

            # Check security metadata
            if not skill.get("metadata") or "security" not in skill.get("metadata", {}):
                issues.append("Missing security metadata")

            if issues:
                self.incomplete.append(
                    {
                        "skill_id": skill.get("skill_id"),
                        "name": skill.get("name"),
                        "file_path": skill.get("file_path"),
                        "issues": issues,
                    }
                )

        print(f"   ⚠️  Found {len(self.incomplete)} incomplete skills")

    def identify_unique_verified(self):
        """Identify unique, verified, production-ready skills"""
        print("\n🎯 Identifying unique, verified skills...")

        # Get IDs of all duplicates and incomplete skills
        duplicate_ids = set()
        for dup_group in self.duplicates:
            for dup in dup_group["duplicates"]:
                duplicate_ids.add(dup["skill"]["skill_id"])

        incomplete_ids = {skill["skill_id"] for skill in self.incomplete}

        # Find unique, complete skills
        for skill in self.skills:
            skill_id = skill.get("skill_id")

            if skill_id not in duplicate_ids and skill_id not in incomplete_ids:
                # Additional quality checks
                has_io_types = bool(skill.get("inputSchema") and skill.get("outputSchema"))
                has_security = "security" in skill.get("metadata", {})
                has_jtbd = "jtbd" in skill.get("metadata", {}).get("categorization", {})

                quality_score = sum([has_io_types, has_security, has_jtbd])

                self.unique_verified.append(
                    {
                        "skill_id": skill_id,
                        "name": skill.get("name"),
                        "domain": skill.get("domain"),
                        "file_path": skill.get("file_path"),
                        "quality_score": quality_score,
                        "has_io_types": has_io_types,
                        "has_security": has_security,
                        "has_jtbd": has_jtbd,
                    }
                )

        print(f"   ✅ Identified {len(self.unique_verified)} unique, verified skills")

    def generate_report(self):
        """Generate comprehensive deduplication report"""
        print("\n📊 Generating deduplication report...")

        report = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "total_skills_analyzed": len(self.skills),
                "similarity_threshold": self.similarity_threshold,
                "model_used": "all-MiniLM-L6-v2",
            },
            "summary": {
                "duplicate_groups": len(self.duplicates),
                "similar_pairs": len(self.similar_pairs),
                "incomplete_skills": len(self.incomplete),
                "unique_verified_skills": len(self.unique_verified),
                "deletion_candidates": sum(len(g["duplicates"]) for g in self.duplicates),
                "merge_candidates": len(
                    [p for p in self.similar_pairs if p["recommendation"] == "merge"]
                ),
                "review_candidates": len(
                    [p for p in self.similar_pairs if p["recommendation"] == "review"]
                ),
            },
            "duplicates": {
                "groups": self.duplicates,
                "action": "DELETE - These are near-identical duplicates",
            },
            "similar_pairs": {
                "pairs": self.similar_pairs,
                "action": "MERGE or REVIEW - These have similar functionality",
            },
            "incomplete": {
                "skills": self.incomplete,
                "action": "FIX - These need additional metadata",
            },
            "unique_verified": {
                "skills": sorted(
                    self.unique_verified, key=lambda x: x["quality_score"], reverse=True
                ),
                "action": "PROMOTE - These are production-ready",
            },
        }

        # Save report
        report_path = self.base_path / "reports" / "dedupe_report.json"
        report_path.parent.mkdir(exist_ok=True)

        with open(report_path, "w") as f:
            json.dump(report, f, indent=2)

        print(f"   ✅ Report saved: {report_path}")

        # Generate summary markdown
        self._generate_summary_markdown(report)

        return report

    def _generate_summary_markdown(self, report):
        """Generate human-readable summary"""
        summary_path = self.base_path / "reports" / "dedupe_summary.md"

        with open(summary_path, "w") as f:
            f.write("# Skills Deduplication Report\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            # Summary
            f.write("## Summary\n\n")
            f.write(f"- **Total Skills Analyzed:** {report['metadata']['total_skills_analyzed']}\n")
            f.write(f"- **Similarity Threshold:** {report['metadata']['similarity_threshold']}\n\n")

            f.write("### Findings\n\n")
            f.write("| Category | Count | Action |\n")
            f.write("|----------|-------|--------|\n")
            f.write(
                f"| 🔴 Duplicate Groups | {report['summary']['duplicate_groups']} | DELETE duplicates |\n"
            )
            f.write(
                f"| 🟡 Similar Pairs | {report['summary']['similar_pairs']} | MERGE or REVIEW |\n"
            )
            f.write(
                f"| ⚠️  Incomplete Skills | {report['summary']['incomplete_skills']} | FIX metadata |\n"
            )
            f.write(
                f"| ✅ Unique & Verified | {report['summary']['unique_verified_skills']} | PROMOTE to production |\n\n"
            )

            f.write("### Impact\n\n")
            f.write(f"- **Skills to Delete:** {report['summary']['deletion_candidates']}\n")
            f.write(f"- **Skills to Merge:** {report['summary']['merge_candidates']}\n")
            f.write(f"- **Skills to Review:** {report['summary']['review_candidates']}\n")
            f.write(f"- **Production-Ready:** {report['summary']['unique_verified_skills']}\n\n")

            # Duplicate groups
            if report["duplicates"]["groups"]:
                f.write("## 🔴 Duplicate Groups (Recommend DELETE)\n\n")
                for i, group in enumerate(report["duplicates"]["groups"][:10], 1):
                    f.write(f"### Group {i}\n\n")
                    primary = group.get("primary")
                    if not primary and group.get("duplicates"):
                        primary = group["duplicates"][0].get("skill") or {}
                    primary = primary or {}
                    primary_id = primary.get("skill_id") or primary.get("id", "?")
                    f.write(f"**Primary:** `{primary_id}`\n\n")
                    f.write("**Duplicates:**\n")
                    for dup in group.get("duplicates", []):
                        sid = (dup.get("skill") or {}).get("skill_id") or (
                            dup.get("skill") or {}
                        ).get("id", "?")
                        sim = dup.get("similarity", 0)
                        f.write(f"- `{sid}` (similarity: {sim:.3f})\n")
                    f.write("\n")

                if len(report["duplicates"]["groups"]) > 10:
                    f.write(
                        f"\n*... and {len(report['duplicates']['groups']) - 10} more groups*\n\n"
                    )

            # Similar pairs
            if report["similar_pairs"]["pairs"]:
                f.write("## 🟡 Similar Pairs (Recommend MERGE or REVIEW)\n\n")
                for i, pair in enumerate(report["similar_pairs"]["pairs"][:10], 1):
                    f.write(f"### Pair {i} - {pair['recommendation'].upper()}\n\n")
                    f.write(f"- **Skill 1:** `{pair['skill1']['skill_id']}`\n")
                    f.write(f"- **Skill 2:** `{pair['skill2']['skill_id']}`\n")
                    f.write(f"- **Similarity:** {pair['similarity']:.3f}\n")
                    f.write(f"- **Recommendation:** {pair['recommendation']}\n\n")

                if len(report["similar_pairs"]["pairs"]) > 10:
                    f.write(
                        f"\n*... and {len(report['similar_pairs']['pairs']) - 10} more pairs*\n\n"
                    )

            # Incomplete
            if report["incomplete"]["skills"]:
                f.write("## ⚠️  Incomplete Skills (Recommend FIX)\n\n")
                for i, skill in enumerate(report["incomplete"]["skills"][:20], 1):
                    f.write(f"{i}. `{skill['skill_id']}` - {', '.join(skill['issues'])}\n")

                if len(report["incomplete"]["skills"]) > 20:
                    f.write(f"\n*... and {len(report['incomplete']['skills']) - 20} more*\n\n")

            # Top quality skills
            f.write("\n## ✅ Top Quality Unique Skills (Production Ready)\n\n")
            top_skills = sorted(
                report["unique_verified"]["skills"], key=lambda x: x["quality_score"], reverse=True
            )[:20]

            f.write("| Skill ID | Domain | Quality Score |\n")
            f.write("|----------|--------|---------------|\n")
            for skill in top_skills:
                f.write(
                    f"| `{skill['skill_id']}` | {skill['domain']} | {skill['quality_score']}/3 |\n"
                )

            f.write("\n---\n\n")
            f.write("**Next Steps:**\n")
            f.write("1. Review duplicate groups and confirm deletions\n")
            f.write("2. Merge or refine similar pairs\n")
            f.write("3. Fix incomplete skills\n")
            f.write("4. Promote unique verified skills to production registry\n")

        print(f"   ✅ Summary saved: {summary_path}")

    def print_summary(self):
        """Print summary to console"""
        print("\n" + "=" * 70)
        print("  DEDUPLICATION ANALYSIS COMPLETE")
        print("=" * 70)
        print(f"\n📊 RESULTS")
        print(f"   Total Skills Analyzed:    {len(self.skills)}")
        print(f"   🔴 Duplicate Groups:       {len(self.duplicates)}")
        print(f"   🟡 Similar Pairs:          {len(self.similar_pairs)}")
        print(f"   ⚠️  Incomplete Skills:      {len(self.incomplete)}")
        print(f"   ✅ Unique & Verified:      {len(self.unique_verified)}")

        print(f"\n💡 RECOMMENDATIONS")
        total_deletions = sum(len(g["duplicates"]) for g in self.duplicates)
        print(f"   Delete:    {total_deletions} duplicate skills")
        print(
            f"   Merge:     {len([p for p in self.similar_pairs if p['recommendation'] == 'merge'])} similar pairs"
        )
        print(
            f"   Review:    {len([p for p in self.similar_pairs if p['recommendation'] == 'review'])} borderline cases"
        )
        print(f"   Fix:       {len(self.incomplete)} incomplete skills")
        print(f"   Promote:   {len(self.unique_verified)} to production")

        print("\n📁 REPORTS")
        print("   • reports/dedupe_report.json (detailed JSON)")
        print("   • reports/dedupe_summary.md (human-readable)")

        print("\n" + "=" * 70 + "\n")


def main():
    print("🔄 Skills Semantic Deduplication Engine")
    print("=" * 70)

    deduplicator = SkillDeduplicator(similarity_threshold=0.88)

    # Execute pipeline
    deduplicator.load_all_skills()
    deduplicator.generate_embeddings()
    deduplicator.find_duplicates()
    deduplicator.validate_completeness()
    deduplicator.identify_unique_verified()

    # Generate reports
    report = deduplicator.generate_report()
    deduplicator.print_summary()

    print("✅ Deduplication complete!")
    print("\nNext: Review reports/dedupe_summary.md for detailed findings")


if __name__ == "__main__":
    main()

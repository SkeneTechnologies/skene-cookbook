#!/usr/bin/env python3
"""
Reorder and renumber SKILL_CHAINS.md so recipes use rolling numbers 1-36
within category order. Updates headings and all #recipe-N- anchors.
"""
import re
from pathlib import Path

DOC = Path(__file__).resolve().parent.parent / "docs" / "SKILL_CHAINS.md"

# (old_recipe_number, slug_hint) in desired order. "quick6" = ### Recipe 6 in Quick Reference.
ORDER = [
    (1, "sales-deal-qualification"), (3, "financial-intelligence"), (13, "product-led-sales"), (22, "competitive-intelligence"),
    (2, "customer-churn"), (14, "ai-support-deflection"), (24, "customer-education"), (32, "ai-ops-conversation"),
    ("quick6", "customer-onboarding"), ("quick7", "support-ticket-triage"),
    (4, "growth-optimization"), (5, "content-marketing"), (11, "freemium-conversion"), (12, "usage-based-pricing"),
    (18, "community-led-growth"), (19, "multi-platform-content"), ("quick9", "pricing--packaging"), ("quick10", "product-analytics"),
    (15, "developer-experience"), (20, "product-experimentation"), (21, "api-lifecycle"), (25, "security-code-review"), (30, "superpowers-development"),
    (23, "brand-consistency"),
    (16, "employee-onboarding"), (17, "data-quality"), (26, "compliance-automation"), (27, "e-commerce-revenue"), (28, "partnership-ecosystem"),
    (35, "people-ops-talent"), (36, "data-ops-experimentation"), ("quick8", "partnership-deal"),
    (29, "scientific-research"), (31, "skene-growth-strategy"),
    (34, "community-advocacy"),
    (33, "finops-standalone"),
]


def slug(s: str) -> str:
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9-]", "", s.lower().replace(" ", "-").replace("&", "and"))).strip("-")


def main():
    text = DOC.read_text(encoding="utf-8")

    # Intro: up to and including "---" after "## Recipe index by domain" table
    idx = text.find("\n## Recipe 1: ")
    if idx == -1:
        raise SystemExit("Could not find ## Recipe 1:")
    intro = text[:idx]

    # Split into sections: ## Recipe N: Title ... or ### Recipe N: Title ...
    section_re = re.compile(
        r'^(## Recipe (\d+): (.+?)|### Recipe (\d+): (.+?)|## Recipe \d+-\d+: .+?)$',
        re.MULTILINE,
    )
    pos = idx
    sections = []
    while pos < len(text):
        m = section_re.search(text, pos)
        if not m:
            # Rest of file (Phase 2, Tips, etc.)
            tail_start = text.find("\n## Phase 2:", pos)
            if tail_start == -1:
                tail_start = text.find("\n## Tips for Building", pos)
            if tail_start == -1:
                tail_start = text.find("\n### Quick Reference: Healthcare", pos)
            if tail_start != -1:
                sections.append(("_tail", None, None, text[pos:tail_start]))
                sections.append(("_tail_rest", None, None, text[tail_start:]))
            break
        start = m.start()
        if start > pos and "_tail" not in [s[0] for s in sections]:
            chunk = text[pos:start].strip()
            if chunk and "Recipe 1:" not in chunk:
                sections.append(("_between", None, None, text[pos:start]))
        full_match = m.group(0)
        if full_match.startswith("## Recipe ") and ":" in full_match and not full_match.startswith("## Recipe 1:"):
            # "## Recipe 6-10: Quick Reference"
            if "-" in full_match.split(":")[0]:
                end = text.find("\n## Recipe ", start + 2)
                if end == -1:
                    end = text.find("\n## Phase ", start + 2)
                if end == -1:
                    end = text.find("\n## Tips ", start + 2)
                if end == -1:
                    end = len(text)
                block = text[start:end]
                # Parse ### Recipe 6, 7, 8, 9, 10
                for q in [6, 7, 8, 9, 10]:
                    qm = re.search(rf'\n### Recipe {q}: (.+?)\n\n', block)
                    if qm:
                        qcontent = block[qm.start():]
                        next_q = re.search(r'\n### Recipe \d+: ', qcontent[10:])
                        if next_q:
                            qcontent = qcontent[:10 + next_q.start()]
                        next_sec = re.search(r'\n## Recipe \d+: ', qcontent)
                        if next_sec:
                            qcontent = qcontent[:next_sec.start()]
                        qcontent = qcontent.strip()
                        title = qm.group(1).strip()
                        sections.append((f"quick{q}", title, qcontent))
                pos = end
                continue
        num = m.group(2) or m.group(4)
        title = (m.group(3) or m.group(5)).strip()
        num = int(num) if num.isdigit() else num
        end = text.find("\n## Recipe ", start + 2)
        if end == -1:
            end = text.find("\n## Phase ", start + 2)
        if end == -1:
            end = text.find("\n## Tips ", start + 2)
        if end == -1:
            end = text.find("\n### Quick Reference: Healthcare", start + 2)
        if end == -1:
            end = len(text)
        content = text[start:end]
        sections.append((num, title, content))
        pos = end
        if pos >= len(text):
            break

    # Build old_key -> new_num (1..36)
    old_to_new = {}
    for i, (old_key, _) in enumerate(ORDER, 1):
        old_to_new[old_key] = i

    # Build old_anchor -> new_anchor for each recipe (we need title for slug)
    # From sections we have (num, title, content). num can be int or "quick6" etc.
    old_anchors_to_new = {}
    for item in sections:
        if item[0] in ("_tail", "_between", "_tail_rest"):
            continue
        old_key, title, _ = item
        s = slug(title)
        if isinstance(old_key, int):
            old_anchors_to_new[f"recipe-{old_key}-{s}"] = None  # fill below
        else:
            old_anchors_to_new[f"recipe-{old_key}-{s}"] = None

    new_num = 0
    for item in sections:
        if item[0] in ("_tail", "_between", "_tail_rest"):
            continue
        old_key, title, _ = item
        new_num = old_to_new.get(old_key, new_num)
        s = slug(title)
        if isinstance(old_key, int):
            old_anchors_to_new[f"recipe-{old_key}-{s}"] = f"recipe-{new_num}-{s}"
        else:
            old_anchors_to_new[f"recipe-{old_key}-{s}"] = f"recipe-{new_num}-{s}"

    # Order sections for output: only recipe sections, sorted by new number
    ordered = []
    for old_key, hint in ORDER:
        for i, item in enumerate(sections):
            if item[0] in ("_tail", "_between", "_tail_rest"):
                continue
            ok, title, content = item
            if ok != old_key:
                continue
            new_num = old_to_new[old_key]
            slug_s = slug(title)
            new_heading = f"## Recipe {new_num}: {title}"
            # Fix anchors in content
            content_fixed = content
            for old_a, new_a in old_anchors_to_new.items():
                if new_a and old_a in content_fixed:
                    content_fixed = content_fixed.replace(f"#{old_a}", f"#{new_a}")
            # Replace first line (old heading) with new heading
            first_line = content_fixed.split("\n")[0]
            if first_line.startswith("## Recipe ") or first_line.startswith("### Recipe "):
                content_fixed = new_heading + content_fixed[len(first_line):]
            else:
                content_fixed = new_heading + "\n" + content_fixed
            ordered.append((new_num, content_fixed))
            break
        else:
            raise SystemExit(f"Section not found for {old_key} / {hint}")

    # New nav and index
    nav = """## 📋 Quick Navigation

### 💼 Sales & Revenue

- [Recipe 1: Sales Deal Qualification Pipeline](#recipe-1-sales-deal-qualification-pipeline)
- [Recipe 2: Financial Intelligence Dashboard](#recipe-2-financial-intelligence-dashboard)
- [Recipe 3: Product-Led Sales Handoff](#recipe-3-product-led-sales-handoff)
- [Recipe 4: Competitive Intelligence Automation](#recipe-4-competitive-intelligence-automation)

### 🤝 Customer Success & Support

- [Recipe 5: Customer Churn Prevention Pipeline](#recipe-5-customer-churn-prevention-pipeline)
- [Recipe 6: AI Support Deflection System](#recipe-6-ai-support-deflection-system)
- [Recipe 7: Customer Education Platform](#recipe-7-customer-education-platform)
- [Recipe 8: AI Ops Conversation Pipeline](#recipe-8-ai-ops-conversation-pipeline)
- [Recipe 9: Customer Onboarding Automation](#recipe-9-customer-onboarding-automation)
- [Recipe 10: Support Ticket Triage & Resolution](#recipe-10-support-ticket-triage--resolution)

### 🚀 Growth & Marketing

- [Recipe 11: Growth Optimization Engine](#recipe-11-growth-optimization-engine)
- [Recipe 12: Content Marketing Automation](#recipe-12-content-marketing-automation)
- [Recipe 13: Freemium Conversion Optimization](#recipe-13-freemium-conversion-optimization)
- [Recipe 14: Usage-Based Pricing Engine](#recipe-14-usage-based-pricing-engine)
- [Recipe 15: Community-Led Growth Engine](#recipe-15-community-led-growth-engine)
- [Recipe 16: Multi-Platform Content Distribution](#recipe-16-multi-platform-content-distribution)
- [Recipe 17: Pricing & Packaging Optimization](#recipe-17-pricing--packaging-optimization)
- [Recipe 18: Product Analytics Intelligence](#recipe-18-product-analytics-intelligence)

### 🔧 Product & Engineering

- [Recipe 19: Developer Experience Onboarding](#recipe-19-developer-experience-onboarding)
- [Recipe 20: Product Experimentation Engine](#recipe-20-product-experimentation-engine)
- [Recipe 21: API Lifecycle Management](#recipe-21-api-lifecycle-management)
- [Recipe 22: Security Code Review Automation](#recipe-22-security-code-review-automation)
- [Recipe 23: Superpowers Development Workflow](#recipe-23-superpowers-development-workflow)

### 🎨 Brand & Content

- [Recipe 24: Brand Consistency Engine](#recipe-24-brand-consistency-engine)

### ⚙️ Operations & Compliance

- [Recipe 25: Employee Onboarding Automation](#recipe-25-employee-onboarding-automation)
- [Recipe 26: Data Quality Automation](#recipe-26-data-quality-automation)
- [Recipe 27: Compliance Automation Hub](#recipe-27-compliance-automation-hub)
- [Recipe 28: E-commerce Revenue Optimization](#recipe-28-e-commerce-revenue-optimization)
- [Recipe 29: Partnership Ecosystem Automation](#recipe-29-partnership-ecosystem-automation)
- [Recipe 30: People Ops Talent Intelligence](#recipe-30-people-ops-talent-intelligence)
- [Recipe 31: Data Ops Experimentation Pipeline](#recipe-31-data-ops-experimentation-pipeline)
- [Recipe 32: Partnership Deal Flow](#recipe-32-partnership-deal-flow)

### 🔬 Research & Strategy

- [Recipe 33: Scientific Research Synthesis Pipeline](#recipe-33-scientific-research-synthesis-pipeline)
- [Recipe 34: Skene Growth Strategy Chain](#recipe-34-skene-growth-strategy-chain)

### 🌐 Community

- [Recipe 35: Community Advocacy Pipeline](#recipe-35-community-advocacy-pipeline)

### 💰 FinOps

- [Recipe 36: FinOps Standalone Dashboard](#recipe-36-finops-standalone-dashboard)

---

## Recipe index by domain

| Domain | Recipe numbers |
|--------|----------------|
| **Sales & RevOps** | 1, 2, 3, 4 |
| **Customer Success & Support** | 5, 6, 7, 8, 9, 10 |
| **Growth & Marketing** | 11, 12, 13, 14, 15, 16, 17, 18 |
| **Product & Engineering** | 19, 20, 21, 22, 23 |
| **Brand & Content** | 24 |
| **Operations & Compliance** | 25, 26, 27, 28, 29, 30, 31, 32 |
| **Research & Strategy** | 33, 34 |
| **Community** | 35 |
| **FinOps** | 36 |

---
"""

    # Replace intro from "## 📋 Quick Navigation" through "---" before "## Recipe 1:"
    intro_start = intro.find("## 📋 Quick Navigation")
    intro_end = intro.find("---", intro.find("## Recipe index by domain"))
    intro_end = intro.find("\n", intro_end + 4) + 1  # include newline after ---
    new_intro = intro[:intro_start] + nav + intro[intro_end:]

    # Reconstruct body: drop "## Recipe 1:" from first ordered block (we added it above)
    body_parts = []
    for _, content in ordered:
        body_parts.append(content)

    tail = ""
    for item in sections:
        if item[0] == "_tail_rest":
            tail = item[3]
            break

    out = new_intro + "\n".join(body_parts) + "\n" + tail
    DOC.write_text(out, encoding="utf-8")
    print("Renumbered SKILL_CHAINS.md (1-36 by category)")


if __name__ == "__main__":
    main()

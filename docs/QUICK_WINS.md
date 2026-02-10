# Quick Wins: Value in Your First Day

Get immediate value from Skills Directory with these time-boxed quick wins. Start small, prove ROI, then expand.

---

## 🚀 15-Minute Win: Lead Scoring

**What You'll Build:** Automated lead scoring that prioritizes your sales team's time

**Value:** Save 5-10 hours/week on manual lead research

**Skills Used:** 2 skills
- `lead_qualification`
- `opportunity_scoring`

### Step-by-Step

#### 1. Install (2 minutes)

```bash
# Install the package
npm install @skene/skills-directory

# Install RevOps skills
npx skills-directory install --target revops
```

#### 2. Set Up Lead Qualification (5 minutes)

Create a simple qualification check:

```json
{
  "skill": "lead_qualification",
  "input": {
    "lead": {
      "company": "Acme Corp",
      "revenue": "$50M",
      "employees": 250,
      "industry": "SaaS",
      "title": "VP Engineering"
    },
    "framework": "BANT"
  }
}
```

#### 3. Add Scoring (5 minutes)

Chain to opportunity scoring:

```json
{
  "skill": "opportunity_scoring",
  "input": {
    "qualificationData": "{{previous.output}}",
    "scoringFactors": ["company_size", "budget_authority", "urgency"]
  }
}
```

#### 4. Test (3 minutes)

Run with sample lead:

```bash
# Test the 2-skill chain
curl -X POST http://localhost:3000/api/chains/lead-scoring \
  -d '{"leadId": "test-123"}'
```

### Expected Output

```json
{
  "qualified": true,
  "score": 85,
  "tier": "high_value",
  "reasoning": {
    "company_size": "Good fit - 250 employees",
    "budget": "Likely has budget - $50M revenue",
    "authority": "Strong - VP level",
    "need": "Confirmed need in SaaS vertical"
  },
  "recommendation": "High priority - schedule call within 48 hours"
}
```

### What You've Achieved

✅ Automated qualification that used to take 30 minutes
✅ Consistent scoring across all leads
✅ Clear prioritization for your sales team
✅ Foundation to add more skills later

### Next Step

Add `deal_inspection` skill to analyze deal health once opportunity is created.

---

## ⚡ 1-Hour Win: Churn Risk Alerts

**What You'll Build:** Real-time customer health monitoring with at-risk alerts

**Value:** Catch churning customers 60-90 days earlier

**Skills Used:** 3 skills
- `health_scoring`
- `churn_prediction`
- `escalation_manager`

### Step-by-Step

#### 1. Install (5 minutes)

```bash
# Install Customer Success skills
npx skills-directory install --target customer_success
```

#### 2. Configure Health Scoring (20 minutes)

Set up continuous health monitoring:

```json
{
  "skill": "health_scoring",
  "trigger": "scheduled_daily",
  "input": {
    "accountId": "{{account.id}}",
    "signals": {
      "product_usage": {
        "source": "analytics",
        "weight": 0.4,
        "threshold": "3_days_no_activity"
      },
      "support_tickets": {
        "source": "zendesk",
        "weight": 0.3,
        "threshold": "3_tickets_in_7_days"
      },
      "nps_score": {
        "source": "survey",
        "weight": 0.3,
        "threshold": "below_6"
      }
    }
  },
  "exit_routing": {
    "healthy": "log_and_continue",
    "at_risk": "churn_prediction"
  }
}
```

#### 3. Add Churn Prediction (15 minutes)

Chain to predictive model:

```json
{
  "skill": "churn_prediction",
  "input": {
    "accountId": "{{previous.accountId}}",
    "healthScore": "{{previous.score}}",
    "historicalData": {
      "usage_trend": "{{analytics.30_day_trend}}",
      "engagement_trend": "{{crm.activity_trend}}",
      "support_sentiment": "{{support.sentiment_score}}"
    },
    "predictionWindow": "90_days"
  },
  "exit_routing": {
    "high_risk": "escalation_manager",
    "medium_risk": "escalation_manager",
    "low_risk": "monitor_only"
  }
}
```

#### 4. Set Up Escalation (15 minutes)

Alert the right people:

```json
{
  "skill": "escalation_manager",
  "input": {
    "accountId": "{{chain.accountId}}",
    "riskLevel": "{{previous.riskScore}}",
    "context": "{{chain.all_data}}"
  },
  "notifications": [
    {
      "role": "assigned_csm",
      "channel": "slack",
      "urgency": "immediate"
    },
    {
      "role": "csm_manager",
      "channel": "email",
      "urgency": "within_24h"
    }
  ]
}
```

#### 5. Test & Deploy (5 minutes)

Run on a test account:

```bash
# Test with known at-risk account
curl -X POST http://localhost:3000/api/chains/churn-prevention \
  -d '{"accountId": "test-account-456"}'
```

### Expected Output

```json
{
  "accountId": "acct-456",
  "healthScore": 42,
  "churnRisk": "high",
  "churnProbability": 0.73,
  "riskFactors": [
    "Usage down 60% over 30 days",
    "3 support tickets in past week",
    "NPS score: 4 (detractor)"
  ],
  "recommendedActions": [
    "Schedule executive business review",
    "Audit product usage and identify gaps",
    "Offer training session"
  ],
  "escalated_to": ["csm-jane-smith", "manager-bob-jones"]
}
```

### What You've Achieved

✅ Automated health monitoring across all accounts
✅ Predictive alerts 60-90 days before churn
✅ Automatic escalation to right team members
✅ Clear action items for retention

### What This Saves

**Before:**
- Manual quarterly business reviews catch issues late
- Reactive responses after customers already frustrated
- Lost: $50K-$100K ARR per churned account

**After:**
- Proactive intervention 60-90 days early
- Time to recover at-risk accounts
- Saved: $200K-$400K ARR annually (4-8 accounts)

### Next Step

Add `risk_mitigation_playbook` to automatically start intervention strategies.

---

## 🎯 Half-Day Win: Campaign Launch Automation

**What You'll Build:** End-to-end campaign creation, launch, and tracking

**Value:** Cut campaign launch time from 2 weeks to 2 days

**Skills Used:** 5 skills
- `content_research_writer`
- `copywriting`
- `social_content_generator`
- `email_sequence`
- `analytics_tracking`

### Step-by-Step

#### 1. Install (10 minutes)

```bash
# Install Marketing skills
npx skills-directory install --target marketing
```

#### 2. Content Research & Creation (1 hour)

Generate campaign content:

```json
{
  "skill": "content_research_writer",
  "input": {
    "topic": "Product launch: New AI features",
    "audience": "B2B SaaS founders and CTOs",
    "contentTypes": ["blog_post", "landing_page", "announcement"],
    "targetLength": 1200,
    "tone": "professional_enthusiastic",
    "includeExamples": true,
    "competitorAnalysis": true
  },
  "exit_routing": {
    "draft_complete": "copywriting"
  }
}
```

#### 3. Copy Refinement (30 minutes)

Polish the messaging:

```json
{
  "skill": "copywriting",
  "input": {
    "draft": "{{previous.output}}",
    "tone": "professional_friendly",
    "brandVoice": "{{company.brand_guidelines}}",
    "optimizeFor": [
      "clarity",
      "engagement",
      "cta_conversion"
    ],
    "includeCTA": {
      "primary": "Start free trial",
      "secondary": "Book demo"
    }
  },
  "exit_routing": {
    "copy_refined": "social_content_generator"
  }
}
```

#### 4. Multi-Channel Content (45 minutes)

Generate social posts:

```json
{
  "skill": "social_content_generator",
  "input": {
    "sourceContent": "{{previous.output}}",
    "platforms": {
      "twitter": {
        "count": 5,
        "style": "thread",
        "includeImages": true
      },
      "linkedin": {
        "count": 3,
        "style": "long_form",
        "includeCarousel": true
      },
      "facebook": {
        "count": 2,
        "style": "engagement"
      }
    },
    "hashtags": "auto_generate",
    "schedule": "optimal_times"
  },
  "exit_routing": {
    "social_content_ready": "email_sequence"
  }
}
```

#### 5. Email Sequence (45 minutes)

Create nurture emails:

```json
{
  "skill": "email_sequence",
  "input": {
    "campaign": "{{chain.campaign_name}}",
    "audience": "existing_users_and_prospects",
    "sequenceType": "product_launch",
    "emails": [
      {
        "timing": "launch_day",
        "subject": "auto_generate",
        "focus": "announcement_and_benefits"
      },
      {
        "timing": "3_days_later",
        "subject": "auto_generate",
        "focus": "social_proof_and_case_study"
      },
      {
        "timing": "7_days_later",
        "subject": "auto_generate",
        "focus": "limited_time_offer"
      }
    ],
    "personalization": ["name", "company", "usage_data"]
  },
  "exit_routing": {
    "sequence_ready": "analytics_tracking"
  }
}
```

#### 6. Analytics Setup (30 minutes)

Track everything:

```json
{
  "skill": "analytics_tracking",
  "input": {
    "campaignId": "{{chain.campaign_id}}",
    "trackingPlan": {
      "events": [
        "email_opened",
        "email_clicked",
        "landing_page_viewed",
        "cta_clicked",
        "trial_started",
        "demo_booked"
      ],
      "properties": [
        "source",
        "medium",
        "campaign",
        "content_variant"
      ]
    },
    "destinations": ["mixpanel", "google_analytics", "crm"],
    "dashboards": ["campaign_overview", "conversion_funnel"]
  }
}
```

#### 7. Deploy & Monitor (30 minutes)

Launch the campaign:

```bash
# Deploy all campaign assets
npx skills-directory run-chain campaign-launch \
  --campaign "ai-features-launch" \
  --launch-date "2025-03-01"
```

### Expected Output

```
Campaign Assets Generated:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📄 Content Created:
   ✓ Blog post (1,247 words)
   ✓ Landing page copy (3 sections)
   ✓ Product announcement

📱 Social Media:
   ✓ Twitter thread (5 tweets)
   ✓ LinkedIn posts (3 long-form)
   ✓ Facebook posts (2)

📧 Email Sequence:
   ✓ Launch announcement
   ✓ Case study follow-up (day 3)
   ✓ Limited offer (day 7)

📊 Tracking:
   ✓ UTM parameters configured
   ✓ Event tracking active
   ✓ Dashboard created

🚀 Status: Ready to launch
```

### Campaign Performance Dashboard

After launch, monitor:

```
┌──────────────────────────────────────────────┐
│ Campaign: AI Features Launch                │
├──────────────────────────────────────────────┤
│ Email Performance:                           │
│   Sent: 5,247                                │
│   Open Rate: 32.4% (↑ 8% vs avg)            │
│   Click Rate: 8.7% (↑ 3% vs avg)            │
│                                              │
│ Social Performance:                          │
│   Impressions: 47K                           │
│   Engagement: 3.2K (6.8% rate)               │
│   Link clicks: 847                           │
│                                              │
│ Conversions:                                 │
│   Landing page visits: 2,134                 │
│   Trials started: 127 (5.9% CVR)             │
│   Demos booked: 34                           │
│                                              │
│ ROI: $47K pipeline generated                 │
└──────────────────────────────────────────────┘
```

### What You've Achieved

✅ Complete campaign launched in 4 hours (was 2 weeks)
✅ Consistent messaging across all channels
✅ Automated tracking and reporting
✅ Professional-quality content

### What This Saves

**Before:**
- 2 weeks: Content writer, designer, campaign manager
- Cost: $10K-$15K in agency/team time
- Launch: Often delayed, inconsistent messaging

**After:**
- 4 hours: One marketing person + skill chain
- Cost: $500-$1K in time
- Launch: On time, consistent across channels

**Savings:** $9K-$14K per campaign, 10x faster

### Next Step

Add `ab_test_setup` to test subject lines and CTAs automatically.

---

## Choose Your Path

### New to AI Agents?
→ Start with **15-Minute Win: Lead Scoring**
- Simplest chain (2 skills)
- Immediate, tangible value
- Foundation for more complex chains

### Have CRM/Analytics Already?
→ Try **1-Hour Win: Churn Alerts**
- Leverages existing data
- High-value outcomes (save ARR)
- Minimal setup required

### Ready to Scale?
→ Deploy **Half-Day Win: Campaign Automation**
- Complex multi-skill chain
- End-to-end workflow
- Maximum time savings

---

## What's Next?

### After Your First Win

1. **Measure the impact** — Track time saved, quality improvements
2. **Share with your team** — Show them what's possible
3. **Expand the chain** — Add more skills to the working chain
4. **Try another use case** — Pick from [SKILL_CHAINS.md](./SKILL_CHAINS.md)

### Building Confidence

Each quick win teaches you:
- How to chain skills together
- How to configure inputs/outputs
- How to test and iterate
- How to measure ROI

### Scaling Up

Once you've proven value with a quick win:
- Browse [SKILL_CHAINS.md](./SKILL_CHAINS.md) for more complex recipes
- Read [VALUE.md](./VALUE.md) for ROI calculations
- Join the community to share your success

---

## Troubleshooting Quick Wins

### "Skill not found" error

**Problem:** Skill isn't installed
**Solution:**
```bash
npx skills-directory install --target all --domain [domain_name]
```

### "Invalid input format" error

**Problem:** Input JSON doesn't match skill's expected format
**Solution:**
```bash
# View skill documentation
npx skills-directory info [skill_name]
```

### Chain doesn't connect

**Problem:** Exit states don't match next skill's entry points
**Solution:**
- Check exit_routing matches available states
- Review skill documentation for valid exit states

### Results are generic

**Problem:** Not enough context in inputs
**Solution:**
- Add more customer/account-specific data
- Include historical context
- Use richer data sources

---

## Support

**Need help?** Check these resources:

- **Full recipes:** [SKILL_CHAINS.md](./SKILL_CHAINS.md)
- **Value & ROI:** [VALUE.md](./VALUE.md)
- **GitHub Issues:** [Report bugs or ask questions](https://github.com/SkeneTechnologies/skene-cookbook/issues)
- **Discussions:** [Community forum](https://github.com/SkeneTechnologies/skene-cookbook/discussions)

---

**Ready to start?** Pick your quick win and deploy your first skill chain today.

```bash
npm install @skene/skills-directory
npx skills-directory install --target all
```

# Integration reference schemas

Reference schemas describe the **exact fields, objects, and events** to wire from external systems (Salesforce, HubSpot, Stripe, etc.) into skill chains. Use them with Clay, n8n, or custom ETL so builders ship faster without reinventing mappings.

## Format

Each reference schema file (JSON or YAML) should include:

- **system**: Name of the system (e.g. `salesforce`, `hubspot`, `stripe`).
- **chain_ids** or **recipe_ids**: Which workflow/recipe(s) this schema supports.
- **required_objects** / **required_events**: Objects or event types that must be available.
- **fields** / **properties**: Required or recommended fields and their types; optional mapping to skill step inputs.

Optional: map fields to skill input names so runtime can bind CRM/billing data to chain steps.

## Files

| File                                       | System     | Purpose                                                                          |
| ------------------------------------------ | ---------- | -------------------------------------------------------------------------------- |
| `salesforce_lead_qualification_chain.json` | Salesforce | Lead/Opportunity/Contact/Account for Recipe 1–style sales chains                 |
| `hubspot_events_lead_scoring.json`         | HubSpot    | Engagement events and properties for lead scoring chains                         |
| `stripe_usage_expansion.json`              | Stripe     | Subscription, usage, invoice for usage-based and expansion chains (Recipe 12/13) |

## Usage in blueprints

In a workflow blueprint YAML, reference these schemas under `integration_reference.schemas`:

```yaml
integration_reference:
  description: 'Exact fields/events to wire for this chain (Clay, n8n, etc.)'
  schemas:
    - ref: registry/integration_schemas/salesforce_lead_qualification_chain.json
      role: 'CRM source for lead/opportunity data'
    - ref: registry/integration_schemas/hubspot_events_lead_scoring.json
      role: 'Engagement events for scoring'
```

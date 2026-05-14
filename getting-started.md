# Getting Started with SRE AI Toolkit

## Prerequisites

- Python 3.9+
- An Anthropic API key (get one at console.anthropic.com)

## Installation

```bash
git clone https://github.com/YOUR_USERNAME/sre-ai-toolkit
cd sre-ai-toolkit
pip install anthropic
export ANTHROPIC_API_KEY=sk-ant-...
```

## Running the Tools

### 1. Alert Triage

```bash
python scripts/alert-triage.py \
  --alert-name "HighErrorRate" \
  --service "checkout-api" \
  --threshold "5%" \
  --current-value "14.2%" \
  --context "Deploy v3.1.0 at 09:15 UTC, added new payment provider"
```

**Output:** Severity assessment, ranked root causes, investigation steps, remediation options.

---

### 2. Runbook Generator

```bash
# From a postmortem file
python scripts/runbook-generator.py \
  --postmortem incidents/2024-01-15-postmortem.txt \
  --service checkout-api \
  --output runbooks/checkout-api-db-exhaustion.md

# Run with demo data (no file needed)
python scripts/runbook-generator.py
```

**Output:** Full Markdown runbook saved to the specified file.

---

### 3. SLO Narrator

```bash
python scripts/slo-narrator.py \
  --service payment-api \
  --slo-target 99.9 \
  --current-availability 99.71 \
  --error-budget-remaining 28 \
  --burn-rate 3.2 \
  --window 30d
```

**Output:** Three versions of an SLO narrative: engineering, leadership, and status page.

---

## Using the Prompt Templates

The `prompts/` directory contains copy-paste templates for Claude.ai chat:

| Template | When to use |
|----------|-------------|
| `alert-enrichment.md` | Paste when triaging a complex alert manually |
| `postmortem-to-runbook.md` | After writing a postmortem, generate the runbook |
| `slo-review.md` | Every Monday for weekly reliability review |

---

## Next Steps

1. **Integrate with PagerDuty**: Pass real alert payloads into `alert-triage.py`
2. **Add to your on-call runbook**: Link these tools in your team's incident response guide
3. **Schedule slo-narrator.py**: Run weekly via cron and post to Slack automatically
4. **Contribute back**: Encountered a new incident pattern? Add a prompt template!

# 🔭 SRE AI Toolkit

> Claude-powered automation for modern observability & SRE workflows.

A production-ready collection of AI agents and prompt templates that automate the most time-consuming parts of site reliability engineering — alert triage, runbook generation, SLO reporting, and incident response.

## 🚀 What's Inside

| Tool | Description |
|------|-------------|
| `alert-triage.py` | Enriches firing alerts with root cause hypotheses and suggested actions |
| `runbook-generator.py` | Generates structured runbooks from incident postmortems |
| `slo-narrator.py` | Converts raw SLO burn rate data into plain-English summaries |

## ⚡ Quick Start

```bash
pip install anthropic
export ANTHROPIC_API_KEY=your_key_here

# Triage a firing alert
python scripts/alert-triage.py --alert-name "HighErrorRate" --service "payment-api" \
    --threshold "5%" --current-value "12.3%"

# Generate a runbook from a postmortem
python scripts/runbook-generator.py --postmortem postmortem.txt --output runbook.md

# Narrate SLO burn rate data
python scripts/slo-narrator.py --service payment-api --slo-target 99.9 \
    --current-availability 99.71 --error-budget-remaining 28 --burn-rate 3.2
```

## 🧠 Philosophy

These tools treat Claude as an **ops reasoning engine** — not a chatbot. Each script feeds structured observability context (metrics, logs, alert definitions) into Claude and extracts structured, actionable output.

## 📁 Structure

```
sre-ai-toolkit/
├── scripts/
│   ├── alert-triage.py        # Alert enrichment agent
│   ├── runbook-generator.py   # Postmortem → Runbook
│   └── slo-narrator.py        # SLO data → Human narratives
├── prompts/
│   ├── alert-enrichment.md    # Chat prompt template for alert triage
│   ├── postmortem-to-runbook.md
│   └── slo-review.md
└── docs/
    └── getting-started.md
```

## 🎯 Use Cases

- **On-call automation**: Pre-triage alerts before the engineer even opens their laptop
- **Runbook authoring**: Turn postmortems into living documentation automatically
- **SLO storytelling**: Make burn rate data understandable to non-technical stakeholders
- **Incident comms**: Draft internal and external incident updates in seconds

## 🗺️ Roadmap

- [ ] PagerDuty webhook integration
- [ ] Prometheus/Grafana API connectors
- [ ] Slack bot interface
- [ ] Multi-agent incident commander

---
Built by an SRE, for SREs. Contributions welcome.

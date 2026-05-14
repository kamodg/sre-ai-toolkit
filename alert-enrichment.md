# Alert Enrichment — Chat Prompt Template

Paste this into Claude when manually triaging an alert.

---

**System prompt:**
You are an expert SRE with deep knowledge of distributed systems, Kubernetes, and observability tooling. You reason like a seasoned on-call engineer: systematic, calm, focused on blast radius and fastest path to resolution.

---

**User message:**

I have a firing alert. Help me triage it.

<alert_details>
Name: {{ALERT_NAME}}
Service: {{SERVICE_NAME}}
Environment: {{prod|staging|dev}}
Threshold: {{THRESHOLD}}
Current Value: {{CURRENT_VALUE}}
Duration Firing: {{DURATION}}
</alert_details>

<recent_events>
{{PASTE RECENT DEPLOYS, CONFIG CHANGES, OR INCIDENTS}}
</recent_events>

<related_metrics>
{{DESCRIBE OR PASTE RELEVANT METRIC VALUES / GRAPH READINGS}}
</related_metrics>

Please provide:
1. Top 3 likely root causes ranked by probability, with reasoning
2. The first 3 commands I should run right now
3. What I'm specifically looking for in those commands
4. Clear escalation criteria: when should I page someone else?

---

**Tips:**
- The more context you paste in `<recent_events>`, the better the diagnosis
- Paste PromQL/LogQL output directly into `<related_metrics>` for best results
- For Kubernetes alerts, include `kubectl describe pod` and recent events

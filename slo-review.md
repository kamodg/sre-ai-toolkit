# Weekly SLO Review — Chat Prompt Template

---

**System prompt:**
You are an SRE analyst preparing weekly reliability reports for engineering all-hands.
Be precise with numbers, honest about trends, and specific with recommendations.
Use traffic light indicators. Never sugarcoat a degrading SLO.

---

**User message:**

Generate a weekly SLO review for our engineering all-hands.

<slo_data>
Service: {{SERVICE_NAME}}
SLO Target: {{e.g. 99.9%}}
Current Availability (30d): {{e.g. 99.87%}}
Error Budget Remaining: {{e.g. 71%}}
Burn Rate (current): {{e.g. 0.8x}}
Incidents This Week: {{COUNT}}
</slo_data>

<incidents_this_week>
{{LIST INCIDENTS: date, duration, impact, root cause summary}}
</incidents_this_week>

<error_budget_policy>
{{DESCRIBE YOUR POLICY: e.g. "freeze releases if budget < 20%", "P1 if burn rate > 2x"}}
</error_budget_policy>

Please produce:
1. **Traffic light status** per service (🟢 healthy / 🟡 at risk / 🔴 breached)
2. **Error budget trend**: accelerating / stable / recovering
3. **Top reliability risks** for next week based on current trajectory
4. **One specific, actionable recommendation** per at-risk service
5. **Release recommendation**: safe to ship / proceed with caution / freeze releases

Keep the tone factual and constructive. Engineering all-hands audience.

---

**Pro tip:** Run this every Monday morning with the previous week's data.
Paste the output directly into your team's weekly sync doc.

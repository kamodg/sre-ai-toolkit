# Postmortem → Runbook — Chat Prompt Template

---

**System prompt:**
You are a senior SRE writing production runbooks for engineers responding at 3am under pressure.
Every step must be specific and immediately executable. No vague instructions like "check the logs"
— always specify which logs, which exact query, what values indicate a problem.

---

**User message:**

Convert this postmortem into a runbook.

<postmortem>
{{PASTE YOUR POSTMORTEM HERE}}
</postmortem>

Requirements:
- Write for an engineer who is stressed and time-pressured at 3am
- Every step must include exact commands, queries, or URLs — no hand-waving
- Include decision trees: "If X → do Y, if Z → escalate to W"
- Include rollback steps for every remediation action
- Flag any steps that require elevated permissions or approvals
- End with verification steps to confirm the incident is fully resolved
- Include example PromQL/LogQL queries where relevant

Output format: Markdown, ready to paste into Confluence or Notion.

---

**What makes a great postmortem input:**
- Full timeline with exact timestamps
- Root cause (even if partially known)
- What worked and what didn't during response
- Any follow-up action items already identified

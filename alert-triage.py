#!/usr/bin/env python3
"""
alert-triage.py
---------------
Feeds a firing alert + recent metric context into Claude and returns:
  - Root cause hypotheses (ranked by likelihood)
  - Immediate investigation steps
  - Suggested remediation actions
  - Related services to check

Usage:
    python alert-triage.py --alert-name "HighErrorRate" --service "payment-api" \
                           --threshold "5%" --current-value "12.3%" \
                           --context "Recent deploy 14:32 UTC"
"""

import anthropic
import argparse
import json
from datetime import datetime, timezone


def triage_alert(
    alert_name: str,
    service: str,
    threshold: str,
    current_value: str,
    context: str = "",
    metric_history: list = None
) -> dict:
    """Send alert context to Claude and return structured triage output."""
    client = anthropic.Anthropic()

    metric_history_str = ""
    if metric_history:
        metric_history_str = "\n".join(
            [f"  {m['time']}: {m['value']}" for m in metric_history]
        )

    prompt = f"""You are an expert SRE performing alert triage. Analyze this firing alert and provide structured guidance.

<alert>
  Name: {alert_name}
  Service: {service}
  Threshold: {threshold}
  Current Value: {current_value}
  Fired At: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}
</alert>

<context>
{context if context else "No additional context provided."}
</context>

<metric_history>
{metric_history_str if metric_history_str else "No metric history provided."}
</metric_history>

Respond ONLY with a JSON object (no markdown, no preamble):
{{
  "severity_assessment": "critical|high|medium|low",
  "likely_causes": [
    {{"rank": 1, "cause": "...", "confidence": "high|medium|low", "reasoning": "..."}}
  ],
  "immediate_steps": ["step 1", "step 2", "step 3"],
  "remediation_options": [
    {{"action": "...", "risk": "low|medium|high", "eta_minutes": 0}}
  ],
  "related_services": ["service1", "service2"],
  "escalate_to_human": true,
  "escalation_reason": "..."
}}"""

    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )

    return json.loads(message.content[0].text.strip())


def format_output(result: dict, alert_name: str) -> str:
    colors = {"critical": "\033[91m", "high": "\033[93m", "medium": "\033[94m", "low": "\033[92m"}
    reset, bold = "\033[0m", "\033[1m"
    sev = result.get("severity_assessment", "unknown")
    c = colors.get(sev, "")

    lines = [
        f"\n{bold}{'='*60}{reset}",
        f"{bold}ALERT TRIAGE: {alert_name}{reset}",
        f"{'='*60}",
        f"{bold}Severity:{reset} {c}{sev.upper()}{reset}\n",
        f"{bold}Likely Causes:{reset}",
    ]
    for cause in result.get("likely_causes", []):
        lines.append(f"  #{cause['rank']} [{cause['confidence'].upper()}] {cause['cause']}")
        lines.append(f"     └─ {cause['reasoning']}")

    lines += [f"\n{bold}Immediate Steps:{reset}"]
    for i, step in enumerate(result.get("immediate_steps", []), 1):
        lines.append(f"  {i}. {step}")

    lines += [f"\n{bold}Remediation Options:{reset}"]
    for opt in result.get("remediation_options", []):
        lines.append(f"  • {opt['action']}  [Risk: {opt['risk']} | ETA: ~{opt['eta_minutes']}min]")

    if result.get("related_services"):
        lines += [f"\n{bold}Check Related Services:{reset}", "  " + ", ".join(result["related_services"])]

    if result.get("escalate_to_human"):
        lines += [f"\n{c}{bold}ESCALATE TO HUMAN{reset}", f"  {result.get('escalation_reason')}"]

    lines.append(f"\n{'='*60}\n")
    return "\n".join(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI-powered alert triage")
    parser.add_argument("--alert-name", default="HighErrorRate")
    parser.add_argument("--service", default="payment-api")
    parser.add_argument("--threshold", default="5%")
    parser.add_argument("--current-value", default="12.3%")
    parser.add_argument("--context", default="Deploy at 14:32 UTC pushed v2.4.1 to payment-api")
    args = parser.parse_args()

    sample_history = [
        {"time": "14:00 UTC", "value": "1.2%"},
        {"time": "14:15 UTC", "value": "1.4%"},
        {"time": "14:30 UTC", "value": "1.3%"},
        {"time": "14:45 UTC", "value": "4.8%"},
        {"time": "15:00 UTC", "value": "12.3%"},
    ]

    print("Analyzing alert with Claude...")
    result = triage_alert(
        alert_name=args.alert_name,
        service=args.service,
        threshold=args.threshold,
        current_value=args.current_value,
        context=args.context,
        metric_history=sample_history
    )

    print(format_output(result, args.alert_name))

    with open("triage-output.json", "w") as f:
        json.dump(result, f, indent=2)
    print("Full JSON saved to triage-output.json")

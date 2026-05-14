#!/usr/bin/env python3
"""
slo-narrator.py
---------------
Converts raw SLO burn rate data into plain-English summaries for:
  - Engineering teams (technical detail)
  - Leadership / stakeholders (business impact)
  - Status page (public-facing)

Usage:
    python slo-narrator.py --service payment-api --slo-target 99.9 \
                           --current-availability 99.71 \
                           --error-budget-remaining 28 --burn-rate 3.2
"""

import anthropic
import argparse
import json


def generate_slo_narrative(slo_data: dict) -> dict:
    client = anthropic.Anthropic()

    prompt = f"""You are an SRE communications specialist. Generate SLO status narratives.

<slo_data>
{json.dumps(slo_data, indent=2)}
</slo_data>

Return ONLY a JSON object (no markdown):
{{
  "engineering": {{
    "subject": "...",
    "body": "3-5 sentences with specific metrics, burn rate context, technical next steps",
    "action_required": true,
    "urgency": "immediate|this-week|monitor"
  }},
  "leadership": {{
    "subject": "...",
    "body": "2-3 sentences in business terms: what users experienced, current status, what team is doing. No jargon.",
    "business_impact": "low|medium|high",
    "customer_facing": true
  }},
  "status_page": {{
    "title": "...",
    "body": "1-2 sentences max. Factual, calm. No internal metrics.",
    "status": "operational|degraded_performance|partial_outage|major_outage"
  }},
  "recommendations": ["specific action 1", "specific action 2"]
}}"""

    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    return json.loads(message.content[0].text.strip())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate SLO narratives")
    parser.add_argument("--service", default="payment-api")
    parser.add_argument("--slo-target", type=float, default=99.9)
    parser.add_argument("--current-availability", type=float, default=99.71)
    parser.add_argument("--error-budget-remaining", type=float, default=28.0)
    parser.add_argument("--burn-rate", type=float, default=3.2)
    parser.add_argument("--window", default="30d")
    args = parser.parse_args()

    minutes_in_window = 43200  # 30 days
    slo_data = {
        "service": args.service,
        "window": args.window,
        "slo_target_percent": args.slo_target,
        "current_availability_percent": args.current_availability,
        "error_budget_remaining_percent": args.error_budget_remaining,
        "burn_rate": args.burn_rate,
        "burn_rate_threshold": 1.0,
        "downtime_consumed_minutes": round(
            (100 - args.current_availability) / 100 * minutes_in_window, 1
        ),
        "total_budget_minutes": round(
            (100 - args.slo_target) / 100 * minutes_in_window, 1
        ),
    }

    print(f"Generating SLO narratives for {args.service}...")
    result = generate_slo_narrative(slo_data)

    sep = "=" * 60
    print(f"\n{sep}\nENGINEERING UPDATE\n{sep}")
    print(f"Subject: {result['engineering']['subject']}")
    print(f"\n{result['engineering']['body']}")
    print(f"\nAction Required: {result['engineering']['action_required']} | Urgency: {result['engineering']['urgency']}")

    print(f"\n{sep}\nLEADERSHIP UPDATE\n{sep}")
    print(f"Subject: {result['leadership']['subject']}")
    print(f"\n{result['leadership']['body']}")
    print(f"\nBusiness Impact: {result['leadership']['business_impact']}")

    print(f"\n{sep}\nSTATUS PAGE\n{sep}")
    print(f"Title: {result['status_page']['title']}")
    print(f"Status: {result['status_page']['status']}")
    print(f"\n{result['status_page']['body']}")

    print(f"\n{sep}\nRECOMMENDATIONS\n{sep}")
    for i, rec in enumerate(result.get("recommendations", []), 1):
        print(f"{i}. {rec}")
    print()

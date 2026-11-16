
import json

from openai import OpenAI
from pydantic import ValidationError

from config.settings import settings
from src.schemas import ExecutiveInsight

SYSTEM_PROMPT = """
You are an enterprise Quality Engineering executive advisor.

Analyze only the supplied quality metrics and risk assessment.

Rules:
- Never invent metrics or claim an improvement not supported by data.
- Distinguish observed facts from hypotheses.
- Explain risks in business language.
- Provide actionable recommendations.
- Do not make the final release go/no-go decision.
- Return valid JSON matching the requested schema.
"""


def fallback_insight(metrics: dict, risk: dict) -> ExecutiveInsight:
    actions = []

    if metrics["open_critical"] > 0:
        actions.append(
            "Review and disposition all open critical defects."
        )

    if metrics["escaped_defects"] > 0:
        actions.append(
            "Perform root-cause analysis of escaped defects."
        )

    if metrics["automation_coverage"] < 70:
        actions.append(
            "Prioritize automation of critical customer journeys."
        )

    if metrics["test_pass_rate"] < 95:
        actions.append(
            "Investigate failing tests and establish recovery owners."
        )

    if not actions:
        actions.append(
            "Continue monitoring quality trends and maintain release gates."
        )

    return ExecutiveInsight(
        overall_status=risk["risk_status"],
        executive_summary=(
            f"Quality risk is {risk['risk_status'].lower()} "
            f"with a calculated risk score of {risk['risk_score']}/100. "
            "This is a rules-based assessment, not an autonomous release decision."
        ),
        key_observations=[
            f"Test pass rate: {metrics['test_pass_rate']}%.",
            f"Automation coverage: {metrics['automation_coverage']}%.",
            f"Escaped defects: {metrics['escaped_defects']}.",
        ],
        business_risks=risk["risk_factors"],
        recommended_actions=actions,
        leadership_attention=(
            "Review high-priority quality risks with engineering owners."
            if risk["risk_status"] != "Low"
            else "Maintain quality governance and trend monitoring."
        ),
    )


def generate_executive_insight(
    metrics: dict,
    risk: dict,
) -> ExecutiveInsight:
    if not settings.ai_enabled or not settings.openai_api_key:
        return fallback_insight(metrics, risk)

    client = OpenAI(api_key=settings.openai_api_key)

    payload = {
        "metrics": metrics,
        "risk_assessment": risk,
        "required_schema": {
            "overall_status": "Low, Medium, or High",
            "executive_summary": "Short business-focused summary",
            "key_observations": ["Observed fact"],
            "business_risks": ["Risk"],
            "recommended_actions": ["Action"],
            "leadership_attention": "Leadership action required",
        },
    }

    try:
        response = client.responses.create(
            model=settings.openai_model,
            instructions=SYSTEM_PROMPT,
            input=json.dumps(payload),
        )

        result = json.loads(response.output_text)
        return ExecutiveInsight.model_validate(result)

    except (ValueError, ValidationError):
        return fallback_insight(metrics, risk)

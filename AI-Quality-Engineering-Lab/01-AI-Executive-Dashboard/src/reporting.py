
import json

from src.schemas import ExecutiveInsight


def create_executive_report(
    metrics: dict,
    risk: dict,
    insight: ExecutiveInsight,
) -> dict:
    return {
        "report_type": "Executive Quality Assessment",
        "metrics": metrics,
        "risk_assessment": risk,
        "ai_insight": insight.model_dump(),
        "disclaimer": (
            "Demonstration report. Risk score is rules-based and "
            "AI recommendations require human review."
        ),
    }


def export_json(report: dict) -> str:
    return json.dumps(report, indent=2, default=str)

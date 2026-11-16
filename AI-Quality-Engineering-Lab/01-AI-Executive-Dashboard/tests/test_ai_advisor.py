
from src.ai_advisor import fallback_insight


def test_fallback_insight():
    metrics = {
        "test_pass_rate": 90,
        "automation_coverage": 50,
        "escaped_defects": 4,
        "open_critical": 1,
        "open_high": 3,
        "production_incidents": 2,
    }

    risk = {
        "risk_score": 80,
        "risk_status": "High",
        "risk_factors": ["Open critical defects"],
    }

    result = fallback_insight(metrics, risk)

    assert result.overall_status == "High"
    assert len(result.recommended_actions) > 0
    assert isinstance(result.executive_summary, str)

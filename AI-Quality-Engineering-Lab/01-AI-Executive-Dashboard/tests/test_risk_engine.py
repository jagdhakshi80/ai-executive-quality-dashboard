
from src.risk_engine import calculate_release_risk


def test_high_risk():
    metrics = {
        "open_critical": 3,
        "open_high": 8,
        "escaped_defects": 10,
        "production_incidents": 5,
        "test_pass_rate": 80,
        "automation_coverage": 40,
    }

    result = calculate_release_risk(metrics)

    assert result["risk_score"] == 100
    assert result["risk_status"] == "High"


def test_low_risk():
    metrics = {
        "open_critical": 0,
        "open_high": 0,
        "escaped_defects": 0,
        "production_incidents": 0,
        "test_pass_rate": 99,
        "automation_coverage": 90,
    }

    result = calculate_release_risk(metrics)

    assert result["risk_score"] == 0
    assert result["risk_status"] == "Low"


def test_medium_risk():
    metrics = {
        "open_critical": 0,
        "open_high": 4,
        "escaped_defects": 2,
        "production_incidents": 1,
        "test_pass_rate": 93,
        "automation_coverage": 80,
    }

    result = calculate_release_risk(metrics)

    assert result["risk_status"] == "Medium"

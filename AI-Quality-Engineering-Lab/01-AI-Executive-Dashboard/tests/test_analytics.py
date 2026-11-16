
from src.analytics import (
    calculate_defect_trends,
    calculate_quality_metrics,
    calculate_team_metrics,
)


def test_quality_metrics(sample_df):
    result = calculate_quality_metrics(sample_df)

    assert result["tests_executed"] == 300
    assert result["tests_passed"] == 285
    assert result["test_pass_rate"] == 95.0
    assert result["automation_coverage"] == 85.0
    assert result["escaped_defects"] == 4
    assert result["production_incidents"] == 1


def test_defect_trends(sample_df):
    result = calculate_defect_trends(sample_df)

    assert len(result) == 2
    assert "escaped_defects" in result.columns


def test_team_metrics(sample_df):
    result = calculate_team_metrics(sample_df)

    assert len(result) == 2
    assert set(result["team"]) == {"Payments", "Identity"}

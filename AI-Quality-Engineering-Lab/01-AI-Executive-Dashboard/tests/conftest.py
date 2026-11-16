
import pandas as pd
import pytest


@pytest.fixture
def sample_df():
    return pd.DataFrame([
        {
            "date": pd.Timestamp("2026-01-01"),
            "release": "R1",
            "team": "Payments",
            "tests_executed": 100,
            "tests_passed": 95,
            "automation_coverage": 80.0,
            "open_critical": 1,
            "open_high": 2,
            "escaped_defects": 3,
            "production_incidents": 1,
        },
        {
            "date": pd.Timestamp("2026-01-02"),
            "release": "R2",
            "team": "Identity",
            "tests_executed": 200,
            "tests_passed": 190,
            "automation_coverage": 90.0,
            "open_critical": 0,
            "open_high": 1,
            "escaped_defects": 1,
            "production_incidents": 0,
        },
    ])

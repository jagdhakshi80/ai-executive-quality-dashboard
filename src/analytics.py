
import pandas as pd


def calculate_quality_metrics(df: pd.DataFrame) -> dict:
    executed = int(df["tests_executed"].sum())
    passed = int(df["tests_passed"].sum())

    pass_rate = (passed / executed * 100) if executed else 0.0

    total_defects = (
        int(df["open_critical"].sum())
        + int(df["open_high"].sum())
        + int(df["escaped_defects"].sum())
    )

    return {
        "tests_executed": executed,
        "tests_passed": passed,
        "test_pass_rate": round(pass_rate, 2),
        "automation_coverage": round(
            float(df["automation_coverage"].mean()), 2
        ),
        "open_critical": int(df["open_critical"].sum()),
        "open_high": int(df["open_high"].sum()),
        "escaped_defects": int(df["escaped_defects"].sum()),
        "production_incidents": int(df["production_incidents"].sum()),
        "total_quality_issues": total_defects,
        "release_count": int(df["release"].nunique()),
        "team_count": int(df["team"].nunique()),
    }


def calculate_defect_trends(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("release", as_index=False)
        .agg(
            escaped_defects=("escaped_defects", "sum"),
            critical_defects=("open_critical", "sum"),
            high_defects=("open_high", "sum"),
            incidents=("production_incidents", "sum"),
        )
    )


def calculate_team_metrics(df: pd.DataFrame) -> pd.DataFrame:
    grouped = df.groupby("team", as_index=False).agg(
        tests_executed=("tests_executed", "sum"),
        tests_passed=("tests_passed", "sum"),
        automation_coverage=("automation_coverage", "mean"),
        escaped_defects=("escaped_defects", "sum"),
        incidents=("production_incidents", "sum"),
    )

    grouped["pass_rate"] = (
        grouped["tests_passed"]
        .div(grouped["tests_executed"].replace(0, float("nan")))
        .mul(100)
        .fillna(0)
        .round(2)
    )

    return grouped

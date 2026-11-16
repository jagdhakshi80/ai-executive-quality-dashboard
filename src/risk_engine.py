
def calculate_release_risk(metrics: dict) -> dict:
    score = 0

    critical = metrics["open_critical"]
    high = metrics["open_high"]
    escaped = metrics["escaped_defects"]
    incidents = metrics["production_incidents"]
    pass_rate = metrics["test_pass_rate"]
    coverage = metrics["automation_coverage"]

    score += min(critical * 15, 40)
    score += min(high * 5, 20)
    score += min(escaped * 4, 16)
    score += min(incidents * 5, 15)

    if pass_rate < 90:
        score += 10
    elif pass_rate < 95:
        score += 5

    if coverage < 50:
        score += 10
    elif coverage < 70:
        score += 5

    score = min(score, 100)

    if score >= 60:
        status = "High"
    elif score >= 30:
        status = "Medium"
    else:
        status = "Low"

    return {
        "risk_score": score,
        "risk_status": status,
        "risk_factors": [
            name
            for name, condition in [
                ("Open critical defects", critical > 0),
                ("Open high defects", high > 0),
                ("Escaped defects", escaped > 0),
                ("Production incidents", incidents > 0),
                ("Low test pass rate", pass_rate < 95),
                ("Low automation coverage", coverage < 70),
            ]
            if condition
        ],
    }

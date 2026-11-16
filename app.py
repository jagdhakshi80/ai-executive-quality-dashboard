
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from src.ai_advisor import generate_executive_insight
from src.analytics import (
    calculate_defect_trends,
    calculate_quality_metrics,
    calculate_team_metrics,
)
from src.data_loader import load_quality_data
from src.reporting import create_executive_report, export_json
from src.risk_engine import calculate_release_risk


BASE_DIR = Path(__file__).resolve().parent
SAMPLE_FILE = BASE_DIR / "data" / "sample_quality_metrics.csv"

st.set_page_config(
    page_title="AI Quality Intelligence",
    page_icon="📊",
    layout="wide",
)

st.title("📊 AI Executive Quality Dashboard")
st.caption(
    "Enterprise Quality Intelligence | AI-powered insights and release risk"
)


@st.cache_data
def load_sample():
    return load_quality_data(SAMPLE_FILE)


def metric_card(label, value, help_text=None):
    st.metric(label, value, help=help_text)


with st.sidebar:
    st.header("Data Configuration")
    uploaded = st.file_uploader(
        "Upload quality metrics CSV",
        type=["csv"],
    )

    use_sample = st.toggle(
        "Use synthetic demonstration data",
        value=uploaded is None,
    )

    st.divider()
    st.caption("AI Executive Advisor")
    st.caption("AI output requires human review.")


try:
    if uploaded is not None and not use_sample:
        # Uploaded files are size-limited and parsed in memory.
        if uploaded.size > 5_000_000:
            st.error("CSV exceeds the 5 MB upload limit.")
            st.stop()

        import io

        temp_df = pd.read_csv(io.BytesIO(uploaded.getvalue()))

        # Validate the same schema and business rules as file-based input.
        from src.schemas import QualityRecord

        records = [
            QualityRecord(**row).model_dump()
            for row in temp_df.to_dict(orient="records")
        ]
        df = pd.DataFrame(records)
        df["date"] = pd.to_datetime(df["date"], errors="raise")

        if df.empty:
            raise ValueError("Uploaded CSV is empty.")

        if (df["tests_passed"] > df["tests_executed"]).any():
            raise ValueError("Passed tests cannot exceed executed tests.")

    else:
        df = load_sample()

except (ValueError, OSError, KeyError) as exc:
    st.error(f"Unable to load quality data: {exc}")
    st.stop()


if df.empty:
    st.warning("No quality records are available.")
    st.stop()


metrics = calculate_quality_metrics(df)
risk = calculate_release_risk(metrics)
insight = generate_executive_insight(metrics, risk)

# -------------------------------------------------
# Executive KPI Overview
# -------------------------------------------------

st.subheader("Executive Quality Overview")

c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    metric_card("Test Pass Rate", f"{metrics['test_pass_rate']}%")

with c2:
    metric_card(
        "Automation Coverage",
        f"{metrics['automation_coverage']}%",
    )

with c3:
    metric_card("Escaped Defects", metrics["escaped_defects"])

with c4:
    metric_card("Production Incidents", metrics["production_incidents"])

with c5:
    metric_card(
        "Release Risk",
        risk["risk_status"],
        f"Score: {risk['risk_score']}/100",
    )

st.divider()

# -------------------------------------------------
# Quality Analytics
# -------------------------------------------------

st.subheader("Quality Engineering Analytics")

left, right = st.columns(2)

with left:
    trends = calculate_defect_trends(df)

    fig = px.bar(
        trends,
        x="release",
        y=["escaped_defects", "critical_defects", "high_defects"],
        barmode="group",
        title="Defect Trends by Release",
        labels={"value": "Defect count", "variable": "Category"},
    )

    st.plotly_chart(fig, use_container_width=True)

with right:
    team_metrics = calculate_team_metrics(df)

    fig = px.bar(
        team_metrics,
        x="team",
        y="automation_coverage",
        color="team",
        title="Automation Coverage by Team",
        labels={"automation_coverage": "Coverage (%)"},
    )

    st.plotly_chart(fig, use_container_width=True)


st.subheader("Team Quality Performance")
st.dataframe(team_metrics, use_container_width=True, hide_index=True)

# -------------------------------------------------
# Release Risk
# -------------------------------------------------

st.divider()
st.subheader("Release Risk Intelligence")

r1, r2 = st.columns([1, 2])

with r1:
    st.metric("Risk Score", f"{risk['risk_score']} / 100")

    if risk["risk_status"] == "High":
        st.error("High quality risk")
    elif risk["risk_status"] == "Medium":
        st.warning("Medium quality risk")
    else:
        st.success("Low quality risk")

with r2:
    st.write("**Identified risk factors**")

    if risk["risk_factors"]:
        for item in risk["risk_factors"]:
            st.write(f"- {item}")
    else:
        st.write("No risk factors identified by the scoring rules.")

st.caption(
    "Risk score is a configurable demonstration heuristic, not a "
    "statistically validated release prediction."
)

# -------------------------------------------------
# AI Executive Advisor
# -------------------------------------------------

st.divider()
st.subheader("🤖 AI Executive Advisor")

st.write(f"**Overall assessment: {insight.overall_status}**")
st.write(insight.executive_summary)

with st.expander("Key observations", expanded=True):
    for item in insight.key_observations:
        st.write(f"- {item}")

with st.expander("Business risks"):
    for item in insight.business_risks:
        st.write(f"- {item}")

with st.expander("Recommended actions"):
    for item in insight.recommended_actions:
        st.write(f"- {item}")

st.info(f"Leadership attention: {insight.leadership_attention}")

# -------------------------------------------------
# Export Reports
# -------------------------------------------------

report = create_executive_report(metrics, risk, insight)

st.divider()
st.subheader("Executive Reporting")

st.download_button(
    "Download Executive Report (JSON)",
    data=export_json(report),
    file_name="executive_quality_report.json",
    mime="application/json",
)

st.download_button(
    "Download Quality Data (CSV)",
    data=df.to_csv(index=False),
    file_name="quality_metrics.csv",
    mime="text/csv",
)

st.caption(
    "AI-generated insights are advisory. Release decisions remain "
    "with authorized engineering and business owners."
)

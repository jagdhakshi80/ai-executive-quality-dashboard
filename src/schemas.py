
from pydantic import BaseModel, Field


class QualityRecord(BaseModel):
    date: str
    release: str
    team: str
    tests_executed: int = Field(ge=0)
    tests_passed: int = Field(ge=0)
    automation_coverage: float = Field(ge=0, le=100)
    open_critical: int = Field(ge=0)
    open_high: int = Field(ge=0)
    escaped_defects: int = Field(ge=0)
    production_incidents: int = Field(ge=0)


class ExecutiveInsight(BaseModel):
    overall_status: str
    executive_summary: str
    key_observations: list[str]
    business_risks: list[str]
    recommended_actions: list[str]
    leadership_attention: str

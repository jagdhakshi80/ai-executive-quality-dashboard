
from pathlib import Path

import pandas as pd

from src.schemas import QualityRecord


REQUIRED_COLUMNS = set(QualityRecord.model_fields.keys())


def load_quality_data(file_path: str | Path) -> pd.DataFrame:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Quality dataset not found: {path.name}")

    if path.suffix.lower() != ".csv":
        raise ValueError("Only CSV files are supported.")

    df = pd.read_csv(path)

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    if df.empty:
        raise ValueError("Dataset cannot be empty.")

    records = [
        QualityRecord(**row)
        for row in df.to_dict(orient="records")
    ]

    validated = pd.DataFrame([r.model_dump() for r in records])
    validated["date"] = pd.to_datetime(
        validated["date"], errors="raise"
    )

    if (validated["tests_passed"] > validated["tests_executed"]).any():
        raise ValueError("Passed tests cannot exceed executed tests.")

    return validated.sort_values("date").reset_index(drop=True)

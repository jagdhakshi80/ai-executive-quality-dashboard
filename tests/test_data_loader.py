
import pytest

from src.data_loader import load_quality_data


def test_load_sample_data():
    df = load_quality_data("data/sample_quality_metrics.csv")

    assert not df.empty
    assert "release" in df.columns
    assert "team" in df.columns
    assert df["tests_executed"].sum() > 0


def test_missing_file():
    with pytest.raises(FileNotFoundError):
        load_quality_data("data/does-not-exist.csv")


def test_wrong_file_extension(tmp_path):
    file = tmp_path / "input.txt"
    file.write_text("test")

    with pytest.raises(ValueError):
        load_quality_data(file)

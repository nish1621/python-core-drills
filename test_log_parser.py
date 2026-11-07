import json
from pathlib import Path

import pytest

from log_parser import LogAnalyzer


def test_parse_valid_log() -> None:
    analyzer = LogAnalyzer("sample.log")
    counts, errors = analyzer.parse()

    assert counts == {"INFO": 3, "WARNING": 1, "ERROR": 3}
    assert len(errors) == 3
    assert errors[0] == "Database connection timeout"
    assert errors[2] == "Malformed error line"


def test_parse_missing_file() -> None:
    analyzer = LogAnalyzer("non_existent.log")
    counts, errors = analyzer.parse()

    assert counts == {"INFO": 0, "WARNING": 0, "ERROR": 0}
    assert errors == []


@pytest.mark.parametrize(
    "bad_filename", ["invalid.json", "photo.png", "data.csv", "script.py"]
)
def test_with_invalid_file_extension(bad_filename: str) -> None:
    with pytest.raises(ValueError, match="Unsupported file extension"):
        LogAnalyzer(bad_filename)


@pytest.mark.parametrize(
    "keyword, expected",
    [
        ("timeout", ["Database connection timeout"]),
        ("DISK", ["Failed to write to disk"]),
        ("nonexistent", []),
    ],
)
def test_filter_errors(keyword: str, expected: list[str]) -> None:
    analyzer = LogAnalyzer("sample.log")
    analyzer.parse()
    assert analyzer.filter_errors(keyword) == expected


def test_save_report(tmp_path: Path) -> None:
    analyzer = LogAnalyzer("sample.log")
    analyzer.parse()

    output_file = tmp_path / "test_report.json"
    analyzer.save_report(output_file)

    assert output_file.exists()
    with open(output_file, "r", encoding="utf-8") as f:
        saved_data = json.load(f)

    assert saved_data["summary"] == {"INFO": 3, "WARNING": 1, "ERROR": 3}
    assert len(saved_data["errors"]) == 3


def test_empty_log_file(tmp_path: Path) -> None:
    empty_log = tmp_path / "empty.log"
    empty_log.write_text("", encoding="utf-8")

    analyzer = LogAnalyzer(empty_log)
    counts, errors = analyzer.parse()

    assert counts == {"INFO": 0, "WARNING": 0, "ERROR": 0}
    assert errors == []

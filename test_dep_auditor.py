import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from dep_auditor import DependencyAuditor


def test_invalid_extension() -> None:
    with pytest.raises(ValueError):
        DependencyAuditor("pyproject.toml")


@patch("dep_auditor.scan_requirements_file")
def test_get_vulnerable_packages(mock_scan: MagicMock, tmp_path: Path) -> None:
    mock_scan.return_value = {
        "jinja2==2.4.1": ["GHSA-1111"],
        "requests==2.32.3": [],
    }

    req_file = tmp_path / "requirements.txt"
    req_file.write_text("jinja2==2.4.1\nrequests==2.32.3\n")

    auditor = DependencyAuditor(str(req_file))
    auditor.run_audit()

    assert auditor.get_vulnerable_packages() == {"jinja2==2.4.1": ["GHSA-1111"]}


@patch("dep_auditor.scan_requirements_file")
def test_export_audit_report(mock_scan: MagicMock, tmp_path: Path) -> None:
    mock_scan.return_value = {
        "jinja2==2.4.1": ["GHSA-1111"],
        "requests==2.32.3": [],
    }

    req_file = tmp_path / "requirements.txt"
    req_file.write_text("jinja2==2.4.1\nrequests==2.32.3\n")

    auditor = DependencyAuditor(req_file)
    auditor.run_audit()

    req_file = tmp_path / "audit.json"
    auditor.export_audit_report(req_file)
    with open(req_file) as f:
        saved = json.load(f)

    assert saved["total_packages_scanned"] == 2
    assert saved["vulnerable_packages_count"] == 1
    assert saved["vulnerable_packages"] == {"jinja2==2.4.1": ["GHSA-1111"]}

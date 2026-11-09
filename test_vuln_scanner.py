from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import requests

from vuln_scanner import fetch_package_vulns, scan_requirements_file


@patch("vuln_scanner.requests.post")
def test_fetch_vulnerable_package(mock_post: MagicMock) -> None:
    fake_response = MagicMock()
    fake_response.json.return_value = {
        "vulns": [{"id": "GHSA-1111"}, {"id": "PYSEC-2222"}]
    }
    mock_post.return_value = fake_response
    assert fetch_package_vulns("jinja2", "2.4.1") == ["GHSA-1111", "PYSEC-2222"]
    mock_post.assert_called_once()


@patch("vuln_scanner.requests.post")
def test_fetch_safe_package(mock_post: MagicMock) -> None:
    fake_response = MagicMock()
    fake_response.json.return_value = {}
    mock_post.return_value = fake_response
    assert fetch_package_vulns("safe_pkg", "1.0.0") == []


@patch("vuln_scanner.requests.post")
def test_fetch_package_http_error(mock_post: MagicMock) -> None:
    fake_response = MagicMock()
    fake_response.raise_for_status.side_effect = requests.HTTPError("500 server error")
    mock_post.return_value = fake_response
    with pytest.raises(requests.HTTPError):
        fetch_package_vulns("django", "4.0.0")


@patch("vuln_scanner.requests.post")
def test_scan_requirements_file(mock_post: MagicMock, tmp_path: Path) -> None:
    req_file = tmp_path / "requirements.txt"
    req_file.write_text("# Comment\njinja2==2.4.1\n\n", encoding="utf-8")
    fake_response = MagicMock()
    fake_response.json.return_value = {"vulns": [{"id": "GHSA-9999"}]}
    mock_post.return_value = fake_response
    report = scan_requirements_file(req_file)
    assert report == {"jinja2==2.4.1": ["GHSA-9999"]}


def test_scan_unpinned_requirement(tmp_path: Path) -> None:
    bad_req = tmp_path / "bad_req.txt"
    bad_req.write_text("flask\n", encoding="utf-8")
    with pytest.raises(ValueError, match="Requirement must pin version"):
        scan_requirements_file(bad_req)

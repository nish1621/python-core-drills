from vuln_scanner import fetch_package_vulns


def test_fetch_vulnerable_package() -> None:
    vulns = fetch_package_vulns("jinja2", "2.4.1")
    assert len(vulns) > 0
    assert isinstance(vulns, list)


def test_fetch_nonexistent_package() -> None:
    vulns = fetch_package_vulns("this-package-definitely-does-not-exist-12345", "0.0.1")
    assert vulns == []

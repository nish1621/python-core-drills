from pathlib import Path

import requests

OSV_API_URL = "https://api.osv.dev/v1/query"


def fetch_package_vulns(package_name: str, version: str) -> list[str]:
    payload = {
        "version": version,
        "package": {
            "name": package_name,
            "ecosystem": "PyPI",
        },
    }
    response = requests.post(OSV_API_URL, json=payload, timeout=10)
    response.raise_for_status()
    data = response.json()

    vulns = data.get("vulns", [])
    return [v["id"] for v in vulns if "id" in v]


def scan_requirements_file(filepath: str | Path) -> dict[str, list[str]]:
    req_path = Path(filepath)
    results: dict[str, list[str]] = {}
    with req_path.open("r", encoding="utf-8") as f:
        for line in f:
            clean_line = line.strip()
            if not clean_line or clean_line.startswith("#"):
                continue
            if "==" in clean_line:
                package_name, version = clean_line.split("==", 1)
                vulns = fetch_package_vulns(package_name.strip(), version.strip())
                results[f"{package_name.strip()}=={version.strip()}"] = vulns
            else:
                raise ValueError(
                    f"Requirement must pin version with '==': {clean_line}"
                )
    return results


if __name__ == "__main__":
    print("jinja2 2.4.1 vulns:", fetch_package_vulns("jinja2", "2.4.1"))
    print("Requests 2.32.3 vulns:", fetch_package_vulns("requests", "2.32.3"))

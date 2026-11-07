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


if __name__ == "__main__":
    print("jinja2 2.4.1 vulns:", fetch_package_vulns("jinja2", "2.4.1"))
    print("Requests 2.32.3 vulns:", fetch_package_vulns("requests", "2.32.3"))

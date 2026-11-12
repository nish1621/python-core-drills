import argparse
import json
from pathlib import Path

from vuln_scanner import scan_requirements_file


class DependencyAuditor:
    def __init__(self, req_filepath: str | Path) -> None:
        self.req_filepath = Path(req_filepath)
        if self.req_filepath.suffix != ".txt":
            raise ValueError(
                f"Invalid requirements file extension: {self.req_filepath.suffix}"
            )
        self.audit_results: dict[str, list[str]] = {}

    def run_audit(self) -> dict[str, list[str]]:
        self.audit_results = scan_requirements_file(self.req_filepath)
        return self.audit_results

    def get_vulnerable_packages(self) -> dict[str, list[str]]:
        return {
            pkg: vulns for pkg, vulns in self.audit_results.items() if len(vulns) > 0
        }

    def export_audit_report(self, output_filepath: str | Path) -> None:
        vulnerable = self.get_vulnerable_packages()
        report = {
            "total_packages_scanned": len(self.audit_results),
            "vulnerable_packages_count": len(vulnerable),
            "vulnerable_packages": vulnerable,
        }
        with open(output_filepath, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=4)

    def main() -> None:
        parser = argparse.ArgumentParser(
            description="Audit Python dependencies for known vulnerabilities."
        )
        parser.add_argument(
            "requirements_file", help="Path to the requirements.txt file to audit"
        )
        parser.add_argument(
            "-o",
            "--output",
            default="audit_report.json",
        )
        args = parser.parse_args()
        auditor = DependencyAuditor(args.requirements_file)
        auditor.run_audit()
        auditor.export_audit_report(args.output)
        print(
            f"Audit complete. Vulnerable packages found: {len(auditor.get_vulnerable_packages())}"
        )

    if __init__ == "__main__":
        main()

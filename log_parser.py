import argparse
import json
from pathlib import Path

LEVELS = ["INFO", "WARNING", "ERROR"]


class LogAnalyzer:
    def __init__(self, filepath: str | Path) -> None:
        self.filepath = Path(filepath)
        if self.filepath.suffix not in (".log", ".txt"):
            raise ValueError(f"Unsupported file extension: {self.filepath.suffix}")

        self.counts: dict[str, int] = {level: 0 for level in LEVELS}
        self.errors: list[str] = []

    def parse(self) -> tuple[dict[str, int], list[str]]:
        self.counts = {level: 0 for level in LEVELS}
        self.errors = []

        try:
            with self.filepath.open("r", encoding="utf-8") as f:
                for line in f:
                    line_to_read = line.strip()
                    if line_to_read.startswith("[ERROR]"):
                        self.counts["ERROR"] += 1
                        parts = line_to_read.split(" - ")
                        if len(parts) > 1:
                            self.errors.append(parts[1])
                        else:
                            self.errors.append("Malformed error line")

                    elif line_to_read.startswith("[WARNING]"):
                        self.counts["WARNING"] += 1

                    elif line_to_read.startswith("[INFO]"):
                        self.counts["INFO"] += 1

        except FileNotFoundError:
            print(f"File not found {self.filepath}")

        return self.counts, self.errors

    def filter_errors(self, keyword: str) -> list[str]:
        return [error for error in self.errors if keyword.lower() in error.lower()]

    def save_report(self, output_filepath: str | Path) -> None:
        report = {
            "summary": self.counts,
            "errors": self.errors,
        }

        with open(output_filepath, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Parse server log files and export JSON reports."
    )
    parser.add_argument("log_file", help="Path to the .log file to parse")
    parser.add_argument(
        "-o",
        "--output",
        default="report.json",
        help="Path to save the output JSON report (default: report.json)",
    )
    parser.add_argument(
        "-k",
        "--keyword",
        help="Filter errors by a specific keyword (case-insensitive)",
    )
    args = parser.parse_args()

    analyzer = LogAnalyzer(args.log_file)
    counts, errors = analyzer.parse()
    print("Count:", counts)
    print("Errors:", errors)

    if args.keyword:
        filtered = analyzer.filter_errors(args.keyword)
        print("Filtered errors:", filtered)

    analyzer.save_report(args.output)

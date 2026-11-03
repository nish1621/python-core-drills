import argparse
import json
from pathlib import Path


def save_report_to_json(counts, errors, output_filepath):
    report = {
        "summary": counts,
        "errors": errors,
    }

    with open(output_filepath, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4)


def filter_errors_by_keyword(errors, keyword):
    return [error for error in errors if keyword.lower() in error.lower()]


def parse_log_file(filepath):
    filepath = Path(filepath)

    LEVELS = ["INFO", "WARNING", "ERROR"]
    data = {level: 0 for level in LEVELS}
    error_message = []

    if filepath.suffix not in (".log", ".txt"):
        raise ValueError(f"Unsupported file extension: {filepath.suffix}")

    try:
        with filepath.open("r", encoding="utf-8") as f:
            for line in f:
                line_to_read = line.strip()

                if line_to_read.startswith("[ERROR]"):
                    data["ERROR"] += 1
                    parts = line_to_read.split(" - ")
                    if len(parts) > 1:
                        error_message.append(parts[1])
                    else:
                        error_message.append("Malformed error line")

                elif line_to_read.startswith("[WARNING]"):
                    data["WARNING"] += 1

                elif line_to_read.startswith("[INFO]"):
                    data["INFO"] += 1

    except FileNotFoundError:
        print(f"File not found {filepath}")
    return data, error_message


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
    counts, errors = parse_log_file(args.log_file)
    if args.keyword:
        errors = filter_errors_by_keyword(errors, args.keyword)
        print("Filtered errors :", errors)
    print("Count:", counts)
    print("Errors:", errors)
    save_report_to_json(counts, errors, args.output)

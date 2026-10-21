def parse_log_file(filepath):
    data={"INFO":0, "WARNING":0, "ERROR":0}
    error_message = []

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line_to_read=line.strip()


                if line_to_read.startswith("[ERROR]"):
                    data["ERROR"] += 1
                    parts=line_to_read.split(" - ")
                    if len(parts)>1:
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
    
counts, errors = parse_log_file("sample.log")

print("Count:", counts)
print("Errors:", errors)
missing_counts, missing_errors = parse_log_file("does_not_exist.log")
def parse_lof_file(filepath):
    data={"INFO":0, "WARNING":0, "ERROR":0}
    error_message=[]

    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line_to_read=line.strip()


            if line_to_read.startswith("[ERROR]"):
                data["ERROR"]+=1
                parts=line_to_read.split(" - ")
                errors=parts[1]
                error_message.append(errors)

            elif line_to_read.startswith("[WARNING]"):
                data["WARNING"]+=1

            elif line_to_read.startswith("[INFO]"):
                data["INFO"]+=1

    return data, error_message
counts, errors = parse_lof_file("sample.log")

print("Count:", counts)
print("Errors:", errors)
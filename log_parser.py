data={"INFO":0, "WARNING":0, "ERROR":0}
error_message=[]

with open("sample.log", "r", encoding="utf-8") as f:
    for line in f:
        lineTOread=line.strip()


        if lineTOread.startswith("[ERROR]"):
            data["ERROR"]+=1
            parts=lineTOread.split(" - ")
            errors=parts[1]
            error_message.append(errors)

        elif lineTOread.startswith("[WARNING]"):
            data["WARNING"]+=1

        elif lineTOread.startswith("[INFO]"):
            data["INFO"]+=1

print(error_message)
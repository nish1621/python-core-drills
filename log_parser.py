import fileinput
from multiprocessing import process



for line in fileinput.input(encoding="utf-8"):
    process(line)
    st=line.split()
    err=0
    info=0
    warn=0
    for i in st:
        if i=="[ERROR]":
            err+=1
        elif i=="[WARNING]":
            warn+=1
        elif i=="[INFO]":
            info+=1
        continue
res={"INFO":info, "WARNING":warn, "ERROR":err}
print(res)
import csv

dirprefix = "../"
fileoffiles = dirprefix + "translate-RESULTS.txt"

filelist = []
with open(fileoffiles) as f:
    reader = csv.reader(f, delimiter=",")
    line_count = 1
    for row in reader:
        # skip the header, we assume the input csv has a header
        if line_count >= 1 and len(row[1].strip()) == 0:
            filelist.append(row[0].strip())
        line_count += 1

f = open("./sat-file-list2.txt", "w")
for i in filelist:
    f.write(i + '\n')
f.close()

print("Completed!")

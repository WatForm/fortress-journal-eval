import csv

rootdir = "../results/sat/bisection/"
filename = rootdir + "get-scope-bisection-LOG.csv"
satfile = rootdir + "sat.csv"
unsatfile = rootdir + "unsat.csv"
tptpdir = rootdir + "/TPTP-v7.5.0/Problems/"

sat_file = open(satfile, "w")
satwriter = csv.writer(sat_file)
unsat_file = open(unsatfile, "w")
unsatwriter = csv.writer(unsat_file)
with open(filename) as f:
    reader = csv.reader(f, delimiter=",")
    for row in reader:
        fname = row[0].strip()
        categoey = row[1].strip()
        if categoey == "Sat":
            satwriter.writerow(row)
        if categoey == "Unsat":
            unsatwriter.writerow(row)

print("Completed!")

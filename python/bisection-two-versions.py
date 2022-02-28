import re
import csv
import math
from statistics import mean
from datetime import datetime
import util

count = 0  # change this if process does not finish
goal = "Unsat"
versions = ["v3si", "v4si"]
startingsc = 15
minscope = 0  # 1 smaller than the min scope you are looking for
maxscope = 1001  # 1 bigger than the min scope you are looking for

lowertimethreshold = 3 * 60  # seconds
uppertimethreshold = 20 * 60  # seconds
fortresstimeout = (uppertimethreshold + 600) * 1000  # ms; always way bigger

dirprefix = "../"
benchmarksfiles = dirprefix + "TPTP-v7.5.0/Problems/"
inputfilelist = dirprefix + "results/unsat/unsat-file-list2.txt"

fortressbin = dirprefix + 'java/libs/fortressdebug-0.1.0/bin/fortressdebug'
stacksize = '-Xss8m'  # fortress JVM Stack size set to 8 MB


def satisfiability_of_output(output):
    if re.search('Unsat', output):
        return 'Unsat'
    elif re.search('Sat', output):
        return 'Sat'
    return output


# from: https://thispointer.com/python-check-if-a-process-is-running-by-name-and-find-its-process-id-pid/

def get_scope_bisection(shortname, longname, sc, fmin, fmax, cnt, j):
    global fortresstimeout, lowertimethreshold, uppertimethreshold, longlogf

    # Run two versions
    fortressargs = ' -J' + stacksize + ' --timeout ' + str(
        fortresstimeout) + ' --mode decision --scope ' + str(
        sc) + ' --version ' + versions[0] + ' --rawdata ' + longname
    longlogf.write("\nRUN NO. " + str(cnt) + "," + str(j) + " scope=" + str(sc) + "\n" + shortname + '\n')
    longlogf.write(fortressbin + fortressargs + '\n')
    longlogf.flush()
    (time1, output1, exitcode1, stderr1) = util.runprocess(fortressbin + fortressargs, longlogf, uppertimethreshold)

    fortressargs = ' -J' + stacksize + ' --timeout ' + str(
        fortresstimeout) + ' --mode decision --scope ' + str(
        sc) + ' --version ' + versions[1] + ' --rawdata ' + longname
    longlogf.write("\nRUN NO. " + str(cnt) + "," + str(j) + " version=" + versions[1] + " scope=" + str(
        sc) + "\n" + shortname + '\n')
    longlogf.write(fortressbin + fortressargs + '\n')
    longlogf.flush()
    (time2, output2, exitcode2, stderr2) = util.runprocess(fortressbin + fortressargs, longlogf, uppertimethreshold)

    # Check if the result aligns with our goal
    output1 = satisfiability_of_output(output1)
    output2 = satisfiability_of_output(output2)
    if (goal == 'Sat' and output1 == 'Unsat') or (goal == 'Unsat' and output1 == 'Sat'):
        return sc, "not goal", versions[0], time1, output1, versions[1], time2, output2
    if (goal == 'Sat' and output2 == 'Unsat') or (goal == 'Unsat' and output2 == 'Sat'):
        return sc, "not goal", versions[0], time1, output1, versions[1], time2, output2

    # If there is time out, looking for a smaller scope
    if (output1 == "TIMEOUT" or output1 == "NONZEROCODE" or output1 == "StackOverflowError") or \
            (output2 == "TIMEOUT" or output2 == "NONZEROCODE" or output2 == "StackOverflowError"):
        fmax = sc
        sc = math.floor(mean([fmin, sc]))
        if sc != fmin:
            return get_scope_bisection(shortname, longname, sc, fmin, fmax, cnt, j + 1)
        else:
            # no scope will work for this file
            return sc, "no scope finishes in time range", versions[0], time1, output1, versions[1], time2, output2

    # If there's version taking too short
    elif time1 < lowertimethreshold or time2 < lowertimethreshold:
        fmin = sc
        sc = math.ceil(mean([sc, fmax]))
        if sc != fmax:
            return get_scope_bisection(shortname, longname, sc, fmin, fmax, cnt, j + 1)
        else:
            # no scope will work for this file
            return sc, "no scope finishes in time range", versions[0], time1, output1, versions[1], time2, output2
    else:
        # found one that works
        return sc, goal, versions[0], time1, output1, versions[1], time2, output2


now = datetime.now()
dt_string = now.strftime("%Y-%m-%d-%H-%M-%S")

longlogf = open(dirprefix + "get-scope-bisection-LONG-LOG.txt", "w")
longlogf.write("\n*** RESTART " + dt_string + " " + " ****\n\n")
longlogf.flush()

logf = open(dirprefix + "get-scope-bisection-LOG.txt", "w")
logf.write("\n*** RESTART " + dt_string + " ****\n\n")
logf.flush()

# read in the randomized list of files for this process
filelist = []
startingscope = {}
with open(inputfilelist) as f:
    reader = csv.reader(f, delimiter=",")
    for row in reader:
        filename = row[0].strip()
        # curscope = row[1].strip()
        filelist.append(filename)
        startingscope[filename] = 15
# start counter: go until 25 sat and 100 unsat
goalcount = 0
overallcount = count
maxcount = len(filelist)

# prep output files
outf = open(dirprefix + "get-scope-RESULTS.txt", "w")

while overallcount < maxcount:
    shortname = filelist[overallcount].strip()
    longname = benchmarksfiles + shortname
    (sc, reason, versions1, time1, output1, versions2, time2, output2) = get_scope_bisection(shortname, longname,
                                                                                             startingsc, minscope,
                                                                                             maxscope, overallcount, 0)
    # every file should have an entry in logf
    # and once this has been written that file is completed
    logf.write(shortname + ", " + reason + ", " + str(sc) + ", " + versions1 + ', ' + str(
        round(time1, 2)) + ", " + output1 + ", " + versions2 + ', ' + str(
        round(time2, 2)) + ", " + output2 + '\n')
    logf.flush()
    if reason == goal:
        outf.write(shortname + ", " + reason + ", " + str(sc) + '\n')
        outf.flush()
    overallcount += 1

outf.close()
logf.close()
longlogf.close()
print("Completed!")

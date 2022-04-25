# Example
# 20170428-Barrett/cdt-cade2015/nada/afp/koenigslemma/x2015_09_10_16_53_27_961_1132522.smt_in.smt2, v1, 9, 593.05

# this file can run fortress or count sorts (see final lines)

import re
import csv
from datetime import datetime
import os

import util

filecount = 0  # change this if process does not finish
numtimestoaverage = 1
foretressdebug_version = "fortressdebug-0.1.0"  # set fortressdebug version here
stacksize = '-Xss8m'  # fortress JVM Stack size set to 8 MB

dirprefix = "./"
fileoffiles = dirprefix + "25-unsat-tptp.txt"
tptpdir = dirprefix + "TPTP-v7.5.0/Problems/"
smtlibdir = dirprefix + "benchmarks/2019-05-06-smt-lib-uf-benchmarks-star-exec/"
prover9dir = dirprefix + "prover9-tptp/Problems/"
alloydir = dirprefix + "alloy-tptp/Problems/"

countsortbin = 'java -cp "' + dirprefix + 'java/libs/*:' + dirprefix + 'java/libs/' + foretressdebug_version + '/lib/*" -Djava.library.path="java/libs" ' + stacksize + ' countsorts.Countsorts'
fortressbin = dirprefix + 'java/libs/' + foretressdebug_version + '/bin/fortressdebug'
alloybin = dirprefix + 'tools/runAlloy/build/distributions/runAlloy/bin/runAlloy'
mace4bin = dirprefix + "tools/LADR-2009-11A/bin/mace4"

uppertimethreshold = 20 * 60  # seconds 1200 = 20 minutes
solvertimeout = uppertimethreshold + 600  # seconds; always way bigger


# from: https://thispointer.com/python-check-if-a-process-is-running-by-name-and-find-its-process-id-pid/

def count_sorts(longname, shortname, filecount):
    global solvertimeout, longlogf, resultsf
    fortressargs = ' -f ' + longname
    longlogf.write("\nRUN NO. " + str(filecount) + "," + str(i) + "\n" + shortname + '\n')
    longlogf.write(countsortbin + fortressargs + '\n')
    longlogf.flush()
    (t, output, exitcode, stderr) = util.runprocess(countsortbin + fortressargs, longlogf, uppertimethreshold)
    output = output.strip()
    if exitcode == 0 and ',' in output and output.find(',') == output.rfind(','):
        resultsf.write(output.strip() + ", \n")
    else:
        resultsf.write("NONZEROCODE, , \n")
    resultsf.flush()


def run_mace4(v, sc, longname, shortname, filecount):
    global solvertimeout, longlogf, resultsf
    # -P means don't print models
    # -c means ignore unrecognized set/clear/assign commands in the input file
    # don't print all the output to the screen
    mace4args = " -c -P 0 -t " + str(solvertimeout) \
                + " -n " + str(sc) + " -N " + str(sc) \
                + " -b 8060 -f " + longname
    for i in range(numtimestoaverage):
        longlogf.write(
            "\nRUN NO. " + str(filecount) + "," + str(i) + " " + v + " scope=" + str(sc) + "\n" + shortname + '\n')
        longlogf.write(mace4bin + mace4args + '\n')
        longlogf.flush()
        (t, output, exitcode, stderr) = util.runprocess(mace4bin + mace4args, longlogf, uppertimethreshold)
        # get the sat/unsat status
        # if process exit code is 0, then it is sat. otherwise, it is unsat.
        if exitcode is not None:
            if exitcode == 0:
                reason = "SAT"
            elif exitcode == 2:
                reason = "UNSAT"
            elif 3 <= exitcode <= 5:
                reason = "UNKNOWN"
            else:
                reason = "NONZEROCODE" + str(exitcode)
                # t = uppertimethreshold
        else:
            reason = output
        resultsf.write(shortname + ", " + v + ", " + str(sc) + ", " + reason + ", " + str(
            round(t, 2)) + ", " + ", " + ", " + ", " + ', \n')
        resultsf.flush()
        sumsf.write(str(round(t, 2)) + ", ")
        sumsf.flush()


def run_fortress(v, sc, longname, shortname, filecount, validate):
    global solvertimeout, longlogf, resultsf
    flags = '--validate --rawdata' if validate else '--rawdata'
    fortressargs = ' -J' + stacksize + ' --timeout ' + str(
        solvertimeout) + ' --mode decision --scope ' + str(
        sc) + ' --version ' + v + ' ' + flags + ' ' + longname
    for i in range(numtimestoaverage):
        longlogf.write(
            "\nRUN NO. " + str(filecount) + "," + str(i) + " " + v + " scope=" + str(sc) + "\n" + shortname + '\n')
        longlogf.write(fortressbin + fortressargs + '\n')
        longlogf.flush()
        (t, output, exitcode, stderr) = util.runprocess(fortressbin + fortressargs, longlogf, uppertimethreshold)
        if re.search(r'EXTRA_Z3', output):
            longlogf.close()
            resultsf.close()
            print("Quit due to extra Z3 process!")
            exit(1)
        if re.search(r'Parse error', output):
            reason = 'parse_error'
        elif re.search(r'Unsat', output):
            reason = 'UNSAT'
        elif re.search(r'Sat', output):
            reason = 'SAT'
        elif re.search(r'Unknown', output):
            reason = 'UNKNOWN'
        elif re.search(r'No new sorts', output):
            reason = 'No_new_sorts'
        else:
            reason = output
        tranformation_time = ''
        convert_time = ''
        solver_time = ''
        verify_instance = ''
        constant_interp = ''
        sort_interp = ''
        func_interp = ''
        interp_time = ''
        verify_time = ''
        for line in output.splitlines():
            if line.startswith('Total transformation time:'):
                tranformation_time = line.replace('Total transformation time: ', '')
            elif line.startswith('Converting to solver format:'):
                convert_time = line.replace('Converting to solver format: ', '')
            elif line.startswith('Z3 solver time:'):
                solver_time = line.replace('Z3 solver time: ', '')
            elif line.startswith('Verifying returned instance:'):
                verify_instance = line.replace('Verifying returned instance: ', '')

            elif line.startswith('Constant interpretations consumed time:'):
                constant_interp = line.replace('Constant interpretations consumed time: ', '')
            elif line.startswith('Sort interpretations consumed time:'):
                sort_interp = line.replace('Sort interpretations consumed time: ', '')
            elif line.startswith('Function interpretations consumed time:'):
                func_interp = line.replace('Function interpretations consumed time: ', '')
            elif line.startswith('Obtain interpretation time:'):
                interp_time = line.replace('Obtain interpretation time: ', '')
            elif line.startswith('Verify instance time:'):
                verify_time = line.replace('Verify instance time: ', '')
        resultsf.write(shortname + ", " + v + ("-validate" if validate else "") + ", " + str(sc) + ", " + reason + ", " + str(round(t, 2)) + ", " +
                       tranformation_time + ", " + convert_time + ", " + solver_time + ", " + verify_instance + ', \n')
        # sumsf.write(str(round(t, 2)) + ", ")
        sumsf.write(v + ("-validate" if validate else "") + ", " + str(
            sc) + ", " + constant_interp + ", " + sort_interp + ", " + func_interp + ", " + interp_time + ", " + verify_time + ", " + str(
            round(t, 2)) + ", ")
        resultsf.flush()


def run_alloy(v, sc, longname, shortname, filecount):
    global solvertimeout, longlogf, resultsf
    alloyargs = ' ' + longname
    # For running tptp translated files only
    alloyf = open(longname, "a")
    alloyf.write("\nrun {} for exactly " + sc + " _UNIV\n")
    alloyf.flush()
    alloyf.close()

    for i in range(numtimestoaverage):
        longlogf.write(
            "\nRUN NO. " + str(filecount) + "," + str(i) + " " + v + " scope=" + str(sc) + "\n" + shortname + '\n')
        longlogf.write(alloybin + alloyargs + '\n')
        longlogf.flush()
        (t, output, exitcode, stderr) = util.runprocess(alloybin + alloyargs, longlogf, uppertimethreshold)
        if re.search(r'Satisfiable\?: UNSAT', output):
            reason = 'UNSAT'
        elif re.search(r'Satisfiable\?: SAT', output):
            reason = 'SAT'
        else:
            reason = "unknown"
        resultsf.write(shortname + ", " + v + ", " + str(sc) + ", " + reason + ", " + str(
            round(t, 2)) + ", " + ", " + ", " + ", " + ', \n')
        sumsf.write(str(round(t, 2)) + ", ")
        sumsf.flush()
        resultsf.flush()

    # Delete last non-empty line
    # Reference: https://stackoverflow.com/questions/1877999/delete-final-line-in-file-with-python
    with open(longname, "r+", encoding = "utf-8") as file:

        # Move the pointer (similar to a cursor in a text editor) to the end of the file
        file.seek(0, os.SEEK_END)

        # This code means the following code skips the very last character in the file -
        # i.e. in the case the last line is null we delete the last line
        # and the penultimate one
        pos = file.tell() - 1

        # Read each character in the file one at a time from the penultimate
        # character going backwards, searching for a newline character
        # If we find a new line, exit the search
        while pos > 0 and file.read(1) != "\n":
            pos -= 1
            file.seek(pos, os.SEEK_SET)

        # So long as we're not at the start of the file, delete all the characters ahead
        # of this position
        if pos > 0:
            file.seek(pos, os.SEEK_SET)
            file.truncate()


now = datetime.now()
dt_string = now.strftime("%Y-%m-%d-%H-%M-%S")

longlogf = open(dirprefix + "run-tests-LONG-LOG.txt", "a")
longlogf.write("\n*** RESTART " + dt_string + " ****\n\n")
longlogf.flush()

resultsf = open(dirprefix + "run-tests-RESULTS.txt", "a")
resultsf.write("\n*** RESTART " + dt_string + " ****\n\n")
# resultsf.write("File,#Sorts,#SortsInferred\n\n")
resultsf.write(
    "File,version,scope,satisfiable,time,transformation_time,convert_time,solver_time,verify,num_sorts,new_sorts_inferred,\n")
# resultsf.write(
#     "File,version,scope,satisfiable,time,transformation_time,convert_time,solver_time,verify,num_sorts,new_sorts_inferred, ,mace4_output,mace4_time\n")
resultsf.flush()

sumsf = open(dirprefix + "run-tests-RESULTS-SUM.txt", "a")
sumsf.write("\n*** RESTART " + dt_string + " ****\n\n")
# sumsf.write("File, upperIter, parIter, upperND, upperPred\n")
sumsf.write("File, v3si, v4si\n")
sumsf.flush()

filelist = []
with open(fileoffiles) as f:
    reader = csv.reader(f, delimiter=",")
    line_count = 0
    for row in reader:
        # skip the header, we assume the input csv has a header
        if line_count >= 0:
            filename = row[0].strip()
            filelist.append((filename, row[2].strip()))
            # if len(row[2].strip()) == 0:
            #     # Run all tests at scope 15
            #     filelist.append((filename, row[2].strip()))
        line_count += 1

for i in range(filecount, len(filelist)):
    shortname = filelist[i][0]
    sc = filelist[i][1]
    for v in ['v3si', 'v4si', "v3"]:
        run_fortress(v, sc, tptpdir + shortname, shortname, i, False)
        run_fortress(v, sc, tptpdir + shortname, shortname, i, True)

    resultsf.flush()
    sumsf.write('\n')
    sumsf.flush()

print("Completed!")

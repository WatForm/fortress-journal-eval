# this file can translate tptp files to .in files
import os
import os.path
import csv
from datetime import datetime

import util

filecount = 0  # change this if process does not finish

# Please run this script in the TPTP repository
dir_prefix = "../"
benchmark_dir = dir_prefix + "TPTP-v7.5.0/Problems/"
target = "alloy"  # "prover9"
target_dir = dir_prefix + target + "-tptp/Problems/"
file_of_files = dir_prefix + "results/sat/sat-file-list.txt"
# alloy_scope_size = 15
num_files_to_translate = 800

# Set ladr bin's position here
ladr_bin = dir_prefix + 'tools/LADR-2009-11A/bin/tptp_to_ladr'
tptp_to_alloy_bin = dir_prefix + 'tools/TPTPtoAlloy-1.0/bin/TPTPtoAlloy'

uppertimethreshold = 60 * 60  # seconds
fortresstimeout = uppertimethreshold + 600  # seconds; always way bigger


# ./tools/LADR-2009-11A/bin/tptp_to_ladr < ./TPTP-v7.4.0/Problems/HWV/HWV063+1.p > ./prover9-tptp/Problems/HWV/HWV063+1.in
def run_tptp_to_ladr(longname, shortname, filecount):
    global fortresstimeout, longlogf, resultsf
    targetfile = target_dir + shortname.replace(".p", ".in")
    os.makedirs(os.path.dirname(targetfile), exist_ok=True)
    ladrargs = ' < ' + longname + ' > ' + targetfile
    longlogf.write("\nRUN NO. " + str(filecount) + "," + str(i) + "  " + shortname + '\n')
    longlogf.write(ladr_bin + ladrargs + '\n')
    longlogf.flush()
    (t, output, exitcode, stderr) = util.runprocess(ladr_bin + ladrargs, longlogf, uppertimethreshold)
    # Check if the file is empty
    if (not os.path.exists(targetfile)) or os.stat(targetfile).st_size == 0:
        if "Segmentation fault (core dumped)" in stderr:
            output = "Segmentation Fault"
        elif "Fatal error:  palloc, Max_megs parameter exceeded" in stderr:
            output = "Out of Memory"
        elif "Fatal error:  sread_term error" in stderr:
            output = "Read Term Error"
        else:
            output = "EMPTY"
    resultsf.write(shortname + ", " + output + '\n')
    resultsf.flush()


# ./gradlew run -q --args='/Users/ruomei.yan/Desktop/UW/Coop-4/fortress-evaluation/TPTP-v7.4.0/Problems/ALG/ALG443+1.p' > test.txt
def run_tptp_to_alloy(longname, shortname, filecount):
    global fortresstimeout, longlogf, resultsf
    targetfile = target_dir + shortname.replace(".p", ".als")
    os.makedirs(os.path.dirname(targetfile), exist_ok=True)
    tptptoalloyargs = ' ' + longname + " > " + targetfile
    longlogf.write("\nRUN NO. " + str(filecount) + "," + str(i) + "  " + shortname + '\n')
    longlogf.write(tptp_to_alloy_bin + tptptoalloyargs + '\n')
    longlogf.flush()
    (t, output, exitcode, stderr) = util.runprocess(tptp_to_alloy_bin + tptptoalloyargs, longlogf, uppertimethreshold)
    # Check if the file is empty
    if (not os.path.exists(targetfile)) or os.stat(targetfile).st_size == 0:
        if output != "StackOverflowError":
            output = "EMPTY"
    else:
        with open(targetfile) as myfile:
            if 'SyntaxError' in myfile.read():
                if "token recognition error at: '<~'" in stderr:
                    output = "unsupported operator <~>"
                elif "token recognition error at: '<= '" in stderr:
                    output = "unsupported operator <="
                elif "extraneous input ''+'' expecting" in stderr:
                    output = "quoted identifier '+'"
                else:
                    output = "SyntaxError"
    resultsf.write(shortname + ", " + output + '\n')
    resultsf.flush()


now = datetime.now()
dt_string = now.strftime("%Y-%m-%d-%H-%M-%S")

longlogf = open(dir_prefix + "translate-LONG-LOG.txt", "w")
longlogf.write("\n*** RESTART " + dt_string + " ****\n\n")
longlogf.flush()

resultsf = open(dir_prefix + "translate-RESULTS.txt", "w")
resultsf.write("File,Status\n")
resultsf.flush()

# Example
# ARI/ARI758=1.p,
filelist = []
with open(file_of_files) as f:
    reader = csv.reader(f, delimiter=",")
    line_count = 1
    for row in reader:
        # skip the header, we assume the input csv has a header
        if line_count >= 1:
            filelist.append(row[0].strip())
        line_count += 1

for i in range(filecount, min(num_files_to_translate, len(filelist))):
    shortname = filelist[i]
    sc = filelist[i][1]
    longname = benchmark_dir + shortname
    if target == "prover9":
        run_tptp_to_ladr(longname, shortname, i)
    elif target == "alloy":
        run_tptp_to_alloy(longname, shortname, i)

print("Completed!")

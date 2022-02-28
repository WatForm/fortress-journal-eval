goal = "Sat"
goal_total = 10000

dir_prefix = "./"
benchmark_dir = dir_prefix + "../TPTP-v7.5.0/Problems/"
random_file_list = dir_prefix + "../results/random-filelist.txt"

# read in the randomized list of files for this process
with open(random_file_list) as f:
    file_list = [f.strip() for f in f.readlines()]

goal_count = 0
overall_count = 0

# prep output files
outf = open(dir_prefix + goal.lower() + "-file-list.txt", "w")

while goal_count < goal_total and overall_count < len(file_list):
    shortname = file_list[overall_count].strip()
    longname = benchmark_dir + shortname
    if '+' in shortname:
        # Obtain its status
        with open(longname, "r") as a_file:
            for line in a_file:
                if 'Status   : ' in line:
                    status = line.split('Status   : ', 1)[1].strip()
                    break

        with open(longname) as myfile:
            if (goal == "Sat" and status in ("CounterSatisfiable", "Satisfiable")) \
                    or (goal == "Unsat" and status in ("Unsatisfiable", "ContradictoryAxioms", "Theorem")):
                outf.write(shortname + ', ' + goal + '\n')
                outf.flush()
                goal_count += 1
    overall_count += 1

outf.close()
print("Completed!")

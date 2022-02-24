# Evaluation included in Fortress Journal Submission

The following are the steps taken to reproduce the evaluation reported in the fortress journal submission:

1. Download TPTP-v7.5.0 from http://www.tptp.org/TPTP/Distribution/TPTP-v7.5.0.tgz
   ```
    wget http://www.tptp.org/TPTP/Distribution/TPTP-v7.5.0.tgz  
    tar -xzf TPTP-v7.5.0.tgz
   ```

2. Generate a list of 3000 FOF problems in random order  
   Adjust parameters in python/get-random-file-list.py and run the script with
   ```
   python3 python/get-random-file-list.py
   ```
   -> fortress-journal-results/random-filelist.txt (3000 files)

3. Divide into expected SAT or UNSAT categories  
   expected sat = Satisfiable or CounterSatisfiable  
   expected unsat = Unsatisfiable or contradictoryAxioms or Theorem  
   Adjust parameters in python/get-sat-or-unsat-file-list.py and run the script with
    ```
    python3 python/get-sat-or-unsat-file-list.py
    ```
   -> fortress-journal-results/sat/sat-file-list.txt (398 files)  
   -> fortress-journal-results/unsat/unsat-file-list.txt (2553 files)

4. Translate sat ones into prover9 format  
   a. Download LADR CLI version of all tools from https://www.cs.unm.edu/~mccune/prover9 (on next page choose version
   11A - Linux, mac OS X)  
   b. Put it under directory tools/   
   c. "make all" - It throws errors, move all "-lm" flags to the end of lines in line 65-84 of "
   LADR-2009-11A/provers.src/Makefile".  
   d. Now "make all" succeeded, all binaries are in bin/  
   e. Adjust parameters in python/translate-list-files.py, and set it to translate from tptp to prover9 format  
   f. Run the script in directory "TPTP-v7.5.0/" with
   ```
   python3 ../python/translate-list-files.py
   ```
   -> fortress-journal-results/sat/results-sat-translate-prover9/translate-RESULTS.txt  
   g. It failed at 1 files b/c Segmentation fault.  
   -> fortress-journal-results/sat/results-sat-translate-prover9/translate-RESULTS-analysis.csv h. We get a clean list
   of files by adjusting parameters and running the script
   ```
   python3 python/clean-filelist.py
   ```
   -> fortress-journal-results/sat/sat-file-list1.txt (397 files)

5. Translate sat ones into alloy format   
   a. Follow readme in util/TPTPtoAlloy to build that utility  
   b. Copy /util/TPTPtoAlloy/build/distributions/TPTPtoAlloy-1.0.zip to root directory and unzip it  
   c. Adjust parameters in python/translate-list-files.py, and set it to translate from tptp to alloy format  
   f. Run the script with
    ```
   python3 python/translate-list-files.py
   ```
   -> fortress-journal-results/sat/results-sat-translate-alloy/translate-RESULTS.txt g. It failed at 30 files b/c
   unsupported operators like “<~>" and “<=”(24), quoted identifiers(2), stack overflow error(4). ->
   fortress-journal-results/sat/results-sat-translate-alloy/translate-RESULTS-analysis.csv h. We get a clean list of
   files by adjusting parameters and running the script
    ```
   python3 python/clean-filelist.py
   ```
   -> fortress-journal-results/sat/sat-file-list2.txt (367 files)

5. (sat) Run bisection method to find scope for v3si and v4si that times between 3 and 20 minutes on tumbo.cs  
   Adjust parameters in python/bisection-two-versions.py and run the script with
   ```
   python3 python/bisection-two-versions.py
   ```
   -> fortress-journal-results/sat/results-bisection/get-scope-bisection-LOG.csv(234 files)

   Looking for a scope between 1 and 1000, and the results are 112 SAT, 87 NOT GOAL, 35 No scope finishes in time range

   Get a list of sat files by running script
   ```
   python3 python/separate-into-sat-and-unsat-list.py
   ```
   We take the top 110 sat files.  
   -> fortress-journal-results/sat/results-bisection/sat.csv (110 sat files list)

7. (sat) Run correctness test. Adjust parameters in python/run-tests.py and run the script with
   ```
   python3 python/run-tests.py
   ```
   -> fortress-journal-results/sat/results-sat-correctness/run-tests-RESULTS.csv  
   4 files time out for both v3si and v4si, 1 times out for v3si and 1 times out for v4si

8. Translate unsat ones into prover9 format  
   a. Adjust parameters in python/translate-list-files.py, and set it to translate from tptp to prover9 format  
   b. Run the script in directory "TPTP-v7.5.0/" with
   ```
   python3 ../python/translate-list-files.py
   ```
   -> fortress-journal-results/unsat/results-unsat-translate-prover9/translate-RESULTS.txt (764 files)

   c. It failed at 36 files b/c 30 read term errors, 2 out of memory errors, 4 segmentation faults.  
   d. We get a clean list of files by adjusting parameters and running the script
   ```
   python3 python/clean-filelist.py
   ```
   -> fortress-journal-results/unsat/unsat-file-list1.txt (764 files)

9. Translate unsat ones into alloy format   
   a. Adjust parameters in python/translate-list-files.py, and set it to translate from tptp to alloy format  
   b. Run the script with
    ```
   python3 python/translate-list-files.py
   ```
   -> fortress-journal-results/unsat/results-unsat-translate-alloy/translate-RESULTS.txt (745 files)

   c. It failed at 19 files b/c unsupported operators like “<~>" and “<=”(9), quoted identifiers(3), stack overflow
   error(7).   
   d. We get a clean list of files by adjusting parameters and running the script
    ```
   python3 python/clean-filelist.py
   ```
   -> fortress-journal-results/unsat/unsat-file-list2.txt (745 files)

10. (unsat) Run bisection method to find scope for v3si and v4si that times between 3 and 20 minutes on tumbo.cs  
    Adjust parameters in python/bisection-two-versions.py and run the script with
    ```
    python3 python/bisection-two-versions.py
    ```

    -> fortress-journal-results/unsat/results-bisection/get-scope-bisection-LOG.csv (229 files)

    Looking for a scope between 1 and 1000, and the results are 110 UNSAT, 119 No scope finishes in time range

    Get a list of unsat files by running script

    ```
    python3 python/separate-into-sat-and-unsat-list.py
    ```

    We take the 110 unsat files.  
    -> fortress-journal-results/unsat/results-bisection/unsat.csv (110 sat files list)

11. (unsat) Run correctness test. Adjust parameters in python/run-tests.py and run the script with
    ```
    python3 python/run-tests.py
    ```

    -> fortress-journal-results/unsat/results-unsat-correctness/run-tests-RESULTS.csv  
    4 files time out for both v3si and v4si, 1 times out for v3si and 1 times out for v4si



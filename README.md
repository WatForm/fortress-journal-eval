# Evaluation included in Fortress Journal Submission

The following are the steps taken to reproduce the evaluation reported in the fortress journal submission.  

1. Download TPTP-v7.5.0 from http://www.tptp.org/TPTP/Distribution/TPTP-v7.5.0.tgz
   ```
    wget http://www.tptp.org/TPTP/Distribution/TPTP-v7.5.0.tgz  
    tar -xzf TPTP-v7.5.0.tgz
   ```
   results in 9091 files.

2. Generate a list of 3000 FOF problems in random order  
   Adjust parameters in python/get-random-file-list.py and run the script with
   ```
   python3 python/get-random-file-list.py
   ```
   The list of resulting files is in results/random-filelist.txt (3000 files).

3. Divide into expected SAT or UNSAT categories based on the status filed in the TPTP problem. 
   expected sat = Satisfiable or CounterSatisfiable  
   expected unsat = Unsatisfiable or ContradictoryAxioms or Theorem  
   (ignoring status = Unknown or Open, 49 files) 
   In finite model finding, some sat problems may be unsat for a particular scope, but this status is a helpful starting point.
   Adjust parameters in python/get-sat-or-unsat-file-list.py and run the script with
    ```
    python3 python/get-sat-or-unsat-file-list.py
    ```
    This results in two lists of files:
   - results/sat/sat-file-list.txt (398 files)  
   - results/unsat/unsat-file-list.txt (2553 files)

4. Translate 398 sat models and first 800 unsat models into prover9 format
    1. Download LADR CLI version of all tools from https://www.cs.unm.edu/~mccune/prover9 (on next page choose version
       11A - Linux, mac OS X)
    2. Put it under directory tools/
    3. "make all" - It throws errors, move all "-lm" flags to the end of lines in line 65-84 of "
       LADR-2009-11A/provers.src/Makefile".
    4. Now "make all" succeeds, all binaries are in bin/
    5. Adjust parameters in python/translate-list-files.py, and set it to translate from tptp to prover9 format
    6. Run the script in directory "TPTP-v7.5.0/" with
   ```
   python3 ../python/translate-list-files.py
   ```
   The translated files can be found ????
   And the following hold the file lists:
   - results/sat/translate-to-prover9/translate-RESULTS.csv  
   - results/unsat/translate-to-prover9/translate-RESULTS.csv  
   7. In the previous step, we lost 1 sat file due to a segmentation fault and we lost 36 unsat files due to 30 read term errors, 2 out of memory errors, 4 segmentation faults.  Remove these from the list of files by adjusting parameters and running the script
   ```
   python3 python/clean-filelist.py
   ```
   This results in two lists of files:
   - results/sat/sat-file-list1.txt (397 files)  
   - results/unsat/unsat-file-list1.txt (764 files)

5. Translate into Alloy format
    1. Follow readme in tools/TPTPtoAlloy to build that utility (standalone program - it does not require Alloy or
       Fortress)
    2. Copy /tools/TPTPtoAlloy/build/distributions/TPTPtoAlloy-1.0.zip to root directory and unzip it
    3. Adjust parameters in python/translate-list-files.py, and set it to translate from tptp to alloy format
    4. Run the script with
    ```
   python3 python/translate-list-files.py
   ```
   The translated files can be found ????
   And the following hold the file lists:
   - results/sat/translate-to-alloy/translate-RESULTS.csv  
   - results/unsat/translate-to-alloy/translate-RESULTS.csv  
   5. In the previous step, we lost 30 sat files due to unsupported operators like “<~>" and “<=”(24), quoted identifiers(2), stack overflow
   error(4).  We lost 19 unsat files due to unsupported operators like “<~>" and “<=”(9), quoted identifiers(3), stack
   overflow error(7).  Remove these from the list of files by adjusting parameters and running the script
    ```
   python3 python/clean-filelist.py
   ```
   This results in two lists of files:
   - results/sat/sat-file-list2.txt (367 files)  
   - results/unsat/unsat-file-list2.txt (745 files)

6. Run a bisection method to find an exact scope between 1 and 1000 for the one sort (univ) for v3si and v4si that takes between 3 and 20 minutes on tumbo.cs
    1. Put a clone of the fortress repo in ../fortress (relative to this directory).
    2. In the java directory, run "make". This creates countsorts.jar and runfortress.jar in java/libs, downloads
       common-cli, and puts the fortress libraries in the java/libs.
    3. Set the dirprefix and other settings in python scripts in "python" directory.
    4. Adjust parameters in python/bisection-two-versions.py and run the script with
   ```
   python3 python/bisection-two-versions.py
   ```
   This results in two file lists:
   - results/sat/bisection/get-scope-bisection-LOG.csv (234 files)  
   - results/unsat/bisection/get-scope-bisection-LOG.csv (229 files)
   ???? where did 234 and 229 come from compared to 367 and 745 in step 5 ????
   234 expected SAT = 112 SAT, 87 NOT GOAL, 35 No scope finishes in time range  
   229 expected UNSAT = 110 UNSAT, 119 No scope finishes in time range
    5. Get a clean list of files by running script
   ```
   python3 python/separate-into-sat-and-unsat-list.py
   ```
   We take the top 110 sat and unsat files.  
   -> results/sat/bisection/sat.csv (110 sat files)  
   -> results/unsat/bisection/unsat.csv (110 unsat files)

7. Check the correctness of the results.  Run v3si exact, v4si exact once for each problem on the scope discovered in the previous step, checking:
    1. SAT → check instance returned is correct and both v3si and v4si return sat
    2. UNSAT -> check both v3si and v4si return unsat
    3. compare v3si and v4si  ????

   Adjust parameters in python/run-tests.py and run the script with
   ```

   python3 python/run-tests.py
   
      ```
   The results can be found in:
   - results/sat/correctness/run-tests-RESULTS.csv  
   - results/unsat/correctness/run-tests-RESULTS.csv   
   All unsat files passed the correctness testing successfully.  All but six sat files successfully completed correctness testing: Four sat files time out for both v3si and v4si for correctness checking.  One additional file timed out for v3si and one for v4si.  Note that correctness checking takes more resources than solving so we do not need to exclude these files from our performance evaluation.
   ???? what's in the following ????
   -> results/sat/correctness/sat.csv (104 sat files)  
   -> results/unsat/correctness/unsat.csv (110 unsat files)


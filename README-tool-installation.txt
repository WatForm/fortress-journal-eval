Nancy's Notes on installation of related tools on Mac

* look in Amir's FM paper for what versions he used

* CVC4 
	cvc4 --finite-model-find --lang=smt2.5 [FILE] --tlimit=MS
	- Input format: smt-lib2
		- need to distill out problems that only use free sorts
	- Installation
		- on mac:
			brew tap cvc4/cvc4
            brew install cvc4/cvc4/cvc4
            (takes awhile ~15 min)
	- Command to run (need to figure out based on papers):
		- (based on CADE 2013 paper) By default, cvc4 with finite model finding uses model-based instantiation, i.e., the configuration cvc4+fm:

		cvc4 --finite-model-find [FILE]

		- There is also "i" meaning enable heuristic instantiation based on E-matching. 
		- There is also "o": adds only one instance per instantiation round. This configuration can be enabled by running:

		cvc4 --finite-model-find --fmf-one-inst-per-round [FILE]
				--tlimit-per=MS        enable time limiting per query (give milliseconds)
  				--tlimit=MS            enable time limiting (give milliseconds)

	- Does it do anything with Ints? no, according to paper this is just for free sorts

	- How set scope?  since it doesn't introduce constants but only does this for quantifier instantiation there may not be away to set the scope.




* Mace 4
	- installation
		- downloaded from 
		(command-line version only)
		- https://www.cs.unm.edu/~mccune/prover9
		- download LADR CLI version of all tools (on next page choose version 11A - Linux, mac OS X)
		- 2009 - no longer maintained?
		- "make all" - compiled with only warnings
		    - If it throws errors, try moving all "-lm" flags to the end of lines in line 65-84 of "LADR-2009-11A/provers.src/Makefile".
		- "make test1" worked fine
		- binaries are in LADR-2009-11A/bin
	- input format
		- .in files (LADR)
		- tptp_to_ladr < PUZ031-1.tptp > PUZ031-1.in
			- can also convert the other way
	- CLI
		- mace4 -t 10 -f subset_trans.in > subset_trans.out4 (limit time to 10sec)
	- sorts or not
		- FOL + equals
		- unsorted finite structure
	- arithmetic
		- command "set (arithmetic)" interprets some int arith in Mace
		- see https://www.cs.unm.edu/~mccune/prover9/manual/2009-11A/
	- scope
		- default domain size is 2 and then increments size until suceeds or reaches some limit
		- "-n 5 -N 11 -i 2" say to try domain sizes 5,7,9,11" - gradually increments
	- "-c" - ignore unrecognized set/clear/assign commands in the input
         file.  This is useful for running MACE4 on an input file
         designed for another program such as a theorem prover.
	- output
		-P 0 does not print model, but still prints a lot of other stuff!
		- "Exiting with 1 model." in output if sat
		- exit code 0 means sat, exit code 2 means unsat and exit code 3-5 means hasn't been decided yet.
    - stack size
        - In the compilation process of mace4, it didn't set any stack size.
        - It might be using the OS max stack size. You can get check the stack size limit on Linux using command "prlimit".
    - heap size
        - the heap size can be set with flag “-b n”. The search will terminate if it tries to dynamically allocate (malloc) more than n megabytes of memory.
	- there is a python script in "fortress-tests-2.0/src/python", which converts a directory of .tptp to .in files
	- Notes: there are some options for setting symbol orders which the manual notes can effect solving time, but we have used defaults

* Paradox
	- written in Haskell
	- installation
		- downloaded from:
		http://www.cse.chalmers.se/~koen/code/folkung.tar.gz
		
		- version 2.0: but no downloads work: https://web.archive.org/web/20070108005818/http://www.cs.chalmers.se/~koen/folkung/
		- version 1.0: http://vlsicad.eecs.umich.edu/BK/Slots/cache/www.cs.chalmers.se/~koen/paradox/
		- http://www.cse.chalmers.se/~koen/code/
2021-06-17 - I just found https://github.com/c-cube/paradox (was updated 5 years ago)

* kodkod/Alloy
	- does it read an input format? No
	- repo includes .java for examples
		- some can be traced to tptp models
		- probably have scopes built-in so hard to test at different scopes


* fortress 
	- use a command-line interface
		- choose either tptp or smtlib input
		- need to pass scopes - typed or untyped
	- You can check the JVM heap size using command "java -XX:+PrintFlagsFinal -version | grep HeapSize"
	- You might need to set the JVM stack size using option "-J-Xss<size>".
    - When running these comparison that stack size does not matter for C programs but does matter for fortress.
    - The antlr parser throws stackoverflow errors when parsing large tptp files.

* smttotptp (tools/peba123 ...)
  ** WON'T work for sorted problems !!
  - Installation
  	- https://bitbucket.org/peba123/smttotptp/downloads/
  	- precompiled version does not seem to exist is repo!
 	- in main directory run "sbt assembly"
 	- compiled for me with warning
 	- java -jar /Users/nday/UW/uw-git/fortress-tests-2.0/tools/peba123-smttotptp-ccad34bfa07d/target/scala-2.12/smttotptp-0.9.9.jar
 	
